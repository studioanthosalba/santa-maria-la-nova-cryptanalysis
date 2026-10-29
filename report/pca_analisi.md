# Analisi PCA delle trascrizioni dell'epigrafe

> **Rettifica di provenienza:** la conversazione archiviata identifica `gemini_full` come simulazione delle righe, non come trascrizione indipendente della lapide. Di conseguenza le sue coordinate PCA, i vicini linguistici e i confronti che la includono non sono evidenza sulla lingua o sull'iscrizione reale. La presente analisi è conservata per tracciabilità; il confronto aggiornato esclude le letture Gemini ed è riportato in [verifica_trascrizioni_corpora_cifrari.md](./verifica_trascrizioni_corpora_cifrari.md).

> **Integrazione nella pipeline (fase 1c).** Questa analisi è stata ricostruita da zero in `scripts/05_pca.py` (output `corpus/05_pca.md`) e discussa nella sezione 4.8 di `report/report.md`. Esito: le coordinate delle tre letture sono riprodotte (scarto massimo 0,44 deviazioni standard, mediana 0,24) e la seconda PCA del repository concorda entro 0,70. Restano validi i limiti dichiarati qui sotto; due passaggi interpretativi non reggono. (i) I 28 descrittori sono invarianti per rietichettatura, quindi la posizione non può testimoniare né escludere un cifrario: l'ipotesi H2 non è un risultato della PCA. (ii) Testi di riferimento **in chiaro, senza cifrario**, con una o due classi di glifi fuse raggiungono la stessa distanza dal centro delle letture, e le tabelle di prossimità non superano il null (p = 0,12-0,45). Seme, definizioni dei descrittori e insieme dei sedici corpora (`MIN_REFERENCE` in `scripts/langmodels.py`) sono ora fissati nel codice, quindi ripetibili.

## Sintesi

Questa sezione documenta la PCA storica, eseguita prima di accertare la provenienza simulata di `gemini_full`. Le sue coordinate, i vicini linguistici e le conclusioni che dipendono da quella sequenza sono conservati per tracciabilità e **non sono evidenza sulla lapide**. Per l'analisi aggiornata delle sole letture Palma si veda [il report di verifica e confronto ampliato](./verifica_trascrizioni_corpora_cifrari.md).

La PCA non decifra l'iscrizione e non identifica una lingua. I risultati sono compatibili con più spiegazioni, fra cui differenze di trascrizione, un sistema diverso dalla sostituzione monoalfabetica semplice, o un testo/registro non rappresentato dai corpora di confronto. Non consentono di scegliere fra queste spiegazioni né di sostenere un nome proprio.

## Dati e metodo

- **Letture analizzate:** `palma_A` (584 glifi), `palma_B` (678), `gemini_full` (569).
- **Riferimenti:** 16 corpora, fra cui latino, ceco, italiano, greco traslitterato, ungherese storico, rumeno e altre lingue. Sono i corpora già configurati nel progetto.
- **Campionamento:** per ogni corpus sono stati estratti 100 segmenti casuali a ciascuna delle tre lunghezze delle letture. Totale: **4.800 campioni** (16 × 3 × 100).
- **Variabili:** 28 descrittori statistici: indice di coincidenza, entropia, numero di glifi e ridondanza; quote dei 12 glifi più frequenti in ordine di frequenza; per n-grammi da 2 a 5 glifi, rapporto n-grammi distinti/totale, tasso di ripetizione ed entropia normalizzata.
- **Pre-elaborazione:** standardizzazione delle 28 variabili e PCA calcolata sui soli segmenti dei corpora di riferimento. Le letture dell'epigrafe sono state proiettate nello spazio risultante.
- **Riproducibilità:** seme pseudocasuale fissato (`20261029`); i risultati sono condizionati da questa selezione di segmenti e dalle scelte di feature.

Le variabili sono invarianti alla rinomina coerente dei glifi: questo rende il confronto pertinente soprattutto come controllo di compatibilità con trasformazioni che preservano tali regolarità, per esempio una sostituzione monoalfabetica. Non rende le statistiche invarianti a trascrizioni errate, fusione di glifi, inserimenti/cancellazioni o trasformazioni più generali.

## Risultati

### Varianza spiegata

