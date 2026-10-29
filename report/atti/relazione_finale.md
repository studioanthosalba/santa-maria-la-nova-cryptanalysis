# Relazione finale di lavoro

**Oggetto.** Analisi statistica e crittanalitica dell'epigrafe della cappella
Turbolo (Santa Maria la Nova, Napoli) e verifica dell'ipotesi che vi sia
sepolto Vlad III di Valacchia.

**Perimetro.** Tre trascrizioni disponibili (569, 584, 678 glifi), 21 corpora di
riferimento, due fotografie della lapide, tre fonti secondarie fornite come PDF.
Nessun accesso diretto alla lapide, nessun motore OCR, nessuna immagine ad alta
risoluzione.

**Data di deposito.** 29 ottobre 2026.
**Stato.** definitivo. Questo documento chiude il lavoro, ne dichiara l'esito e
registra agli atti i prodotti con le loro impronte SHA256.

## 0. Come leggere questo documento

La relazione non ripete il rapporto: lo chiude. Il rapporto (`report/report.md`,
433 righe) è il resoconto tecnico con tutte le tabelle; qui stanno il **bilancio**
del lavoro, la **conclusione**, ciò che è stato **escluso** e ciò che resta
**indecidibile**. I rinvii sono a sezioni del rapporto (§) e a file del
repository. Ogni numero citato è prodotto da uno script della pipeline ed è
registrato in `corpus/*_summary.json`: nessun numero di questa relazione è
stimato a mano.

## 1. Mandato e consegnato

| richiesta | consegna | dove |
|---|---|---|
| Che tipo di testo è l'epigrafe | verdetto motivato: testo strutturato, non casuale, non spiegato da alcun modello classico; la variabile dominante è la qualità della trascrizione | §3, §6 |
| Verificare l'ipotesi Dracula | verdetto negativo **per assenza di dati**, con l'elenco esatto di che cosa manca | §6 |
| Mettere a frutto le tre fonti secondarie | lettura pagina per pagina, con tabella di confutazione delle ipotesi | `report/documenti_agli_atti.md` |
| Riprodurre l'analisi PCA ricevuta | ricostruita (scarto mediano 0,24) e **confutata** come prova di cifrario | rapporto §4.8 |
| Rendere il lavoro riproducibile | pipeline in 7 fasi, deterministica, senza dipendenze oltre `requests` | §9 |
| Non fabbricare dati mancanti | nessuna trascrizione inventata, nessun OCR simulato, nessun testo estratto da PDF che non ne hanno | §6, §9 |
| Spiegare il lavoro a un lettore medio | rapporto divulgativo: obiettivo, risultati, conclusione, ipotesi, glossario, senza gergo | `report/report_divulgativo.md` |

## 2. Lavoro svolto, in ordine di esecuzione

Sette fasi, un file di output per fase, tempi misurati sull'ultima esecuzione
completa (macchina di sviluppo, un solo processo per volta).

| fase | script | produce | tempo |
|---|---|---|---|
| 0 | `00_corpus.py` | corpus canonico, rietichettatura, allineamenti fra letture, sonda imaging | 9,6 s |
| 1a | `01_descriptive.py` | frequenze, n-grammi, struttura delle parole, periodicità | 23,8 s |
| 1b | `02_inferential.py` | permutazioni, bootstrap, 16 lingue, test esaustivo C3 | 92 s |
| 2 | `03_attacks.py` | auto-validazione del solver, null, chiavi, sostituzione, crib | 150 s |
| 3 | `04_predictive.py` | calibrazione, modello a rumore, fattori di Bayes | 53 s |
| 1c | `05_pca.py` | PCA a 28 descrittori, riproduzione dell'analisi ricevuta, confutazione | 94 s |
| 6 | `06_report.py` | il rapporto, generato dai JSON (nessun numero scritto a mano) | 13,5 s |

Fuori pipeline, per le fonti secondarie: `_extract_pdf.py` (inventario + SHA256
dei PDF, non distruttivo) e `_pdf_pages.py` (rende leggibile una pagina di un PDF
senza livello di testo, sola libreria standard).

Che cosa ha stabilito ciascuna fase, in una riga:

- **Fase 0** — le tre letture non sono la stessa sequenza (blocco comune massimo
  4-5 simboli su ~600) e la sequenza del log Gemini è una *simulazione delle
  righe*, non un testimone indipendente. È la scoperta che riorienta tutto il
  lavoro: **il problema non era crittografico, era documentario**.
