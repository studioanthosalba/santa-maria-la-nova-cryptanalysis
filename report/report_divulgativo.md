# L'epigrafe misteriosa di Santa Maria la Nova: che cosa sappiamo (e che cosa no)

Una spiegazione per chi non è del mestiere. I numeri citati qui sono gli stessi
del rapporto tecnico (`report/report.md`), solo raccontati in parole comuni.

## 1. Di che cosa parliamo

In una chiesa di Napoli, Santa Maria la Nova, c'è una cappella — la cappella
Turbolo — con una lastra di pietra incisa. Accanto alla lapide sta una tomba
che la tradizione popolare attribuisce a Vlad III di Valacchia, l'uomo che ha
ispirato il personaggio di Dracula.

La lastra porta un'iscrizione latina normale (un'indulgenza di papa
Gregorio XIII) e, accanto, un'altra iscrizione di circa 600 segni in un alfabeto
che non assomiglia a nessuno conosciuto: un misto di forme latine (A, B, E…)
e greche (Δ, Φ, Λ, Σ…). Nessuno sa che cosa dica. È il nostro oggetto di studio.

## 2. Obiettivo dello studio

Due domande:

1. **Che tipo di testo è?** Una lingua scritta in un alfabeto sconosciuto? Un
   messaggio cifrato? Un esercizio decorativo senza significato?
2. **Che cosa si può dire dell'ipotesi Dracula?** L'iscrizione conferma,
   smentisce o non tocca la leggenda?

La promessa del metodo è semplice: non indovinare, non costruire storie, ma
fare dire ai dati tutto quello che possono dire — e dichiarare onestamente
quello che non possono.

## 3. Che cosa avevamo in mano (e il primo problema)

Per studiare un testo serve il testo. Ne esistevano tre versioni, e nessuna è
una lettura diretta della pietra: due sono del ricercatore che ha pubblicato
l'unico studio sull'epigrafe (Palma, 2023) e sono, a conti fatti, stadi intermedi
del suo procedimento; la terza è una **simulazione** delle righe, costruita a
partire dall'impianto visibile nelle fotografie, che assomiglia alla lapide senza
esserne un testimone indipendente. Più due fotografie della lastra.

Il primo problema è emerso subito e spiega metà della storia: **le tre
stringhe non raccontano la stessa lapide**. Confrontate con le regole del
mestiere (rinominando i simboli in modo uniforme, così che due letture della
stessa sequenza debbano combaciare carattere per carattere), due stringhe
qualsiasi condividono al massimo **4-5 simboli consecutivi su 600**. È come
se due copisti avessero trascritto la stessa pagina e nessuno dei due
concordasse con l'altro per più di un paio di parole di fila.

Questo non è un dettaglio: significa che **non esiste ancora una trascrizione
affidabile della pietra**, e che qualunque analisi fatta su quelle stringhe
misura anche — o soprattutto — gli errori dei trascrittori. Averlo stabilito
con precisione è già un risultato, perché spiega perché il problema sembrava
impossibile.

## 4. Risultati: che cosa dice la matematica

### 4.1 Non è una decorazione casuale

Il primo sospetto è il più semplice: forse è un insieme di segni messi lì a
caso, per fare scena. Si può verificare. L'indice di coincidenza (IC) misura
quanto un testo si ripete: in un testo a caso ogni segno ha più o meno la
stessa probabilità; in una lingua vera alcune lettere tornano molto più spesso
di altre (pensate alla E italiana) e le combinazioni di due-tre lettere si
ripetono con regolarità.

Le nostre tre stringhe hanno un IC lontano **38, 94 e 146 deviazioni standard**
da quello di un testo casuale della stessa lunghezza; il test classico di
Friedman rifiuta la casualità con **meno di una probabilità su mille miliardi
(p < 10⁻¹²)**. Le sequenze di tre segni si ripetono fra 4 e 10 volte più del caso.
Conclusione: chi ha inciso la pietra ha seguito un **sistema**. Non sappiamo
quale, ma un sistema c'è.

### 4.2 Non assomiglia a nessuna lingua

Allora forse è una lingua scritta con un alfabeto strano. Per controllarlo
abbiamo confrontato le stringhe con 16 lingue di riferimento (ceco, greco,
latino, ungherese, italiano e altre, su Bibbie e classici), usando misure che
non dipendono dai nomi dei simboli (un cifrario rinomina le lettere, non
cambia le loro abitudini: la lettera più frequente resta la più frequente
anche se la chiami un altro simbolo).

Nessuna lingua regge il confronto: la migliore somiglianza resta **oltre la
soglia di incompatibilità** in tutti i casi. Il difetto è sempre lo stesso:
le nostre stringhe ripetono **troppo poco** le combinazioni di due e tre
segni. In una lingua reale le “sillabe statistiche” tornano in continuazione;
qui quasi mai.

