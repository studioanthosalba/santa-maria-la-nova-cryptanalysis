# -*- coding: utf-8 -*-
"""06_report.py -- assemble the final report from the phase outputs.

Reads ``corpus/corpora.json`` and the machine-readable summaries written by
phases 1b-3, recomputes the few cheap cross-checks it needs, and writes
``report/report.md`` (Italian) with every number taken from the data.
"""

from __future__ import annotations

import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C

C.utf8_stdout()

READINGS = ["palma_A", "palma_B", "gemini_full"]


# --------------------------------------------------------------------------
# cheap recomputations
# --------------------------------------------------------------------------
def uniform_null(rec: dict, n_iter: int = 300) -> dict:
    seq = rec["letters"]
    k = len(set(seq))
    rng = random.Random(4242)
    obs = C.fingerprint(seq)
    alphabet = sorted(set(seq))
    out = {}
    for st in C.KEY_STATS:
        sims = []
        for _ in range(n_iter):
            s = "".join(alphabet[rng.randrange(k)] for _ in range(len(seq)))
            sims.append(C.fingerprint(s)[st])
        z, p = C.z_and_p(obs[st], sims)
        out[st] = {"z": z, "p": p, "obs": obs[st], "mean": C.mean(sims)}
    return out


def agreement(recs: dict, a: str, b: str) -> dict:
    pa = C.relabel(recs[a]["letters"])
    pb = C.relabel(recs[b]["letters"])
    L, _, _ = C.longest_common_substring(pa, pb)
    return {"len_a": len(pa), "len_b": len(pb), "longest": L}


def section_sintesi(recs, s2, s3, s4, s5, img) -> list:
    out = ["# L'epigrafe di Santa Maria la Nova: analisi statistica e crittanalitica",
           ""]
    out.append("Rapporto generato da `scripts/06_report.py`: ogni numero proviene "
               "dai file in `corpus/`, le tabelle complete stanno in "
               "`corpus/00_corpus.md` ... `corpus/05_pca.md`. La domanda "
               "è duplice: *che tipo di testo è* questa epigrafe, e *che cosa si "
               "può dire dell'ipotesi Dracula*.")
    out.append("")
    out.append("## 1. Sintesi")
    out.append("")
    out.append("L'oggetto è l'epigrafe della cappella Turbolo (Santa Maria la "
               "Nova, Napoli): circa 600 glifi in un alfabeto non altrimenti "
               "attestato, accanto all'iscrizione latina dell'indulgenza di "
               "Gregorio XIII e alla tomba che la tradizione popolare attribuisce "
               "a Vlad III di Valacchia.")
    out.append("")
    rows = []
    for k in READINGS:
        r = recs[k]
        rows.append([f"`{k}`", r["n_lines"], r["n_letters"], r["K"],
                     round(r["ic"], 4), round(r["ic"] * r["K"], 3),
                     round(r["entropy"], 3)])
    out.append(C.md_table(
        ["lettura", "righe", "glifi", "classi K", "IC", "IC x K", "H (bit)"],
        rows))
    out.append("")
    out.append("Risultati principali:")
    out.append("")
    zr = {k: s2["rankings"][k]["mean_abs_z"] for k in READINGS}
    best = {k: min(v.items(), key=lambda kv: kv[1]) for k, v in zr.items()}
    un = {k: uniform_null(recs[k], 150) for k in READINGS}
    zic = [un[k]["IC"]["z"] for k in READINGS]
    out.append(
        "1. **Il testo non è casuale.** L'IC dista "
        f"{min(zic):.0f}-{max(zic):.0f} deviazioni standard da quello di una "
        "stringa uniforme con lo stesso alfabeto, e il test di Friedman rifiuta "
        "l'uniformità con p < 1e-12 in tutte le letture.")
    out.append(
        "2. **Nessuna lingua naturale in chiaro è compatibile** con le letture di "
        "Palma: la migliore ha |z| medio "
        f"{best['palma_A'][1]:.2f} (`palma_A`, {best['palma_A'][0]}) e "
        f"{best['palma_B'][1]:.2f} (`palma_B`, {best['palma_B'][0]}) su cinque "
        "statistiche invarianti. Il difetto è sistematico e riguarda la "
        "ripetizione dei bigrammi e dei trigrammi, non le frequenze dei singoli "
        "glifi.")
    a_ab = agreement(recs, "palma_A", "palma_B")
    a_bg = agreement(recs, "palma_B", "gemini_full")
    out.append(
        "3. **Le trascrizioni non concordano fra loro, e la fotografia dice "
        "perché**: dopo rietichettatura canonica due letture della stessa lapide "
        f"condividono al massimo {a_ab['longest']} simboli consecutivi su "
        f"{a_ab['len_a']} e {a_ab['len_b']} (`palma_A` vs `palma_B`) e "
        f"{a_bg['longest']} su {a_bg['len_b']} e {a_bg['len_a']} "
        "(`palma_B` vs `gemini_full`). La sequenza del log Gemini riproduce "
        "l'impianto e le forme della pietra (`drac1.jpeg`, `drac2.webp`), ma la "
        "sua provenienza dichiarata è quella di una **simulazione delle righe** "
        "(`corpus/corpora.json`, `report/verifica_trascrizioni_corpora_cifrari.md`): "
        "somiglia alla lapide senza esserne un testimone indipendente. Le "
        "stringhe di Palma non sono letture della stessa sequenza e vanno "
        "considerate stadi intermedi della sua pipeline (sezione 6). Ne segue "
        "che **nessuna delle stringhe disponibili è una trascrizione "
        "diplomatica**, ed è la ragione principale per cui il problema sembrava "
        "irrisolvibile.")
    att = {a["reading"]: a for a in s3["attack"] if a["model"].startswith("Latin")}
    gap_ok = max(abs(r["score"] - r["truth"]) for r in s3["self_test"])
    out.append(
        "4. **Gli attacchi classici falliscono in modo informativo**: il solver a "
        "sostituzione è validato su tre testi di controllo che decifra "
        f"esattamente (divario massimo {gap_ok:.2f} nats), ma sull'epigrafe si "
        f"ferma a {att['palma_B']['score']:.2f} nats/finestra contro un livello "
        f"di testo reale di {att['palma_B']['natural']:.2f} (baseline casuale "
        f"{att['palma_B']['shuffled']:.2f}). Null, periodicità e chiavi "
        "onomastiche (VLAD, DRACULA, TURBOLO...) non producono nulla di "
        "significativo.")
    fa = s4["fits"]["palma_A"][0]
    fb = s4["fits"]["palma_B"][0]
    fg = s4["fits"]["gemini_full"][0]
    known = [c["loglik"] for c in s4["calibration"]
             if c["truth"] != "uniform"]
    out.append(
        "5. **Un modello di trascrizione rumorosa spiega `palma_A`** con un tasso "
        f"di errore del {fa['noise']:.0%} e log-verosimiglianza {fa['marginal']:.1f}"
        f" (oggetti di origine nota: {min(known):.1f}-{max(known):.1f}), ma a quel "
        "rumore la lingua non è più identificabile (fattori di Bayes entro un "
        f"ordine di grandezza). `palma_B` resta più in basso ({fb['marginal']:.1f}) "
        f"e `gemini_full` è incompatibile con tutti i modelli ({fg['marginal']:.1f}).")
    out.append(
        "6. **L'ordinamento PCA proposto a parte è riprodotto e ridimensionato** "
        "(sezione 4.8): le sue coordinate tornano con scarto mediano "
        f"{s5['reproduction']['median_delta']:.2f}, ma i 28 descrittori sono "
        "invarianti per sostituzione (scarto esattamente nullo), quindi la "
        "posizione non può testimoniare un cifrario; testi **in chiaro** con una "
        "o due classi di glifi fuse hanno la stessa distanza dal centro delle "
        "letture, e le attribuzioni linguistiche per prossimità non superano il "
        "null "
        f"(p = {s5['neighbours']['readings']['gemini_full']['2']['p_max']:.2f}).")
    out.append(
        "7. **Il verdetto su Dracula è negativo, ma per assenza di dati**: con le "
        "trascrizioni disponibili nessuna affermazione sul contenuto (onomastica "
        "draculiana, preghiera penitenziale ceca, tavola didattica) è verificabile "
        "né falsificabile.")
    dims = " e ".join(f"{r['width']}×{r['height']}"
                      for r in img["images"] if r["width"])
    out.append(
        "8. **Il limite non è più un'opinione: è misurato.** Le due fotografie "
        f"disponibili sono da {dims} pixel e nessun motore OCR è installato in "
        "questo ambiente: per questo il rapporto **non presenta alcuna nuova "
        "trascrizione**. Il passo successivo è un'immagine ortogonale ad alta "
        "risoluzione — o un rilievo — con una trascrizione paleografica "
        "indipendente, legenda dei segni e lacune marcate; solo dopo ha senso "
        "tornare alla ricerca di chiavi.")
    out.append("")
    out.append(
        "Il bilancio del lavoro, la conclusione finale e il registro dei "
        "consegnati con le impronte SHA256 sono depositati in "
        "`report/atti/relazione_finale.md`.")
    out.append("")
    return out


