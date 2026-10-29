# L'epigrafe di Santa Maria la Nova: analisi statistica e crittanalitica

Rapporto generato da `scripts/06_report.py`: ogni numero proviene dai file in `corpus/`, le tabelle complete stanno in `corpus/00_corpus.md` ... `corpus/05_pca.md`. La domanda è duplice: *che tipo di testo è* questa epigrafe, e *che cosa si può dire dell'ipotesi Dracula*.

## 1. Sintesi

L'oggetto è l'epigrafe della cappella Turbolo (Santa Maria la Nova, Napoli): circa 600 glifi in un alfabeto non altrimenti attestato, accanto all'iscrizione latina dell'indulgenza di Gregorio XIII e alla tomba che la tradizione popolare attribuisce a Vlad III di Valacchia.

| lettura | righe | glifi | classi K | IC | IC x K | H (bit) |
|---|---|---|---|---|---|---|
| `palma_A` | 38 | 584 | 24 | 0.0595 | 1.4290 | 4.2690 |
| `palma_B` | 1 | 678 | 23 | 0.0813 | 1.8700 | 3.9900 |
| `gemini_full` | 36 | 569 | 23 | 0.1147 | 2.6380 | 3.5500 |

Risultati principali:

1. **Il testo non è casuale.** L'IC dista 38-146 deviazioni standard da quello di una stringa uniforme con lo stesso alfabeto, e il test di Friedman rifiuta l'uniformità con p < 1e-12 in tutte le letture.
2. **Nessuna lingua naturale in chiaro è compatibile** con le letture di Palma: la migliore ha |z| medio 2.61 (`palma_A`, Czech (Bible Kralicka 1613)) e 2.08 (`palma_B`, Greek (Brenton, translit.)) su cinque statistiche invarianti. Il difetto è sistematico e riguarda la ripetizione dei bigrammi e dei trigrammi, non le frequenze dei singoli glifi.
3. **Le trascrizioni non concordano fra loro, e la fotografia dice perché**: dopo rietichettatura canonica due letture della stessa lapide condividono al massimo 4 simboli consecutivi su 584 e 678 (`palma_A` vs `palma_B`) e 5 su 569 e 678 (`palma_B` vs `gemini_full`). La sequenza del log Gemini riproduce l'impianto e le forme della pietra (`drac1.jpeg`, `drac2.webp`), ma la sua provenienza dichiarata è quella di una **simulazione delle righe** (`corpus/corpora.json`, `report/verifica_trascrizioni_corpora_cifrari.md`): somiglia alla lapide senza esserne un testimone indipendente. Le stringhe di Palma non sono letture della stessa sequenza e vanno considerate stadi intermedi della sua pipeline (sezione 6). Ne segue che **nessuna delle stringhe disponibili è una trascrizione diplomatica**, ed è la ragione principale per cui il problema sembrava irrisolvibile.
4. **Gli attacchi classici falliscono in modo informativo**: il solver a sostituzione è validato su tre testi di controllo che decifra esattamente (divario massimo 0.00 nats), ma sull'epigrafe si ferma a -13.45 nats/finestra contro un livello di testo reale di -10.09 (baseline casuale -14.00). Null, periodicità e chiavi onomastiche (VLAD, DRACULA, TURBOLO...) non producono nulla di significativo.
5. **Un modello di trascrizione rumorosa spiega `palma_A`** con un tasso di errore del 30% e log-verosimiglianza 13.1 (oggetti di origine nota: 14.3-16.2), ma a quel rumore la lingua non è più identificabile (fattori di Bayes entro un ordine di grandezza). `palma_B` resta più in basso (6.9) e `gemini_full` è incompatibile con tutti i modelli (-28.2).
6. **L'ordinamento PCA proposto a parte è riprodotto e ridimensionato** (sezione 4.8): le sue coordinate tornano con scarto mediano 0.24, ma i 28 descrittori sono invarianti per sostituzione (scarto esattamente nullo), quindi la posizione non può testimoniare un cifrario; testi **in chiaro** con una o due classi di glifi fuse hanno la stessa distanza dal centro delle letture, e le attribuzioni linguistiche per prossimità non superano il null (p = 0.15).
7. **Il verdetto su Dracula è negativo, ma per assenza di dati**: con le trascrizioni disponibili nessuna affermazione sul contenuto (onomastica draculiana, preghiera penitenziale ceca, tavola didattica) è verificabile né falsificabile.
8. **Il limite non è più un'opinione: è misurato.** Le due fotografie disponibili sono da 225×225 e 544×1024 pixel e nessun motore OCR è installato in questo ambiente: per questo il rapporto **non presenta alcuna nuova trascrizione**. Il passo successivo è un'immagine ortogonale ad alta risoluzione — o un rilievo — con una trascrizione paleografica indipendente, legenda dei segni e lacune marcate; solo dopo ha senso tornare alla ricerca di chiavi.

Il bilancio del lavoro, la conclusione finale e il registro dei consegnati con le impronte SHA256 sono depositati in `report/atti/relazione_finale.md`.

## 2. Fonti e costruzione del corpus

| fonte | contenuto | uso |
|---|---|---|
| Palma 2023 (HistoCrypt), repo `Glottocrisio/MaLaNova` | 9 file di trascrizione: due letture in lettere latine (`stringaoriginale`, `stringanospaces`), una in etichette greche (`soluzione`), varianti fuse e riempite (`scriptiocontinua*`) | corpus primario |
| `dracula_epigrafe.md` (log Gemini) | trascrizione di 33 righe + blocco centrale di 8 righe ripetuto tre volte, dichiarata come simulazione delle righe della lapide | termine di confronto |
| `epigrafe drac.md` | lettura degradata, 68 righe con duplicazioni | controllo di sensibilità |
| Palma 2023, PDF HistoCrypt | metodo, IC normalizzato 1.72, entropia 4.1, tabella per 12 lingue, esiti AZdecrypt | confronto |
| Antal, Marak, Zajac, Lengyelova, Duchonova (Archivio Nazionale Slovacco) | 96 documenti cifrati e 9 chiavi, sec. XVIII-XIX: nomenclatore numerico, chiavi conservate ma non combacianti con i testi, chiaro spesso conservato accanto al cifrato | confronto |
| Layfield et al. 2022 (convegno Voynich) | rapporto di un convegno peer-reviewed su un manoscritto indecifrato: revisione in doppio cieco, paleografia, testi privi di senso che non sono tutti dello stesso tipo | criterio di metodo |
| `sources/external` (16 corpora) | Bibbie parallele (Vulgata, Kralická 1613, Riveduta, Károli, romeno, albanese, croato, slovacco, polacco, tedesco, inglese, greco) più Dante e un catechismo ceco | modelli linguistici |
| cartella `corpora/` del repo | codici ungheresi e cechi, latino umanistico, copto, greco | modelli aggiuntivi |