C'è un secondo test, più astuto. In ogni lingua le vocali e le consonanti si
alternano: nessuna parola ha otto consonanti di fila. Poiché i simboli sono
etichette arbitrarie, abbiamo provato **tutte le 33 649 combinazioni possibili**
di 5 vocali su 23 segni e preso la migliore: un'assegnazione migliore di quella
non esiste. Risultato: sotto le trascrizioni di Palma nessuna scelta produce
un'alternanza naturale; sotto la sequenza simulata sì, ed è perfetta (le vocali
risultano esattamente i segni che *sembrano* vocali: A, E, I, O, V) — ma quella
sequenza è una simulazione, cioè un testo generato per somigliare alla lapide:
la sua naturalezza non è una prova sulla pietra, è la firma di chi l'ha
prodotta. Le stringhe disponibili
descrivono quindi **testi con struttura diversa** — un'altra conferma del
problema del punto 3.

### 4.3 Nessun cifrario classico la spiega

Il passo successivo: provare i cifrari storici uno per uno.

- **Sostituzione semplice** (ogni simbolo sta per una lettera, tipo il
  cryptogramma dei giornali). Il nostro programma è capace di risolverli: su
  tre testi di controllo in latino, ceco e italiano li decifra **esattamente,
  lettera per lettera**. Sull'epigrafe si ferma lontanissimo da qualunque
  testo reale, al livello di una sequenza senza senso. Il fallimento non è
  dello strumento: è del dato.
- **Cifrari periodici** (quelli dove la chiave si ripete, tipo Vigenère):
  nessun periodo nascosto. I piccoli indizi di periodicità che si vedevano a
  occhio risultano, al test statistico, puro rumore.
- **Segni riempitivo** (simboli messi lì per confondere): l'ipotesi non è
  sostenuta dai confronti calibrati.
- **Chiavi onomastiche**: VLAD, DRACULA, TURBOLO e gli altri nomi della
  leggenda, usati come chiavi, non producono nulla di meglio di una chiave
  inventata a caso della stessa lunghezza.

Un avvertimento importante, scoperto leggendo i documenti d'archivio messi
agli atti: in un archivio reale di cifrari sette-ottocenteschi le chiavi
conservate **non corrispondono ai testi conservati** (96 documenti cifrati,
9 chiavi, che non combaciano). Quindi il fatto che i nomi non funzionino come
chiavi **non smentisce** che il testo sia cifrato: la mancata corrispondenza
è normale anche dove cifrato e chiave esistono entrambi.

### 4.4 La spiegazione più compatibile: una trascrizione piena di errori

Abbiamo costruito un simulatore che prende una lingua vera, la cifra, ci
aggiunge rumore (segni letti male, saltati, aggiunti) e confronta il risultato
con le nostre stringhe. La calibrazione sui testi di origine nota funziona.

Risultato: la stringa più ricca di Palma diventa spiegabile **se circa un
segno su tre è sbagliato** (30% di errori di trascrizione). A quel livello di
rumore, però, nessun metodo può più riconoscere la lingua di partenza: trenta
errori su cento cancellano la firma linguistica. L'altra stringa di Palma e la
sequenza simulata restano fuori portata persino di questa spiegazione (la
simulazione è incompatibile con tutti i modelli).

In parole povere: **i dati che abbiamo sono troppo rovinati per dire di più**.
Non è una scusa, è un numero: il 30%.

### 4.5 Il grafico PCA: riprodotto e ridimensionato

Circolava un'analisi statistica (ordinamento PCA) che collocava le nostre
stringhe lontane da tutte le lingue e concludeva: “quindi è un cifrario”.
L'abbiamo ricostruita da zero: i calcoli tornano (scarto mediano 0,24
deviazioni standard). Ma i suoi 28 descrittori sono **invarianti per
sostituzione**: un cifrario che rinomina le lettere finisce nello stesso punto
del testo in chiaro da cui deriva. Il grafico, quindi, non può distinguere un
cifrario da una lingua, e i controlli lo confermano: testi **in chiaro** con
qualche segno fuso fra loro producono la stessa posizione delle nostre
stringhe. L'ipotesi “è un cifrario, lo dice la PCA” è stata **ritirata**.

## 5. Le ipotesi: che cosa resta in piedi