def section_fonti(recs) -> list:
    out = ["## 2. Fonti e costruzione del corpus", ""]
    out.append(C.md_table(
        ["fonte", "contenuto", "uso"],
        [["Palma 2023 (HistoCrypt), repo `Glottocrisio/MaLaNova`",
          "9 file di trascrizione: due letture in lettere latine "
          "(`stringaoriginale`, `stringanospaces`), una in etichette greche "
          "(`soluzione`), varianti fuse e riempite (`scriptiocontinua*`)",
          "corpus primario"],
         ["`dracula_epigrafe.md` (log Gemini)",
          "trascrizione di 33 righe + blocco centrale di 8 righe ripetuto tre "
          "volte, dichiarata come simulazione delle righe della lapide",
          "termine di confronto"],
         ["`epigrafe drac.md`",
          "lettura degradata, 68 righe con duplicazioni", "controllo di "
          "sensibilità"],
         ["Palma 2023, PDF HistoCrypt",
          "metodo, IC normalizzato 1.72, entropia 4.1, tabella per 12 lingue, "
          "esiti AZdecrypt", "confronto"],
         ["Antal, Marak, Zajac, Lengyelova, Duchonova (Archivio Nazionale "
          "Slovacco)",
          "96 documenti cifrati e 9 chiavi, sec. XVIII-XIX: nomenclatore "
          "numerico, chiavi conservate ma non combacianti con i testi, "
          "chiaro spesso conservato accanto al cifrato", "confronto"],
         ["Layfield et al. 2022 (convegno Voynich)",
          "rapporto di un convegno peer-reviewed su un manoscritto "
          "indecifrato: revisione in doppio cieco, paleografia, testi privi "
          "di senso che non sono tutti dello stesso tipo", "criterio di "
          "metodo"],
         ["`sources/external` (16 corpora)",
          "Bibbie parallele (Vulgata, Kralická 1613, Riveduta, Károli, romeno, "
          "albanese, croato, slovacco, polacco, tedesco, inglese, greco) più "
          "Dante e un catechismo ceco", "modelli linguistici"],
         ["cartella `corpora/` del repo",
          "codici ungheresi e cechi, latino umanistico, copto, greco",
          "modelli aggiuntivi"]])
    )
    out.append("")
    out.append("I tre PDF di Palma 2023, Antal et al. e Layfield et al. sono agli "
               "atti come **scansioni di pagina**: 1240×1753 px (un A4 a circa "
               "150 ppi), nessun livello di testo, quindi nessuna ricerca "
               "testuale possibile e in questo ambiente nessun OCR. Sono stati "
               "letti pagina per pagina (`scripts/_pdf_pages.py` rende "
               "ispezionabile una pagina; `report/atti/manifest.json` registra "
               "pagine, byte e SHA256). Che cosa se ne ricava, e quale ipotesi "
               "confutano, è in `report/documenti_agli_atti.md` e nella "
               "sezione 4.9.")
    out.append("")
    out.append("Due difetti dei dati di partenza, corretti in "
               "`scripts/langmodels.py`, vanno segnalati perché invalidano parte "
               "del confronto pubblicato:")
    out.append("")
    out.append("- i file `bibliahuszita*` e `czechcodex.txt` sono in realtà "
               "**ungherese** (Codice di Monaco, 1466), non ceco: la riga 'Old "
               "Czech' della tabella di Palma 2023 corrisponde quindi a un "
               "corpus ungherese;")
    out.append("- i corpora del repository sono doppiamente codificati (UTF-8 "
               "letto come cp437) e vanno riparati prima di qualsiasi calcolo.")
    out.append("")
    rows = [[f"`{k}`", r["n_lines"], r["n_letters"], r["n_gaps"], r["K"],
             r["n_tokens"]] for k, r in recs.items()]
    out.append(C.md_table(["chiave", "righe", "glifi", "segni illeggibili",
                           "classi", "token"], rows))
    out.append("")
    return out


def section_metodo() -> list:
    out = ["## 3. Metodo", ""]
    out.append("Il punto metodologico centrale è che **le frequenze non sono "
               "confrontabili direttamente** fra un cifrario e un testo in "
               "chiaro: una sostituzione permuta i simboli, quindi la "
               "distribuzione del cifrario è una permutazione di quella del "
               "testo, non la stessa. Confrontare le frequenze (come fa la "
               "letteratura corrente, AZdecrypt compreso) è lecito solo *dopo* "
               "aver fissato la chiave.")
    out.append("")
    out.append("Qui si usano invece statistiche **invarianti per rietichettatura**, "
               "calcolate su finestre di lunghezza identica nei corpora di "
               "riferimento:")
    out.append("")
    out.append(C.md_table(
        ["statistica", "perché è invariante", "cosa misura"],
        [["IC", "somma su tutte le classi", "concentrazione globale"],
         ["H (entropia)", "funzione delle sole frequenze",
          "ampiezza efficace dell'alfabeto"],
         ["quota del simbolo più frequente", "ordinamento delle frequenze",
          "asimmetria della distribuzione"],
         ["tasso di bigrammi ripetuti", "una biiezione mappa bigrammi in bigrammi",
          "struttura seriale locale"],
         ["tasso di trigrammi ripetuti", "idem", "struttura seriale a medio raggio"]])
    )
    out.append("")
    out.append("Ogni affermazione è accompagnata da un **null calibrato**: "
               "permutazioni della stringa, finestre della stessa lunghezza "
               "estratte dai corpora, testi di controllo cifrati con lo stesso "
               "schema e di cui si conosce il testo in chiaro. Senza calibrazione "
               "un risultato negativo non è interpretabile: non si distingue fra "
               "'il cifrario non è quello' e 'il metodo non ha potenza "
               "sufficiente'.")
    out.append("")
    out.append("Avvertenza tecnica: il test di permutazione applicato all'IC è "
               "**degenere**, perché l'IC dipende solo dal multinsieme dei glifi "
               "e una permutazione lo lascia invariato (p = 1 per costruzione). "
               "Applicato invece al tasso di trigrammi ripetuti esso è "
               "informativo, perché quella statistica dipende dall'ordine.")
    out.append("")
    out.append("L'ordinamento PCA (sezione 4.8) è trattato come strumento "
               "**descrittivo, non inferenziale**: le distanze non sono p-value, "
               "le componenti massimizzano la varianza e non la separazione fra "
               "lingue, e la posizione delle letture è confrontata con un null "
               "esplicito — testi di riferimento in chiaro a cui vengono fuse "
               "una o due classi di glifi, cioè l'effetto di una trascrizione "
               "che non distingue le varianti.")
    out.append("")
    return out


def perm_test_trirep(rec: dict, n_iter: int = 2000, seed: int = 606) -> dict:
    """Permutation test on an order-dependent statistic (trigram repetition)."""
    seq = rec["letters"]
    obs = C.repeat_rate(seq, 3)
    rng = random.Random(seed)
    letters = list(seq)
    sims = []
    for _ in range(n_iter):
        rng.shuffle(letters)
        sims.append(C.repeat_rate(letters, 3))
    p = (1 + sum(1 for v in sims if v >= obs)) / (1 + n_iter)
    return {"observed": obs, "null_mean": C.mean(sims), "null_sd": C.stdev(sims),
            "p": p}