| Componente | Varianza spiegata | Cumulativa |
|---|---:|---:|
| PC1 | 36,03% | 36,03% |
| PC2 | 17,37% | 53,40% |
| PC3 | 11,03% | 64,43% |
| PC4 | 8,55% | 72,98% |
| PC5 | 7,04% | 80,02% |
| PC6 | 3,41% | 83,43% |

PC1 è associata soprattutto ai descrittori degli n-grammi di lunghezza 3–5: rapporto di n-grammi distinti, tasso di ripetizione ed entropia. PC2 è associata soprattutto all'entropia dei glifi e alle quote dei glifi più frequenti. La PCA riassume quindi prevalentemente differenze di ripetizione e concentrazione, non significati o parole.

### Posizione delle letture

Le coordinate `z` qui sotto sono le coordinate PCA divise per la deviazione standard della rispettiva componente, stimata sui riferimenti. Gli intervalli di riferimento sono il 5°–95° percentile dei campioni della lunghezza corrispondente; non sono intervalli di confidenza né test formali.

| Lettura | n | PC1 z | PC2 z | PC3 z | Intervallo PC1 di riferimento | Intervallo PC2 | Intervallo PC3 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `palma_A` | 584 | 2,77 | 1,61 | 1,01 | -1,57–1,40 | -1,63–1,52 | -1,44–1,88 |
| `palma_B` | 678 | 1,29 | 0,47 | 3,52 | -1,84–1,17 | -1,62–1,52 | -1,61–1,79 |
| `gemini_full` | 569 | -0,87 | -2,40 | 6,03 | -1,58–1,45 | -1,59–1,56 | -1,42–1,92 |

Le tre letture non mostrano un profilo stabile: `palma_A` è spostata soprattutto su PC1, `palma_B` su PC3, mentre `gemini_full` è molto distante dai riferimenti su PC2 e soprattutto PC3. Questa eterogeneità è un risultato descrittivo; non stabilisce se la causa sia la trascrizione, la lingua o il sistema di cifratura.

### Vicini nello spazio PCA

I risultati dipendono dal numero di componenti usate e dalla metrica di distanza:

| Lettura | 15 campioni di riferimento più vicini in PC1–PC2 | 15 più vicini in PC1–PC3 standardizzate |
|---|---|---|
| `palma_A` | Slovacco 10; ceco Kralická 4; catechismo ceco 1 | Slovacco 11; ceco Kralická 3; polacco 1 |
| `palma_B` | Slovacco 10; croato 3; ceco Kralická 1; catechismo ceco 1 | Ungherese storico (codice Érdy) 12; ungherese Károli 2; albanese 1 |
| `gemini_full` | Italiano Riveduta 9; rumeno 4; latino Vulgata 2 | Ungherese storico 6; rumeno 6; albanese 2; latino Vulgata 1 |

Le assegnazioni di “vicino” non sono stabili passando da due a tre componenti. Non vanno lette come probabilità che la lingua sia quella indicata: i conteggi sono vicinanze geometriche fra campioni, non classificazione convalidata. Le componenti omesse possono inoltre contenere differenze importanti.

## Ipotesi di lavoro, ordinate per priorita

Le ipotesi seguenti sono alternative da sottoporre a verifica, non conclusioni.

### H1 — La variabilità delle trascrizioni contribuisce sostanzialmente ai risultati

**Motivazione:** le tre letture hanno posizioni PCA divergenti; la documentazione del corpus segnala inoltre basso accordo relabel-invariant fra letture indipendenti (identità circa 0,245–0,329 per le coppie principali).

**Predizione verificabile:** una nuova trascrizione indipendente, basata su immagini ad alta risoluzione e con una legenda esplicita dei glifi, dovrebbe ridurre le differenze se il problema è soprattutto di lettura. Se l’accordo restasse basso dopo un allineamento paleografico affidabile, questa spiegazione perderebbe forza.

### H2 — Una sostituzione monoalfabetica semplice non basta a spiegare le letture considerate

**Motivazione:** le statistiche di ripetizione degli n-grammi e la PCA non collocano stabilmente le letture nel profilo dei testi naturali di riferimento. Per una sostituzione monoalfabetica, le ripetizioni dei pattern restano invarianti.