| ipotesi | stato | in parole semplici |
|---|---|---|
| Segni incisi a caso | **non sostenuta** | troppo strutturata per essere caso: IC a 38-146 σ, p < 10⁻¹² |
| Lingua naturale in chiaro, travestita da alfabeto esotico | **improponibile** | nessuna delle 16 lingue si avvicina: le ripetizioni sono troppo poche |
| Testo greco scritto in lettere greche | **non sostenuta** | con le vocali greche reali le sequenze di consonanti valgono 0,445 contro meno di 0,10 in ogni lingua |
| Sostituzione semplice (un simbolo = una lettera) | **non sostenuta** | il programma che decifra i tre controlli resta 3 nats per finestra sotto il testo reale |
| Sostituzione con segni riempitivo | **non sostenuta** | il guadagno è quello dei controlli senza riempitivi (p = 0,077) |
| Cifrario polialfabetico periodico | **non sostenuta** | nessun periodo nascosto: p = 0,44 e 0,93 |
| Chiavi onomastiche (VLAD, DRACULA, TURBOLO…) | **non sostenuta** | indistinguibili da chiavi casuali; e in archivio le chiavi non combaciano comunque |
| «È un cifrario, lo dice la PCA» | **ritirata** | i 28 descrittori sono invarianti: non distinguono un cifrario dal chiaro |
| Preghiera penitenziale ceca medievale | **non confermata** | il ceco è la lingua più vicina a una lettura, ma il confronto generativo la boccia (Δ = −4,9) |
| Trascrizione rumorosa di una lingua reale | **la più compatibile** | spiega la lettura più ricca di Palma con 1 errore su 3, e a quel rumore la lingua non è più identificabile |
| Tavola didattica / decorazione senza messaggio | **possibile, non dimostrabile** | strutturata sì, ma nessun modello linguistico la cattura |
| Beffa o gioco intellettuale | **possibile** | posizione di metodo discussa in letteratura, non dimostrabile |

Le due letture di Palma indicano come lingua più vicina due lingue diverse
(il ceco per una, il greco per l'altra): un altro sintomo che è il rumore di
trascrizione a dominare il segnale, non la lingua.

## 6. Conclusione: e Dracula?

La lapide contiene un **testo sistematico, non casuale, che oggi non è
leggibile**: non perché il cifrario sia troppo difficile, ma perché non
disponiamo di una trascrizione abbastanza fedele da poter essere interrogata.

Per l'ipotesi Dracula questo significa una cosa precisa: **l'iscrizione, come
possiamo leggerla oggi, non può essere usata né a favore né contro la
leggenda**. Cercare “VLAD” o “DRACULA” in stringhe che due letture della stessa
lapide non fanno combaciare è cercare in un testo che non abbiamo. Il test è
stato fatto comunque, per completezza, e non ha dato nulla — ma il suo valore
è limitato, per la ragione d'archivio spiegata sopra.

Non è un fallimento: è una **localizzazione del problema**. All'inizio il
mistero sembrava crittografico; alla fine è dimostrato che la variabile
dominante è la qualità delle trascrizioni, e che il passo giusto è un altro.

## 7. Che cosa servirebbe per andare avanti

In ordine:

1. **Una fotografia ad alta risoluzione della lastra** (o un rilievo):
   le due immagini disponibili danno al massimo 14-34 pixel per segno — bastano
   per dire com'è fatta la lapide, non per rileggerla.
2. **Una nuova trascrizione, fatta da un paleografo**, con i segni incerti
   segnati come tali e, se possibile, due persone indipendenti che si
   confrontano.
3. Solo dopo, riprendere la ricerca: alfabeti storici (cariano, copto,
   glagolitico, simboli alchemici) e archivi con chiavi documentate.

Che cosa **non** serve: altre chiavi tentate sulle trascrizioni attuali, o
altri calcoli statistici sulle stesse tre stringhe. I dati dicono che il
problema non è lì.

## 8. Piccolo glossario

- **Glifo**: un segno dell'iscrizione, come una lettera.
- **Trascrizione**: la copia su carta/computer dei segni incisi. Le tre
  disponibili non concordano fra loro — e una non è una trascrizione, è una
  simulazione.
- **IC (indice di coincidenza)**: misura quanto un testo si ripete; in un
  testo casuale è basso, in una lingua è più alto.
- **Deviazione standard (σ)**: l'unità con cui si misura quanto un valore è
  lontano dal caso: 38 σ è “impossibile che sia fortuna”.
- **Cifrario a sostituzione**: ogni simbolo sta per una lettera, sempre la
  stessa.
- **PCA**: tecnica per disegnare su un grafico le somiglianze fra testi;
  utile per orientarsi, ma — come abbiamo dimostrato — non può rivelare se un
  testo è cifrato.

---

*Rapporto divulgativo derivato da `report/report.md` (pipeline riproducibile,
nessun numero inventato a mano). Il bilancio completo del lavoro, con le
impronte SHA256 di tutti i consegnati, è in `report/atti/relazione_finale.md`.*