- **Fase 1a** — il testo è fortemente strutturato (IC 0,0595 / 0,0813 / 0,1147;
  trigrammi ripetuti 0,15 / 0,27 / 0,46) e non ha alcun periodo nascosto.
- **Fase 1b** — nessuna delle 16 lingue di riferimento è compatibile: |z| medio
  minimo 2,61 (`palma_A`, ceco Kralická) e 2,08 (`palma_B`, greco Brenton),
  contro una soglia di 2; il test esaustivo vocali/consonanti mostra che sotto
  Palma *nessuna* assegnazione dà un'alternanza naturale (C3 minimo 0,30 e 0,17
  contro 0,025 delle lingue), mentre sotto Gemini l'insieme ottimale è
  `a, i, v, o, e` con C3 0,028.
- **Fase 2** — il solver decifra esattamente tre testi di controllo (divario
  0,00 nats) e sull'epigrafe si ferma 3 nats/finestra sotto il livello di testo
  reale: **il fallimento è del testo, non dello strumento**. Null, periodi e
  chiavi onomastiche non producono nulla di significativo (p 0,085-0,960).
- **Fase 3** — solo `palma_A` entra nella fascia degli oggetti di origine nota
  (13,06 al 30% di rumore, contro 14,26-16,23 dei controlli), ma a quel rumore
  la lingua non è identificabile; `gemini_full` è incompatibile con tutti i
  modelli (-28,18).
- **Fase 1c** — le coordinate PCA si riproducono (scarto massimo 0,44, mediana
  0,24), ma i 28 descrittori sono **invarianti per sostituzione** (scarto
  esattamente nullo): la posizione non può testimoniare un cifrario. Testi in
  chiaro con una o due classi di glifi fuse riproducono la stessa distanza; le
  attribuzioni linguistiche per prossimità non superano il null (p = 0,15).
- **Fase 6** — il rapporto è rigenerato dai JSON, con tabelle di integrità
  verificate e hash stabile fra esecuzioni consecutive.

## 3. Che cosa è stato accertato

Sono i risultati che reggono indipendentemente dal giudizio sul resto, perché
ognuno ha il proprio controllo e il proprio null.

1. **Il testo non è una decorazione casuale.** IC a 37,8-146,4 deviazioni
   standard dal valore atteso di una stringa uniforme con lo stesso alfabeto;
   entropia corrispondentemente bassa; quota del simbolo più frequente doppia o
   tripla rispetto al caso; trigrammi ripetuti 4-11 volte il caso. Test di
   Friedman: p < 1e-12 in tutte e tre le letture. La struttura seriale è
   confermata dal null di permutazione (p = 0,005 / 0,042 / 0,008).
2. **La struttura non è periodica.** Il massimo guadagno di IC su periodi
   k = 1..20 non supera mai il 95° percentile del null (p = 0,4351 e 0,9341):
   la "periodicità" intravista dagli esami di Kasiski è rumore di campionamento.
   Questo esclude la famiglia dei cifrari polialfabetici periodici.
3. **Nessuna lingua naturale in chiaro è compatibile.** Sedici corpora, finestre
   di lunghezza identica sui due lati del confronto, cinque statistiche
   invarianti per rietichettatura: il |z| medio minimo è 2,61 (`palma_A`) e 2,08
   (`palma_B`), cioè sopra la soglia di 2. Il difetto è sistematico e riguarda
   bigrammi e trigrammi (z da -2,97 a -6,67), non la frequenza dei singoli
   glifi.
4. **Il solver a sostituzione non è il limite.** Tre testi di controllo (latino,
   ceco, italiano) vengono decifrati esattamente, con divario 0,00 nats dal vero
   testo in chiaro. Sull'epigrafe lo stesso solver resta a -13,43…-13,63 nats
   contro un livello di testo reale di -9,81…-10,57 e una baseline casuale di
   -13,93…-14,00: il guasto è nel dato, non nell'algoritmo.
5. **Il test esaustivo vocali/consonanti localizza il problema.** Poiché i glifi
   sono etichette arbitrarie, sono stati provati tutti i C(23,5) = 33 649
   insiemi di vocali. Sotto `gemini_full` l'ottimo è naturale (C3 = 0,028, con
   `a, i, v, o, e`); sotto `palma_A` e `palma_B` nessun insieme scende a livelli
   linguistici (0,305 e 0,165 contro 0,025). Poiché C3 dipende dall'ordine e non
   dai nomi, **le due trascrizioni descrivono strutture diverse**: è una prova
   interna, non un'opinione.