I tre PDF di Palma 2023, Antal et al. e Layfield et al. sono agli atti come **scansioni di pagina**: 1240×1753 px (un A4 a circa 150 ppi), nessun livello di testo, quindi nessuna ricerca testuale possibile e in questo ambiente nessun OCR. Sono stati letti pagina per pagina (`scripts/_pdf_pages.py` rende ispezionabile una pagina; `report/atti/manifest.json` registra pagine, byte e SHA256). Che cosa se ne ricava, e quale ipotesi confutano, è in `report/documenti_agli_atti.md` e nella sezione 4.9.

Due difetti dei dati di partenza, corretti in `scripts/langmodels.py`, vanno segnalati perché invalidano parte del confronto pubblicato:

- i file `bibliahuszita*` e `czechcodex.txt` sono in realtà **ungherese** (Codice di Monaco, 1466), non ceco: la riga 'Old Czech' della tabella di Palma 2023 corrisponde quindi a un corpus ungherese;
- i corpora del repository sono doppiamente codificati (UTF-8 letto come cp437) e vanno riparati prima di qualsiasi calcolo.

| chiave | righe | glifi | segni illeggibili | classi | token |
|---|---|---|---|---|---|
| `drac_raw` | 68 | 863 | 0 | 24 | 201 |
| `gemini_central` | 8 | 164 | 0 | 18 | 27 |
| `gemini_central_in_full` | 8 | 165 | 0 | 17 | 27 |
| `gemini_full` | 36 | 569 | 0 | 23 | 124 |
| `palma_A` | 38 | 584 | 20 | 24 | 123 |
| `palma_A2` | 19 | 357 | 9 | 24 | 63 |
| `palma_A_nosp` | 1 | 584 | 20 | 24 | 27 |
| `palma_B` | 1 | 678 | 93 | 23 | 1 |
| `palma_B2` | 1 | 678 | 184 | 24 | 1 |
| `palma_B3` | 3 | 641 | 89 | 24 | 3 |
| `palma_B4` | 52 | 589 | 0 | 24 | 52 |
| `palma_C` | 1 | 681 | 174 | 17 | 1 |
| `palma_C_nq` | 1 | 681 | 0 | 17 | 1 |

## 3. Metodo

Il punto metodologico centrale è che **le frequenze non sono confrontabili direttamente** fra un cifrario e un testo in chiaro: una sostituzione permuta i simboli, quindi la distribuzione del cifrario è una permutazione di quella del testo, non la stessa. Confrontare le frequenze (come fa la letteratura corrente, AZdecrypt compreso) è lecito solo *dopo* aver fissato la chiave.

Qui si usano invece statistiche **invarianti per rietichettatura**, calcolate su finestre di lunghezza identica nei corpora di riferimento:

| statistica | perché è invariante | cosa misura |
|---|---|---|
| IC | somma su tutte le classi | concentrazione globale |
| H (entropia) | funzione delle sole frequenze | ampiezza efficace dell'alfabeto |
| quota del simbolo più frequente | ordinamento delle frequenze | asimmetria della distribuzione |
| tasso di bigrammi ripetuti | una biiezione mappa bigrammi in bigrammi | struttura seriale locale |
| tasso di trigrammi ripetuti | idem | struttura seriale a medio raggio |

Ogni affermazione è accompagnata da un **null calibrato**: permutazioni della stringa, finestre della stessa lunghezza estratte dai corpora, testi di controllo cifrati con lo stesso schema e di cui si conosce il testo in chiaro. Senza calibrazione un risultato negativo non è interpretabile: non si distingue fra 'il cifrario non è quello' e 'il metodo non ha potenza sufficiente'.

Avvertenza tecnica: il test di permutazione applicato all'IC è **degenere**, perché l'IC dipende solo dal multinsieme dei glifi e una permutazione lo lascia invariato (p = 1 per costruzione). Applicato invece al tasso di trigrammi ripetuti esso è informativo, perché quella statistica dipende dall'ordine.

L'ordinamento PCA (sezione 4.8) è trattato come strumento **descrittivo, non inferenziale**: le distanze non sono p-value, le componenti massimizzano la varianza e non la separazione fra lingue, e la posizione delle letture è confrontata con un null esplicito — testi di riferimento in chiaro a cui vengono fuse una o due classi di glifi, cioè l'effetto di una trascrizione che non distingue le varianti.

## 4. Risultati

### 4.1 Le letture non concordano fra loro

| coppia | glifi A | glifi B | blocco comune più lungo | quota |
|---|---|---|---|---|
| `palma_A` ~ `palma_B` | 584 | 678 | 4 | 0.0068 |
| `palma_A` ~ `gemini_full` | 584 | 569 | 4 | 0.0070 |
| `palma_B` ~ `gemini_full` | 678 | 569 | 5 | 0.0088 |
| `palma_A` ~ `palma_B2` | 584 | 678 | 4 | 0.0068 |
| `palma_B` ~ `palma_B2` | 678 | 678 | 70 | 0.1032 |

Il confronto è fatto dopo **rietichettatura canonica** (i simboli sono rinominati per ordine di prima occorrenza), che è l'unico confronto lecito fra trascrizioni che usano alfabeti-etichetta diversi: se due letture fossero la stessa stringa di glifi con nomi diversi coinciderebbero carattere per carattere.

Il blocco comune è di 4-5 simboli su ~600 fra letture di origine diversa, mentre fra due file dello stesso autore con lo stesso numero di glifi (`palma_B` e `palma_B2`) sale a un blocco di decine di simboli: la metrica distingue i gradi di parentela, e le letture indipendenti risultano **non sovrapponibili**.

### 4.2 Struttura contro il caso

| lettura | statistica | osservato | media uniforme | z | p |
|---|---|---|---|---|---|
| `palma_A` | IC | 0.0595 | 0.0417 | 37.8000 | 0.0066 |
| `palma_A` | H | 4.2685 | 4.5564 | -37.5000 | 0.0066 |
| `palma_A` | top1 | 0.1301 | 0.0585 | 17.2000 | 0.0066 |
| `palma_A` | bi_rep | 0.7530 | 0.6351 | 5.7000 | 0.0066 |
| `palma_A` | tri_rep | 0.1546 | 0.0410 | 10.4000 | 0.0066 |
| `palma_B` | IC | 0.0813 | 0.0434 | 93.9000 | 0.0066 |
| `palma_B` | H | 3.9903 | 4.5001 | -70.8000 | 0.0066 |
| `palma_B` | top1 | 0.1711 | 0.0591 | 26.3000 | 0.0066 |
| `palma_B` | bi_rep | 0.8198 | 0.7237 | 6.4000 | 0.0066 |
| `palma_B` | tri_rep | 0.2722 | 0.0521 | 16.9000 | 0.0066 |
| `gemini_full` | IC | 0.1147 | 0.0434 | 146.4000 | 0.0066 |
| `gemini_full` | H | 3.5495 | 4.4962 | -107.1000 | 0.0066 |
| `gemini_full` | top1 | 0.2144 | 0.0607 | 32.0000 | 0.0066 |
| `gemini_full` | bi_rep | 0.8873 | 0.6571 | 12.1000 | 0.0066 |
| `gemini_full` | tri_rep | 0.4586 | 0.0470 | 30.0000 | 0.0066 |

