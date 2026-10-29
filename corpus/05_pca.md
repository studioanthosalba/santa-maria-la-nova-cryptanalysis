# Fase 1c -- ordinazione PCA dei profili invarianti

Ricostruzione e verifica critica dell'analisi PCA prodotta a parte (`report/pca_analisi.md`).

**Dati.** Tre letture dell'epigrafe (`palma_A` 584 glifi, `palma_B` 678, `gemini_full` 569) e 16 corpora di riferimento; 100 segmenti casuali per corpus e per ciascuna delle tre lunghezze (4800 campioni).

**Variabili.** 28 descrittori invarianti per rietichettatura: IC, entropia, numero di classi, ridondanza; quote dei 12 glifi più frequenti in ordine decrescente (ordinate, quindi non associate a un simbolo); per n = 2..5 rapporto tipi/totale, tasso di ripetizione ed entropia normalizzata degli n-grammi.

**Metodo.** Standardizzazione sui soli riferimenti, PCA sulla matrice di correlazione (autosolutore di Jacobi in sola libreria standard, 28 x 28), letture proiettate nello spazio risultante; seme 20261029.

## Varianza spiegata e significato degli assi

| componente | varianza spiegata | cumulativa |
|---|---|---|
| PC1 | 39.62% | 39.62% |
| PC2 | 17.44% | 57.06% |
| PC3 | 11.30% | 68.36% |
| PC4 | 7.69% | 76.04% |
| PC5 | 6.49% | 82.53% |
| PC6 | 3.33% | 85.86% |

Carichi più forti (correlazione variabile-componente):

| componente | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| PC1 | n3_types (+0.29) | n3_rep (-0.29) | n3_Hn (+0.29) | n4_types (+0.28) | n4_rep (-0.28) |
| PC2 | share7 (+0.32) | H (-0.32) | share6 (+0.31) | share8 (+0.30) | share5 (+0.28) |
| PC3 | share1 (+0.39) | IC (+0.34) | share10 (-0.30) | redundancy (+0.28) | share9 (-0.28) |
| PC4 | share11 (+0.38) | share10 (+0.35) | share5 (-0.34) | share4 (-0.33) | share12 (+0.29) |
| PC5 | K (+0.52) | share3 (-0.38) | n2_rep (-0.33) | redundancy (+0.25) | share7 (+0.22) |
| PC6 | share11 (+0.44) | share4 (+0.38) | K (+0.37) | share12 (+0.34) | redundancy (+0.27) |

## Posizione delle letture e confronto con l'analisi pubblicata

| lettura | n | PC1 z | PC2 z | PC3 z | intervallo 5-95% di PC1 nei riferimenti |
|---|---|---|---|---|---|
| `palma_A` | 584 | 2.94 | -1.37 | 0.57 | -1.69 - 1.41 |
| `palma_B` | 678 | 1.54 | -0.34 | 3.22 | -1.96 - 1.14 |
| `gemini_full` | 569 | -0.56 | 2.38 | 6.18 | -1.61 - 1.44 |

Confronto con i valori pubblicati in `report/pca_analisi.md` (stessi 28 descrittori, stesso schema di campionamento, stesso seme). Il segno di ciascun autovettore è arbitrario e l'orientamento scelto qui, pur deterministico, è indipendente da quello dell'analisi pubblicata: le componenti vengono perciò allineate una per una prima del confronto.

| lettura | pubblicato | ricalcolato | differenza assoluta |
|---|---|---|---|
| `palma_A` | 2.77, 1.61, 1.01 | 2.94, 1.37, 0.57 | 0.17, 0.24, 0.44 |
| `palma_B` | 1.29, 0.47, 3.52 | 1.54, 0.34, 3.22 | 0.25, 0.13, 0.30 |
| `gemini_full` | -0.87, -2.40, 6.03 | -0.56, -2.38, 6.18 | 0.31, 0.02, 0.15 |

Le nove coordinate concordano entro 0.44 deviazioni standard (mediana 0.24): l'ordinazione pubblicata è riprodotta. Restano non ricostruibili due suoi elementi: **quali** sedici corpora abbia usato (la pipeline ne configura 21 e ne seleziona sedici con una regola dichiarata, almeno 30.000 lettere, che esclude i cinque testi brevi del repository di Palma — `scripts/langmodels.py`) e le definizioni operative di «tasso di ripetizione» ed «entropia normalizzata» degli n-grammi. La riproduzione è quindi buona sul risultato e imperfetta sul protocollo.