6. **L'analisi PCA ricevuta è riproducibile e non probante.** Ricostruita da
   zero (28 descrittori, 16 corpora, 4 800 finestre, autosolutore in sola
   libreria standard): coordinate concordi entro 0,44 deviazioni standard
   (mediana 0,24). Ma i descrittori sono invarianti per sostituzione (scarto
   esattamente 0,00), quindi la posizione non distingue un cifrario da un testo
   in chiaro; e i controlli a classi fuse riproducono la distanza osservata.
7. **La lapide, come possiamo leggerla oggi, non è decifrabile.** Non è
   un'affermazione metafisica: è la conseguenza misurata di due fatti — nessuna
   lingua compatibile (punto 3) e nessuna trascrizione diplomatica disponibile
   (§4.1 del rapporto) — con la quantificazione del disaccordo fra letture
   (4-5 simboli consecutivi in comune su ~600).

## 4. Che cosa è stato escluso, e perché è il valore del lavoro

Un risultato negativo con un null calibrato vale più di un'ipotesi non testata.
Queste posizioni sono state **testate e ritirate**.

| ipotesi | test | risultato | esito |
|---|---|---|---|
| Sostituzione monoalfabetica semplice di una lingua naturale | 16 corpora × 5 statistiche invarianti + attacco a sostituzione validato su 3 controlli | nessuna lingua sotto \|z\| = 2; solver fermo 3 nats sotto il testo reale | **non sostenuta** |
| Sostituzione con null (caratteri riempitivo) | guadagno di IC eliminando un glifo, contro controlli senza null e con 10% di null | 0,00709 contro 0,00583 (p = 0,0769) | **non sostenuta** |
| Cifrario polialfabetico periodico | scansione k = 1..20 con null di permutazione | nessun picco; p = 0,4351 e 0,9341 | **non sostenuta** |
| Chiavi onomastiche (VLAD, DRACULA, TURBOLO, MARIA, BALSA, FERRILLO, NAPOLI, IESUS) | Vigenère/Bellaso, chiave casuale della stessa lunghezza come null | p da 0,085 a 0,960; IC residuo 0,047-0,052 contro 0,073 atteso | **non sostenuta** |
| "Cifrario di tipo diverso", dedotto dalla posizione PCA | ricostruzione + controllo di invarianza per sostituzione + testi in chiaro a classi fuse | descrittori invarianti, scarto 0,00; il controllo riproduce la distanza; p = 0,15 | **ritirata** |
| Testo greco scritto in lettere greche | C3 con le vocali greche reali | 0,445 contro < 0,10 di qualsiasi lingua | **non sostenuta** |