**Predizione verificabile:** con una trascrizione confermata e un corpus del registro/lingua appropriati, un attacco calibrato dovrebbe produrre testo coerente su ampie porzioni e superare controlli cifrati della stessa lunghezza. Il mancato successo attuale non esclude altri cifrari o una trascrizione difettosa.

### H3 — Lingua, genere o corpus di riferimento non adeguati

**Motivazione:** la PCA usa un insieme finito di lingue e soprattutto testi di prosa religiosa o corpora specifici; una breve epigrafe, una lingua non inclusa, un registro formulare o una traslitterazione atipica possono avere profili differenti.

**Predizione verificabile:** aggiungere corpora epigrafici comparabili per epoca, genere e supporto dovrebbe avvicinare il profilo solo se una delle ipotesi linguistiche è corretta. La selezione dei corpora va fissata prima di confrontare le proiezioni per evitare di scegliere retrospettivamente il riferimento più conveniente.

### H4 — Il testo potrebbe usare una trasformazione diversa dalla sostituzione semplice

**Motivazione:** le letture non corrispondono bene a un singolo profilo semplice. Tuttavia, i test di periodicità già eseguiti non hanno trovato evidenza di un periodo fino a 20 per le letture Palma.

**Predizione verificabile:** testare una famiglia definita in anticipo (per esempio trasposizione con regole dichiarate, cifrario polialfabetico con periodi delimitati, o codifica per gruppi) su controlli sintetici della stessa lunghezza. Senza una regola e controlli positivi, esplorare molte trasformazioni aumenta il rischio di sovradattamento.

### H5 — Le lettere greche nella lettura sono etichette dei glifi, non necessariamente suoni greci

**Motivazione:** la lettura `palma_B` usa lettere greche come convenzione per rappresentare classi di glifi. La PCA ne usa i profili di ripetizione senza interpretarne il valore fonetico.

**Predizione verificabile:** una trascrizione paleografica che colleghi ciascuna etichetta al segno osservato e un attacco a greco traslitterato validato su controlli greci cifrati sono necessari prima di trarre conclusioni sulla lingua. Il tentativo preliminare con il solver greco non ha superato adeguatamente il controllo positivo, quindi non consente di confermare o confutare il greco.

## Limiti interpretativi

1. **PCA è descrittiva, non una prova d'ipotesi.** Le distanze non sono p-value e le componenti massimizzano la varianza, non la capacità di riconoscere una lingua.
2. **Il campionamento dei riferimenti è dipendente.** Finestre casuali dello stesso testo possono sovrapporsi; 4.800 campioni non equivalgono a 4.800 testi indipendenti.
3. **La standardizzazione e le feature influenzano gli assi.** Cambiare le statistiche, i corpora, la normalizzazione o i segmenti può cambiare coordinate e vicini.
4. **I dati target sono letture incerte.** La PCA non corregge errori, segni illeggibili, fusioni di glifi o differenze fra trascrittori.
5. **Nessuna traduzione è stata ottenuta.** Le vicinanze con lingue di riferimento non validano parole, nomi, la chiave «Vlad» o un significato funerario.

## Prossimi controlli consigliati

1. Stabilire una trascrizione diplomatica comune, con ogni glifo distinto, incertezza segnalata e posizioni sulla lastra.
2. Rifare la PCA con finestre non sovrapposte o bootstrap per blocchi e riportare la sensibilità a varianti delle feature.
3. Separare le statistiche invarianti alla sostituzione dalle statistiche dipendenti dai glifi e analizzare esplicitamente le due famiglie.
4. Confrontare con iscrizioni coeve di lunghezza e genere simili, includendo il greco solo se le corrispondenze paleografiche lo giustificano.
5. Valutare ogni modello crittografico con controlli positivi e una regola fissata prima di cercare nomi o frasi.

## Riferimenti interni

- Dati e provenienza delle trascrizioni: [00_corpus.md](../corpus/00_corpus.md)
- Statistiche descrittive: [01_descriptive.md](../corpus/01_descriptive.md)
- Confronti inferenziali e periodicità: [02_inferential.md](../corpus/02_inferential.md)
- Attacchi e controlli crittanalitici: [03_attacks.md](../corpus/03_attacks.md)