## La definizione ambigua del «tasso di ripetizione»

L'analisi pubblicata non specifica come calcoli il tasso di ripetizione degli n-grammi. Le due definizioni plausibili sono la quota di n-grammi *token* che compaiono più di una volta e il complemento del rapporto tipi/totale, 1 − U/N. L'ordinazione è rifatta con la seconda, a parità di tutto il resto:

| lettura | scarto dalla PCA pubblicata con 1 - U/N | spostamento rispetto alla definizione a token |
|---|---|---|
| `palma_A` | 0.64 | 0.20 |
| `palma_B` | 0.37 | 0.10 |
| `gemini_full` | 0.24 | 0.15 |

Le due definizioni spostano le coordinate di al massimo 0.20 deviazioni standard e lasciano la riproduzione allo stesso livello: **l'ambiguità non è la causa delle differenze residue con l'analisi pubblicata**.

## Confronto con la seconda PCA presente nel repository

In `report/verifica_trascrizioni_corpora_cifrari.md` esiste una seconda ordinazione, eseguita in modo indipendente con 21 corpora (i sedici di questa pipeline più i cinque testi brevi) e con le sole letture Palma. Le sue coordinate, allineate nel segno, si confrontano con quelle calcolate qui:

| lettura | seconda PCA | questa pipeline | scarto massimo |
|---|---|---|---|
| `palma_A` | -2.86, 0.67, -0.84 | -2.94, 1.37, -0.57 | 0.70 |
| `palma_B` | -1.33, -0.44, -3.34 | -1.54, -0.34, -3.22 | 0.21 |

Con un insieme di corpora diverso e un codice diverso le coordinate delle due letture Palma concordano entro 0.70 deviazioni standard, e la seconda PCA conferma il punto che conta: le prossimità cambiano da una lettura all'altra, quindi non identificano una lingua. Le due analisi convergono anche sul resto — il merito della PCA è descrivere, non attribuire.

## Che cosa questa ordinazione non può vedere

I 28 descrittori sono invarianti per rietichettatura biiettiva: una sostituzione monoalfabetica **non sposta di un millimetro** il punto nello spazio PCA. Non è un'asserzione, è una verifica:

| controllo | n | scarto massimo sui 28 descrittori | scarto massimo su PC1-PC3 | IC | H |
|---|---|---|---|---|---|
| Latin (Vulgate) | 569 | 0.0e+00 | 0.0e+00 | 0.0787 | 3.9330 |
| Italian (Riveduta) | 584 | 0.0e+00 | 0.0e+00 | 0.0798 | 3.8800 |
| Slovak | 678 | 0.0e+00 | 0.0e+00 | 0.0899 | 3.9670 |
| Latin (humanist corpus) | 569 | 0.0e+00 | 0.0e+00 | 0.0679 | 4.0690 |

Scarto massimo su tutti i controlli: 0.0e+00. **L'ordinazione è cieca rispetto alla trasformazione che si vuole studiare.** Un'anomalia di posizione può quindi nascere solo da due cause: la struttura di ripetizione del testo, oppure il modo in cui è stato **trascritto** — mai dal fatto che sia cifrato per sostituzione, che quella struttura la lascia intatta.

## Il controllo decisivo: testo in chiaro con classi di glifi fuse

Se l'invarianza vale per sostituzione, la spiegazione più semplice — e non linguistica — della posizione anomala delle letture è il livello di dettaglio della trascrizione. Si prende allora un testo di riferimento **in chiaro, senza alcun cifrario**, e gli si fondono le prime k classi di glifi in una sola: è l'effetto di un trascrittore che non distingue le varianti Α/Λ/∀ o Ε/Є. Se il punto proiettato finisce dove finisce l'epigrafe, l'anomalia è di trascrizione, non di cifrario.

**Lettura `palma_A`** (n = 584): distanza dal centro dei riferimenti 2.15. Controlli alla stessa lunghezza:

| classi fuse | distanza mediana | frazione di controlli oltre la lettura | z PC1 | z PC2 | z PC3 |
|---|---|---|---|---|---|
| 0 | 1.31 | 0.06 | -1.51 | -0.15 | -0.09 |
| 1 | 2.19 | 0.50 | -2.69 | -0.16 | +2.66 |
| 2 | 3.65 | 1.00 | -3.97 | -0.11 | +5.80 |
| 3 | 5.55 | 1.00 | -5.36 | +0.46 | +9.06 |
| 4 | 7.50 | 1.00 | -6.88 | +1.06 | +12.07 |

**Lettura `palma_B`** (n = 678): distanza dal centro dei riferimenti 1.64. Controlli alla stessa lunghezza:

| classi fuse | distanza mediana | frazione di controlli oltre la lettura | z PC1 | z PC2 | z PC3 |
|---|---|---|---|---|---|
| 0 | 1.42 | 0.25 | -1.90 | -0.17 | +0.00 |
| 1 | 2.30 | 0.75 | -2.98 | -0.27 | +2.72 |
| 2 | 3.86 | 1.00 | -4.17 | -0.16 | +5.77 |
| 3 | 5.62 | 1.00 | -5.52 | +0.36 | +8.95 |
| 4 | 7.35 | 1.00 | -6.98 | +0.93 | +11.89 |

**Lettura `gemini_full`** (n = 569): distanza dal centro dei riferimenti 2.56. Controlli alla stessa lunghezza:

| classi fuse | distanza mediana | frazione di controlli oltre la lettura | z PC1 | z PC2 | z PC3 |
|---|---|---|---|---|---|
| 0 | 1.29 | 0.00 | -1.57 | -0.10 | -0.00 |
| 1 | 2.17 | 0.25 | -2.70 | -0.13 | +2.72 |
| 2 | 3.65 | 0.88 | -3.90 | -0.04 | +5.91 |
| 3 | 5.53 | 1.00 | -5.22 | +0.53 | +9.21 |
| 4 | 7.47 | 1.00 | -6.81 | +1.10 | +12.22 |

**Livello di fusione equivalente.** Per ogni lettura si riporta l'intervallo di fusioni in cui la sua distanza cade fuori dalle code della distribuzione dei controlli (frazione di testi naturali più lontani del centro compresa fra 0,10 e 0,90), con due valori di riferimento:

| lettura | distanza osservata | classi fuse compatibili | frazione di controlli oltre la lettura (m = 0) | frazione oltre (m = 2) |
|---|---|---|---|---|
| `palma_A` | 2.15 | 1 | 0.06 | 1.00 |
| `palma_B` | 1.64 | 0-1 | 0.25 | 1.00 |
| `gemini_full` | 2.56 | 1-2 | 0.00 | 0.88 |

Nessuna lettura richiede più di due fusioni, e `palma_B` sta già dentro la variabilità di un testo in chiaro senza alcuna fusione.

Attenzione alla differenza fra **scala** e **direzione**: la corrispondenza riguarda la distanza (una misura scalare, invariante per rotazione degli assi), non il profilo. A m = 0 il PC1 mediano dei controlli ha segno opposto a quello di `palma_A`, `palma_B`: la fusione delle classi riproduce *quanto* una lettura è lontana dal centro, non *dove* si trova. La conclusione corretta è quindi più stretta di quella che l'analisi pubblicata suggerisce e più stretta anche di una semplice equivalenza: **l'ampiezza dell'allontanamento non è evidenza di un cifrario diverso dalla sostituzione**, perché è la stessa che producono testi naturali non cifrati trascritti con una o due classi fuse.

## I vicini: quanto vale una tabella di prossimità

| lettura | componenti usate | prime 15 prossimità (lingua, conteggio) |
|---|---|---|
| `palma_A` | 2 | Slovak 11; Czech (catechism) 2; Czech (Bible Kralicka 1613) 2 |
| `palma_B` | 2 | Slovak 7; Croatian 7; Czech (catechism) 1 |
| `gemini_full` | 2 | Italian (Riveduta) 10; Latin (Vulgate) 4; Romanian 1 |
| `palma_A` | 3 | Slovak 15 |
| `palma_B` | 3 | Hungarian (Erdy codex, XV c.) 12; Albanian 2; Greek (Brenton, translit.) 1 |
| `gemini_full` | 3 | Hungarian (Erdy codex, XV c.) 8; Romanian 6; Albanian 1 |
| `palma_A` | 6 | Czech (catechism) 6; Slovak 5; Hungarian (Erdy codex, XV c.) 2; Czech (Bible Kralicka 1613) 2 |
| `palma_B` | 6 | Hungarian (Erdy codex, XV c.) 10; Albanian 4; Hungarian (Karoli) 1 |
| `gemini_full` | 6 | Romanian 6; Albanian 3; Greek (Brenton, translit.) 3; Hungarian (Erdy codex, XV c.) 3 |