Accanto a queste restano **aperte e non decidibili** con i dati attuali: la
tavola didattica o decorazione senza messaggio (il testo è strutturato, quindi
qualcosa di sistematico c'è, ma nessun modello linguistico lo cattura) e la
beffa o gioco intellettuale (posizione di metodo dichiarata al convegno Voynich
2022, sostenuta da Rosenmeyer 2019 citata in Palma 2023, non dimostrabile senza
una trascrizione).

## 5. Quattro correzioni a cose date per assodate

Sono il contributo più duraturo, perché cambiano il modo di porre il problema e
non solo la risposta.

1. **Le trascrizioni pubblicate non sono letture concordanti della stessa
   sequenza.** Dopo rietichettatura canonica due letture della stessa lapide
   condividono al massimo 4-5 simboli consecutivi su ~600, mentre due file dello
   stesso autore con lo stesso numero di glifi ne condividono decine: la metrica
   distingue i gradi di parentela, e le letture indipendenti non risultano
   sovrapponibili. Le stringhe del repository di Palma vanno trattate come stadi
   intermedi della sua pipeline, non come testimoni della pietra.
2. **Due corpora "cechi" del repository di riferimento sono ungheresi.** I file
   `bibliahuszita*` e `czechcodex.txt` contengono il Codice di Monaco (1466), e i
   corpora sono doppiamente codificati (UTF-8 letto come cp437). Entrambi i
   difetti sono corretti in `scripts/langmodels.py`; senza la correzione una
   parte del confronto pubblicato è invalida.
3. **La posizione nell'ordinamento PCA non può dire nulla sul cifrario.** I 28
   descrittori usati sono invarianti per sostituzione: qualunque cifrario a
   sostituzione finisce nello stesso punto del testo in chiaro da cui deriva.
   L'allontanamento osservato è quello di una trascrizione a maglia larga —
   riprodotto da testi in chiaro con una o due classi di glifi fuse — e le
   attribuzioni linguistiche per prossimità non superano il null.
4. **Il fatto che nessuna chiave decifri la lapide non smentisce la cifratura.**
   Nell'archivio reale dell'Archivio Nazionale Slovacco (96 documenti cifrati,
   9 chiavi conservate, 1711-1834) le chiavi conservate **non corrispondono ai
   testi conservati**, e le chiavi sono in due fondi su tre. La mancata
   corrispondenza si osserva quindi anche dove cifrato e chiave esistono
   entrambi: il nostro null sulle chiavi onomastiche resta un null, non una
   confutazione. Corollario operativo: cercare chiavi non è il passo successivo.

## 6. Conclusione finale

**Verdetto.** L'epigrafe della cappella Turbolo contiene un testo strutturato e
non casuale, prodotto da un sistema di segni con regole interne; nessun modello
crittografico classico lo spiega, nessuna delle sedici lingue di riferimento gli
somiglia, e la ragione principale per cui il problema è oggi irrisolvibile non è
la difficoltà del cifrario ma **l'assenza di una trascrizione diplomatica
affidabile**. Sull'ipotesi Dracula il verdetto è negativo, ma per assenza di
dati, non per smentita: con ciò che si può leggere oggi, l'iscrizione non può
essere addotta né a favore né contro.

Che cosa è dimostrato, che cosa non lo è, che cosa non è decidibile:

| categoria | contenuto |
|---|---|
| **dimostrato** | il testo non è casuale (z = 37,8-146,4; p < 1e-12); la struttura non è periodica (p = 0,4351/0,9341); il solver a sostituzione funziona (3 controlli esatti) e sull'epigrafe fallisce di 3 nats; nessuna delle 16 lingue è compatibile (\|z\| minimo 2,08-2,61); le due trascrizioni descrivono strutture diverse (C3 0,305/0,165 contro 0,028); i 28 descrittori PCA sono invarianti per sostituzione (scarto 0,00) |
| **non dimostrato** | che il testo sia cifrato; che sia in chiaro travestito; che sia una tavola didattica; che sia una beffa; che sia una preghiera; che sia un epitaffio |
| **non decidibile con i dati attuali** | il contenuto, la lingua, la datazione interna, l'attribuzione, il rapporto con la tomba di Vlad III |

**Sull'ipotesi Dracula**, in concreto: la tradizione popolare collega la lapide
alla tomba che Miriello (2021) argomenta per via storico-araldica. Il nostro
lavoro non tocca quell'argomento e non ne produce uno alternativo. Dice una cosa
sola e la dice con i numeri: **non esiste oggi una lettura dell'epigrafe
sufficientemente stabile da poter essere interrogata**. Cercare «VLAD» o
«DRACULA» in una stringa che due trascrittori non leggono allo stesso modo è
cercare in un testo che non abbiamo. Il test è stato fatto comunque, per
completezza, e non ha dato nulla (p 0,085-0,960) — ma il suo null non va
raccontato come una smentita, perché negli archivi reali le chiavi conservate
non corrispondono ai testi conservati (§5, punto 4).

**Perché questo non è un fallimento.** Un'analisi che conclude «serve un'altra
trascrizione» dopo aver speso 33 649 insiemi di vocali, 16 corpora, un solver
validato e 4 800 finestre non ha perso: ha **localizzato** il guasto. All'inizio
del lavoro il problema sembrava crittografico e la letteratura lo trattava come
tale; alla fine è dimostrato che il segnale disponibile è dominato dall'errore
di trascrizione, che il rumore necessario a spiegare `palma_A` (30%) è compatibile
con *qualsiasi* lingua, e che la variabile su cui investire è l'immagine, non il
calcolo. Questo cambia l'ordine delle operazioni per chiunque riprenda il testo,
ed è un risultato trasferibile: vale per ogni iscrizione nota solo attraverso
trascrizioni non concordanti.

**Tre errori da non scrivere**, che il lavoro ha escluso uno per uno:

1. «Nessuna lingua fra 16, quindi è un cifrario»: il confronto esclude lingue
   naturali in chiaro, **non identifica** una tecnica (Boxer 2022: due testi
   privi di senso non sono dello stesso tipo; cfr. `documenti_agli_atti.md` §4).
2. «La PCA colloca la lapide fuori dal gruppo delle lingue, quindi è cifrata»:
   i descrittori sono invarianti per sostituzione, quindi la posizione è la
   stessa del testo in chiaro da cui il cifrario deriva. L'ipotesi è ritirata.
3. «Le chiavi storiche non funzionano, quindi non è cifrata»: negli archivi
   reali le chiavi conservate non combaciano con i testi conservati. Il null
   resta un null.

## 7. Che cosa serve per proseguire, in ordine di priorità

1. **Un'immagine ortogonale ad alta risoluzione della lastra** (o un rilievo):
   lastra intera più i singoli righi, almeno 300 ppi sul formato reale, con luce
   radente per l'erosione. Con le due fotografie disponibili (225×225 e
   544×1024 pixel, al più 14 e 34 pixel per cella di glifo) questa è la variabile
   che oggi manca e che nessun calcolo può sostituire.