Il testo è lontanissimo da una decorazione casuale di glifi. Va però notato il segno: `palma_A` e `palma_B` stanno **sopra** il caso per concentrazione (IC, H, quota del simbolo più frequente) ma restano molto **sotto** le lingue naturali per ripetizione dei trigrammi (0.15 e 0.27 contro 0.41-0.63).

### 4.3 Struttura seriale e periodicità

| lettura | trigrammi ripetuti | null di permutazione | p (permutazione) | periodo migliore | guadagno IC | p (periodo) |
|---|---|---|---|---|---|---|
| `palma_A` | 0.1550 | 0.1080 | 0.0050 | 17 | 0.0037 | 0.4351 |
| `palma_B` | 0.2720 | 0.2400 | 0.0420 | 11 | 0.0017 | 0.9341 |
| `gemini_full` | 0.4590 | 0.4130 | 0.0080 | 11 | 0.0053 | 0.3253 |

Le due colonne di p dicono cose diverse e complementari: la prima conferma che esiste struttura seriale (il testo ripete i trigrammi molto più di una permutazione delle sue stesse lettere), la seconda mostra che **non c'è alcun periodo** nascosto. Il massimo guadagno di IC su k = 1..20 non supera mai il 95° percentile del null: la 'periodicità' intravista dagli esami di Kasiski è rumore di campionamento.

### 4.4 Confronto con sedici lingue di riferimento

**`palma_A`** (n = 584): migliori sei corrispondenze, ordinate per |z| medio

| lingua | z medio (assoluto) | z(trigrammi) | z(bigrammi) | z(IC) |
|---|---|---|---|---|
| Czech (Bible Kralicka 1613) | 2.6100 | -4.1700 | -6.5500 | 0.0600 |
| Czech (catechism) | 2.9300 | -4.6500 | -6.3200 | -0.4500 |
| Polish | 2.9400 | -4.5500 | -5.7800 | -1.1400 |
| Greek (Brenton, translit.) | 3.1800 | -4.1900 | -4.7400 | -2.9700 |
| Slovak | 3.3100 | -5.0000 | -6.6700 | -1.0900 |
| English (KJV) | 3.7500 | -5.4800 | -5.7000 | -3.1700 |

**`palma_B`** (n = 678): migliori sei corrispondenze, ordinate per |z| medio

| lingua | z medio (assoluto) | z(trigrammi) | z(bigrammi) | z(IC) |
|---|---|---|---|---|
| Greek (Brenton, translit.) | 2.0800 | -3.3100 | -3.0500 | 1.1700 |
| Albanian | 2.1400 | -4.5800 | -4.3500 | 0.2200 |
| Hungarian (Erdy codex, XV c.) | 2.2200 | -5.8000 | -4.4800 | 0.2400 |
| German (Schlachter) | 2.2400 | -5.1800 | -4.7600 | 0.8600 |
| Hungarian (Karoli) | 2.2900 | -4.3300 | -4.7900 | 1.0600 |
| English (KJV) | 3.2800 | -4.7000 | -4.0900 | 3.1600 |

**`gemini_full`** (n = 569): migliori sei corrispondenze, ordinate per |z| medio

| lingua | z medio (assoluto) | z(trigrammi) | z(bigrammi) | z(IC) |
|---|---|---|---|---|
| Hungarian (Erdy codex, XV c.) | 3.0600 | -0.4200 | 1.0900 | 6.2600 |
| Albanian | 3.4200 | -1.4700 | 0.2000 | 5.9900 |
| Romanian | 3.7000 | -1.6500 | -1.7500 | 6.6100 |
| German (Schlachter) | 3.8600 | -1.8000 | 0.2000 | 7.4400 |
| Hungarian (Karoli) | 3.9700 | -1.3100 | 0.1400 | 7.7300 |
| Greek (Brenton, translit.) | 4.0100 | -0.9200 | 0.7000 | 7.2300 |

Ogni z è calcolato su finestre di lunghezza identica a quella della lettura, quindi l'errore di campionamento è lo stesso sui due lati del confronto. **Nessuna lingua scende sotto |z| = 2**: il |z| medio minimo è 2.08. Il colpevole è sempre lo stesso: z(bigrammi) e z(trigrammi) fortemente negativi, cioè la lettura ripete troppo poco.

### 4.5 Vocali e consonanti: il test esaustivo

In ogni lingua naturale vocali e consonanti si alternano, quindi la frazione di testo che cade dentro sequenze di tre o più consonanti (`C3`) è piccola. Poiché nel cifrario i glifi sono etichette arbitrarie, si possono provare **tutti** i C(K,5) insiemi di vocali (33 649 per K = 23) e prendere il migliore: un'assegnazione migliore di quella trovata non esiste.

| lettura | miglior insieme di vocali | C3 minimo raggiungibile | C3 mediano su tutti gli insiemi | C3 migliore fra le lingue |
|---|---|---|---|---|
| `gemini_full` | `a`, `i`, `v`, `o`, `e` | 0.0281 | 0.6942 | 0.0251 |
| `palma_A` | `i`, `a`, `u`, `r`, `n` | 0.3048 | 0.7123 | 0.0250 |
| `palma_B` | `ρ`, `α`, `ω`, `δ`, `λ` | 0.1652 | 0.6947 | 0.0253 |

È il risultato più diagnostico dell'analisi: sotto la trascrizione **Gemini** l'insieme ottimale è `a, i, v, o, e` con C3 = 0.028, cioè un'alternanza perfettamente naturale (le vocali sono le lettere che *sembrano* vocali); sotto le trascrizioni di Palma nessun insieme scende a livelli naturali. Poiché `C3` dipende dall'ordine dei glifi e non dai loro nomi, la differenza non è un effetto delle etichette: le due trascrizioni descrivono **strutture diverse**.

### 4.6 Attacchi classici

