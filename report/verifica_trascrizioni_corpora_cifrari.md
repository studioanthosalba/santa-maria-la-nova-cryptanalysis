# Verifica delle trascrizioni, corpora ampliati e ipotesi crittografiche

## Sintesi esecutiva

- **Trascrizione:** ho reperito nella pubblicazione di Palma una fotografia incorporata a 2633 × 2249 px, più dettagliata delle immagini locali, ma mostra solo una porzione della lapide. Non basta quindi per una trascrizione integrale verificata. `gemini_full` è una simulazione dichiarata nella conversazione archiviata, non una trascrizione indipendente: è esclusa dai nuovi confronti.
- **Corpora:** ai 16 modelli già configurati sono stati aggiunti cinque testi storici locali: due boemi/cechi, due ungheresi antichi e uno lussemburghese antico. Sono stati usati anche i modelli latini e ungheresi storici già presenti.
- **Sostituzione monoalfabetica:** gli attacchi non producono testo vicino ai riferimenti naturali, pur recuperando controlli cifrati positivi della stessa lunghezza. L'evidenza è contraria alla sostituzione semplice *nelle lingue e nei modelli provati*, non a ogni cifrario.
- **Vigenère a periodo 2–20:** i picchi osservati non sono significativi rispetto a permutazioni che conservano le frequenze dei glifi. I controlli positivi mostrano anche che il test individua spesso un multiplo del periodo, non necessariamente il periodo fondamentale.
- **PCA ampliata:** le due letture Palma restano lontane da parte della distribuzione di riferimento, ma i vicini cambiano con la lettura; PCA e statistiche descrittive non identificano una lingua.

## 1. Dati e verifica della trascrizione

### Materiale disponibile

| Fonte | Dimensioni / contenuto | Valutazione |
|---|---|---|
| `drac2.webp` | 544 × 1024 px; fotografia dell'intera lapide | Sufficiente per riconoscere la struttura e molte forme generali, non per risolvere con certezza ogni glifo eroso |
| `drac1.jpeg` | 225 × 225 px | Miniatura, non adatta a una trascrizione indipendente |
| `palma_A` | 584 glifi normalizzati, con spazi e lacune | Lettura pubblicata/localmente conservata; da confrontare con l'originale ad alta risoluzione |
| `palma_B` | 678 glifi normalizzati, 23 classi | Variante di trascrizione Palma con etichette greche assegnate ai glifi; le etichette non dimostrano che il testo sia greco |
| `gemini_full` e varianti centrali | 569 glifi nella lettura completa | **Escluse:** la conversazione archiviata definisce esplicitamente il testo esteso come “simulazione delle 33 righe della lastra” |
| `drac_raw` | 863 caratteri normalizzati | Lettura degradata/OCR-like, non indipendentemente convalidata |
| Palma, Figura 1 | fotografia incorporata nel PDF HistoCrypt, 2633 × 2249 px | Dettaglio più definito disponibile pubblicamente; porzione della lapide, non immagine completa |