2. **Una trascrizione paleografica indipendente**, con legenda dei segni,
   lacune e caratteri dubbi marcati esplicitamente, varianti distinte (Α/Λ/∀,
   Ε/Є) e, se possibile, due trascrittori con matrice di confusione. Serve a
   stabilire se le letture esistenti divergono per *errori* o per *sistemi di
   notazione*: nel secondo caso il problema cambia natura.
3. **Solo dopo**, l'allineamento glifo-per-glifo con le tavole di alfabeti
   storici (cariano, copto, glagolitico, sillabari alchemici) e la ripresa della
   ricerca di chiavi in archivi con provenienza documentata.

Che cosa **non** serve, e il lavoro lo ha stabilito con i numeri: altre chiavi
tentate sulla trascrizione attuale; altri modelli statistici sulle stesse tre
stringhe (il rumore necessario è già al 30%, che azzera il potere
discriminante); un'altra ordinazione PCA (i descrittori sono invarianti per
sostituzione).

Se si ottenesse solo il punto 1, sarebbero già possibili tre cose: certificare
la sequenza `ΔΕΔΕΔ` del rigo 22 (marchio o parola), verificare se le 4-5
coincidenze fra le letture sono reali o casuali, e distinguere le varianti di
glifo che oggi appiattiscono l'inventario e gonfiano l'IC a 0,115.

## 8. Registro degli atti

Sono registrati qui i **consegnati**: il rapporto, il rapporto divulgativo, la lettura critica, gli strumenti, gli output delle fasi e i materiali di partenza. Le impronte sono SHA256 calcolate su questa copia di lavoro; un byte diverso, un'impronta diversa.

Sono **esclusi** dal registro, e dichiarati qui: la cartella `sources/external/` (16 corpora scaricabili con `python scripts/_fetch_external.py`), il repository `sources/MaLaNova-master/` e il suo archivio `.zip` (materiale di terzi, non prodotto da questo lavoro) e la pagina rasterizzata `report/atti/pages/*.png`, che è derivata dai PDF e riproducibile con `_pdf_pages.py`; le sue impronte sono elencate in coda per completezza.

### 8.1 Rapporto e lettura critica

| file | byte | SHA256 |
|---|---|---|
| `report/report.md` | 47 409 | `0B96D76E3E6084B45C65F8FFA03E77D0105E4CE8CA1804D256FC75F0B1E432F1` |
| `report/report_divulgativo.md` | 13 262 | `C8DBF8B0A798858D5C99C560AE06EC93887462B8E6FFB6F421B4399DF778F9EA` |
| `report/documenti_agli_atti.md` | 18 723 | `8DFEDFD278B02769D6386AC419F3D4DDF97881A632DB2D10114A08FD0A712A99` |
| `report/pca_analisi.md` | 11 764 | `ABB8A9EBEC669BBEE5A133128A88EF70C0A1EC3E3FD169D6161157D739FDBE39` |
| `report/verifica_trascrizioni_corpora_cifrari.md` | 22 158 | `F74908F8976B1A111A23F56886AC06B883049413AE0247BF0302B82285AAD1BE` |
| `report/palma_histocrypt2023.txt` | 33 164 | `9B596FB1211D29C8CD18FCEF5DA35F383DE239ED1917E07725DDE06F53294D86` |

Il rapporto divulgativo è **scritto a mano, non generato**: rilegge il rapporto per
un lettore non specialista (obiettivo, risultati, conclusione, ipotesi, glossario)
senza introdurre alcun numero nuovo — ogni cifra che cita è in `report/report.md`
o in `corpus/*_summary.json`. Per questo è registrato fra i consegnati e non fra
gli output della pipeline.

### 8.2 Materiali di partenza (radice)

| file | byte | SHA256 |
|---|---|---|
| `README.md` | 8 174 | `CF9628F6A7E7093F5F9F7B7D6C44DE21323AF423D7F8CDE22300D08376DDB489` |
| `dracula_epigrafe.md` | 73 269 | `3A5D7CD2B9DB21B4BC3640C3E68E9AE6F8E0045A3E5E2F0FC80457F7D142035C` |
| `epigrafe drac.md` | 1 230 | `A83CEDCB3FC55E5ACDBA8D1D89C5C3FC508FD37C6554169124BB2741DE9E4168` |
| `drac1.jpeg` | 11 932 | `B3E98A1650E370F2208DAD452F252ADE3D4417F619781856B64D98EF828EF4C9` |
| `drac2.webp` | 162 504 | `77424C4CC6FD6E754DAD795593FB6DCD2133EDECFC754CC9608A3C8D8EAB2137` |