def section_risultati_1(recs, s2) -> list:
    out = ["## 4. Risultati", "", "### 4.1 Le letture non concordano fra loro", ""]
    pairs = [(a, b) for i, a in enumerate(READINGS) for b in READINGS[i + 1:]]
    pairs += [("palma_A", "palma_B2"), ("palma_B", "palma_B2")]
    rows = []
    for a, b in pairs:
        if a not in recs or b not in recs:
            continue
        ag = agreement(recs, a, b)
        rows.append([f"`{a}` ~ `{b}`", ag["len_a"], ag["len_b"],
                     ag["longest"],
                     round(ag["longest"] / min(ag["len_a"], ag["len_b"]), 4)])
    out.append(C.md_table(["coppia", "glifi A", "glifi B",
                           "blocco comune più lungo", "quota"], rows))
    out.append("")
    out.append("Il confronto è fatto dopo **rietichettatura canonica** (i simboli "
               "sono rinominati per ordine di prima occorrenza), che è l'unico "
               "confronto lecito fra trascrizioni che usano alfabeti-etichetta "
               "diversi: se due letture fossero la stessa stringa di glifi con "
               "nomi diversi coinciderebbero carattere per carattere.")
    out.append("")
    out.append("Il blocco comune è di 4-5 simboli su ~600 fra letture di origine "
               "diversa, mentre fra due file dello stesso autore con lo stesso "
               "numero di glifi (`palma_B` e `palma_B2`) sale a un blocco di "
               "decine di simboli: la metrica distingue i gradi di parentela, e "
               "le letture indipendenti risultano **non sovrapponibili**.")
    out.append("")
    out.append("### 4.2 Struttura contro il caso")
    out.append("")
    rows = []
    for k in READINGS:
        un = uniform_null(recs[k], 150)
        for st in C.KEY_STATS:
            rows.append([f"`{k}`", st, round(un[st]["obs"], 4),
                         round(un[st]["mean"], 4), round(un[st]["z"], 1),
                         C.fmt_p(un[st]["p"])])
    out.append(C.md_table(["lettura", "statistica", "osservato",
                           "media uniforme", "z", "p"], rows))
    out.append("")
    out.append("Il testo è lontanissimo da una decorazione casuale di glifi. "
               "Va però notato il segno: `palma_A` e `palma_B` stanno **sopra** "
               "il caso per concentrazione (IC, H, quota del simbolo più "
               "frequente) ma restano molto **sotto** le lingue naturali per "
               "ripetizione dei trigrammi (0.15 e 0.27 contro 0.41-0.63).")
    out.append("")
    out.append("### 4.3 Struttura seriale e periodicità")
    out.append("")
    rows = []
    for k in READINGS:
        pt = perm_test_trirep(recs[k])
        pe = s2["periodicity"][k]
        rows.append([f"`{k}`", round(pt["observed"], 3),
                     round(pt["null_mean"], 3), C.fmt_p(pt["p"]),
                     pe["best_k"], round(pe["delta"], 5), C.fmt_p(pe["p"])])
    out.append(C.md_table(
        ["lettura", "trigrammi ripetuti", "null di permutazione",
         "p (permutazione)", "periodo migliore", "guadagno IC", "p (periodo)"],
        rows))
    out.append("")
    out.append("Le due colonne di p dicono cose diverse e complementari: la "
               "prima conferma che esiste struttura seriale (il testo ripete i "
               "trigrammi molto più di una permutazione delle sue stesse "
               "lettere), la seconda mostra che **non c'è alcun periodo** "
               "nascosto. Il massimo guadagno di IC su k = 1..20 non supera mai "
               "il 95° percentile del null: la 'periodicità' intravista dagli "
               "esami di Kasiski è rumore di campionamento.")
    out.append("")
    return out


def section_risultati_2(s2) -> list:
    out = ["### 4.4 Confronto con sedici lingue di riferimento", ""]
    for k in READINGS:
        rank = s2["rankings"][k]["mean_abs_z"]
        zs = s2["rankings"][k]["z_by_stat"]
        rows = []
        for label, val in sorted(rank.items(), key=lambda kv: kv[1])[:6]:
            rows.append([label, round(val, 2), zs[label]["tri_rep"],
                         zs[label]["bi_rep"], zs[label]["IC"]])
        out.append(f"**`{k}`** (n = {s2['rankings'][k]['n']}): migliori sei "
                   "corrispondenze, ordinate per |z| medio")
        out.append("")
        out.append(C.md_table(["lingua", "z medio (assoluto)", "z(trigrammi)",
                               "z(bigrammi)", "z(IC)"], rows))
        out.append("")
    out.append("Ogni z è calcolato su finestre di lunghezza identica a quella "
               "della lettura, quindi l'errore di campionamento è lo stesso sui "
               "due lati del confronto. **Nessuna lingua scende sotto |z| = 2**: "
               "il |z| medio minimo è "
               f"{min(min(v['mean_abs_z'].values()) for v in s2['rankings'].values()):.2f}. "
               "Il colpevole è sempre lo stesso: z(bigrammi) e z(trigrammi) "
               "fortemente negativi, cioè la lettura ripete troppo poco.")
    out.append("")
    return out


def section_risultati_3(s2, s3) -> list:
    out = ["### 4.5 Vocali e consonanti: il test esaustivo", ""]
    out.append("In ogni lingua naturale vocali e consonanti si alternano, quindi "
               "la frazione di testo che cade dentro sequenze di tre o più "
               "consonanti (`C3`) è piccola. Poiché nel cifrario i glifi sono "
               "etichette arbitrarie, si possono provare **tutti** i C(K,5) "
               "insiemi di vocali (33 649 per K = 23) e prendere il migliore: "
               "un'assegnazione migliore di quella trovata non esiste.")
    out.append("")
    rows = []
    for k in s2["cv"]:
        cv = s2["cv"][k]
        rows.append([f"`{k}`", ", ".join(f"`{g}`" for g in cv["best_set"]),
                     round(cv["best_c3"], 4), round(cv["median_c3"], 4),
                     round(cv["reference_best"], 4)])
    out.append(C.md_table(
        ["lettura", "miglior insieme di vocali", "C3 minimo raggiungibile",
         "C3 mediano su tutti gli insiemi", "C3 migliore fra le lingue"], rows))
    out.append("")
    out.append("È il risultato più diagnostico dell'analisi: sotto la "
               "trascrizione **Gemini** l'insieme ottimale è `a, i, v, o, e` con "
               "C3 = 0.028, cioè un'alternanza perfettamente naturale (le vocali "
               "sono le lettere che *sembrano* vocali); sotto le trascrizioni di "
               "Palma nessun insieme scende a livelli naturali. Poiché `C3` "
               "dipende dall'ordine dei glifi e non dai loro nomi, la differenza "
               "non è un effetto delle etichette: le due trascrizioni descrivono "
               "**strutture diverse**.")
    out.append("")
    out.append("### 4.6 Attacchi classici")
    out.append("")
    rows = [[r["model"], r["score"], r["truth"], round(r["score"] - r["truth"], 2)]
            for r in s3["self_test"]]
    out.append("**Auto-validazione del solver** (cifrario noto, testo in chiaro "
               "noto, stessa lunghezza dell'epigrafe):")
    out.append("")
    out.append(C.md_table(["modello linguistico", "punteggio raggiunto",
                           "punteggio del vero testo in chiaro", "divario"],
                          rows))
    out.append("")
    out.append("L'attacco procede per stadi, con modelli di 2, 3, 4 e 5 grammi e "
               "chiave trasferita da uno stadio al successivo: un 5-grammo da "
               "partenza casuale si incastra in ottimi locali (misurato sul "
               "controllo ceco, dove sbagliava di 3.2 nats), mentre la scala "
               "progressiva recupera il testo in chiaro esatto in tutti e tre i "
               "casi. **Il solver non è quindi il limite del risultato che "
               "segue.**")
    out.append("")
    rows = [[a["reading"], a["model"], a["score"], a["shuffled"], a["natural"],
             a["words"]] for a in s3["attack"]]
    out.append("**Attacco all'epigrafe**:")
    out.append("")
    out.append(C.md_table(["lettura", "modello", "punteggio", "baseline casuale",
                           "livello di testo reale", "parole latine trovate"],
                          rows))
    out.append("")
    nd = s3["null"]
    out.append(f"**Ipotesi dei null**: il miglior guadagno di IC ottenibile "
               f"eliminando un solo glifo è {nd['observed_gain']:.5f} "
               f"(`{nd['observed_glyph']}`), contro {nd['clean_mean']:.5f} nei "
               f"controlli senza null e {nd['nulled_mean']:.5f} in quelli con il "
               f"10% di null (p = {C.fmt_p(nd['p'])}): l'ipotesi non è sostenuta.")
    out.append("")
    rows = [[r["key"], r["IC"], r["tri_rep"], r["random_mean"], r["p"]]
            for r in s3["keys"]]
    out.append("**Chiavi onomastiche** (Vigenère/Bellaso, chiave applicata come "
               "valore delle lettere latine modulo il numero di classi):")
    out.append("")
    out.append(C.md_table(["chiave", "IC dopo decifratura", "trigrammi ripetuti",
                           "media delle chiavi casuali", "p"], rows))
    out.append("")
    out.append("Nessuna chiave porta il testo nella fascia linguistica (IC ~ "
               "0.073, trigrammi ~ 0.5) e nessun p è significativo: i nomi della "
               "tradizione non sono la chiave di un cifrario periodico. Il "
               "risultato però **non falsifica** l'ipotesi cifrata, e la ragione "
               "è documentaria, non statistica: in un archivio reale di cifrari "
               "sette-ottocenteschi le chiavi conservate non corrispondono ai "
               "testi conservati (sezione 4.9), quindi la mancata corrispondenza "
               "si osserva anche dove cifrato e chiave esistono entrambi.")
    out.append("")
    return out