La tabella cambia con il numero di componenti: è il sintomo che l'analisi pubblicata stessa segnala. Per sapere se una concentrazione come «dieci su quindici da una sola lingua» è informativa serve una distribuzione nulla, e la si ottiene applicando la stessa statistica ai punti di riferimento stessi (escludendo ciascun punto dai propri vicini):

| lettura | massimo su 15 (2 comp.) | p (nulla) | massimo su 15 (3 comp.) | p (nulla) |
|---|---|---|---|---|
| `palma_A` | 11 | 0.11 | 15 | 0.04 |
| `palma_B` | 7 | 0.46 | 12 | 0.13 |
| `gemini_full` | 10 | 0.15 | 8 | 0.49 |

Nei 300 punti di riferimento la concentrazione massima su una lingua va da 3 a 15 (mediana 6) su due componenti e da 3 a 15 su tre; le lingue distinte da 1 a 9. Valori osservati: a due componenti `palma_A` p = 0.11, `palma_B` p = 0.46, `gemini_full` p = 0.15; a tre componenti `palma_A` p = 0.04, `palma_B` p = 0.13, `gemini_full` p = 0.49.

Una concentrazione fuori dal null compare solo per `palma_A` e solo usando tre assi: riguarda produzioni intermedie della pipeline di Palma, non la lastra stessa (sezione 6), e non si ripete a due componenti. Le tabelle di prossimità, in questa forma, non identificano una lingua: descrivono quanto è affollata una regione dello spazio.

## Stabilità: seme del campionamento e insieme dei riferimenti

L'ordinazione viene rifatta con quattro semi diversi e, separatamente, escludendo quattro corpora periferici (inglese, tedesco, latino umanistico, Dante): dodici riferimenti al posto di sedici. Per ogni lettura si riporta l'oscillazione delle coordinate.

| lettura | PC1 z (min/max) | PC2 z | PC3 z | distanza (min/max) | lingua più prossima (la più frequente) |
|---|---|---|---|---|---|
| `palma_A` | +2.94 / +3.01 | -1.35 / +1.44 | -0.54 / +0.69 | 2.14 / 2.17 | Slovak |
| `palma_B` | +1.54 / +1.69 | -0.83 / +0.29 | -2.73 / +3.23 | 1.63 / 1.66 | Croatian |
| `gemini_full` | -0.59 / -0.42 | -3.77 / +2.23 | -5.04 / +6.38 | 2.46 / 2.58 | Italian (Riveduta) |

Le righe sono minime e massime su cinque ordinazioni indipendenti (quattro semi più il sottoinsieme ridotto a dodici corpora). **La distanza dal centro è la statistica che regge**: è invariante per rotazione degli assi e resta stabile. Le singole componenti oltre la prima no: PC2 e PC3 si scambiano o cambiano segno quando cambia il campione dei riferimenti, quindi un valore come «PC3 z = 6» non è riproducibile come grandezza isolata.

La lingua più prossima **cambia con il campionamento** (`palma_B`: Croatian, Slovak): l'attribuzione linguistica per prossimità non è un risultato.

## Quale famiglia di descrittori produce l'allontanamento

Le stesse letture proiettate in tre ordinazioni separate, una per famiglia di descrittori: se l'anomalia nasce dalla ripetizione degli n-grammi compare in tutte, se nasce dalla concentrazione delle frequenze compare solo nelle quote.