### 8.3 Fonti secondarie in radice (PDF)

| file | byte | SHA256 |
|---|---|---|
| `View of Encrypted epigraphy - the case of a mysterious inscription in the Neapolitan church of Santa Maria La Nova.pdf` | 4 849 816 | `AEC01A098EBE4D702169805EF7E11B4FF596E2786B47128677AD59A53229710F` |
| `View of Encrypted Documents and Cipher Keys From the 18th and 19th Century in the Archives of Aristocratic Families in Slovakia.pdf` | 9 914 463 | `6B77B10120BD574039FD0E0CDB10C8DEC4DC289AAC176A72B723493C037D1291` |
| `View of International Conference on the Voynich Manuscript 2022.pdf` | 2 932 872 | `A02DC21EA250DD576F907E920D893FE03CAAAD4463BD6ADFB5F220448D4526CF` |

### 8.4 Strumenti (`scripts/`)

| file | byte | SHA256 |
|---|---|---|
| `scripts/00_corpus.py` | 21 778 | `05B582C86F83D3FE4A9EC01A94B6FF530AF8D7DA54CC21827632CA35C5F7191A` |
| `scripts/01_descriptive.py` | 14 160 | `B57D63E1716EE0457975502BD8B675EEFC76F62948DF5AFD896E4121A1490177` |
| `scripts/02_inferential.py` | 15 820 | `20B87EFC4EA66FBDB907B12EF80B862A2616582BB184553BFD4EBEE97C1E324D` |
| `scripts/03_attacks.py` | 29 401 | `35B5D954F50441CEFC31933E54873C6685A26D522139F0E89E10555B6E7F0389` |
| `scripts/04_predictive.py` | 8 023 | `6E9B2E0A72250573AF7801B876E4BF92B3D539762E9F11292D323AB1778AA585` |
| `scripts/05_pca.py` | 45 469 | `9B879ABA120C534FA7C4335448845309C5F2BE87AE3A6288D939F6A0C13397E6` |
| `scripts/06_report.py` | 68 981 | `5B1FDD11FDAA32BF0DA27998396FB29F7A00CF58E6837B09899B31AA1453607E` |
| `scripts/_extract_pdf.py` | 6 197 | `ADA2A84C697F569B7E6BDECED3DB33E72AEE70DF7867A0BB30F54D2891651442` |
| `scripts/_fetch_external.py` | 3 114 | `9C1DFAFB53E0C7D4CF0D190BB57DE9A06620B0223174D739C71C9525B1367EB0` |
| `scripts/_pdf_pages.py` | 6 636 | `5694E8FABEEB4F98FC7CB1F99F25B99F23BA0F542A21FBD0822A10F483B57A8A` |
| `scripts/common.py` | 23 532 | `2345AAB0C781A78681CEB38A0B5A319644197A8CA627B617CAC514E5F5AE4EE7` |
| `scripts/langmodels.py` | 8 228 | `F86BF19BEA09196DAD43FCD30022F139A550C5702F59628BAC351CE4C4961A88` |

### 8.5 Output delle fasi (`corpus/`)