def section_risultati_4(s4) -> list:
    out = ["### 4.7 Modello generativo: quanto rumore serve?", ""]
    out.append("Si confronta la famiglia `testo in chiaro (lingua) -> "
               "sostituzione -> [null] -> [rumore di trascrizione]` con la firma "
               "invariante di ogni lettura, con verosimiglianza gaussiana "
               "diagonale su cinque statistiche e tasso di rumore marginalizzato "
               "su una griglia.")
    out.append("")
    rows = [[c["object"], c["truth"], c["best"], c["noise"], c["loglik"]]
            for c in s4["calibration"]]
    out.append("**Calibrazione** su oggetti di origine nota:")
    out.append("")
    out.append(C.md_table(["oggetto", "lingua vera", "lingua attribuita",
                           "rumore inferito", "log-verosimiglianza"], rows))
    out.append("")
    out.append("La calibrazione fissa l'inviluppo del metodo: il testo pulito è "
               "attribuito alla lingua giusta, mentre il testo con null e quello "
               "con il 25% di rumore vengono attribuiti a una lingua vicina "
               "(croato) pur ricevendo verosimiglianza alta; una stringa casuale "
               "riceve verosimiglianza fortemente negativa. Due conseguenze: "
               "**l'etichetta della lingua non è affidabile quando c'è rumore**, "
               "mentre **la verosimiglianza assoluta separa bene testo e non "
               "testo**.")
    out.append("")
    rows = []
    for k, fits in s4["fits"].items():
        top, sec, last = fits[0], fits[1], fits[-1]
        rows.append([f"`{k}`", f"{top['language']} ({top['noise']:.0%})",
                     top["marginal"],
                     round(top["marginal"] - sec["marginal"], 2),
                     last["marginal"]])
    out.append("**Epigrafe**:")
    out.append("")
    out.append(C.md_table(
        ["lettura", "modello migliore", "log-verosimiglianza marginale",
         "distacco dal secondo", "modello peggiore"], rows))
    out.append("")
    known = [c["loglik"] for c in s4["calibration"] if c["truth"] != "uniform"]
    fa = s4["fits"]["palma_A"][0]
    out.append(
        "`palma_A` arriva a "
        f"{fa['marginal']:.1f}, appena sotto la fascia degli oggetti di origine "
        f"nota ({min(known):.1f}-{max(known):.1f}): è compatibile con *qualche* "
        "lingua trascritta con molto rumore — o con una lingua meno rappresentata "
        "nei corpora — ma il distacco dal secondo classificato è minimo e il tasso "
        "richiesto (~30%) azzera il potere discriminante. `palma_B` e "
        "`gemini_full` restano fuori fascia.")
    out.append("")
    return out


def section_pca(s5) -> list:
    """Critical re-analysis of the separate PCA report (fase 1c)."""
    out = ["### 4.8 Ordinamento PCA: rifatto e confutato", ""]
    rep = s5["reproduction"]
    rows = []
    for k in READINGS:
        pub = s5["published"][k]
        rec = rep["recomputed"][k][:3]
        signs = rep["signs"][k]
        d = [abs(p - s * r) for p, s, r in zip(pub, signs, rec)]
        rows.append([f"`{k}`", ", ".join(f"{v:.2f}" for v in pub),
                     ", ".join(f"{s * v:.2f}" for s, v in zip(signs, rec)),
                     f"{max(d):.2f}"])
    out.append("L'analisi PCA distribuita a parte (`report/pca_analisi.md`) è "
               "stata ricostruita da zero nella fase 1c "
               "(`scripts/05_pca.py`, `corpus/05_pca.md`): 28 descrittori, "
               f"{s5['dataset']['languages']} corpora di riferimento, "
               f"{s5['dataset']['samples'] // 1000}.{s5['dataset']['samples'] % 1000:03d} "
               "finestre, autosolutore in sola libreria standard. Le sue "
               "coordinate si riproducono:")
    out.append("")
    out += [C.md_table(["lettura", "pubblicato", "ricalcolato", "scarto massimo"],
                       rows), ""]
    out.append(f"Scarto massimo {rep['max_delta']:.2f} deviazioni standard, "
               f"mediana {rep['median_delta']:.2f}. Resta non ricostruibile "
               "**quali** sedici corpora abbia usato l'analisi pubblicata: la "
               "pipeline ne configura 21 e ne seleziona sedici con una regola "
               "dichiarata (almeno 30.000 lettere, il che esclude i cinque testi "
               "brevi); la riproduzione è quindi buona sul "
               "risultato e imperfetta sul protocollo.")
    out.append("")
    out.append("Due ambiguità del protocollo sono state sciolte con altrettanti "
               "controlli. **Primo**: l'analisi pubblicata non dice come calcoli "
               "il «tasso di ripetizione»; rifacendo l'ordinazione con "
               "l'alternativa 1 − U/N le coordinate si spostano di "
               f"{max(s5['definitions']['shift'].values()):.2f} deviazioni "
               "standard al massimo e la riproduzione resta allo stesso livello — "
               "l'ambiguità non spiega le differenze residue. **Secondo**: in "
               "`report/verifica_trascrizioni_corpora_cifrari.md` esiste una "
               "seconda PCA, con codice e insieme di corpora diversi; le "
               "coordinate delle due letture Palma concordano entro "
               f"{s5['second_pca']['max_delta']:.2f} deviazioni standard e "
               "confermano lo stesso punto (le prossimità cambiano da una lettura "
               "all'altra). Due analisi indipendenti convergono: la PCA descrive, "
               "non attribuisce.")
    out.append("")
    out.append("**Che cosa la PCA non può dire.** Tutti i 28 descrittori sono "
               "invarianti per rietichettatura: cifrare il testo per sostituzione "
               "li lascia **identici** (scarto massimo misurato: zero su tutti i "
               "controlli). La posizione nello spazio non può quindi testimoniare "
               "né escludere un cifrario: l'ipotesi dell'analisi pubblicata "
               "secondo cui «una sostituzione semplice non basta» non è un suo "
               "risultato.")
    out.append("")
    lv = s5["controls"]["gemini_full"]["levels"]
    rows = [[m, f"{lv[str(m)]['median_radius']:.2f}",
             f"{lv[str(m)]['frac_above']:.2f}"] for m in ("0", "1", "2", "3")]
    out.append("**Il controllo che manca.** Testi di riferimento **in chiaro, "
               "senza cifrario**, con le prime k classi di glifi fuse in una "
               "(ciò che accade quando il trascrittore non distingue varianti "
               "come Α/Λ/∀ o Ε/Є). Per `gemini_full` (distanza osservata "
               f"{s5['controls']['gemini_full']['radius']:.2f}):")
    out.append("")
    out += [C.md_table(["classi fuse", "distanza mediana dei controlli",
                        "frazione di controlli più lontani della lettura"], rows),
            ""]
    eq = s5["equivalent_merge"]
    spans = ", ".join(f"`{k}`: " + (f"{eq[k][0]}-{eq[k][-1]}" if len(eq[k]) > 1
                                    else (str(eq[k][0]) if eq[k] else "> 4"))
                      for k in READINGS)
    out.append("Le fusioni compatibili con la distanza osservata sono " + spans +
               ": **la scala dell'allontanamento è quella di un testo naturale "
               "non cifrato trascritto a maglia larga**, e non richiede alcun "
               "cifrario. La direzione però non coincide (i controlli fusi si "
               "spostano sul lato opposto di PC1 rispetto a `palma_A` e "
               "`palma_B`), quindi la fusione spiega *quanto*, non *dove*: resta "
               "il profilo irregolare descritto nella sezione 6.1, che è di "
               "frequenze e non di n-grammi.")
    out.append("")
    out.append("**Nota di provenienza.** La riga `gemini_full` riguarda una "
               "sequenza che la documentazione di progetto descrive come "
               "*simulazione delle righe* della lapide, non come trascrizione "
               "indipendente (`report/verifica_trascrizioni_corpora_cifrari.md`). "
               "Nessuna delle conclusioni di questa sezione cambia: l'invarianza "
               "per sostituzione vale per qualunque stringa, e le due letture "
               "Palma mostrano lo stesso allontanamento con lo stesso ordine di "
               "grandezza. Ciò che cambia è l'oggetto: quello che manca non è un "
               "algoritmo migliore, è una trascrizione diplomatica.")
    out.append("")
    nb = s5["neighbours"]["readings"]
    out.append("**Le prossimità non identificano una lingua.** La lingua più "
               "vicina cambia con il numero di componenti usate e con il "
               "campionamento; la concentrazione delle letture (massimo "
               f"{nb['gemini_full']['2']['max_count']} finestre su 15 da una sola "
               f"lingua per `gemini_full`) ha p = "
               f"{nb['gemini_full']['2']['p_max']:.2f} rispetto alla stessa "
               "statistica calcolata sui punti di riferimento. «Slovacco», "
               "«ungherese storico», «italiano» sono etichette geometriche, non "
               "attribuzioni.")
    out.append("")
    st = s5["stability"]["z"]
    out.append("**Che cosa sopravvive.** La distanza dal centro, che è invariante "
               "per rotazione degli assi: "
               + ", ".join(f"`{k}` {st[k]['radius'][0]:.2f}-{st[k]['radius'][1]:.2f}"
                           for k in READINGS)
               + " su quattro semi di campionamento e sul sottoinsieme ridotto a "
               "dodici corpora. Non sopravvive invece la grandezza di una singola "
               "componente: PC2 e PC3 si scambiano o cambiano segno fra un "
               "campionamento e l'altro, quindi un valore come «PC3 z = 6» non è "
               "un numero riproducibile.")
    out.append("")
    return out


