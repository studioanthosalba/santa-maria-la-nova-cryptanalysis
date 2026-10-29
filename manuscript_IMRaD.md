# L'Epigrafe Cifrata di Santa Maria la Nova: Analisi Crittanalitica Riproducibile e Confutazione Quantitativa dell'Ipotesi Vlad III di Valacchia

**Autore:** Antonino Magazzù*  
*Ricercatore Indipendente*  
*\*Autore Corrispondente: Antonino Magazzù*

---

## Abstract

**Background:** L'epigrafe incisa nella Cappella Turbolo del complesso monumentale di Santa Maria la Nova a Napoli (circa 600 glifi in un sistema scrittorio anomalo) è stata ripetutamente associata dalla divulgazione e da recenti contributi crittanalitici (Palma, 2023) alla presunta sepoltura di Vlad III di Valacchia ("l'Impalatore").  
**Obiettivo:** Questo studio si propone di sottoporre l'epigrafe, le trascrizioni esistenti e l'ipotesi "Dracula" a uno stress-test computazionale rigoroso, deterministico e riproducibile, stabilendo: (1) se la sequenza sia casuale o strutturata; (2) se sia compatibile con una lingua naturale in chiaro; (3) se sia spiegabile mediante cifrari classici a sostituzione o con chiavi onomastiche; (4) quanto il rumore di trascrizione condizioni l'identificabilità crittografica.  
**Metodi:** È stata sviluppata una pipeline computazionale in 7 fasi (open-source e deterministica) applicata a tre trascrizioni (`palma_A`, 584 glifi; `palma_B`, 678 glifi; `gemini_full`, 569 glifi) e confrontata con 16 corpora di riferimento in 12 lingue (>30.000 caratteri ciascuno). L'analisi ha impiegato metriche invarianti per rietichettatura (Indice di Coincidenza, Entropia di Shannon, tassi di bigrammi e trigrammi ripetuti), null calibrati di permutazione e bootstrap, un test combinatorio esaustivo dell'alternanza vocalica $C_3$ su tutti i $\binom{K}{5}$ sottoinsiemi, un solver a sostituzione ad ascesa di gradiente (validato su controlli con divario nullo: $0.00\text{ nats}$), crib-dragging onomastico e un modello generativo a rumore gaussiano con fattori di Bayes.  
**Risultati:** Il testo non è casuale: l'Indice di Coincidenza dista tra 38 e 146 deviazioni standard dall'uniformità e il test di Friedman rigetta l'ipotesi nulla ($p < 10^{-12}$). Tuttavia, nessuna lingua in chiaro è compatibile (distanza media $|z| > 2.08$), con un deficit sistematico nelle ripetizioni n-grammatiche. Le trascrizioni pubblicate non concordano fra loro: condividono un massimo di soli 4–5 simboli consecutivi, dimostrando di non essere letture indipendenti della medesima sequenza lapidea. Il solver crittanalitico fallisce sull'epigrafe ($-13.45\text{ nats/finestra}$ contro il livello di testo reale a $-10.09$, a fronte di un baseline casuale di $-14.00$). Tutti i crib onomastici (VLAD, DRACULA, TURBOLO) non superano il null ($p \in [0.085, 0.960]$). Un modello generativo ammette verosimiglianza solo assumendo un tasso di errore di trascrizione $\ge 30\%$, livello al quale i fattori di Bayes collassano nell'indecidibilità linguistica. Infine, l'ordinamento PCA a 28 descrittori viene confutato: i descrittori sono invarianti per sostituzione e la distanza dal centro è interamente spiegabile dalla fusione artificiale di classi di glifi.  
**Conclusioni:** L'epigrafe di Santa Maria la Nova è un manufatto testuale strutturato, ma l'ipotesi di una decifrazione legata a Vlad III è allo stato attuale non verificabile né falsificabile per assenza di dati documentari primari. Il blocco epistemologico non è crittanalitico ma paleografico: nessuna ricerca di chiavi ha senso prima dell'acquisizione di una fotogrammetria ortogonale ad altissima risoluzione e di una trascrizione diplomatica indipendente con censimento delle lacune.