| file | byte | SHA256 |
|---|---|---|
| `corpus/00_corpus.md` | 10 940 | `511ADF5E01AFA46F72F1D95335AE7BC30F093E81A4CCEB643D9FB51F826378FA` |
| `corpus/01_descriptive.md` | 19 295 | `70C27FEFE80230574CB2847D196CABF484C42B84111DA3C280B81E4B2CC61250` |
| `corpus/02_inferential.md` | 19 606 | `33FA23041AA7A66C078A98A1651D4346815CDE2FDD75E903B443981E987A5DD5` |
| `corpus/02_summary.json` | 10 805 | `976EBC97ACC6587CDA8F3AD22AF7CABE56DB38FC764DF9219D0471B3027B9BE4` |
| `corpus/03_attacks.md` | 13 150 | `00F45AA34298CB595ECFADF2D8A03ADAE525C93516E2E18C9A813797C8340E78` |
| `corpus/03_summary.json` | 3 547 | `D10E18C970F784BF423FF0EE785FB150076F4B77CE0968B09F1EDFBA3E0C8BF2` |
| `corpus/04_predictive.md` | 5 501 | `FBC97A80F9095E3B020820DD675A50C95031B83CA8EE106E7ED135D0E6FF7982` |
| `corpus/04_summary.json` | 6 051 | `3E7FEA07870B95E313EF521D5FDEBFAAC587C0F610540E07907A5C63150C5971` |
| `corpus/05_pca.md` | 17 207 | `411606770BCCFF99734EFF2E2CC69586339885FF66769C2802BFCBDB309F22C4` |
| `corpus/05_pca_summary.json` | 9 054 | `362BCED6A3AFC065FDC443C3529BDDA0784527DAD4B5B61990DF5C54BBF24F9A` |
| `corpus/corpora.json` | 34 795 | `D12D8BD2BF9307E6C223A7EC2B201484FB301F50B7199BF683733035CA8007A1` |
| `corpus/imaging.json` | 674 | `E6414896D5582351E1BC376513BF25BBE50E39374CAB06B5765F051E24DEB773` |
| `corpus/lines.json` | 11 068 | `ED8B24429358319A148077892F0754238779132B35CF05C48B5DFC7454A7FBF4` |

### 8.6 Atti (`report/atti/`)

| file | byte | SHA256 |
|---|---|---|
| `report/atti/manifest.json` | 5 331 | `ED3A0AB6CEAE2A68B23D874E31A883A287E7AE0500674E40B9941A2C1C578F9C` |
| `report/atti/relazione_finale.md` | questo documento | non autocertificabile: un file non può contenere il proprio SHA256; si ricalcola con `Get-FileHash report\atti\relazione_finale.md` |

Pagine raster dei PDF (riproducibili con `_pdf_pages.py`):

| file | byte | SHA256 |
|---|---|---|
| `report/atti/pages/View-of-Encrypted-Do-p1.png` | 105 445 | `4BC04642E0D3C7D336507CD3E4166E6FECBCF39F5D662427511E4717816383F6` |
| `report/atti/pages/View-of-Encrypted-Do-p12.png` | 181 421 | `A96E44DCD83E9C5F7E259257B44DD5C721D20DF1FA6DAE079DB5B86BE6424CFF` |
| `report/atti/pages/View-of-Encrypted-Do-p2.png` | 175 161 | `19FBFC6DA9D2C6D0EC334730BDB11B662D5FBD959DFD40AE50DF76DD0AD2A9CD` |
| `report/atti/pages/View-of-Encrypted-Do-p3.png` | 364 642 | `CDD590F2E9CC34917A76014F5B568A5721313EB724F9F775425E4AE609D56CBF` |
| `report/atti/pages/View-of-Encrypted-ep-p1.png` | 217 943 | `68467317D9A1107462AE526948FD4BF59569BBE12D06B2CAFB640E688C6B7098` |
| `report/atti/pages/View-of-Encrypted-ep-p2.png` | 117 795 | `9AB525903DFED8D307DBBFE208ECC091DFE0CCAF80EC8F3E4FE9B9510A257F94` |
| `report/atti/pages/View-of-Encrypted-ep-p9.png` | 112 668 | `67FFAD00CB76F7E0C330FFB4F3E109B71D56F56159589AD10890D380BA53CFD6` |
| `report/atti/pages/View-of-Internationa-p1.png` | 103 867 | `64CC7DFE502350915C3E025C6E4A23A12A3FBD3672555CCA6CA144CC9F6FC47A` |
| `report/atti/pages/View-of-Internationa-p2.png` | 123 528 | `286F52D50359991423E7B8A147A5DDB49CFD2743A00A9B92BAF7CC73D67BC72D` |

## 9. Dichiarazioni finali

### 9.1 Riproducibilità

```
python scripts/00_corpus.py        # 9,6 s
python scripts/01_descriptive.py   # 23,8 s
python scripts/02_inferential.py   # 92 s
python scripts/03_attacks.py       # 150 s
python scripts/04_predictive.py    # 53 s
python scripts/05_pca.py           # 94 s
python scripts/06_report.py        # 13,5 s
```

Totale **7 min 16 s** su una macchina di sviluppo, senza parallelismo. Dipendenze:
Python 3.10+ e `requests` (solo per il download dei corpora); `scipy` opzionale
(code del chi-quadro, con fallback in sola libreria standard). I due strumenti
per le fonti secondarie richiedono `PyPDF2`, e solo quelli: la pipeline non ne
dipende.

### 9.2 Determinismo