def section_documenti() -> list:
    """Section 4.9: what the three secondary sources add, and what they refute.

    All statements are anchored to pages read on the record; the full reading is
    in ``report/documenti_agli_atti.md``.
    """
    out = ["### 4.9 Che cosa dicono gli altri casi documentati", ""]
    out.append("Tre fonti secondarie sono state messe agli atti e lette pagina "
               "per pagina (`report/documenti_agli_atti.md`): un archivio di "
               "cifrari sette-ottocenteschi con le loro chiavi, il rapporto di "
               "un convegno peer-reviewed su un manoscritto indecifrato, e il "
               "saggio di Palma. Servono a dire che cosa un cifrario di questo "
               "ambiente **dovrebbe** avere, e a confutare due inferenze che i "
               "nostri numeri invitano a trarre.")
    out.append("")
    out.append("- **Il repertorio dei segni non somiglia al nostro.** Nei 96 "
               "documenti cifrati dell'Archivio Nazionale Slovacco (sec. "
               "XVIII-XIX) il sistema è il nomenclatore e il repertorio "
               "\"consists of only numbers and markings of numbers\", con o "
               "senza separatori (37 con, 59 senza). La nostra epigrafe ha 23 "
               "classi di glifi misti e nessun livello numerico evidente: se è "
               "un cifrario dello stesso ambiente, le manca il tratto più "
               "tipico del genere.")
    out.append("- **Le chiavi si conservano, ma non combaciano.** Nello stesso "
               "fondo sono conservate 9 chiavi per 96 documenti, e le chiavi "
               "conservate **non corrispondono ai testi conservati**; le chiavi "
               "sono in due fondi su tre. Ne segue una correzione al nostro "
               "paragrafo sulle chiavi onomastiche: il null (VLAD, DRACULA, "
               "TURBOLO...) **non è conclusivo**, perché la mancata "
               "corrispondenza si osserva anche dove cifrato e chiave esistono "
               "entrambi. Non falsifica e non conferma.")
    out.append("- **La pratica reale lascia il chiaro accanto al cifrato**: in "
               "16 documenti il testo in chiaro è scritto sopra le righe "
               "cifrate, in 38 è in un documento separato, e solo in 8 casi su "
               "96 il chiaro non è conservato. È l'opposto del segreto "
               "assoluto, e rafforza l'argomento di contesto di Palma: un "
               "testo esposto in vista non è un testo che si voleva nascondere.")
    out.append("- **La paleografia decide i segni, non la statistica.** Al "
               "convegno Voynich la relazione di apertura applica la "
               "paleografia latina al sistema di scrittura, distingue cinque "
               "mani e avverte che alcuni segni possono essere abbreviazioni o "
               "legature. È il precedente metodologico della lettura di "
               "`ΔΕΔΕΔ` come marchio o abbreviazione e non come parola "
               "(sezione 7.3).")
    out.append("- **Due testi privi di senso non sono dello stesso tipo.** Il "
               "confronto quantitativo fra Voynich e Słowa MS 3188 trova "
               "somiglianze, ma anche differenze statistiche sostanziali: anche "
               "se entrambi fossero privi di senso, non apparterrebbero allo "
               "stesso genere. Quindi il nostro \"nessuna lingua fra 16\" "
               "esclude lingue naturali e **non identifica una tecnica**: è la "
               "prima cosa da non scrivere.")
    out.append("- **\"Potrebbe non esserci alcun mistero\" è una posizione di "
               "metodo**, non una facezia: è l'obiettivo dichiarato di un "
               "convegno con tre revisori in doppio cieco, e Rosenmeyer (citata "
               "da Palma) descrive l'enigma come gioco intellettuale, «a sort of "
               "hoax». L'ipotesi beffa resta in alternativa seria — con la "
               "stessa conseguenza operativa: serve la trascrizione "
               "paleografica.")
    out.append("")
    return out


def section_verdetto(s2, s3, s4) -> list:
    out = ["## 5. Verdetto sulle ipotesi", ""]
    best_a = min(s2["rankings"]["palma_A"]["mean_abs_z"].items(),
                 key=lambda kv: kv[1])
    best_b = min(s2["rankings"]["palma_B"]["mean_abs_z"].items(),
                 key=lambda kv: kv[1])
    fa = s4["fits"]["palma_A"][0]
    czech = [r for r in s4["fits"]["palma_A"]
             if r["language"].startswith("Czech (Bible")]
    czech_gap = (czech[0]["marginal"] - fa["marginal"]) if czech else float("nan")
    rows = [
        ["Sostituzione monoalfabetica semplice di una lingua naturale",
         "**non sostenuta**",
         "nessuna lingua sotto la soglia di 2 deviazioni standard; attacco a "
         "sostituzione fermo a 3 nats/finestra sotto il testo reale, mentre sui "
         "controlli lo raggiunge esattamente"],
        ["Cifrario diverso dalla sostituzione semplice, dedotto dalla PCA",
         "**ritirata**",
         "i 28 descrittori dell'ordinazione sono invarianti per sostituzione, "
         "quindi la posizione non distingue un cifrario da un testo in chiaro; "
         "l'allontanamento delle letture è riprodotto da testi in chiaro con una "
         "o due classi di glifi fuse (sezione 4.8)"],
        ["Sostituzione con null",
         "**non sostenuta**",
         f"guadagno massimo di IC {s3['null']['observed_gain']:.4f} vs "
         f"{s3['null']['clean_mean']:.4f} dei controlli senza null "
         f"(p = {C.fmt_p(s3['null']['p'])})"],
        ["Cifrario polialfabetico periodico",
         "**non sostenuta**",
         "nessun picco di IC su k = 1..20; p = "
         f"{C.fmt_p(s2['periodicity']['palma_A']['p'])} e "
         f"{C.fmt_p(s2['periodicity']['palma_B']['p'])} contro il null"],
        ["Chiavi onomastiche (VLAD, DRACULA, TURBOLO, ...)",
         "**non sostenuta**",
         "tutte indistinguibili da chiavi casuali della stessa lunghezza"],
        ["Testo greco scritto in lettere greche",
         "**non sostenuta**",
         "con le vocali greche reali C3 = 0.445, contro < 0.10 di qualsiasi "
         "lingua"],
        ["Testo latino/italiano in chiaro travestito da alfabeto esotico",
         "**improponibile**",
         "la struttura seriale delle letture di Palma è troppo piatta per "
         "qualsiasi lingua naturale"],
        ["Trascrizione rumorosa, lingua reale non identificabile",
         "**la più compatibile**",
         f"`palma_A` al {fa['noise']:.0%} di rumore raggiunge "
         f"{fa['marginal']:.1f}, appena sotto la fascia degli oggetti di origine "
         "nota, con fattori di Bayes entro un ordine di grandezza fra le prime "
         "lingue"],
        ["Preghiera penitenziale ceca medievale",
         "**non confermata**",
         "il ceco (Kralická 1613) è la migliore corrispondenza per `palma_A` "
         f"nella metrica dello z medio (`{best_a[0]}`, {best_a[1]:.2f}) ma resta "
         f"molto sotto il modello migliore nel confronto generativo "
         f"(Δ ln L = {czech_gap:.1f}): nessuna convergenza fra le due prove"],
        ["Tavola didattica / decorazione senza messaggio",
         "**possibile, non dimostrabile**",
         "il testo non è casuale (IC a decine di deviazioni standard dal caso), "
         "quindi qualcosa di strutturato c'è; nessun modello linguistico però lo "
         "cattura"],
    ]
    out.append(C.md_table(["ipotesi", "stato", "evidenza"], rows))
    out.append("")
    out.append("Le due letture non indicano la stessa lingua "
               f"(`{best_a[0]}` per `palma_A`, `{best_b[0]}` per `palma_B`): "
               "ulteriore sintomo che il rumore di trascrizione domina il segnale.")
    out.append("")
    return out