| famiglia | lettura | PC1 z | PC2 z | distanza |
|---|---|---|---|---|
| globali (IC, H, K, ridondanza) | `palma_A` | -1.51 | +1.65 | 1.54 |
| globali (IC, H, K, ridondanza) | `palma_B` | +0.87 | +0.62 | 0.82 |
| globali (IC, H, K, ridondanza) | `gemini_full` | +4.88 | +0.27 | 4.06 |
| quote di frequenza ordinate | `palma_A` | -1.19 | +0.72 | 0.89 |
| quote di frequenza ordinate | `palma_B` | -1.86 | -1.52 | 1.61 |
| quote di frequenza ordinate | `gemini_full` | -0.56 | -5.28 | 2.92 |
| n-grammi 2-5 | `palma_A` | +2.82 | -4.59 | 3.03 |
| n-grammi 2-5 | `palma_B` | +1.95 | -1.21 | 1.87 |
| n-grammi 2-5 | `gemini_full` | +0.78 | +1.93 | 1.11 |

Per `gemini_full` l'allontanamento più forte è nella famiglia «globali (IC, H, K, ridondanza)» (distanza 4.06), il più debole in «n-grammi 2-5» (1.11): l'irregolarità della sequenza non sta nella struttura di ripetizione degli n-grammi ma nella **concentrazione delle frequenze e nell'entropia**, cioè nel numero e nella distribuzione delle classi di glifi che la trascrizione distingue. È la stessa diagnosi della sezione 6.1, ottenuta per un'altra via.

## Verdetto su questa ordinazione

**Che cosa regge.**

1. L'analisi pubblicata è **riprodotta**: le nove coordinate delle tre letture concordano entro 0.44 deviazioni standard (mediana 0.24) con protocollo ricostruito da una descrizione verbale. La sua conclusione descrittiva — nessun profilo linguistico comune alle tre letture, `gemini_full` la più lontana — è confermata.
2. La **distanza dal centro** delle letture è stabile su quattro semi di campionamento e sul sottoinsieme ridotto a dodici corpora (`gemini_full`: 2.46-2.58; `palma_A`: 2.14-2.17).

**Che cosa non regge.**

1. **L'ordinazione non può testare un cifrario.** I 28 descrittori sono invarianti per sostituzione (scarto 0.0e+00): nessuna posizione PCA può dire se il testo è cifrato per sostituzione o in chiaro. L'ipotesi secondo cui «una sostituzione monoalfabetica non basta» non è un risultato di quella PCA: è un'ipotesi esterna che la PCA non può né sostenere né escludere.
2. **L'ampiezza dell'allontanamento non è un'anomalia.** Testi di riferimento **in chiaro, senza alcun cifrario**, a cui sono state fuse una o due classi di glifi hanno la stessa distanza dal centro delle letture: le fusioni compatibili sono `palma_A`: 1, `palma_B`: 0-1, `gemini_full`: 1-2. La via più economica per produrre quello spostamento non richiede alcun cifrario: basta una trascrizione che non distingua le varianti di glifo — ciò che la fotografia suggerisce (sezione 6.1).
3. **La direzione però non è quella.** La fusione delle classi sposta i controlli sul lato opposto di PC1 rispetto a `palma_A`, `palma_B`: il profilo delle letture resta irregolare anche dopo la fusione, e l'irregolarità riguarda le frequenze, non i n-grammi. La PCA dice quindi *quanto* è strano il profilo, non *perché*, e non può attribuirlo né a un cifrario né a un errore di lettura.
4. **Le tabelle di prossimità non identificano una lingua.** La lingua più vicina cambia con il numero di componenti e con il campionamento; la concentrazione delle letture (massimo 10 finestre su 15 da una sola lingua per `gemini_full`) ha p = 0.15 rispetto alla stessa statistica calcolata sui punti di riferimento. «Slovacco», «ungherese storico» e «italiano» sono etichette geometriche, non attribuzioni.
5. **Le componenti oltre la prima non sono stabili**, e i riferimenti non sono campioni indipendenti (cento finestre sovrapposte per corpus): le distanze non sono p-value e le componenti massimizzano la varianza, non la separazione fra lingue.

**Conclusione.** La PCA resta un buon strumento descrittivo e un cattivo strumento inferenziale. Integrata nella pipeline dice una cosa sola e la dice bene: le letture disponibili non sono profili di lingua naturale, e la loro distanza dai riferimenti è quella che produce una trascrizione a maglia larga. Non dice, e non può dire, se il testo sia cifrato, in quale lingua, né se contenga un nome.