Ogni fase è stata eseguita **due volte consecutive** e gli output confrontati
byte per byte (SHA256): i 14 file di `corpus/` più `report/report.md` risultano
identici. Tutti i generatori casuali sono inizializzati con seed espliciti
(`random.Random(seed)`); nessun seme dipende dal tempo o dall'ordine dei
processi. `report/report.md` ha hash SHA256 stabile fra esecuzioni consecutive di
`06_report.py`.

Una sola divergenza è stata osservata e corretta. Al primo confronto
`corpus/03_summary.json` differiva, mentre `corpus/03_attacks.md` — cioè le
tabelle e i numeri riportati — restava identico. La causa: due cicli in
`03_attacks.py` (`greedy_strip`, `max_gain`) risolvevano i pareggi iterando un
`set` di stringhe, il cui ordine segue il seed di hashing del processo Python;
il glifo registrato nel caso di pareggio cambiava quindi da un processo
all'altro, senza che cambiasse alcun valore. L'iterazione è ora canonica
(`sorted(set(...))`), e **due esecuzioni consecutive della fase 2 danno byte
identici**. Il difetto era cosmetico, ma in un atto non deve esistere.

### 9.3 Limiti dichiarati

- **Le fotografie non bastano.** 225×225 e 544×1024 pixel, al più 14 e 34 pixel
  per cella di glifo: nessuna trascrizione nuova è stata prodotta, e nessun OCR è
  stato simulato (il binario `tesseract` non è disponibile).
- **Le tre fonti secondarie sono state lette solo in parte**: 9 pagine su 28
  (Palma p1, p2, p9; Antal et al. p1-p3, p12; Layfield et al. p1-p2). Le
  restanti 19 sono agli atti come raster ma non sono state lette, e nessuna
  affermazione di questo lavoro si fonda su di esse.
- **I PDF agli atti non hanno livello di testo**: 1240×1753 px, ~150 ppi, zero
  caratteri estraibili. Le citazioni sono state trascritte a vista dal raster:
  errori sui singoli caratteri sono possibili, il senso no.
- **Potenza statistica**: con ~600 glifi il rifiuto di un modello è solido, ma
  l'identificazione della lingua richiederebbe migliaia di caratteri.
- **I corpora di riferimento sono biblici**: registri notarili o devozionali
  possono differire; il ceco medievale usato è la Bibbia Kralická (1613) e
  l'ungherese antico viene dal Codice Erdélyi.
- **Il dato «le chiavi non combaciano»** viene da un solo fondo archivistico
  (13 scatole, 96 documenti): è un fatto locale, non una legge.

### 9.4 Un incidente, dichiarato e corretto

La prima versione dello strumento di estrazione ha sovrascritto
`report/palma_histocrypt2023.txt` con un file vuoto, perché i tre PDF non hanno
livello di testo. Il file è stato ripristinato integralmente dal backup
(33 164 byte) e lo strumento è stato riscritto per essere **non distruttivo**:
non sovrascrive un estratto esistente con meno di 500 caratteri, salvo `--force`
esplicito. Nella stessa occasione si è accertato che quel `.txt` **non è
riproducibile** dai PDF agli atti — non può esserne stato estratto — e contiene
mojibake da passaggio HTML → cp1252: è classificato come ausilio non verificato,
e le citazioni di Palma sono state rilette sulle pagine raster p1, p2, p9.

### 9.5 Nota sul manifest dei PDF

`report/atti/manifest.json` registra per ogni PDF `extract_written: false`: il
campo `text_out` indica il percorso che l'estrattore *userebbe*, e nessun file è
stato scritto perché l'estrazione produce zero caratteri. Pagine, byte e SHA256
dei tre PDF in radice sono nel manifest; i nomi dei file conservano il prefisso
`View of` aggiunto dall'archivio online.

## 10. Chiusura

Il lavoro è chiuso con un risultato negativo, quantificato e riproducibile, e con
quattro correzioni che cambiano il modo di porre il problema. Non è stata
prodotta la trascrizione che servirebbe, perché non era producibile con i mezzi
disponibili, e non è stata simulata: la differenza fra «non ho i dati» e «ho
inventato i dati» è l'unica cosa che separa un'analisi da un'opinione.

Consegna: pipeline eseguibile in 7 minuti, rapporto generato dai dati, rapporto
divulgativo per il lettore medio, lettura
critica delle fonti secondarie, registro degli atti con impronte SHA256. Chi
riprende il lavoro trova l'ordine delle operazioni già stabilito (immagine, poi
trascrizione, poi chiavi) e tre affermazioni da non ripetere (§6, «tre errori da
non scrivere»).

Depositato agli atti in data 29 ottobre 2026.