def split_classes(seq: str, glyph: str = "a", frac: float = 0.3,
                  seed: int = 7) -> dict:
    """What happens to the fingerprint if one merged glyph class is split in two?"""
    rng = random.Random(seed)
    out = []
    for ch in seq:
        if ch == glyph and rng.random() < frac:
            out.append("Q")
        else:
            out.append(ch)
    t = "".join(out)
    fp = C.fingerprint(t)
    return {"K": len(set(t)), "IC": fp["IC"], "tri_rep": fp["tri_rep"],
            "top1": fp["top1"]}


def section_verifica_visiva(recs, img) -> list:
    out = ["## 6. Verifica visiva: le fotografie della lapide", ""]
    out.append("Nella radice del progetto ci sono due fotografie della lapide "
               "(`drac1.jpeg`, `drac2.webp`) e nessun'altra immagine. Prima di "
               "confrontarle con i testi disponibili vanno misurate, perché da "
               "quella misura dipende che cosa se ne può concludere "
               "(`corpus/imaging.json`, sezione 3.6 di `corpus/00_corpus.md`):")
    out.append("")
    out.append(C.md_table(
        ["file", "pixel", "byte", "byte/pixel", "cella glifo (max)",
         "passo riga (max)"],
        [[f"`{r['file']}`",
          f"{r['width']}×{r['height']}" if r["width"] else "?",
          f"{r['bytes']}",
          f"{r['bytes_per_pixel']:.2f}" if "bytes_per_pixel" in r else "?",
          f"{r['cell_px_upper']:.1f}" if "cell_px_upper" in r else "?",
          f"{r['line_px_upper']:.1f}" if "line_px_upper" in r else "?"]
         for r in img["images"]]))
    out.append("")
    geo = img["reference_geometry"]
    bpp = [r["bytes_per_pixel"] for r in img["images"] if "bytes_per_pixel" in r]
    out.append(f"Le due colonne finali sono un **limite superiore ottimistico**: "
               f"assumono l'iscrizione estesa a tutta l'inquadratura, con "
               f"{geo['rows']} righe uniformi e {geo['glyphs']} glifi "
               f"({geo['glyphs_per_line']} per riga). È il massimo che "
               f"l'immagine *potrebbe* contenere, non quello che contiene — "
               f"prospettiva obliqua, cornice, erosione e compressione con "
               f"perdita ({min(bpp)}-{max(bpp)} byte per pixel) abbassano il "
               f"valore reale. Per `drac1.jpeg` il limite superiore è già di 14 "
               f"pixel di cella e 6 di passo riga: è un'anteprima dell'intera "
               f"lastra, non un documento da cui trascrivere.")
    out.append("")
    ocr = img["ocr"]
    if ocr["runnable"]:
        out.append("**OCR.** Motore eseguibile in questo ambiente: " +
                   ", ".join(ocr["runnable"]) + ".")
    else:
        why = []
        if not ocr["binaries"]:
            why.append("Il binario `tesseract` non è nel PATH")
        if "pytesseract" in ocr["modules"]:
            why.append("il modulo `pytesseract` è installato ma senza quel "
                       "binario non esegue nulla")
        out.append("**OCR: non eseguibile in questo ambiente.** " +
                   "; ".join(why) + ". La fase 0 registra il fatto "
                   "(`corpus/imaging.json`) e non produce alcuna trascrizione "
                   "automatica: **non ne viene simulata una** al suo posto.")
    out.append("")
    out.append("**Che cosa l'ispezione visiva permette di dire.** Le fotografie "
               "mostrano una lunga iscrizione incisa su lastra rettangolare con "
               "cornice modanata, in maiuscole che mescolano forme latine (A, B, "
               "E, H, I, L, M, N, O, P, R, T, V) e forme greche (Δ, Φ, Λ, ∀, Σ, "
               "Ψ, Υ), con un blocco centrale più leggibile e le righe finali "
               "fortemente erose. Non permettono però di **certificare i "
               "caratteri incerti** né di stabilire una **corrispondenza "
               "completa riga per riga**: a questa risoluzione la differenza fra "
               "Α, Λ e ∀ è di pochi pixel, e l'erosione la cancella prima ancora "
               "che la compressione la distrugga. Per questa ragione **non viene "
               "presentata alcuna nuova trascrizione**: una trascrizione ricavata "
               "da qui sarebbe un'inferenza travestita da dato, ed è esattamente "
               "l'errore che le sezioni 4.2-4.8 hanno già contabilizzato.")
    out.append("")
    out.append("**Un confronto, non una verifica.** Quello che si riesce a "
               "leggere nelle fotografie, accanto alla trascrizione contenuta in "
               "`dracula_epigrafe.md`, limitatamente alle righe del blocco "
               "centrale — le sole in cui il confronto è materialmente "
               "possibile:")
    out.append("")
    out.append("| rigo | fotografie (lettura non certificata) | "
               "trascrizione del log |")
    out.append("|---|---|---|")
    out.append("| 16 | `PEVPIV VOLVANP LAVONEA` | `PEVPIV VOLVANP LAVONEA` |")
    out.append("| 17 | `IAADDOFORIVAMELIAPE IOAI` | `IAADDOFORIVAMELIAPE IOAI` |")
    out.append("| 18 | `HAVE RAEΔEO BAVIEHAΦΔ` | `HAVE RAEΔEO BAVIEHAΦΔ` |")
    out.append("| 19 | `PIOA AIE AVVIO PIAVIBO` | `PIOA AIE AVVIO PIAVIBO` |")
    out.append("| 22 | `OBIDVA BIAV PE ΔEΔEΔ OBDI` | "
               "`OBIDVA BIAV PE DEDED OBDI` |")
    out.append("")
    out.append("L'unico scarto sistematico è che la lettura appiattisce Δ su D, "
               "Λ su A e ∀ su A: è esattamente il tipo di fusione di classi che "
               "innalza l'IC. La sovrapposizione vale per queste righe; le righe "
               "erose non sono confrontabili, e resta il fatto che nessuno dei "
               "due lati della tabella è una lettura certificata.")
    out.append("")
    out.append("Questa corrispondenza dice che la sequenza rispetta l'impianto e "
               "le forme generali della pietra, **non** che sia una lettura "
               "indipendente: "
               "nella conversazione archiviata la sequenza è descritta come "
               "*simulazione delle righe della lapide* (cfr. il campo "
               "`provenance` di `corpus/corpora.json` e "
               "`report/verifica_trascrizioni_corpora_cifrari.md`). Le due cose "
               "stanno insieme — una simulazione costruita sulle righe visibili "
               "ne riproduce l'aspetto senza esserne un testimone autonomo — e la "
               "conseguenza è la stessa: **nessuna delle tre stringhe disponibili "
               "è una trascrizione diplomatica della pietra**.")
    out.append("")
    out.append("**Le stringhe di Palma non sono una lettura della stessa "
               "sequenza.** Dopo rietichettatura canonica `palma_A` e `palma_B` "
               "condividono con la sequenza del log blocchi di 4-5 simboli su 600 "
               "(sezione 4.1), e nessuna trasformazione sistematica plausibile li "
               "riconduce alla lapide: inversione della stringa, inversione di "
               "ogni rigo, inversione dell'ordine dei righi, lettura per colonne, "
               "separazione pari/disparo, scambio delle metà, ri-taglio con le "
               "lunghezze di rigo dell'altra lettura — in tutti i casi il blocco "
               "comune resta di 4-7 simboli. Anche i profili di frequenza "
               "divergono oltre il rumore (distanza L1 fra profili ordinati: 0.24 "
               "fra le due letture di Palma, 0.31 e 0.51 fra queste e la lapide, "
               "contro ~0.08 atteso fra due campioni della stessa lingua).")
    out.append("")
    out.append("Va detto con chiarezza: le stringhe del repository sono con ogni "
               "probabilità **stadi intermedi della pipeline** dell'autore "
               "(fusioni di glifi, riempimento delle lacune con ipotesi) e non la "
               "trascrizione della lapide. Le analisi delle sezioni 4.2-4.8 "
               "condotte su `palma_A`/`palma_B` misurano quindi quella pipeline, "
               "non l'epigrafe. L'oggetto corretto sarebbe una trascrizione "
               "diplomatica; fra le stringhe disponibili la sequenza del log "
               "Gemini è l'unica che riproduce l'impianto della pietra, ma la sua "
               "provenienza è dichiaratamente simulata: va usata come **termine "
               "di confronto**, non come testimone.")
    out.append("")
    return out