**Auto-validazione del solver** (cifrario noto, testo in chiaro noto, stessa lunghezza dell'epigrafe):

| modello linguistico | punteggio raggiunto | punteggio del vero testo in chiaro | divario |
|---|---|---|---|
| Latin (Vulgate) | -10.4610 | -10.4610 | 0 |
| Czech (Bible Kralicka 1613) | -9.9910 | -9.9910 | 0 |
| Italian (Riveduta) | -10.1050 | -10.1050 | 0 |

L'attacco procede per stadi, con modelli di 2, 3, 4 e 5 grammi e chiave trasferita da uno stadio al successivo: un 5-grammo da partenza casuale si incastra in ottimi locali (misurato sul controllo ceco, dove sbagliava di 3.2 nats), mentre la scala progressiva recupera il testo in chiaro esatto in tutti e tre i casi. **Il solver non è quindi il limite del risultato che segue.**

**Attacco all'epigrafe**:

| lettura | modello | punteggio | baseline casuale | livello di testo reale | parole latine trovate |
|---|---|---|---|---|---|
| palma_B | Latin | -13.4520 | -13.9980 | -10.0920 | 6 |
| palma_B | Czech | -13.5450 | -13.9980 | -10.2910 | 5 |
| palma_B | Italian | -13.4310 | -13.9980 | -9.8110 | 6 |
| palma_A | Latin | -13.5770 | -13.9330 | -10.5670 | 3 |
| palma_A | Czech | -13.6280 | -13.9560 | -10.4690 | 3 |
| palma_A | Italian | -13.5450 | -13.9490 | -9.9540 | 4 |

**Ipotesi dei null**: il miglior guadagno di IC ottenibile eliminando un solo glifo è 0.00709 (`δ`), contro 0.00583 nei controlli senza null e 0.00450 in quelli con il 10% di null (p = 0.0769): l'ipotesi non è sostenuta.

**Chiavi onomastiche** (Vigenère/Bellaso, chiave applicata come valore delle lettere latine modulo il numero di classi):

| chiave | IC dopo decifratura | trigrammi ripetuti | media delle chiavi casuali | p |
|---|---|---|---|---|
| VLAD | 0.0521 | 0.1300 | 0.1220 | 0.2394 |
| DRACULA | 0.0485 | 0.0960 | 0.1030 | 0.6808 |
| TURBOLO | 0.0469 | 0.0810 | 0.1010 | 0.9601 |
| MARIA | 0.0524 | 0.1350 | 0.1280 | 0.2868 |
| BALSA | 0.0509 | 0.1140 | 0.1310 | 0.9252 |
| FERRILLO | 0.0487 | 0.0860 | 0.0810 | 0.3591 |
| NAPOLI | 0.0499 | 0.0920 | 0.1060 | 0.8828 |
| IESUS | 0.0506 | 0.1480 | 0.1290 | 0.0848 |

Nessuna chiave porta il testo nella fascia linguistica (IC ~ 0.073, trigrammi ~ 0.5) e nessun p è significativo: i nomi della tradizione non sono la chiave di un cifrario periodico. Il risultato però **non falsifica** l'ipotesi cifrata, e la ragione è documentaria, non statistica: in un archivio reale di cifrari sette-ottocenteschi le chiavi conservate non corrispondono ai testi conservati (sezione 4.9), quindi la mancata corrispondenza si osserva anche dove cifrato e chiave esistono entrambi.

### 4.7 Modello generativo: quanto rumore serve?

Si confronta la famiglia `testo in chiaro (lingua) -> sostituzione -> [null] -> [rumore di trascrizione]` con la firma invariante di ogni lettura, con verosimiglianza gaussiana diagonale su cinque statistiche e tasso di rumore marginalizzato su una griglia.

**Calibrazione** su oggetti di origine nota:

| oggetto | lingua vera | lingua attribuita | rumore inferito | log-verosimiglianza |
|---|---|---|---|---|
| clean substitution of Latin | Latin (Vulgate) | Latin (Vulgate) | 0.0500 | 15.1800 |
| Latin + 10% nulls | Latin (Vulgate) | Croatian | 0.0500 | 16.2300 |
| Latin, 10% transcription noise | Latin (Vulgate) | Latin (Vulgate) | 0.1000 | 14.2600 |
| Latin, 25% transcription noise | Latin (Vulgate) | Croatian | 0.3000 | 16.1800 |
| uniform random glyphs | uniform | Czech (catechism) | 0.4000 | -13.0500 |

La calibrazione fissa l'inviluppo del metodo: il testo pulito è attribuito alla lingua giusta, mentre il testo con null e quello con il 25% di rumore vengono attribuiti a una lingua vicina (croato) pur ricevendo verosimiglianza alta; una stringa casuale riceve verosimiglianza fortemente negativa. Due conseguenze: **l'etichetta della lingua non è affidabile quando c'è rumore**, mentre **la verosimiglianza assoluta separa bene testo e non testo**.

**Epigrafe**:

| lettura | modello migliore | log-verosimiglianza marginale | distacco dal secondo | modello peggiore |
|---|---|---|---|---|
| `gemini_full` | German (Schlachter) (0%) | -28.1800 | 0.0600 | -466.1700 |
| `palma_A` | Hungarian (Karoli) (30%) | 13.0600 | 0.5600 | 5.2700 |
| `palma_B` | Hungarian (Erdy codex, XV c.) (15%) | 6.8800 | 1.2000 | -55.4200 |

`palma_A` arriva a 13.1, appena sotto la fascia degli oggetti di origine nota (14.3-16.2): è compatibile con *qualche* lingua trascritta con molto rumore — o con una lingua meno rappresentata nei corpora — ma il distacco dal secondo classificato è minimo e il tasso richiesto (~30%) azzera il potere discriminante. `palma_B` e `gemini_full` restano fuori fascia.

### 4.8 Ordinamento PCA: rifatto e confutato

L'analisi PCA distribuita a parte (`report/pca_analisi.md`) è stata ricostruita da zero nella fase 1c (`scripts/05_pca.py`, `corpus/05_pca.md`): 28 descrittori, 16 corpora di riferimento, 4.800 finestre, autosolutore in sola libreria standard. Le sue coordinate si riproducono:

| lettura | pubblicato | ricalcolato | scarto massimo |
|---|---|---|---|
| `palma_A` | 2.77, 1.61, 1.01 | 2.94, 1.37, 0.57 | 0.44 |
| `palma_B` | 1.29, 0.47, 3.52 | 1.54, 0.34, 3.22 | 0.30 |
| `gemini_full` | -0.87, -2.40, 6.03 | -0.56, -2.38, 6.18 | 0.31 |

Scarto massimo 0.44 deviazioni standard, mediana 0.24. Resta non ricostruibile **quali** sedici corpora abbia usato l'analisi pubblicata: la pipeline ne configura 21 e ne seleziona sedici con una regola dichiarata (almeno 30.000 lettere, il che esclude i cinque testi brevi); la riproduzione è quindi buona sul risultato e imperfetta sul protocollo.

Due ambiguità del protocollo sono state sciolte con altrettanti controlli. **Primo**: l'analisi pubblicata non dice come calcoli il «tasso di ripetizione»; rifacendo l'ordinazione con l'alternativa 1 − U/N le coordinate si spostano di 0.20 deviazioni standard al massimo e la riproduzione resta allo stesso livello — l'ambiguità non spiega le differenze residue. **Secondo**: in `report/verifica_trascrizioni_corpora_cifrari.md` esiste una seconda PCA, con codice e insieme di corpora diversi; le coordinate delle due letture Palma concordano entro 0.70 deviazioni standard e confermano lo stesso punto (le prossimità cambiano da una lettura all'altra). Due analisi indipendenti convergono: la PCA descrive, non attribuisce.

**Che cosa la PCA non può dire.** Tutti i 28 descrittori sono invarianti per rietichettatura: cifrare il testo per sostituzione li lascia **identici** (scarto massimo misurato: zero su tutti i controlli). La posizione nello spazio non può quindi testimoniare né escludere un cifrario: l'ipotesi dell'analisi pubblicata secondo cui «una sostituzione semplice non basta» non è un suo risultato.

**Il controllo che manca.** Testi di riferimento **in chiaro, senza cifrario**, con le prime k classi di glifi fuse in una (ciò che accade quando il trascrittore non distingue varianti come Α/Λ/∀ o Ε/Є). Per `gemini_full` (distanza osservata 2.56):

| classi fuse | distanza mediana dei controlli | frazione di controlli più lontani della lettura |
|---|---|---|
| 0 | 1.29 | 0.00 |
| 1 | 2.17 | 0.25 |
| 2 | 3.65 | 0.88 |
| 3 | 5.53 | 1.00 |

Le fusioni compatibili con la distanza osservata sono `palma_A`: 1, `palma_B`: 0-1, `gemini_full`: 1-2: **la scala dell'allontanamento è quella di un testo naturale non cifrato trascritto a maglia larga**, e non richiede alcun cifrario. La direzione però non coincide (i controlli fusi si spostano sul lato opposto di PC1 rispetto a `palma_A` e `palma_B`), quindi la fusione spiega *quanto*, non *dove*: resta il profilo irregolare descritto nella sezione 6.1, che è di frequenze e non di n-grammi.

**Nota di provenienza.** La riga `gemini_full` riguarda una sequenza che la documentazione di progetto descrive come *simulazione delle righe* della lapide, non come trascrizione indipendente (`report/verifica_trascrizioni_corpora_cifrari.md`). Nessuna delle conclusioni di questa sezione cambia: l'invarianza per sostituzione vale per qualunque stringa, e le due letture Palma mostrano lo stesso allontanamento con lo stesso ordine di grandezza. Ciò che cambia è l'oggetto: quello che manca non è un algoritmo migliore, è una trascrizione diplomatica.

**Le prossimità non identificano una lingua.** La lingua più vicina cambia con il numero di componenti usate e con il campionamento; la concentrazione delle letture (massimo 10 finestre su 15 da una sola lingua per `gemini_full`) ha p = 0.15 rispetto alla stessa statistica calcolata sui punti di riferimento. «Slovacco», «ungherese storico», «italiano» sono etichette geometriche, non attribuzioni.

**Che cosa sopravvive.** La distanza dal centro, che è invariante per rotazione degli assi: `palma_A` 2.14-2.17, `palma_B` 1.63-1.66, `gemini_full` 2.46-2.58 su quattro semi di campionamento e sul sottoinsieme ridotto a dodici corpora. Non sopravvive invece la grandezza di una singola componente: PC2 e PC3 si scambiano o cambiano segno fra un campionamento e l'altro, quindi un valore come «PC3 z = 6» non è un numero riproducibile.

### 4.9 Che cosa dicono gli altri casi documentati

Tre fonti secondarie sono state messe agli atti e lette pagina per pagina (`report/documenti_agli_atti.md`): un archivio di cifrari sette-ottocenteschi con le loro chiavi, il rapporto di un convegno peer-reviewed su un manoscritto indecifrato, e il saggio di Palma. Servono a dire che cosa un cifrario di questo ambiente **dovrebbe** avere, e a confutare due inferenze che i nostri numeri invitano a trarre.

- **Il repertorio dei segni non somiglia al nostro.** Nei 96 documenti cifrati dell'Archivio Nazionale Slovacco (sec. XVIII-XIX) il sistema è il nomenclatore e il repertorio "consists of only numbers and markings of numbers", con o senza separatori (37 con, 59 senza). La nostra epigrafe ha 23 classi di glifi misti e nessun livello numerico evidente: se è un cifrario dello stesso ambiente, le manca il tratto più tipico del genere.
- **Le chiavi si conservano, ma non combaciano.** Nello stesso fondo sono conservate 9 chiavi per 96 documenti, e le chiavi conservate **non corrispondono ai testi conservati**; le chiavi sono in due fondi su tre. Ne segue una correzione al nostro paragrafo sulle chiavi onomastiche: il null (VLAD, DRACULA, TURBOLO...) **non è conclusivo**, perché la mancata corrispondenza si osserva anche dove cifrato e chiave esistono entrambi. Non falsifica e non conferma.
- **La pratica reale lascia il chiaro accanto al cifrato**: in 16 documenti il testo in chiaro è scritto sopra le righe cifrate, in 38 è in un documento separato, e solo in 8 casi su 96 il chiaro non è conservato. È l'opposto del segreto assoluto, e rafforza l'argomento di contesto di Palma: un testo esposto in vista non è un testo che si voleva nascondere.
- **La paleografia decide i segni, non la statistica.** Al convegno Voynich la relazione di apertura applica la paleografia latina al sistema di scrittura, distingue cinque mani e avverte che alcuni segni possono essere abbreviazioni o legature. È il precedente metodologico della lettura di `ΔΕΔΕΔ` come marchio o abbreviazione e non come parola (sezione 7.3).
- **Due testi privi di senso non sono dello stesso tipo.** Il confronto quantitativo fra Voynich e Słowa MS 3188 trova somiglianze, ma anche differenze statistiche sostanziali: anche se entrambi fossero privi di senso, non apparterrebbero allo stesso genere. Quindi il nostro "nessuna lingua fra 16" esclude lingue naturali e **non identifica una tecnica**: è la prima cosa da non scrivere.
- **"Potrebbe non esserci alcun mistero" è una posizione di metodo**, non una facezia: è l'obiettivo dichiarato di un convegno con tre revisori in doppio cieco, e Rosenmeyer (citata da Palma) descrive l'enigma come gioco intellettuale, «a sort of hoax». L'ipotesi beffa resta in alternativa seria — con la stessa conseguenza operativa: serve la trascrizione paleografica.

## 5. Verdetto sulle ipotesi

| ipotesi | stato | evidenza |
|---|---|---|
| Sostituzione monoalfabetica semplice di una lingua naturale | **non sostenuta** | nessuna lingua sotto la soglia di 2 deviazioni standard; attacco a sostituzione fermo a 3 nats/finestra sotto il testo reale, mentre sui controlli lo raggiunge esattamente |
| Cifrario diverso dalla sostituzione semplice, dedotto dalla PCA | **ritirata** | i 28 descrittori dell'ordinazione sono invarianti per sostituzione, quindi la posizione non distingue un cifrario da un testo in chiaro; l'allontanamento delle letture è riprodotto da testi in chiaro con una o due classi di glifi fuse (sezione 4.8) |
| Sostituzione con null | **non sostenuta** | guadagno massimo di IC 0.0071 vs 0.0058 dei controlli senza null (p = 0.0769) |
| Cifrario polialfabetico periodico | **non sostenuta** | nessun picco di IC su k = 1..20; p = 0.4351 e 0.9341 contro il null |
| Chiavi onomastiche (VLAD, DRACULA, TURBOLO, ...) | **non sostenuta** | tutte indistinguibili da chiavi casuali della stessa lunghezza |
| Testo greco scritto in lettere greche | **non sostenuta** | con le vocali greche reali C3 = 0.445, contro < 0.10 di qualsiasi lingua |
| Testo latino/italiano in chiaro travestito da alfabeto esotico | **improponibile** | la struttura seriale delle letture di Palma è troppo piatta per qualsiasi lingua naturale |
| Trascrizione rumorosa, lingua reale non identificabile | **la più compatibile** | `palma_A` al 30% di rumore raggiunge 13.1, appena sotto la fascia degli oggetti di origine nota, con fattori di Bayes entro un ordine di grandezza fra le prime lingue |
| Preghiera penitenziale ceca medievale | **non confermata** | il ceco (Kralická 1613) è la migliore corrispondenza per `palma_A` nella metrica dello z medio (`Czech (Bible Kralicka 1613)`, 2.61) ma resta molto sotto il modello migliore nel confronto generativo (Δ ln L = -4.9): nessuna convergenza fra le due prove |
| Tavola didattica / decorazione senza messaggio | **possibile, non dimostrabile** | il testo non è casuale (IC a decine di deviazioni standard dal caso), quindi qualcosa di strutturato c'è; nessun modello linguistico però lo cattura |

Le due letture non indicano la stessa lingua (`Czech (Bible Kralicka 1613)` per `palma_A`, `Greek (Brenton, translit.)` per `palma_B`): ulteriore sintomo che il rumore di trascrizione domina il segnale.

## 6. Verifica visiva: le fotografie della lapide

Nella radice del progetto ci sono due fotografie della lapide (`drac1.jpeg`, `drac2.webp`) e nessun'altra immagine. Prima di confrontarle con i testi disponibili vanno misurate, perché da quella misura dipende che cosa se ne può concludere (`corpus/imaging.json`, sezione 3.6 di `corpus/00_corpus.md`):

| file | pixel | byte | byte/pixel | cella glifo (max) | passo riga (max) |
|---|---|---|---|---|---|
| `drac1.jpeg` | 225×225 | 11932 | 0.24 | 14.2 | 6.2 |
| `drac2.webp` | 544×1024 | 162504 | 0.29 | 34.4 | 28.4 |

Le due colonne finali sono un **limite superiore ottimistico**: assumono l'iscrizione estesa a tutta l'inquadratura, con 36 righe uniformi e 569 glifi (15.8 per riga). È il massimo che l'immagine *potrebbe* contenere, non quello che contiene — prospettiva obliqua, cornice, erosione e compressione con perdita (0.236-0.292 byte per pixel) abbassano il valore reale. Per `drac1.jpeg` il limite superiore è già di 14 pixel di cella e 6 di passo riga: è un'anteprima dell'intera lastra, non un documento da cui trascrivere.

**OCR: non eseguibile in questo ambiente.** Il binario `tesseract` non è nel PATH; il modulo `pytesseract` è installato ma senza quel binario non esegue nulla. La fase 0 registra il fatto (`corpus/imaging.json`) e non produce alcuna trascrizione automatica: **non ne viene simulata una** al suo posto.

**Che cosa l'ispezione visiva permette di dire.** Le fotografie mostrano una lunga iscrizione incisa su lastra rettangolare con cornice modanata, in maiuscole che mescolano forme latine (A, B, E, H, I, L, M, N, O, P, R, T, V) e forme greche (Δ, Φ, Λ, ∀, Σ, Ψ, Υ), con un blocco centrale più leggibile e le righe finali fortemente erose. Non permettono però di **certificare i caratteri incerti** né di stabilire una **corrispondenza completa riga per riga**: a questa risoluzione la differenza fra Α, Λ e ∀ è di pochi pixel, e l'erosione la cancella prima ancora che la compressione la distrugga. Per questa ragione **non viene presentata alcuna nuova trascrizione**: una trascrizione ricavata da qui sarebbe un'inferenza travestita da dato, ed è esattamente l'errore che le sezioni 4.2-4.8 hanno già contabilizzato.

**Un confronto, non una verifica.** Quello che si riesce a leggere nelle fotografie, accanto alla trascrizione contenuta in `dracula_epigrafe.md`, limitatamente alle righe del blocco centrale — le sole in cui il confronto è materialmente possibile:

| rigo | fotografie (lettura non certificata) | trascrizione del log |
|---|---|---|
| 16 | `PEVPIV VOLVANP LAVONEA` | `PEVPIV VOLVANP LAVONEA` |
| 17 | `IAADDOFORIVAMELIAPE IOAI` | `IAADDOFORIVAMELIAPE IOAI` |
| 18 | `HAVE RAEΔEO BAVIEHAΦΔ` | `HAVE RAEΔEO BAVIEHAΦΔ` |
| 19 | `PIOA AIE AVVIO PIAVIBO` | `PIOA AIE AVVIO PIAVIBO` |
| 22 | `OBIDVA BIAV PE ΔEΔEΔ OBDI` | `OBIDVA BIAV PE DEDED OBDI` |

L'unico scarto sistematico è che la lettura appiattisce Δ su D, Λ su A e ∀ su A: è esattamente il tipo di fusione di classi che innalza l'IC. La sovrapposizione vale per queste righe; le righe erose non sono confrontabili, e resta il fatto che nessuno dei due lati della tabella è una lettura certificata.

Questa corrispondenza dice che la sequenza rispetta l'impianto e le forme generali della pietra, **non** che sia una lettura indipendente: nella conversazione archiviata la sequenza è descritta come *simulazione delle righe della lapide* (cfr. il campo `provenance` di `corpus/corpora.json` e `report/verifica_trascrizioni_corpora_cifrari.md`). Le due cose stanno insieme — una simulazione costruita sulle righe visibili ne riproduce l'aspetto senza esserne un testimone autonomo — e la conseguenza è la stessa: **nessuna delle tre stringhe disponibili è una trascrizione diplomatica della pietra**.

**Le stringhe di Palma non sono una lettura della stessa sequenza.** Dopo rietichettatura canonica `palma_A` e `palma_B` condividono con la sequenza del log blocchi di 4-5 simboli su 600 (sezione 4.1), e nessuna trasformazione sistematica plausibile li riconduce alla lapide: inversione della stringa, inversione di ogni rigo, inversione dell'ordine dei righi, lettura per colonne, separazione pari/disparo, scambio delle metà, ri-taglio con le lunghezze di rigo dell'altra lettura — in tutti i casi il blocco comune resta di 4-7 simboli. Anche i profili di frequenza divergono oltre il rumore (distanza L1 fra profili ordinati: 0.24 fra le due letture di Palma, 0.31 e 0.51 fra queste e la lapide, contro ~0.08 atteso fra due campioni della stessa lingua).

Va detto con chiarezza: le stringhe del repository sono con ogni probabilità **stadi intermedi della pipeline** dell'autore (fusioni di glifi, riempimento delle lacune con ipotesi) e non la trascrizione della lapide. Le analisi delle sezioni 4.2-4.8 condotte su `palma_A`/`palma_B` misurano quindi quella pipeline, non l'epigrafe. L'oggetto corretto sarebbe una trascrizione diplomatica; fra le stringhe disponibili la sequenza del log Gemini è l'unica che riproduce l'impianto della pietra, ma la sua provenienza è dichiaratamente simulata: va usata come **termine di confronto**, non come testimone.

### 6.1 L'anomalia della sequenza del log Gemini

| misura | sequenza del log | `a` separata al 20% | al 30% | al 50% |
|---|---|---|---|---|
| classi K | 23 | 24 | 24 | 24 |
| IC | 0.1147 | 0.0988 | 0.0947 | 0.0918 |
| trigrammi ripetuti | 0.4590 | 0.3770 | 0.3790 | 0.3510 |
| quota del simbolo più frequente | 0.2140 | 0.1670 | 0.1530 | 0.1530 |

La sequenza possiede **tre proprietà insieme**: (i) alternanza vocalica naturale, se le vocali sono le lettere che sembrano vocali (C3 = 0.028, migliore di ogni lingua di riferimento); (ii) trigrammi ripetuti nella fascia delle lingue (0.46); (iii) IC troppo alta (0.115 contro 0.06-0.085). La spiegazione più economica della (iii), coerente con quanto si intravede nelle fotografie, è che l'inventario dei segni sia **più ricco** di quanto la trascrizione distingua: forme affini della stessa lettera (Α/Λ/∀, Δ/E, Ε/Є) fuse in una classe sola. La tabella mostra che separare una sola classe frequente abbassa l'IC di 0.01-0.02: poche separazioni di questo tipo bastano a riportarla nella fascia linguistica.

È la ragione per cui il passo successivo non è un altro algoritmo ma una **trascrizione che distingua le varianti di glifo**: è l'informazione che i dati richiedono e che nessuna analisi statistica può ricostruire.

Contro l'ipotesi che il cifrario lasci comunque leggibili le vocali (scuola di Della Porta) è stato eseguito un attacco dedicato, con A-E-I-O-V inchiodate alle vocali e solo le consonanti da risolvere: il punteggio resta fra -13.67 e -13.23, contro −10 circa di un testo reale e −14 di una permutazione casuale, e il testo prodotto è una sequenza vuota di senso (`corpus/03_attacks.md`). Anche questa strada è chiusa.

## 7. Il caso Dracula

La tesi popolare (Miriello 2021) è che nella chiesa sia sepolto Vlad III di Valacchia e che l'epigrafe misteriosa sia legata alla sua presenza: nome, epitaffio, simbolo dinastico.

Che cosa si può dire con i dati:

1. **Come chiave non funziona.** `VLAD`, `DRACULA`, `TURBOLO`, `MARIA`, `BALSA`, `FERRILLO`, `NAPOLI`, `IESUS` applicate come cifrario periodico danno statistiche indistinguibili da chiavi casuali (sezione 4.6).
2. **Come crib non funziona, ma la prova è debole.** La ricerca di crib è stata condotta su `palma_A`, che ora sappiamo non essere una trascrizione della lapide (sezione 6): il risultato (`corpus/03_attacks.md`) non è quindi un test dell'iscrizione. Nessun token è comunque isomorfo a un crib onomastico *informativo*.
3. **Il palindromo centrale è reale, e non è una parola.** La trascrizione del log colloca al rigo 22 la sequenza `ΔΕΔΕΔ`, isolata fra due parole, e il rigo cade nel blocco centrale, la parte più leggibile delle fotografie (da confermare su un'immagine ad alta risoluzione, sezione 6): è un elemento non lessicale (abbreviazione, monogramma, marchio) oppure una parola di schema ABABA, che nessuna delle lingue candidate possiede. L'OCR del log Gemini la scrive `DEDED` perché appiattisce Δ su D. Che sia un *marchio* e non una parola è un indizio contro la lettura dell'epigrafe come epitaffio funerario continuo.
4. **Nulla vieta la tesi, ma nulla la sostiene.** Se il testo fosse un'iscrizione funeraria latina con il nome del defunto, dovremmo vedere la struttura seriale del latino (trigrammi ripetuti ~0.54): nella sequenza del log i trigrammi ripetuti sono 0.46, cioè nella fascia delle lingue, ma l'IC è troppo alta perché una sostituzione semplice di una lingua naturale possa spiegarla. Mancano insomma le condizioni per leggere un nome: **questa iscrizione, come possiamo leggerla oggi, non è decifrabile**, e non può essere addotta né a favore né contro la tesi.

## 8. Limiti e che cosa servirebbe

- **Ordine di lavoro: prima le immagini e la trascrizione, poi le chiavi.** Non è una preferenza metodologica, è ciò che i dati impongono. (1) Un'immagine ortogonale ad alta risoluzione — o un rilievo — della lastra intera e dei singoli righi. (2) Una trascrizione paleografica indipendente, con legenda dei segni, marcatura esplicita delle lacune e dei caratteri dubbi e, se possibile, due trascrittori con matrice di confusione. (3) Solo su quella base, riprendere la ricerca di chiavi. Con le immagini disponibili (225×225 e 544×1024 pixel, sezione 6) e senza motore OCR il passo (2) non è eseguibile: ampliare adesso la ricerca di chiavi non aggiungerebbe informazione, misurerebbe ancora una volta la pipeline di trascrizione. Due letture della stessa lapide condividono intanto 4-5 simboli consecutivi su 600, e nessun algoritmo recupera un testo in chiaro da quel livello di disaccordo.
- **Potenza statistica.** Con ~600 glifi un modello senza rumore è rifiutabile solo se la discrepanza supera |z| ≈ 2; qui siamo a |z| = 2-7, quindi il rifiuto è solido, ma *l'identificazione* della lingua richiede tipicamente migliaia di caratteri. La simulazione lo mostra: al 25-30% di rumore la lingua corretta viene regolarmente scambiata con una lingua vicina.
- **I corpora di riferimento sono biblici**: registri funerari, notarili o devozionali possono differire. Il ceco medievale usato qui è la Bibbia Kralická (1613), non un testo penitenziale quattrocentesco; l'ungherese antico viene dal Codice Erdélyi.
- **Scritture non alfabetiche**: un abjad (solo consonanti) o un sillabario produrrebbero un profilo vocalico diverso da quello atteso; il test C3 non distingue fra 'nessuna lingua' e 'scrittura consonantica'. Va ripetuto su una trascrizione affidabile.
- **La PCA non è un test d'ipotesi**: le distanze nello spazio delle componenti non sono p-value. Il confronto con i controlli a classi fuse (sezione 4.8) mostra che l'ampiezza dell'allontanamento è quella di una trascrizione a maglia larga; non dimostra né esclude che il testo sia cifrato.
- **La verifica visiva ha un limite misurato, non presunto.** Le due fotografie danno al più 14 e 34 pixel per cella di glifo (sezione 6): bastano a riconoscere il repertorio dei segni e l'impianto della lastra, non a certificare i caratteri incerti né a separare le varianti Α/Λ/∀ ed Ε/Є che l'analisi indica come probabili, e non consentono una corrispondenza completa riga per riga. Un allineamento automatico glifo-per-glifo con le tavole di alfabeti storici (cariano, copto, glagolitico, sillabari alchemici) resta da fare su scansioni ad alta risoluzione.

## 9. Riproducibilità

```
python scripts/_fetch_external.py   # scarica i 16 corpora
python scripts/00_corpus.py        # corpus canonico + allineamenti
python scripts/01_descriptive.py   # statistiche descrittive
python scripts/02_inferential.py   # test inferenziali (~2 min)
python scripts/03_attacks.py       # attacchi (~2 min)
python scripts/04_predictive.py    # modelli generativi (~2 min)
python scripts/05_pca.py           # ordinamento PCA (~1 min)
python scripts/06_report.py        # questo rapporto
```

Strumenti fuori pipeline, per le fonti secondarie (richiedono `PyPDF2`, solo per questo):

```
python scripts/_extract_pdf.py                    # inventario + SHA256 dei PDF
python scripts/_pdf_pages.py FILE.pdf 3 --scale 2  # rende leggibile una pagina
```

Dipendenze: Python 3.10+ con `requests` (solo per il download); `scipy` è opzionale (code del chi-quadro, con fallback in pura libreria standard). Nessun altro pacchetto richiesto dalla pipeline: la sonda imaging della fase 0 legge le dimensioni dai soli header JPEG/WEBP/PNG, senza Pillow, e verifica la disponibilità del motore OCR senza installarne alcuno.

| file | contenuto |
|---|---|
| `corpus/00_corpus.md` | inventario delle trascrizioni, allineamenti, matrici di confusione, sonda imaging/OCR |
| `corpus/imaging.json` | misure delle fotografie e disponibilità del motore OCR (sezione 6) |
| `corpus/01_descriptive.md` | frequenze, n-grammi, struttura delle parole, posizioni, periodicità |
| `corpus/02_inferential.md` | permutazioni, bootstrap, confronto con 16 lingue, test C3 esaustivo |
| `corpus/03_attacks.md` | auto-validazione, null, chiavi, attacco a sostituzione, crib |
| `corpus/04_predictive.md` | calibrazione e fattori di Bayes |
| `corpus/05_pca.md` | ordinamento PCA, riproduzione dell'analisi pubblicata e controlli di confutazione |
| `corpus/*_summary.json` | tutti i numeri citati in questo rapporto |
| `report/documenti_agli_atti.md` | lettura critica delle tre fonti secondarie, pagina per pagina, e tabella di confutazione |
| `report/atti/manifest.json` | pagine, byte, SHA256 e raster dei tre PDF agli atti |
| `report/atti/pages/*.png` | pagine dei PDF rese leggibili con `_pdf_pages.py`, perché i documenti non hanno livello di testo |
| `report/atti/relazione_finale.md` | relazione finale di lavoro: bilancio, conclusione, registro degli atti con le impronte SHA256 di tutti i consegnati |
| `report/report_divulgativo.md` | versione divulgativa del rapporto, per il lettore medio: obiettivo, risultati, conclusione, ipotesi, glossario |
| `report/palma_histocrypt2023.txt` | estratto **preesistente e non riproducibile** dai PDF agli atti (che non hanno livello di testo): conservato come ausilio non verificato; le citazioni di Palma sono state rilette sulle pagine raster p1, p2, p9 |

## 10. Riferimenti

- Palma, C. (2023). *Encrypted epigraphy -- the case of a mysterious inscription in the Neapolitan church of Santa Maria La Nova*. HistoCrypt 2023, 139-147.
- Palma, C. Repository *MaLaNova* -- https://github.com/Glottocrisio/MaLaNova (trascrizioni, corpora, funzioni per n-grammi).
- Miriello, L. (2021). *Sulla presunta tomba di Dracula a Napoli*. Stamperia del Valentino.
- Rocco, G. (1928). *Il convento e la chiesa di Santa Maria La Nova*. Tipografia Pontificia degli Artigianelli, Napoli.
- Rosenmeyer, P. A. (2019). *Encrypted Inscriptions: a Paradoxical Practice*. Brill, 373-392.
- Antal, E., Marák, P., Zajac, P., Lengyelová, T., Duchoňová, D. *Encrypted Documents and Cipher Keys From the 18th and 19th Century in the Archives of Aristocratic Families in Slovakia*, PDF agli atti (12 pp., senza note tipografiche leggibili in prima pagina): 96 documenti cifrati e 9 chiavi, nomenclatori numerici, chiavi conservate ma non combacianti con i testi.
- Layfield, C., Abela, J., Zandbergen, R., Bowern, C., Davis, L. F., Rosner, M., van der Plas, L. (2022). *International Conference on the Voynich Manuscript 2022*, rapporto del convegno, PDF agli atti (7 pp.): revisione in doppio cieco, paleografia delle mani, confronto quantitativo fra testi privi di senso.
- Della Porta, G. B. (1563). *De furtivis literarum notis*.
- Trithemius, J. (1518). *Polygraphiae libri sex*.
- Bellaso, G. B. (1553). *Il vero modo di scrivere in cifra*.
- Knight, K., Megyesi, B., Schaefer, C. (2011). *The Copiale cipher*. BUCC 2011, 12-19.
- Hauer, B., Kondrak, G. (2016). *Decoding anagrammed texts written in an unknown language and script*. TACL 4, 75-86.
- Shannon, C. E. (1951). *Prediction and entropy of printed English*. Bell System Technical Journal 30(1), 50-64.
- Corpora: HistCorp (Uppsala), Project Gutenberg, github.com/thiagobodruk/bible (Bibbie parallele).

*Nota*: l'ipotesi di una preghiera penitenziale ceca circolata come seguito del lavoro di Palma non è stata verificabile su una fonte primaria in questa sede; è quindi trattata come ipotesi da testare, ed è testata nella sezione 5. Dalla lettura diretta del saggio (p1, p2, p9) non risulta alcun riferimento a un testo **ceco**: abstract, ipotesi in campo e bibliografia parlano di latino, di un originale greco, di traslitterazione e di isopsephy. L'ipotesi va quindi attribuita a una fonte diversa da Palma 2023, e non al saggio (si veda `report/documenti_agli_atti.md`, sezione 5).