La fonte pubblica individuata è Cosimo Palma, [“Encrypted epigraphy - the case of a mysterious inscription in the Neapolitan church of Santa Maria La Nova”](https://doi.org/10.3384/ecp195703), HistoCrypt 2023; la [pagina dell'articolo](https://ecp.ep.liu.se/index.php/histocrypt/article/view/703) offre il PDF e la Figura 1. L'immagine incorporata nel PDF è di 2633 × 2249 px, ma inquadra solo una parte dell'iscrizione. Lo stesso articolo spiega che la fotografia completa è stata omessa per le cancellazioni ed erosioni, soprattutto nelle zone superiore e inferiore. La Figura 1 consente di vedere meglio alcune forme nella porzione inquadrata, ma non di assegnare con certezza ogni glifo o di riallineare l'intera iscrizione alle trascrizioni.

Non è installato il motore OCR Tesseract. L'ispezione visiva della foto locale e del dettaglio della pubblicazione conferma l'esistenza di una lunga iscrizione, ma erosione, contrasto e inquadratura parziale non permettono di certificare caratteri incerti o una corrispondenza completa riga-per-riga. Non presento quindi una nuova trascrizione come se fosse verificata. Per farlo servono l'immagine originale completa ad alta risoluzione o un rilievo, più una trascrizione paleografica indipendente con legenda e marcatura esplicita delle lacune. La Figura 1 è un riferimento utile per un successivo confronto limitato alle righe visibili, non sostituisce quel materiale.

La conseguenza metodologica è rilevante: le precedenti analisi PCA che includevano `gemini_full` descrivono anche una sequenza simulata e non possono essere usate come prova sulla lapide. Il file [00_corpus.md](../corpus/00_corpus.md) ora riporta questa provenienza.

## 2. Corpi di confronto ampliati

Sono stati aggiunti a `scripts/langmodels.py` i seguenti testi presenti nel repository:

| Modello | Lettere dopo normalizzazione | IC | N-grammi distinti di 5 lettere | Cautela |
|---|---:|---:|---:|---|
| Old Czech (Bohemian 2) | 8.709 | 0,06055 | 6.203 | Corpus storico breve |
| Old Czech (Bohemian 3) | 15.351 | 0,05881 | 10.950 | Corpus storico breve |
| Old Hungarian (Funeral Sermon) | 1.401 | 0,06519 | 1.237 | Molto breve; modello 5-grammi sparso |
| Old Hungarian (Lamentation of Mary) | 734 | 0,06555 | 700 | Molto breve e di genere poetico |
| Old Luxembourgish (Codex Mariendalensis) | 3.579 | 0,06627 | 3.065 | Corpus breve |

È stata applicata la normalizzazione già usata dal progetto (minuscole, rimozione dei diacritici e dei caratteri non ASCII); per i due testi ungheresi è stata applicata la riparazione UTF-8/CP437 già usata dal loader. Le dimensioni ridotte dei testi antichi limitano soprattutto la stabilità dei modelli di n-grammi; per questo i controlli positivi sono parte essenziale dell'interpretazione.

## 3. Ipotesi crittografiche preregistrate e controlli

### 3.1 Sostituzione monoalfabetica

**Ipotesi:** ogni glifo della lettura corrisponde stabilmente a una lettera in chiaro; gli spazi sono ignorati. Si è usato il solver simulated-annealing già presente nel progetto, con ladder di modelli 2-, 3-, 4- e 5-grammi. Le lingue sono state scelte prima di confrontare i punteggi: latino Vulgata e corpus umanistico; ceco/boemo storico (due testi); ungherese storico (codice Érdy e due testi antichi); lussemburghese antico.

**Controllo positivo:** per ciascun modello sono stati estratti testi casuali e cifrati con una sostituzione casuale, a lunghezza esatta 584 o 678. Impostazione iniziale: 1.000 iterazioni e 2 restart per livello di n-grammi. Quindici dei sedici controlli abbinati sono stati recuperati esattamente in questa configurazione. Il controllo ceco Bohemian 3 di 584 caratteri è stato recuperato esattamente aumentando il budget a 5.000 iterazioni e 3 restart; lo stesso budget è stato usato per confrontare quel modello con entrambe le letture. Un controllo lussemburghese da 678 caratteri ha mostrato sensibilità al campione/seed a budget basso, ma è stato recuperato esattamente con il budget maggiore. Questi esiti calibrano il solver, ma non garantiscono che un singolo testo rappresenti la variabilità di ciascun corpus breve.

| Modello linguistico | `palma_A`: punteggio attacco − media naturale | `palma_B`: punteggio attacco − media naturale |
|---|---:|---:|
| Latino (Vulgata) | −2,950 | −2,824 |
| Latino (corpus umanistico) | −2,315 | −2,266 |
| Ceco antico (Bohemian 2) | −1,236 | −1,241 |
| Ceco antico (Bohemian 3) | −1,164 | −1,171 |
| Ungherese (codice Érdy, XV sec.) | −3,294 | −3,065 |
| Ungherese antico (Funeral Sermon) | −0,881 | −0,885 |
| Ungherese antico (Lamentation of Mary) | −0,742 | −0,740 |
| Lussemburghese antico (Codex Mariendalensis) | −0,897 | −0,898 |

Il punteggio è la media della log-probabilità 5-grammi; per ciascun modello la seconda quantità è la media su 80 finestre di testo di riferimento della medesima lunghezza. Un divario negativo indica che il candidato decifrato resta meno simile al corpus rispetto a finestre di testo naturale. Per i corpora ungheresi più brevi questo confronto è particolarmente instabile e va considerato indicativo. Nessuna delle ricerche ha prodotto una sequenza leggibile e vicina al livello naturale. Il risultato indebolisce l'ipotesi di una sostituzione monoalfabetica semplice in queste lingue, ma **non** esclude trasposizioni, cifrari polialfabetici, codifiche non linguistiche o errori di trascrizione.

### 3.2 Cifrario polialfabetico periodico

**Ipotesi:** una cifratura additiva periodica tipo Vigenère produce profili di coincidenza differenti per le colonne modulo il periodo. Sono stati considerati periodi 2–20 e, per ogni lettura, è stato confrontato il massimo osservato con 1.500 permutazioni casuali dei glifi, mantenendo inalterata la frequenza totale di ogni simbolo.

Per il periodo `k`, la statistica è la coincidenza aggregata entro le colonne:
`I_k = Σ_j Σ_s c_js(c_js−1) / Σ_j n_j(n_j−1)`, dove `c_js` è il conteggio del glifo `s` nella colonna `j` e `n_j` è la lunghezza della colonna. Il p empirico del massimo è `(1 + # massimi permutati ≥ massimo osservato) / 1501`.

| Lettura | Periodo con massimo picco | IC di colonna massimo | p empirico del massimo |
|---|---:|---:|---:|
| `palma_A` (n=584) | 17 | 0,06324 | 0,4011 |
| `palma_B` (n=678) | 11 | 0,08304 | 0,8894 |

Il p-value è corretto per la ricerca su tutti i periodi 2–20 (si confronta il massimo, non un periodo scelto dopo aver visto i dati). Non emerge un picco superiore a quello plausibile sotto il nullo di ordine casuale.

Come controlli positivi sono stati cifrati testi latini di pari lunghezza con chiavi casuali di periodi 3, 5, 7 e 11, 100 replicazioni per combinazione lunghezza/periodo. Il periodo esatto è risultato il massimo rispettivamente nel 4%, 18%, 50% e 100% dei controlli di 584 caratteri; e nel 7%, 20%, 52% e 100% dei controlli di 678 caratteri. Tuttavia, in tutti i controlli il massimo cadeva sul periodo vero **o su un suo multiplo**. Ciò mostra la confusione fra periodo fondamentale e armoniche; non autorizza a leggere il periodo massimo come chiave. I controlli dimostrano che la statistica risponde a una periodicità artificiale, ma la sensibilità esatta dipende dal periodo e dalla lunghezza.

## 4. PCA ampliata, senza trascrizioni simulate

La PCA è stata ricalcolata sui soli `palma_A` e `palma_B`, escludendo tutte le letture Gemini. I riferimenti sono i 16 modelli già configurati più i cinque corpora storici della tabella precedente: **21 corpora**, 100 finestre casuali di ciascuna lunghezza per corpus, per un totale di 4.200 campioni di riferimento. Gli inizi delle finestre sono stati estratti con rimpiazzo: nei corpora brevi alcune finestre si sovrappongono o possono ripetersi, quindi i campioni non sono osservazioni indipendenti. Le variabili sono 28 descrittori: IC, entropia, numero di glifi, ridondanza, quote dei 12 glifi più frequenti e, per n=2–5, rapporto `U/N`, ripetizione `1−U/N` ed entropia normalizzata `H_n/log2(N)`, con `U` n-grammi distinti e `N` finestre n-gramma. Il seme è 20261029. PCA addestrata sui soli riferimenti; le due letture sono state proiettate.

| Componente | Varianza spiegata | Cumulativa |
|---|---:|---:|
| PC1 | 41,77% | 41,77% |
| PC2 | 17,39% | 59,16% |
| PC3 | 11,51% | 70,67% |

| Lettura | PC1 standardizzata | PC2 standardizzata | PC3 standardizzata | Nota rispetto ai riferimenti |
|---|---:|---:|---:|---|
| `palma_A` | −2,864 | 0,667 | −0,841 | PC1 oltre il 5°–95° percentile dei riferimenti di pari lunghezza |
| `palma_B` | −1,333 | −0,442 | −3,344 | PC3 oltre il 5°–95° percentile dei riferimenti di pari lunghezza |

I gruppi geometricamente più vicini sui primi tre assi non concordano: `palma_A` è più vicina ai campioni della *Lamentation of Mary*, allo slovacco e al Bohemian 3; `palma_B` al lussemburghese antico, al codice Érdy e alla *Lamentation of Mary*. Queste distanze non sono probabilità di lingua: dipendono da feature, dimensione e genere dei corpora. Il fatto che le vicinanze cambino tra le letture e che entrambe escano dall'intervallo centrale su almeno una componente non identifica una lingua o un cifrario.

## 5. Conclusioni e limiti

1. Con le immagini locali non è possibile certificare una trascrizione indipendente completa; `gemini_full` non va trattata come testimone della lapide.
2. Sono stati ampliati i riferimenti con corpora storici pertinenti e verificati gli attacchi contro controlli positivi della stessa lunghezza. I controlli brevi impongono cautela, ma non spiegano il divario dei candidati Palma dai testi naturali.
3. I test svolti non sostengono né una decifrazione né una lingua specifica. Non forniscono prova in favore dell'identificazione con Vlad o di altre letture nominali.
4. I test NIST/Dieharder/TestU01 e le sequenze binarie a codifica arbitraria non sono ripetuti qui: la lunghezza di circa 600 simboli è troppo piccola e gli esiti dipendono dalla codifica scelta, come già documentato nel corpus.
5. Ho trovato e verificato una fotografia parziale più definita nella pubblicazione scientifica; il passo ancora necessario è ottenere l'immagine completa originale o un rilievo ad alta risoluzione e una trascrizione paleografica indipendente, con glifi incerti e lacune marcati, prima di ampliare ancora la ricerca di chiavi.

## 6. Documenti esaminati e acquisiti agli atti

I tre PDF consegnati sono copie di visualizzazioni web stampate in PDF: ogni pagina contiene una scansione raster e non testo selezionabile. Per controllarne il contenuto ho esaminato le pagine e verificato i testi contro gli articoli originali pubblicati. Di seguito registro i dati pertinenti, separando i fatti documentati dall'applicabilità al caso Turbolo.

### 6.1 Antal et al., documenti cifrati slovacchi

**Riferimento:** Eugen Antal, Pavol Marák, Pavol Zajac, Tünde Lengyelová e Diana Duchoňová, “Encrypted Documents and Cipher Keys From the 18th and 19th Century in the Archives of Aristocratic Families in Slovakia”, HistoCrypt 2023, pp. 1–12, [DOI 10.3384/ecp195689](https://doi.org/10.3384/ecp195689), [pagina ufficiale e PDF](https://ecp.ep.liu.se/index.php/histocrypt/article/view/689). Corrisponde al PDF locale [View of Encrypted Documents and Cipher Keys From the 18th and 19th Century in the Archives of Aristocratic Families in Slovakia.pdf](../View%20of%20Encrypted%20Documents%20and%20Cipher%20Keys%20From%20the%2018th%20and%2019th%20Century%20in%20the%20Archives%20of%20Aristocratic%20Families%20in%20Slovakia.pdf).

**Fatti documentati dall'articolo**

- La collezione dell'Archivio Nazionale Slovacco comprende 96 documenti cifrati e 9 chiavi, in 13 scatole, relativi agli archivi familiari Amade-Üchtritz, Esterházy e Pálffy-Daun. I documenti vanno dal 1711 al 1834 e coprono quasi 300 pagine.
- Il sistema più comune descritto è il *nomenclator*: cifre, eventualmente con separatori o marcatori, combinate con sostituzione semplice/omofonica, sostituzioni di bigrammi o trigrammi, codici e nulli. Delle nove chiavi censite, solo una corrispondeva a un documento cifrato conservato nello stesso insieme; altre chiavi considerate da archivi austriaci e ungheresi non corrispondevano ai testi esaminati.
- Il prototipo YOLOv7 lavora su **cifre manoscritte**, non su glifi alfabetici della lapide. Fu addestrato con 18 immagini (12 addestramento, 3 validazione, 3 test) e oltre 12.000 annotazioni di cifre. Sul test, il paper riporta per le maschere mAP@0.50 91,3%, mAP@0.50:0.95 60,9%, precisione 88,2%, recall 91,0%; per le bounding box rispettivamente 91,6%, 66,8%, 88,6% e 91,1%.
- Gli autori precisano che il riconoscimento automatico lascia errori di rilevamento e trascrizione; questi sono particolarmente difficili da riconoscere nel cifrato perché il risultato può sembrare una sequenza casuale. Indicano come lavoro futuro l'estensione dei dati di addestramento e sistemi capaci di tollerare gli errori di trascrizione.

**Valore per il dossier Turbolo:** è un confronto utile per il metodo archivistico (identificare mittenti e destinatari, datare, associare chiavi, cercare testi paralleli e conservare la provenienza delle letture) e per registrare esplicitamente gli errori di trascrizione. **Non** è evidenza che l'iscrizione della Turbolo usi un *nomenclator*, cifre, o lo stesso schema: il corpus è di epoca successiva, con alfabeti e supporti diversi, e l'algoritmo YOLOv7 del paper non è un OCR paleografico adatto ai glifi della lapide. I tassi di accuratezza pubblicati non sono trasferibili a questa fotografia.

### 6.2 Palma, epigrafe della Cappella Turbolo

**Riferimento:** Cosimo Palma, “Encrypted epigraphy - the case of a mysterious inscription in the Neapolitan church of Santa Maria La Nova”, HistoCrypt 2023, [DOI 10.3384/ecp195703](https://doi.org/10.3384/ecp195703), [pagina ufficiale e PDF](https://ecp.ep.liu.se/index.php/histocrypt/article/view/703). Corrisponde al PDF locale [View of Encrypted epigraphy - the case of a mysterious inscription in the Neapolitan church of Santa Maria La Nova.pdf](../View%20of%20Encrypted%20epigraphy%20-%20the%20case%20of%20a%20mysterious%20inscription%20in%20the%20Neapolitan%20church%20of%20Santa%20Maria%20La%20Nova.pdf).

L'articolo descrive l'iscrizione come circa 600 glifi, segnala erosioni e cancellazioni soprattutto in alto e in basso, e propone come ipotesi di lavoro una sostituzione monoalfabetica con possibili trasposizioni o polialfabetismo. Tuttavia, dichiara che l'analisi preliminare di n-grammi e di combinazioni vocali/consonanti non ha individuato una lingua in chiaro; nelle conclusioni l'autore lascia aperte ulteriori spiegazioni e richiede collaborazione filologica. Le traduzioni automatiche di frammenti sono esplicitamente giudicate inaffidabili dall'articolo stesso. La frase dell'abstract che parla di convergenza “unequivocabile” verso la sostituzione è dunque una valutazione dell'ipotesi di cifratura, **non** una decifrazione o una identificazione linguistica replicata.

La fotografia della Figura 1 è solo un dettaglio. L'articolo spiega che la fotografia completa è stata omessa per la quantità di erosione e cancellazioni. Questo conferma il limite documentale già registrato alla sezione 1; non aggiunge una trascrizione paleografica completa né una prova a favore di una traduzione specifica.

### 6.3 Layfield et al., conferenza sul manoscritto Voynich

**Riferimento:** Colin Layfield, René Zandbergen, Lisa Fagin Davis, John Abela, Claire Bowern, Michael Rosner e Lonneke van der Plas, “International Conference on the Voynich Manuscript 2022”, HistoCrypt 2023, [DOI 10.3384/ecp195700](https://doi.org/10.3384/ecp195700), [pagina ufficiale e PDF](https://ecp.ep.liu.se/index.php/histocrypt/article/view/700). Corrisponde al PDF locale [View of International Conference on the Voynich Manuscript 2022.pdf](../View%20of%20International%20Conference%20on%20the%20Voynich%20Manuscript%202022.pdf).

Questo articolo è una rassegna della conferenza, non un tentativo di decifrazione dell'iscrizione Turbolo. Riferisce che la discussione sul Voynich non ha risolto se il testo sia cifrato o non significativo. Per il presente dossier sono metodologicamente pertinenti tre risultati riportati nella rassegna:

1. Lo studio di Bowern e Gaskell applica 22 trasformazioni a testi naturali e confronta le caratteristiche risultanti con quelle del Voynich. Alcune trasformazioni si avvicinano al Voynich per alcune metriche ma divergono per altre: una statistica superficiale isolata non determina il meccanismo né il significato.
2. La rassegna descrive un metodo storico di Trithemius (*Polygraphia III*) in cui lettere sono rese con parole inventate e si possono aggiungere nulli: un testo privo di significato può quindi imitare proprietà di superficie di una lingua, e un cifrato può apparire anomalo.
3. La relazione riferisce inoltre problemi di accuratezza nelle traslitterazioni esistenti del Voynich e mette in evidenza l'utilità di rappresentazioni che consentano di confrontarle. Il principio è pertinente qui: un modello quantitativo non può compensare una trascrizione incerta o una convenzione di etichettatura non documentata.

**Valore per il dossier Turbolo:** è supporto metodologico alla prudenza già adottata—confronti multipli, controlli positivi, trascrizioni versionate e nessuna conclusione da PCA o test casuali da soli. Non trasferisce all'iscrizione le proprietà del Voynich e non costituisce prova che la Turbolo sia cifrata o sia gibberish.

### Esito complessivo dell'esame

I documenti rafforzano tre regole operative, non una traduzione: (i) mantenere separati dati materiali, trascrizione e ipotesi; (ii) ricercare chiavi e contesto storico-documentario, senza supporre che ogni chiave vicina appartenga al testo; (iii) calibrare ogni metodo su controlli e riportare i suoi errori. Nessuno dei tre articoli fornisce una nuova chiave, un testo in chiaro, una trascrizione completa o una prova identificativa per l'iscrizione Turbolo. Le nuove fonti sono confronti contestuali e metodologici, non testimonianze dirette della lapide.

## Riproducibilità

- Modelli storici aggiunti: `scripts/langmodels.py`.
- Trascrizioni e provenienza: `corpus/00_corpus.md` e `corpus/corpora.json`.
- Solver monoalfabetico: `scripts/03_attacks.py`.
- Semi: PCA `20261029`; nullo periodico `819` (1.500 permutazioni); controlli Vigenère `44` (100 replicazioni per periodo/lunghezza). Per gli attacchi monoalfabetici, i controlli standard sono generati con `seed=3100+j+n` e risolti con `seed=4100+j+n` per i primi sei modelli, e con `seed=6100+j+n` / `7100+j+n` per gli ultimi due (`j` indice del modello nella rispettiva lista e `n` lunghezza). Le finestre naturali di confronto sono 80 per lettura/modello, campionate con seed `31`. Gli attacchi standard usano `seed=900+j` per i primi sei modelli e `8100+j` per gli ultimi due; i controlli/attacchi con budget rafforzato usano i seed riportati nel codice di sessione: Czech 3 `3687`/`4687`, Luxembourg `2405`/`500`, target rafforzati `7001`.
- Il codice statistico della PCA e dei controlli periodici è stato eseguito in sessione; feature, formule, impostazioni, semi e dimensioni sono riportati qui per rendere trasparente la procedura.