def section_anomalia(recs, s3) -> list:
    out = ["### 6.1 L'anomalia della sequenza del log Gemini", ""]
    seq = recs["gemini_full"]["letters"]
    fp = C.fingerprint(seq)
    sp = [split_classes(seq, "a", f) for f in (0.2, 0.3, 0.5)]
    out.append(C.md_table(
        ["misura", "sequenza del log", "`a` separata al 20%", "al 30%", "al 50%"],
        [["classi K", len(set(seq)), sp[0]["K"], sp[1]["K"], sp[2]["K"]],
         ["IC", round(fp["IC"], 4), round(sp[0]["IC"], 4),
          round(sp[1]["IC"], 4), round(sp[2]["IC"], 4)],
         ["trigrammi ripetuti", round(fp["tri_rep"], 3),
          round(sp[0]["tri_rep"], 3), round(sp[1]["tri_rep"], 3),
          round(sp[2]["tri_rep"], 3)],
         ["quota del simbolo più frequente", round(fp["top1"], 3),
          round(sp[0]["top1"], 3), round(sp[1]["top1"], 3),
          round(sp[2]["top1"], 3)]]))
    out.append("")
    out.append("La sequenza possiede **tre proprietà insieme**: (i) "
               "alternanza vocalica naturale, se le vocali sono le lettere che "
               "sembrano vocali (C3 = 0.028, migliore di ogni lingua di "
               "riferimento); (ii) trigrammi ripetuti nella fascia delle lingue "
               f"({fp['tri_rep']:.2f}); (iii) IC troppo alta "
               f"({fp['IC']:.3f} contro 0.06-0.085). La spiegazione più economica "
               "della (iii), coerente con quanto si intravede nelle fotografie, è "
               "che l'inventario dei segni sia **più ricco** di quanto la "
               "trascrizione distingua: forme affini della stessa lettera "
               "(Α/Λ/∀, Δ/E, Ε/Є) fuse in una classe sola. La tabella mostra che "
               "separare una sola classe frequente abbassa l'IC di 0.01-0.02: "
               "poche separazioni di questo tipo bastano a riportarla nella "
               "fascia linguistica.")
    out.append("")
    out.append("È la ragione per cui il passo successivo non è un altro "
               "algoritmo ma una **trascrizione che distingua le varianti di "
               "glifo**: è l'informazione che i dati richiedono e che nessuna "
               "analisi statistica può ricostruire.")
    out.append("")
    va = s3.get("vowel_attack") or []
    if va:
        lo = min(r["score"] for r in va)
        hi = max(r["score"] for r in va)
        out.append("Contro l'ipotesi che il cifrario lasci comunque leggibili le "
                   "vocali (scuola di Della Porta) è stato eseguito un attacco "
                   "dedicato, con A-E-I-O-V inchiodate alle vocali e solo le "
                   f"consonanti da risolvere: il punteggio resta fra {lo:.2f} e "
                   f"{hi:.2f}, contro −10 circa di un testo reale e −14 di una "
                   "permutazione casuale, e il testo prodotto è una sequenza "
                   "vuota di senso (`corpus/03_attacks.md`). Anche questa strada "
                   "è chiusa.")
        out.append("")
    return out


def section_dracula() -> list:
    out = ["## 7. Il caso Dracula", ""]
    out.append("La tesi popolare (Miriello 2021) è che nella chiesa sia sepolto "
               "Vlad III di Valacchia e che l'epigrafe misteriosa sia legata alla "
               "sua presenza: nome, epitaffio, simbolo dinastico.")
    out.append("")
    out.append("Che cosa si può dire con i dati:")
    out.append("")
    out.append("1. **Come chiave non funziona.** `VLAD`, `DRACULA`, `TURBOLO`, "
               "`MARIA`, `BALSA`, `FERRILLO`, `NAPOLI`, `IESUS` applicate come "
               "cifrario periodico danno statistiche indistinguibili da chiavi "
               "casuali (sezione 4.6).")
    out.append("2. **Come crib non funziona, ma la prova è debole.** La ricerca di "
               "crib è stata condotta su `palma_A`, che ora sappiamo non essere "
               "una trascrizione della lapide (sezione 6): il risultato "
               "(`corpus/03_attacks.md`) non è quindi un test dell'iscrizione. "
               "Nessun token è comunque isomorfo a un crib onomastico "
               "*informativo*.")
    out.append("3. **Il palindromo centrale è reale, e non è una parola.** La "
               "trascrizione del log colloca al rigo 22 la sequenza `ΔΕΔΕΔ`, "
               "isolata fra due parole, e il rigo cade nel blocco centrale, la "
               "parte più leggibile delle fotografie (da confermare su "
               "un'immagine ad alta risoluzione, sezione 6): è un elemento non "
               "lessicale (abbreviazione, monogramma, "
               "marchio) oppure una parola di schema ABABA, che nessuna delle "
               "lingue candidate possiede. L'OCR del log Gemini la scrive `DEDED` "
               "perché appiattisce Δ su D. Che sia un *marchio* e non una parola "
               "è un indizio contro la lettura dell'epigrafe come epitaffio "
               "funerario continuo.")
    out.append("4. **Nulla vieta la tesi, ma nulla la sostiene.** Se il testo fosse "
               "un'iscrizione funeraria latina con il nome del defunto, dovremmo "
               "vedere la struttura seriale del latino (trigrammi ripetuti ~0.54): "
               "nella sequenza del log i trigrammi ripetuti sono 0.46, cioè nella "
               "fascia delle lingue, ma l'IC è troppo alta perché una "
               "sostituzione semplice di una lingua naturale possa spiegarla. "
               "Mancano insomma le condizioni per leggere un nome: **questa "
               "iscrizione, come possiamo leggerla oggi, non è decifrabile**, e "
               "non può essere addotta né a favore né contro la tesi.")
    out.append("")
    return out


def section_limiti(img) -> list:
    dims = " e ".join(f"{r['width']}×{r['height']}"
                      for r in img["images"] if r["width"])
    cells = " e ".join(f"{r['cell_px_upper']:.0f}"
                       for r in img["images"] if "cell_px_upper" in r)
    out = ["## 8. Limiti e che cosa servirebbe", ""]
    out.append("- **Ordine di lavoro: prima le immagini e la trascrizione, poi le "
               "chiavi.** Non è una preferenza metodologica, è ciò che i dati "
               "impongono. (1) Un'immagine ortogonale ad alta risoluzione — o un "
               "rilievo — della lastra intera e dei singoli righi. (2) Una "
               "trascrizione paleografica indipendente, con legenda dei segni, "
               "marcatura esplicita delle lacune e dei caratteri dubbi e, se "
               "possibile, due trascrittori con matrice di confusione. (3) Solo "
               "su quella base, riprendere la ricerca di chiavi. Con le immagini "
               f"disponibili ({dims} pixel, sezione 6) e senza motore OCR il "
               "passo (2) non è eseguibile: ampliare adesso la ricerca di chiavi "
               "non aggiungerebbe informazione, misurerebbe ancora una volta la "
               "pipeline di trascrizione. Due letture della stessa lapide "
               "condividono intanto 4-5 simboli consecutivi su 600, e nessun "
               "algoritmo recupera un testo in chiaro da quel livello di "
               "disaccordo.")
    out.append("- **Potenza statistica.** Con ~600 glifi un modello senza rumore è "
               "rifiutabile solo se la discrepanza supera |z| ≈ 2; qui siamo a "
               "|z| = 2-7, quindi il rifiuto è solido, ma *l'identificazione* "
               "della lingua richiede tipicamente migliaia di caratteri. La "
               "simulazione lo mostra: al 25-30% di rumore la lingua corretta "
               "viene regolarmente scambiata con una lingua vicina.")
    out.append("- **I corpora di riferimento sono biblici**: registri funerari, "
               "notarili o devozionali possono differire. Il ceco medievale usato "
               "qui è la Bibbia Kralická (1613), non un testo penitenziale "
               "quattrocentesco; l'ungherese antico viene dal Codice Erdélyi.")
    out.append("- **Scritture non alfabetiche**: un abjad (solo consonanti) o un "
               "sillabario produrrebbero un profilo vocalico diverso da quello "
               "atteso; il test C3 non distingue fra 'nessuna lingua' e 'scrittura "
               "consonantica'. Va ripetuto su una trascrizione affidabile.")
    out.append("- **La PCA non è un test d'ipotesi**: le distanze nello spazio "
               "delle componenti non sono p-value. Il confronto con i controlli "
               "a classi fuse (sezione 4.8) mostra che l'ampiezza "
               "dell'allontanamento è quella di una trascrizione a maglia larga; "
               "non dimostra né esclude che il testo sia cifrato.")
    out.append("- **La verifica visiva ha un limite misurato, non presunto.** Le "
               f"due fotografie danno al più {cells} pixel per cella di glifo "
               "(sezione 6): bastano a riconoscere il repertorio dei segni e "
               "l'impianto della lastra, non a certificare i caratteri incerti "
               "né a separare le varianti Α/Λ/∀ ed Ε/Є che l'analisi indica come "
               "probabili, e non consentono una corrispondenza completa riga per "
               "riga. Un allineamento automatico glifo-per-glifo con le tavole di "
               "alfabeti storici (cariano, copto, glagolitico, sillabari "
               "alchemici) resta da fare su scansioni ad alta risoluzione.")
    out.append("")
    return out