**Keywords:** Crittografia Storica; Epigrafia Cifrata; Santa Maria la Nova; Vlad III; Indice di Coincidenza; Statistiche Invarianti; Riproducibilità Scientifica.

---

## 1. Introduzione (Introduction)

### 1.1 Contesto Storico ed Epigrafico
Nel complesso monumentale di Santa Maria la Nova a Napoli, all'interno della cappella della famiglia Turbolo, è collocato un monumento sepolcrale tardo-rinascimentale recante una singolare iscrizione epigrafica di circa 600 caratteri. I glifi, incisi su marmo accanto a un'epigrafe latina che commemora l'indulgenza plenaria concessa da Papa Gregorio XIII, appartengono a un repertorio alfabetico anomalo, caratterizzato dalla commistione di forme pseudo-greche, caratteri latini arcaizzanti, simboli cruciformi e glifi geometrici non riconducibili a nessuna scrittura epigrafica standard del Mezzogiorno rinascimentale.

Negli ultimi decenni, una tradizione storiografica eterodossa e una vasta eco mediatica hanno associato questo monumento alla presunta sepoltura di Vlad III di Valacchia (noto storicamente come Vlad Țepeș, l'Impalatore, e trasfigurato nel mito di Dracula). Secondo tale congettura, il voivoda valacco non sarebbe perito in battaglia nel 1476, bensì sarebbe stato riscattato dalla figlia Maria Balsa, condotto nel Regno di Napoli sotto la protezione della corte aragonese e ivi inumato in forma criptata per sottrarne le spoglie alle profanazioni ottomane.

### 1.2 Stato dell'Arte e Limiti delle Pubblicazioni Precedenti
Il tentativo più organico di analisi crittografica è stato presentato da Palma (2023) negli atti del convegno internazionale *HistoCrypt*. Palma ha sostenuto che l'epigrafe celi una preghiera penitenziale in lingua ceca medievale ("Old Czech"), cifrata mediante un sistema a sostituzione monoalfabetica con varianti e omologhi, e ha proposto l'individuazione di stringhe onomastiche latenti.

Tuttavia, un'analisi critica preliminare dei dati depositati da Palma evidenzia anomalie documentarie e metodologiche non trascurabili:
1. **Confusione e corruzione dei corpora di controllo:** Come rilevato nel presente studio, i file indicati come testi cechi di riferimento (`bibliahuszita` e `czechcodex.txt`) contengono in realtà ungherese quattrocentesco (il Codice di Monaco del 1466), con una doppia codifica errata dei caratteri (UTF-8 interpretato come CP437). Di conseguenza, i valori statistici attribuiti all'Old Czech nelle pubblicazioni precedenti risultano viziati ab origine.
2. **Confronti diretti di frequenza illegittimi:** Confrontare i vettori di frequenza dei simboli cifrati direttamente con i profili alfabetici delle lingue naturali (ad esempio mediante software quali *AZdecrypt*) presuppone che i simboli del cifrario condividano l'ordinamento naturale dell'alfabeto in chiaro. In un cifrario a sostituzione, i simboli subiscono una permutazione arbitraria; pertanto, ogni confronto tra testo e lingue è matematicamente fondato solo se basato su **statistiche invarianti per permutazione** (re-labeling invariant statistics).
3. **Discrepanza radicale tra trascrizioni:** Le stringhe diffuse nella letteratura recente non sono state verificate rispetto all'effettiva disposizione lapidea o presentano discordanze macroscopiche non quantificate.

### 1.3 Il "Research Gap" e Obiettivi dello Studio
Nella letteratura su Santa Maria la Nova manca finora un'indagine formale, quantitativa e replicabile che separi il segnale statistico intrinseco dell'epigrafe dagli artefatti indotti dalle trascrizioni manuali. Non è stato mai chiarito se il fallimento della decifrazione sia imputabile alla complessità del cifrario o alla corruzione delle trascrizioni di partenza.

Il presente lavoro si prefigge tre obiettivi formali:
1. **Valutazione della natura del testo:** Determinare mediante test d'ipotesi non parametrici e inferenziali se l'epigrafe sia un testo strutturato, un'iscrizione priva di senso (*gibberish*) o una sequenza generata casualmente.
2. **Stress-test crittanalitico sistematico:** Applicare algoritmi di decifrazione ad ascesa di gradiente, crib-dragging su chiavi storiche/onomastiche e modelli generativi di rumore gaussiano, calibrando ogni test su distribuzioni nulle controllate.
3. **Verifica empirica dell'ipotesi "Dracula":** Misurare quantitativamente se gli elementi onomastici o linguistici associati a Vlad III emergano con significatività statistica superiore al rumore di fondo, fornendo un protocollo definitivo per la ricerca epigrafica futura.

---

## 2. Materiali e Metodi (Materials & Methods)

Lo studio adotta una metodologia interamente deterministica e riproducibile, implementata in un'architettura software in 7 fasi sequenziali descritte nella Tabella 1.

### 2.1 Il Corpus delle Trascrizioni Epigrafiche
Non essendo possibile operare un prelievo autoptico diretto durante la presente campagna di studio, sono state acquisite e normalizzate tre trascrizioni storiche primarie e di controllo:
- **`palma_A` (Trascrizione a righe):** 584 glifi, suddivisi in 38 righe, con un inventario di $K = 24$ classi grafiche distinte e 20 segni segnalati come degradati o illeggibili.
- **`palma_B` (Trascrizione continua):** 678 glifi in un'unica stringa ininterrotta, $K = 23$ classi e 93 glifi incerti.
- **`gemini_full` (Testimone sintetico / Simulazione multimodale):** 569 glifi organizzati in 36 righe, $K = 23$ classi, generata da una sessione assistita da intelligenza artificiale multimodale (Google Gemini).
- **Controllo di sensibilità (`drac_raw`):** 863 caratteri (68 righe con duplicazioni da rilievi parziali).

#### 2.1.1 Genesi, Ruolo e Meccanica Operativa di `gemini_full`
La sequenza `gemini_full` merita una menzione metodologica esplicita per il suo valore epistemologico nell'ambito della *Digital Epigraphy*. Essa è stata generata nel corso di una sessione esplorativa mediante un modello di fondazione multimodale (Google Gemini, sessione archiviata `gemini.google.com/app/f772b148032e8663`), al quale sono state fornite le fotografie storiche dell'epigrafe (`drac1.jpeg` e `drac2.webp`) chiedendo di modellare un algoritmo di rotazione rinascimentale con chiave `VLAD`.

Il modello ha operato una **trascrizione/simulazione a vista delle 36 righe della lapide**:
1. **Aderenza strutturale:** Il modello ha catturato fedelmente l'impaginato complessivo e il nucleo centrale di 8 righe, inclusa la caratteristica struttura simmetrica a specchio con il palindromo lapideo ben leggibile `ΔΕΔΕΔ`.
2. **Il meccanismo della fusione grafica (Macro-Classi):** Operando su immagini a bassa risoluzione (14–34 pixel per glifo), la visione artificiale ha manifestato una tendenza intrinseca al collasso delle varianti grafiche sottili. Il modello ha unificato i glifi triangolari (fondendo $A$, $\Lambda$ e $\forall$) e ha accorpato i glifi curvilinei ($E$, $\epsilon$, $\Sigma$) in macro-classi omogenee.
3. **Funzione di controllo di sensibilità:** `gemini_full` non è stata inclusa nello studio con la pretesa di rappresentare un testimone diplomatico indipendente del marmo, bensì come **esperimento di calibrazione controllata**: ha permesso di misurare sperimentalmente quale impatto statistico produca la trascrizione automatica guidata da LLM in presenza di rumore d'immagine, rivelando che la fusione di classi grafiche è la causa diretta dell'impennata dell'Indice di Coincidenza ($IC = 0.1147$).

Tutte le sequenze sono state canonizzate mappando i simboli in etichette intere progressive ordinate per frequenza decrescente, rendendo l'analisi indipendente dalle convenzioni di traslitterazione adottate dai singoli trascrittori.

### 2.2 Corpora Linguistici di Riferimento
Per evitare bias di campionamento e distorsioni dovute alla brevità dei campioni, sono stati selezionati **16 corpora indipendenti** in 12 lingue storiche e moderne, con una soglia minima di $N \ge 30.000$ caratteri alfabetici continui:
- Latino (Vulgata Clementina; testi umanistici);
- Ceco (Bibbia Kralická del 1613; Catechismo storico);
- Ungherese antico (Codice di Monaco, 1466; Bibbia di Károli);
- Romeno, Greco biblico, Albanese, Croato, Slovacco, Polacco, Tedesco, Inglese e Italiano tardo-medievale (Dante, *Commedia*).

I testi sono stati puliti rimuovendo punteggiatura, spaziature e diacritici, ed estratti in finestre scorrevoli di ampiezza identica alla lunghezza delle trascrizioni epigrafiche ($L = 584$ e $L = 678$).

### 2.3 Metriche Invarianti per Rietichettatura
Dato un testo di lunghezza $N$ su un alfabeto di $K$ classi con frequenze assolute $f_i$ ($i = 1, \dots, K$), sono state calcolate cinque metriche matematicamente invarianti rispetto a qualsiasi permutazione biiettiva dei simboli $\pi: \Sigma \to \Sigma$:
1. **Indice di Coincidenza ($IC$):**
   $$IC = \frac{\sum_{i=1}^K f_i (f_i - 1)}{N(N - 1)}$$
   e la sua versione normalizzata rispetto all'ampiezza dell'alfabeto $IC \times K$.
2. **Entropia di Shannon di primo ordine ($H$):**
   $$H = - \sum_{i=1}^K p_i \log_2 p_i \quad \text{con } p_i = \frac{f_i}{N}$$
3. **Quota del simbolo dominante ($p_{\max}$):**
   $$p_{\max} = \max_{i} (p_i)$$
4. **Tasso di bigrammi ripetuti ($R_2$):** Quota dei bigrammi che compaiono più di una volta sul totale dei bigrammi possibili.
5. **Tasso di trigrammi ripetuti ($R_3$):** Quota dei trigrammi ricorrenti, indicatore chiave della regolarità morfo-sintattica locale.

### 2.4 Modelli Null e Test Inferenziali
Per ciascuna metrica osservata, sono stati costruiti tre modelli null rigorosi:
- **Null di Permutazione:** Rimescolamento casuale uniforme delle posizioni dei simboli nel testo osservato ($M = 10.000$ repliche).
- **Null Linguistico:** Campionamento bootstrap di 1.000 finestre indipendenti di lunghezza $N$ dai 16 corpora di riferimento.
- **Test Esaustivo $C_3$ (Alternanza Vocale/Consonante):** Poiché le etichette dei glifi sono arbitrarie, è stata calcolata la metrica di Sukhotin/Palma su **tutti i possibili $\binom{K}{5}$ sottoinsiemi** di 5 glifi candidati ad agire da vocali, identificando la combinazione $V^*$ che minimizza il deficit di alternanza:
  $$C_3(V) = \frac{\text{Bigrammi } VV + \text{Bigrammi } CC}{\text{Totale Bigrammi}}$$

### 2.5 Solver Crittanalitico e Calibrazione ad Ascesa di Gradiente
Per testare l'ipotesi di una sostituzione monoalfabetica (MASC), è stato implementato un algoritmo di ascesa di gradiente (*hill-climbing*) basato sulla verosimiglianza di transizione dei trigrammi log-arricchiti (calcolati in *nats* per finestra).  
**Protocollo di Validazione dello Strumento:** Il solver è stato preventivamente testato su tre crittogrammi di controllo sintetici generati cifrando testi latini e volgari noti della stessa lunghezza dell'epigrafe. In tutti e tre i controlli, il solver ha ricostruito la chiave esatta con un **divario di verosimiglianza nullo ($0.00\text{ nats}$)**, dimostrando che l'algoritmo possiede una potenza statistica ideale per decifrare testi di questa estensione.

### 2.6 Modello Generativo a Rumore di Trascrizione
È stato sviluppato un modello bayesiano in cui il testo osservato $Y$ è generato da una lingua $L$ attraverso una sostituzione casuale $\pi$ seguita da un processo di corruzione bernoulliana con probabilità d'errore $\epsilon \in [0.0, 0.40]$:
$$P(Y \mid L, \epsilon) = \mathcal{N}\left(\mathbf{s}(Y); \boldsymbol{\mu}_{L}, \boldsymbol{\Sigma}_{L} + \epsilon^2 \mathbf{I}\right)$$
dove $\mathbf{s}(Y)$ è il vettore delle statistiche invarianti osservate, calcolando i relativi Fattori di Bayes rispetto all'ipotesi di testo casuale.

---

## 3. Risultati (Results)

I dati quantitativi raccolti nelle sette fasi dell'indagine sono riassunti nelle Tabelle e Figure seguenti.

### 3.1 Proprietà Globali e Non-Casualità del Testo
Come riportato nella Tabella 2, l'epigrafe di Santa Maria la Nova manifesta una struttura intrinseca marcatamente distante dall'uniformità. L'Indice di Coincidenza ($IC$) varia da $0.0595$ (`palma_A`) a $0.0813$ (`palma_B`) fino a $0.1147$ (`gemini_full`), distanziando la distribuzione casuale uniforme di $38.4$, $66.1$ e $146.2$ deviazioni standard rispettivamente. Il test non parametrico di Friedman rifiuta l'ipotesi di casualità con $p < 10^{-12}$ per tutte le trascrizioni.

**Table 1.** *Caratteristiche descrittive globali delle trascrizioni epigrafiche.*

| Trascrizione | Righe | Glifi Totali ($N$) | Classi di Glifi ($K$) | Indice Coincidenza ($IC$) | $IC \times K$ | Entropia $H$ (bit) | Tasso Trigrammi Ripetuti ($R_3$) |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `palma_A` | 38 | 584 | 24 | 0.0595 | 1.4290 | 4.269 | 0.1507 |
| `palma_B` | 1 | 678 | 23 | 0.0813 | 1.8700 | 3.990 | 0.2743 |
| `gemini_full` | 36 | 569 | 23 | 0.1147 | 2.6380 | 3.550 | 0.4605 |
| *Testo Casuale (Uniforme)* | — | 600 | 24 | 0.0416 | 1.0000 | 4.585 | 0.0012 |

*Nota: I valori delle trascrizioni divergono sensibilmente tra loro; in particolare, l'elevato IC di `gemini_full` è riconducibile alla compressione di varianti grafiche (es. fusione di A/Λ e E/Є).*

---

### 3.2 Incompatibilità con le Lingue Naturali in Chiaro
Il confronto delle statistiche invarianti rispetto alle distribuzioni bootstrap dei 16 corpora di controllo evidenzia una discrepanza sistematica. Nessuna lingua naturale esaminata risulta compatibile con le trascrizioni di Palma.

Come sintetizzato nella Tabella 2, la distanza $z$-score media minima per `palma_A` è $|z| = 2.61$ (registrata rispetto al ceco della Bibbia Kralická), mentre per `palma_B` è $|z| = 2.08$ (greco biblico translitterato). In entrambi i casi, la distanza supera la soglia convenzionale di compatibilità biologico-linguistica ($|z| \le 2.00$).

**Table 2.** *Distanza z-score multivariata tra le trascrizioni e le principali lingue storiche candidate.*

| Lingua di Riferimento | Corpus / Fonte | Distanza Media $\|z\|$ (`palma_A`) | Distanza Media $\|z\|$ (`palma_B`) | $p$-value Congiunto |
|---|---|:---:|:---:|:---:|
| **Ceco Umanistico** | Bibbia Kralická (1613) | **2.61** | 2.84 | 0.009 |
| **Latino Classico/Eccl.** | Vulgata Clementina | 3.12 | 2.45 | 0.002 |
| **Greco Ellenistico** | Versione Brenton | 3.40 | **2.08** | 0.038 |
| **Romeno Storico** | Bibbia Romena Tradizionale | 3.58 | 2.91 | < 0.001 |
| **Ungherese Antico** | Codice di Monaco (1466) | 3.89 | 3.15 | < 0.001 |
| **Italiano Tardo-Mediev.** | Dante, *Divina Commedia* | 3.95 | 3.22 | < 0.001 |

*Nota: La colonna 'Ceco Umanistico' riflette il testo ceco corretto, non il corpus ungherese erroneamente etichettato nelle ricerche pregresse.*

L'incompatibilità più marcata risiede nella microstruttura sequenziale: mentre la frequenza unigrammatica simulerebbe un alfabeto fonetico, i tassi di bigrammi e trigrammi ripetuti cadono costantemente al di sotto del primo percentile delle lingue naturali ($p < 0.01$), rivelando un deficit di ridondanza tipico di trascrizioni corrotte o di cifrari frazionatori.

---

### 3.3 Test di Allineamento Inter-Trascrizione: Il Fallimento della Concordanza
L'allineamento a scorrimento dinamico tra le trascrizioni produce il risultato epistemologicamente più rilevante dell'intera indagine:
- Tra `palma_A` (584 glifi) e `palma_B` (678 glifi), dopo rietichettatura canonica ottimale, la massima sequenza continua identica è costituita da soli **4 simboli consecutivi**.
- Tra `palma_B` e `gemini_full`, la massima sequenza comune è pari a **5 simboli consecutivi**.

Dal punto di vista probabilistico, due trascrizioni corrette e indipendenti di una medesima epigrafe lapidea di 600 caratteri dovrebbero mostrare una concordanza superficiale di almeno il 75–85% ($>450$ caratteri allineati). L'assenza di blocchi comuni superiori a 5 glifi rigetta formalmente l'ipotesi che `palma_A` e `palma_B` siano letture della stessa sequenza: esse rappresentano stadi intermedi di elaborazione algoritmica interna o estrazioni da porzioni disomogenee del monumento.

---

### 3.4 Esito degli Attacchi Crittanalitici Classici
- **Solver ad Ascesa di Gradiente:** Applicato alle trascrizioni epigrafiche con $5.000$ iterazioni di riavvio casuale, il solver si è arrestato a un punteggio massimo di verosimiglianza pari a **$-13.45\text{ nats/finestra}$**. Questo valore si colloca a ridosso della baseline del rumore casuale ($-14.00\text{ nats}$) ed è drammaticamente inferiore alla soglia di un testo decifrato reale ($-10.09\text{ nats}$). Poiché il solver ha decifrato i controlli con divario $0.00$, l'insuccesso dimostra che il testo epigrafico trascritto **non è una cifratura a sostituzione monoalfabetica diretta di una delle 16 lingue testate**.
- **Crib-Dragging su Nomi Propri (Ipotesi Dracula):** La ricerca esaustiva di chiavi onomastiche e cribs storici (`VLAD`, `DRACULA`, `TEPES`, `TURBOLO`, `GREGORIUS`, `BALSA`) non ha prodotto alcuna corrispondenza statisticamente significativa. Le verosimiglianze associate ai vincoli onomastici hanno generato $p$-value distribuiti uniformemente nell'intervallo $p \in [0.085, 0.960]$, coerenti con pure fluttuazioni stocastiche.

---

### 3.5 Modello di Rumore e De-costruzione della PCA
Il modello generativo bayesiano dimostra che `palma_A` può essere ricondotta nell'orbita di una lingua naturale solo ipotizzando un **tasso di errore di trascrizione di almeno il 30%** ($\epsilon \ge 0.30$, log-verosimiglianza 13.06). A questo livello di rumore, tuttavia, la capacità discriminatoria del modello decade: i fattori di Bayes tra le diverse lingue scendono al di sotto di 3.0, rendendo matematicamente impossibile stabilire se il chiaro sottostante fosse latino, ceco, ungherese o romeno.

Infine, l'analisi delle componenti principali (PCA) su 28 descrittori, proposta in precedenza come indizio crittografico, è stata interamente replicata (scarto medio di coordinate $0.24$) e confutata:
1. I 28 descrittori impiegati sono matematicamente invarianti per sostituzione monoalfabetica; pertanto, la posizione occupata nel piano fattoriale non fornisce alcuna informazione sulla presenza di un cifrario.
2. Esperimenti di controllo condotti su testi in chiaro hanno dimostrato che la semplice fusione accidentale di 2 classi di glifi frequenti (errore paleografico comune su marmo eroso) sposta le coordinate esattamente nella regione occupata dalle trascrizioni epigrafiche.

---

## 4. Discussione (Discussion)

### 4.1 Interpretazione dei Risultati: Il Problema è Documentario, Non Crittografico
I risultati ottenuti consentono di rispondere con chiarezza alle domande di ricerca poste nell'Introduzione. L'epigrafe di Santa Maria la Nova manifesta proprietà statistiche inequivocabilmente non casuali ($IC \gg 0.0416$, $p < 10^{-12}$), attestando la presenza di una struttura sintattica o crittografica deliberata.

Tuttavia, l'insuccesso convergente di tutti gli attacchi monoalfabetici e la mancata concordanza tra i testimoni testuali evidenziano che **l'ostacolo principale alla decifrazione non risiede nell'intrinseca complessità matematica dell'algoritmo cifrante, bensì nella radicale inaffidabilità delle trascrizioni attualmente disponibili**.

Quando due trascrizioni della medesima epigrafe condividono al più 4 simboli consecutivi, qualsiasi tentativo di forzare la decifrazione mediante dizionari storici produce inevitabilmente decifrazioni illusorie (*overfitting* su rumore), spiegando la proliferazione di letture divergenti prive di valore scientifico.

### 4.2 Confronto Critico con la Letteratura e Fonti Archivistiche
La tesi di Palma (2023), secondo cui l'iscrizione celerebbe una preghiera in ceco medievale, risulta indebolita da due riscontri oggettivi emersi in questo studio:
1. La correlazione linguistica originariamente calcolata si basava su corpora contaminati da codici ungheresi. Ricalcolando le metriche sul ceco reale (Bibbia Kralická e testi penitenziali), la significatività scompare ($|z| = 2.61$).
2. Le fonti secondarie archivistiche depositate agli atti (in particolare lo studio di Antal et al. sui cifrari aristocratici del Regno d'Ungheria conservati nell'Archivio Nazionale Slovacco) documentano che nei fondi diplomatici del XVIII-XIX secolo i cifrari crittografici reali operavano frequentemente con nomenclatori a cifre, elenchi di parole nulle e chiavi esterne non coincidenti con i testi conservati. Pretendere di decifrare una lapide complessa assumendo una sostituzione semplice a alfabeto costante costituisce una semplificazione anacronistica.

### 4.3 Il Ruolo dei Modelli Multimodali (LLM) e la Lezione Metodologica di `gemini_full`
L'inclusione di `gemini_full` offre un contributo originale di rilievo per il settore emergente dell'intelligenza artificiale applicata ai beni culturali (*AI in Digital Epigraphy*). Quando modelli di visione e linguaggio elaborano manufatti epigrafici fortemente degradati, tendono fisiologicamente a colmare l'incertezza visiva attraverso euristiche di regolarizzazione:
- Da un lato, il modello ha identificato correttamente i pattern macro-strutturali (il palindromo `ΔΕΔΕΔ` e la scansione a blocchi).
- Dall'altro, ha prodotto una fusione forzata di varianti grafiche sottili, distorcendo l'Indice di Coincidenza ($IC = 0.1147$) e generando un testo che non concorda per più di 5 caratteri con le letture umane.

Questa constatazione dimostra che **l'impiego di modelli generativi nella trascrizione non può sostituire la paleografia autoptica**: l'AI non deve essere usata per "allucinare" una lettura continua su foto a bassa risoluzione, ma semmai come strumento a valle per testare ipotesi combinatorie una volta acquisita una trascrizione diplomatica certificata.

### 4.3 Limiti dello Studio (Limitations)
Nel rispetto dei canoni di integrità accademica, si dichiarano i seguenti limiti tecnici della presente indagine:
1. **Risoluzione delle Immagini Primarie:** L'ispezione visiva si è basata sulle fotografie storiche disponibili (`drac1.jpeg`, 225×225 pixel; `drac2.webp`, 544×1024 pixel), che garantiscono al più 14–34 pixel per cella di glifo. Tale densità impedisce l'applicazione di algoritmi OCR affidabili o la verifica autoptica dei tratti incisi.
2. **Potenza Statistica della Lunghezza Campionaria:** Con un testo di circa 600 caratteri, i test globali ($IC$, entropia) possiedono una potenza eccellente per rigettare ipotesi nulle, ma risultano deboli nel discriminare dialetti o lingue affini in presenza di un rumore di trascrizione $>20\%$.

---

## 5. Conclusioni e Prospettive Future (Conclusions)

L'indagine quantitativa condotta conduce a tre conclusioni definitive:
1. **Natura del Manufatto:** L'epigrafe della Cappella Turbolo a Santa Maria la Nova non è una composizione casuale né un mero ornamento fantastico, ma un manufatto testuale dotato di forte coerenza statistica locale.
2. **Stato dell'Ipotesi Vlad III (Dracula):** L'ipotesi che l'epigrafe costituisca la tomba di Vlad III di Valacchia è **scientificamente non verificabile né falsificabile con i dati attualmente esistenti**. Nessuna evidenza onomastica o statistica la supporta, e i tentativi di lettura finora divulgati derivano da trascrizioni metodologicamente incoerenti e inquinate da rumore documentario.
3. **Roadmap per la Ricerca Futura:** La ricerca crittanalitica sull'epigrafe di Santa Maria la Nova deve essere sospesa fino al compimento di due passaggi preliminari obbligati:
   - Acquisizione in situ di rilievi fotogrammetrici ortogonali ad altissima risoluzione (sub-millimetrici) o scansione 3D a luce strutturata.
   - Redazione di una **trascrizione diplomatica aperta e indipendente**, corredata da una tavola paleografica dei glifi, dall'esplicita registrazione dei dubbi di lettura e dalla marcatura rigorosa delle lacune lapidee.

Solo in presenza di un testo diplomaticamente certificato sarà scientificamente legittimo riaprire la ricerca della chiave crittografica.

---

## Dichiarazioni Obbligatorie (Compliance Declarations)

- **Ethics Approval:** La ricerca non ha coinvolto soggetti umani né modelli animali; non è stata richiesta l'approvazione di comitati etici (IRB).
- **Data & Code Availability:** La pipeline analitica è interamente deterministica e riproducibile. Tutto il codice sorgente Python, i dati numerici JSON, le matrici di allineamento e i log con impronte hash SHA256 stabili sono accessibili nel repository di progetto (percorso locale: `/mnt/c/Progetti/dracula/`).
- **Conflict of Interest:** L'autore Antonino Magazzù dichiara l'assenza di conflitti di interesse finanziari, professionali o personali relativi alla presente ricerca.
- **Funding:** Questo studio è una ricerca indipendente condotta in totale autonomia scientifica da Antonino Magazzù, senza finanziamenti esterni, sponsorizzazioni o vincoli istituzionali.

---

## Bibliografia (References)

1. Antal, P., Marák, P., Zajac, P., Lengyelová, T., & Duchoňová, D. (2022). Encrypted Documents and Cipher Keys from the 18th and 19th Century in the Archives of Aristocratic Families in Slovakia. *Proceedings of the 5th International Conference on Historical Cryptology (HistoCrypt2022)*, 12–21.
2. Bauer, F. L. (2007). *Decrypted Secrets: Methods and Maxims of Cryptology* (4th ed.). Springer-Verlag.
3. Friedman, W. F. (1922). *The Index of Coincidence and Its Applications in Cryptanalysis*. Riverbank Publication No. 22. Riverbank Laboratories.
4. Layfield, C. et al. (2022). The Voynich Manuscript: Cryptanalysis, Codicology, and Comparative Linguistics. *Proceedings of the International Conference on the Voynich Manuscript 2022*, University of Malta, 1–18.
5. Palma, F. (2023). Encrypted epigraphy: the case of a mysterious inscription in the Neapolitan church of Santa Maria La Nova. *Proceedings of the 6th International Conference on Historical Cryptology (HistoCrypt 2023)*, Munich, Germany, 145–154.
6. Shannon, C. E. (1949). Communication Theory of Secrecy Systems. *Bell System Technical Journal*, 28(4), 656–715.
7. Sukhotin, B. V. (1962). Eksperimental'noe vydelenie glasnykh bukv pri pomoshchi EVM (Experimental identification of vowels using an electronic computer). *Problemy Strukturnoj Lingvistiki*, 1, 61–72.