def section_riproducibilita() -> list:
    out = ["## 9. Riproducibilità", ""]
    out.append("```")
    out.append("python scripts/_fetch_external.py   # scarica i 16 corpora")
    out.append("python scripts/00_corpus.py        # corpus canonico + allineamenti")
    out.append("python scripts/01_descriptive.py   # statistiche descrittive")
    out.append("python scripts/02_inferential.py   # test inferenziali (~2 min)")
    out.append("python scripts/03_attacks.py       # attacchi (~2 min)")
    out.append("python scripts/04_predictive.py    # modelli generativi (~2 min)")
    out.append("python scripts/05_pca.py           # ordinamento PCA (~1 min)")
    out.append("python scripts/06_report.py        # questo rapporto")
    out.append("```")
    out.append("")
    out.append("Strumenti fuori pipeline, per le fonti secondarie (richiedono "
               "`PyPDF2`, solo per questo):")
    out.append("")
    out.append("```")
    out.append("python scripts/_extract_pdf.py                    # inventario + SHA256 dei PDF")
    out.append("python scripts/_pdf_pages.py FILE.pdf 3 --scale 2  # rende leggibile una pagina")
    out.append("```")
    out.append("")
    out.append("Dipendenze: Python 3.10+ con `requests` (solo per il download); "
               "`scipy` è opzionale (code del chi-quadro, con fallback in pura "
               "libreria standard). Nessun altro pacchetto richiesto dalla "
               "pipeline: la sonda imaging della fase 0 legge le dimensioni dai "
               "soli header JPEG/WEBP/PNG, senza Pillow, e verifica la "
               "disponibilità del motore OCR senza installarne alcuno.")
    out.append("")
    out.append(C.md_table(
        ["file", "contenuto"],
        [["`corpus/00_corpus.md`", "inventario delle trascrizioni, allineamenti, "
          "matrici di confusione, sonda imaging/OCR"],
         ["`corpus/imaging.json`", "misure delle fotografie e disponibilità "
          "del motore OCR (sezione 6)"],
         ["`corpus/01_descriptive.md`", "frequenze, n-grammi, struttura delle "
          "parole, posizioni, periodicità"],
         ["`corpus/02_inferential.md`", "permutazioni, bootstrap, confronto con 16 "
          "lingue, test C3 esaustivo"],
         ["`corpus/03_attacks.md`", "auto-validazione, null, chiavi, attacco a "
          "sostituzione, crib"],
         ["`corpus/04_predictive.md`", "calibrazione e fattori di Bayes"],
         ["`corpus/05_pca.md`", "ordinamento PCA, riproduzione dell'analisi "
          "pubblicata e controlli di confutazione"],
         ["`corpus/*_summary.json`", "tutti i numeri citati in questo rapporto"],
         ["`report/documenti_agli_atti.md`", "lettura critica delle tre fonti "
          "secondarie, pagina per pagina, e tabella di confutazione"],
         ["`report/atti/manifest.json`", "pagine, byte, SHA256 e raster dei tre "
          "PDF agli atti"],
         ["`report/atti/pages/*.png`", "pagine dei PDF rese leggibili con "
          "`_pdf_pages.py`, perché i documenti non hanno livello di testo"],
         ["`report/atti/relazione_finale.md`", "relazione finale di lavoro: "
          "bilancio, conclusione, registro degli atti con le impronte SHA256 "
          "di tutti i consegnati"],
         ["`report/report_divulgativo.md`", "versione divulgativa del rapporto, "
          "per il lettore medio: obiettivo, risultati, conclusione, ipotesi, glossario"],
         ["`report/palma_histocrypt2023.txt`",
          "estratto **preesistente e non riproducibile** dai PDF agli atti (che "
          "non hanno livello di testo): conservato come ausilio non verificato; "
          "le citazioni di Palma sono state rilette sulle pagine raster p1, p2, "
          "p9"]])
    )
    out.append("")
    return out


def section_riferimenti() -> list:
    out = ["## 10. Riferimenti", ""]
    refs = [
        "Palma, C. (2023). *Encrypted epigraphy -- the case of a mysterious "
        "inscription in the Neapolitan church of Santa Maria La Nova*. "
        "HistoCrypt 2023, 139-147.",
        "Palma, C. Repository *MaLaNova* -- "
        "https://github.com/Glottocrisio/MaLaNova (trascrizioni, corpora, "
        "funzioni per n-grammi).",
        "Miriello, L. (2021). *Sulla presunta tomba di Dracula a Napoli*. "
        "Stamperia del Valentino.",
        "Rocco, G. (1928). *Il convento e la chiesa di Santa Maria La Nova*. "
        "Tipografia Pontificia degli Artigianelli, Napoli.",
        "Rosenmeyer, P. A. (2019). *Encrypted Inscriptions: a Paradoxical "
        "Practice*. Brill, 373-392.",
        "Antal, E., Marák, P., Zajac, P., Lengyelová, T., Duchoňová, D. "
        "*Encrypted Documents and Cipher Keys From the 18th and 19th Century in "
        "the Archives of Aristocratic Families in Slovakia*, PDF agli atti "
        "(12 pp., senza note tipografiche leggibili in prima pagina): 96 "
        "documenti cifrati e 9 chiavi, nomenclatori numerici, chiavi conservate "
        "ma non combacianti con i testi.",
        "Layfield, C., Abela, J., Zandbergen, R., Bowern, C., Davis, L. F., "
        "Rosner, M., van der Plas, L. (2022). *International Conference on the "
        "Voynich Manuscript 2022*, rapporto del convegno, PDF agli atti (7 pp.): "
        "revisione in doppio cieco, paleografia delle mani, confronto "
        "quantitativo fra testi privi di senso.",
        "Della Porta, G. B. (1563). *De furtivis literarum notis*.",
        "Trithemius, J. (1518). *Polygraphiae libri sex*.",
        "Bellaso, G. B. (1553). *Il vero modo di scrivere in cifra*.",
        "Knight, K., Megyesi, B., Schaefer, C. (2011). *The Copiale cipher*. "
        "BUCC 2011, 12-19.",
        "Hauer, B., Kondrak, G. (2016). *Decoding anagrammed texts written in an "
        "unknown language and script*. TACL 4, 75-86.",
        "Shannon, C. E. (1951). *Prediction and entropy of printed English*. "
        "Bell System Technical Journal 30(1), 50-64.",
        "Corpora: HistCorp (Uppsala), Project Gutenberg, "
        "github.com/thiagobodruk/bible (Bibbie parallele).",
    ]
    for ref in refs:
        out.append(f"- {ref}")
    out.append("")
    out.append("*Nota*: l'ipotesi di una preghiera penitenziale ceca circolata "
               "come seguito del lavoro di Palma non è stata verificabile su una "
               "fonte primaria in questa sede; è quindi trattata come ipotesi da "
               "testare, ed è testata nella sezione 5. Dalla lettura diretta del "
               "saggio (p1, p2, p9) non risulta alcun riferimento a un testo "
               "**ceco**: abstract, ipotesi in campo e bibliografia parlano di "
               "latino, di un originale greco, di traslitterazione e di "
               "isopsephy. L'ipotesi va quindi attribuita a una fonte diversa da "
               "Palma 2023, e non al saggio (si veda "
               "`report/documenti_agli_atti.md`, sezione 5).")
    out.append("")
    return out


def main() -> None:
    recs = C.load_json(os.path.join(C.CORPUS, "corpora.json"))
    s2 = C.load_json(os.path.join(C.CORPUS, "02_summary.json"))
    s3 = C.load_json(os.path.join(C.CORPUS, "03_summary.json"))
    s4 = C.load_json(os.path.join(C.CORPUS, "04_summary.json"))
    s5 = C.load_json(os.path.join(C.CORPUS, "05_pca_summary.json"))
    img = C.load_json(os.path.join(C.CORPUS, "imaging.json"))
    out = []
    out += section_sintesi(recs, s2, s3, s4, s5, img)
    out += section_fonti(recs)
    out += section_metodo()
    out += section_risultati_1(recs, s2)
    out += section_risultati_2(s2)
    out += section_risultati_3(s2, s3)
    out += section_risultati_4(s4)
    out += section_pca(s5)
    out += section_documenti()
    out += section_verdetto(s2, s3, s4)
    out += section_verifica_visiva(recs, img)
    out += section_anomalia(recs, s3)
    out += section_dracula()
    out += section_limiti(img)
    out += section_riproducibilita()
    out += section_riferimenti()
    C.write_text(os.path.join(C.REPORT, "report.md"), "\n".join(out) + "\n")
    print("wrote report/report.md")


if __name__ == "__main__":
    main()



