# Documenti agli atti

Lettura critica dei tre PDF messi a disposizione per confronto e confutazione.
Questo documento è **l'atto**: dice che cosa i tre testi sono, dove sono stati
letti, che cosa affermano e — soprattutto — quale ipotesi del rapporto
`report.md` ciascuno **sostiene, indebolisce o confuta**. Le affermazioni qui
sotto sono ancorate a numeri di pagina; quelle che non ho potuto leggere non
sono usate (sezione 7). Il bilancio complessivo del lavoro e la conclusione
finale sono in `report/atti/relazione_finale.md`.

## 1. Stato documentale (misurato, non stimato)

| documento | pagine | byte | SHA256 (inizio) | livello di testo | raster di pagina |
|---|---|---|---|---|---|
| Palma 2023 (HistoCrypt) | 9 | 4 849 816 | `aec01a09…29710f` | **assente** | 1240×1753 px |
| Antal, Marák, Zajac, Lengyelová, Duchoňová | 12 | 9 914 463 | `6b77b101…7d1291` | **assente** | 1240×1753 px |
| Layfield, Abela, Zandbergen, Bowern, Davis, Rosner, van der Plas 2022 | 7 | 2 932 872 | `a02dc21e…526cf` | **assente** | 1240×1753 px |

Numeri meccanici completi in `report/atti/manifest.json`, rigenerabile con
`python scripts/_extract_pdf.py`. I tre file stanno nella radice del repository
con i nomi originali del download (`View of Encrypted epigraphy …pdf`,
`View of Encrypted Documents and Cipher Keys …pdf`,
`View of International Conference on the Voynich Manuscript 2022.pdf`): il
prefisso `View of` è quello che aggiunge l'archivio online, non parte del titolo.

Tre conseguenze, tutte misurate:

1. **I PDF sono scansioni di pagina, non documenti nativi digitali.** Ogni pagina
   è un solo `/Image` XObject, `/FlateDecode`, 8 bit, `ICCBased` RGB,
   1240×1753 px — cioè un A4 a **≈150 ppi**, senza alcun `/Font` (verificato con
   `python scripts/_pdf_pages.py FILE.pdf --info`). Non esiste quindi ricerca
   testuale: `_extract_pdf.py` restituisce **0 caratteri** su tutti e tre.
2. **In questo ambiente non c'è OCR** (`tesseract` assente, sezione 6 del
   rapporto). La lettura è stata fatta **a vista, pagina per pagina**:
   `scripts/_pdf_pages.py` decodifica il raster con la sola libreria standard e
   scrive un PNG (fattore 2 → 620×877) in `report/atti/pages/`, poi ispezionato.
   È lo stesso limite delle fotografie della lapide, applicato alle fonti
   secondarie; la differenza è che qui i caratteri sono stampati e leggibili,
   non incisi a 14 px per glifo.
3. **Le pagine effettivamente lette** sono queste, e solo queste: Palma p1, p2,
   p9; Antal et al. p1, p2, p3, p12; Layfield et al. p1, p2. Il resto dei tre
   documenti è agli atti come raster ma **non** è stato letto, e nulla in questo
   documento si fonda su di esso.

### Un dato da correggere nel rapporto

`report/palma_histocrypt2023.txt` (33 164 byte) è un estratto **preesistente** e
**non riproducibile dai PDF qui agli atti**: questi ultimi non hanno livello di
testo, quindi quel `.txt` non può esserne stato ricavato con un estrattore PDF,
e la sua provenienza non è tracciata (contiene inoltre mojibake `â€`, tipico di
un passaggio HTML → cp1252, non di un'estrazione PDF). Va trattato come
**ausilio non verificato**. Il rapporto non si appoggia a quel file: i punti
attribuiti a Palma 2023 sono stati riletti sulle pagine raster p1, p2, p9.
`_extract_pdf.py` è stato scritto proprio per non ripetere l'incidente: non
sovrascrive un estratto esistente con uno vuoto (soglia `MIN_CHARS = 500`,
opzione `--force` per farlo apposta).


## 2. Palma 2023 — che cosa afferma davvero

1. **Le dimensioni dichiarate dell'iscrizione** (p1, nota 1): «approximately six
   hundred forty characters, namely one thousand seven hundred eighty symbols».
   Due conteggi, unità non definite. Le tre stringhe del nostro corpus misurano
   **569 / 584 / 678 caratteri**: compatibili con i ~640 dichiarati (scarto
   ≤ 7%). È una verifica indipendente della provenienza delle stringhe di Palma,
   e va messa a verbale come tale. Il numero **1780 non è usabile**: senza la
   trascrizione originale non si sa che cosa conti (probabilmente anche le
   «many defects and residues» citate nella stessa nota), e statistiche calcolate
   su unità diverse non sono confrontabili. Noi contiamo caratteri.
2. **La tesi centrale** (p1, abstract): «linguistic features converging
   unequivocally to the hypothesis that its clear-text is encrypted by
   monophabetic substitution from a natural language, possibly alongside with
   transposition and polyalphabetism». Ma nello stesso abstract: «A preliminary
   analysis on characters n-grams and vocal-consonants combinations has not
   succeeded yet in individuating any clear-text language among all the analysed
   corpora». Dunque la convergenza riguarda la **forma** (la sostituzione), non
   la **lingua**: che è esattamente la conclusione del nostro rapporto.
3. **Le ipotesi in campo** (p2, §2): Rocco 1928 (tratti artistici e
   architettonici); Miriello 2021 (tesi storico-artistica e araldica, traslazione
   della tomba «on the other side of the very same epigraph's wall», Vlad III);
   l'iscrizione come **traslitterazione latina di un originale greco**;
   l'iscrizione come «nothing else than a **table used by the Franciscan monks**
   for didactic purposes»; datazione radiocarbonica fra XIV e XVI secolo; un
   tentativo di crittanalisi per sostituzione («each glyph by probable phonemes
   referable to similar glyphs in other alphabets»), concluso «without
   satisfactory results»; e Rosenmeyer 2019, dove l'epigrafia cifrata è anche
   potere magico delle lettere e l'enigma è **gioco intellettuale** («the
   enigmographer may want to tease the observer with a riddle, as an intellectual
   game, and not with the real purpose to conceal a message»), «a sort of
   **hoax**», con l'isopsephy (valore numerico 1-900 per lettera greca e
   l'esempio del calcolo 1000 − 700 = 300).
4. **L'argomento di contesto** (p2, §3), il più utile per noi: «the fact itself
   that the artifact is located in plain sight, allows us to imagine that
   whatever information contained therein must not be excessively secret, and is
   required to be unlocked by a group of people possessing the suitable key or a
   sufficient amount of time».
5. **Il metodo** (p2, §4): rassegna di alfabeti e codici storici; analisi
   statistica su caratteri singoli; corpora candidati per lingua; trasposizione
   dei glifi in caratteri latini.
6. **Un difetto di metodo da segnalare** (p9, Appendice, elenco delle funzioni di
   `MaLaNova`): la funzione `generateciocorpus` «creates the input corpus of
   "anagrams" ... by selecting those files whose **Index of Coincidence is most
   similar** to the epigraph's one». I corpora di riferimento sono quindi scelti
   *in funzione* della somiglianza con l'epigrafe: la vicinanza che poi si osserva
   è in parte costruita dalla selezione. Non è un errore fatale — l'IC è un
   filtro legittimo di primo passaggio — ma la tabella per 12 lingue **non è un
   test indipendente**, e va letta come «quali lingue hanno un IC compatibile»,
   non «quali lingue spiegano il testo».
7. **La bibliografia** (p9) è ampia e pertinente, e contiene le voci che contano
   per il nostro problema: Adiego 2006 sul **cariano**; King 2001 su *The Ciphers
   of the Monks* (la **notazione numerica** monastica); Kranz & Oberschelp 2009
   sulla crittografia monastica 1450-1550; Meister 1992 sulla *Geheimschrift*
   diplomatica; Schöning 2014 sulla cancelleria papale; una voce del 2006 sui
   «tetragrammi» greci e slavoni come codice universale; Trithemius, Della Porta,
   Bellaso, Copiale (Knight, Megyesi & Schaefer 2011), Shannon 1951.

## 3. Antal, Marák, Zajac, Lengyelová, Duchoňová — cifrari d'archivio con chiavi conservate

Che cosa documentano (p1-p2):

- Oggetto: documenti cifrati e **chiavi** dei secoli XVIII-XIX di tre famiglie
  aristocratiche (Amadé-Üchtritz, Esterházy, Pálffy-Daun) nell'Archivio Nazionale
  Slovacco di Bratislava; **13 scatole**, contenenti **96 documenti cifrati e 9
  chiavi**; il più antico è del 1711, il più recente del 1834 (p2).
- Il sistema più diffuso è il **nomenclatore**; il repertorio dei segni «consists
  of only numbers ... and markings of numbers»; l'uso delle cifre diventa
  standard fra XVII e XVIII secolo; il nomenclatore può essere usato con o senza
  separatori (**37** documenti con separatore, **59** senza) (p2).
- Stato di conservazione del testo in chiaro (p2): 8 casi con solo il cifrato;
  16 con il chiaro **scritto sopra** le righe cifrate; 38 con il chiaro in un
  documento separato; 14 casi non verificabili.
- **Le chiavi sono conservate solo in due dei tre fondi, e le chiavi conservate
  non corrispondono ai testi conservati**; anche cifrari di altri archivi
  (Austria, Holstein, Sassonia, Ungheria) sono stati confrontati e non
  corrispondono (p2).
- Metodo di trascrizione (p1): digitalizzazione completa e **rilevamento
  automatico dei segni con YOLOv7**, addestrato a tollerare carta rumorosa e
  cifre in trasparenza dal verso del foglio.
- Progetti di riferimento (p1): JCRYPT (Megyesi et al. 2020, 2022, ~3600
  record, in gran parte non pubblici) e HCryptoPortal (Antal & Zajac 2020,
  2022, 764 record, tutti liberamente accessibili).

Che cosa significa per noi, in quattro punti:

1. **Il repertorio dei segni non somiglia al nostro.** Un cifrario reale di quel
   milieu è un nomenclatore **numerico**: cifre e segni di cifra, con o senza
   separatori. L'epigrafe ha 23 classi di glifi misti e nessun livello numerico
   evidente: se è un cifrario dello stesso ambiente, le manca il tratto più
   tipico del genere. È un argomento *contro* l'assimilazione ingenua
   "iscrizione misteriosa = cifrario dell'epoca", non contro la cifratura in sé.
2. **L'assenza di chiave non prova nulla** — ed è la correzione più importante al
   nostro §4.6. In questo corpus, con 9 chiavi conservate su 96 documenti, **le
   chiavi non combaciano con i documenti**. Quindi: (a) trovare una chiave
   "giusta" richiede l'archivio giusto, non una ricerca a tappeto; (b) la mancata
   corrispondenza di `VLAD`/`DRACULA`/`TURBOLO` ecc. con un cifrario periodico
   non falsifica l'ipotesi cifrata, perché la corrispondenza manca anche dove
   entrambi i pezzi esistono. Il nostro null resta un null.
3. **La pratica reale è "cifrato + chiaro archiviato"**, l'opposto del segreto
   assoluto: 16 volte il chiaro è sopra le righe cifrate, 38 volte è in un
   documento separato, e solo 8 volte su 96 il chiaro non c'è. Questo **rafforza**
   l'argomento di Palma (§3: testo in vista ⇒ informazione non segretissima) e
   **toglie forza** all'ipotesi "iscrizione cifrata per nascondere un messaggio":
   chi voleva nascondere aveva un archivio e una chiave, non una lastra esposta.
4. **La loro pipeline presuppone ciò che a noi manca.** YOLOv7 sui manoscritti
   funziona su scansioni ad alta risoluzione di carta; per la pietra abbiamo
   14 px per cella di glifo (sezione 6 del rapporto). Il confronto conferma
   l'ordine di lavoro: prima le immagini, poi la trascrizione, poi le chiavi.

## 4. Layfield et al. 2022 (Voynich) — lo standard metodologico

Che cosa documentano (p1-p2):

- È il **rapporto di una conferenza peer-reviewed** dedicata a un manoscritto
  indecifrato: 32 sottomissioni, 16 accettate, selezione con **3 revisori in
  doppio cieco**, con la possibilità di un secondo giro; obiettivo dichiarato,
  testuale: «to determine if there is a mystery at all, **it may also be a
  hoax**» (p1).
- Keynote (p2): Zandbergen sulla trascrizione (accuratezza delle trascrizioni
  esistenti, nuovi formati, alfabeto di trascrizione con tutte le varianti);
  **Davis sulla paleografia latina applicata al sistema di scrittura Voynich**,
  con i tratti distintivi di **cinque mani** e l'avvertenza che «some symbols may
  be abbreviations or ligatures».
- Sessione prima (p2): **Boxer 2022, "Fingerprinting Gibberish"**, confronto
  quantitativo Voynich vs *Słowa MS 3188*: molte somiglianze quantitative, ma
  anche differenze statistiche sostanziali, e «even if both manuscripts are
  gibberish they do not belong to the same type of gibberish».

Che cosa significa per noi:

1. **La paleografia decide i segni, non la statistica** (Davis). La nostra
   lettura di `ΔΕΔΕΔ` come abbreviazione/monogramma/marchio e non come parola
   (sezione 7.3 del rapporto) ha qui un precedente autorevole e un metodo: si
   stabilisce guardando le mani e le legature, non contando n-grammi.
2. **"Statistiche da non-lingua" non identifica la famiglia del cifrario**
   (Boxer). È la confutazione di un'inferenza che sarebbe facile fare: che una
   sequenza con IC e entropia anomale appartenga a un tipo di cifrario noto.
   Due testi entrambi non-linguistici possono essere di tipi diversi. Quindi il
   nostro «nessuna lingua fra 16» va scritto come esclusione di lingue naturali,
   **non** come identificazione di una tecnica.
3. **"Potrebbe non esserci alcun mistero" è una posizione di metodo**, non una
   facezia: è l'obiettivo dichiarato di un convegno con revisori. L'ipotesi
   beffa/gioco (Rosenmeyer 2019, citata da Palma) va quindi tenuta in alternativa
   seria — e la conseguenza operativa è la stessa: serve la trascrizione
   paleografica.


## 5. Ipotesi: confronto e confutazione

Legenda dell'esito: **confutata** (i dati o i documenti la escludono),
**in tensione** (i dati la rendono difficile ma non impossibile),
**non decidibile** (mancano dati), **rafforzata** (i documenti la rendono più
plausibile senza dimostrarla).

| ipotesi | stato nel rapporto | cosa dicono i documenti | esito |
|---|---|---|---|
| Vlad III / Dracula sepolto qui (Miriello 2021) | sezione 7: verdetto negativo per assenza di dati | Palma p2 cita Miriello come tesi storico-artistica e araldica sulla traslazione della tomba; non porta dati epigrafici | **non decidibile**, e nessuna delle tre fonti la sostiene |
| Preghiera penitenziale ceca | sezione 5: testata, non conclusiva | Palma 2023 non la menziona: parla di latino, greco, traslitterazione, isopsephy. Nessuna traccia nei tre testi | **senza base documentale in Palma 2023**: va attribuita ad altra fonte |
| Tavola didattica dei frati francescani | menzionata, mai testata | Palma p2 la riporta come ipotesi di un autore; la sua bibliografia include King 2001 sulla notazione numerica monastica e Kranz & Oberschelp 2009 sulla crittografia monastica; Antal p2 mostra come è fatto il materiale cifrato "da lavoro" dell'epoca: numerico, con chiave | **plausibile ma non testata**; se i glifi fossero una notazione numerica, i nostri test di lingua sarebbero fuori bersaglio |
| Sostituzione monoalfabetica da una lingua naturale (tesi di Palma) | sezioni 4.2-4.5: 23 classi, IC 0.08-0.11, nessuna lingua fra 16, serve un ~30% di rumore | Palma stesso ammette di non aver individuato la lingua; Antal p2 documenta nomenclatori **numerici**, non alfabeti di 23 glifi | **in tensione** quanto a "lingua naturale"; **non confutata** quanto alla forma "sostituzione" |
| Cifrario con chiave conservata altrove (nostra ricerca in §4.6) | 8 chiavi onomastiche testate, nulla di significativo | Antal p2: 9 chiavi su 96 documenti, **chiavi che non combaciano con i testi**, chiavi in 2 fondi su 3 | il null **non è conclusivo**; cercare chiavi non è il passo successivo |
| Isopsephy / gematria (valori numerici delle lettere) | non testata | Palma p2 (via Rosenmeyer): valori 1-900, esempio 1000 − 700 = 300 | **non decidibile** senza la mappatura glifo→lettera, che non abbiamo |
| Beffa, gioco intellettuale, "nessun mistero" | sezione 7.3 (segno non lessicale) e sezione 8 | Palma p2 (Rosenmeyer: «a sort of hoax»); Layfield et al. p1 («it may also be a hoax») e p2 (Boxer: due gibberish non sono dello stesso tipo) | **rafforzata** come alternativa legittima, non dimostrata |
| "Somiglianza statistica ⇒ stesso tipo di cifrario" | rischio presente nelle sezioni 4.5 e 4.8 | Boxer 2022: somiglianze quantitative fra due testi non-linguistici, ma differenze statistiche sostanziali | **confutata come inferenza**: non va usata |

## 6. Che cosa cambia nel rapporto

- **§2 Fonti**: i tre PDF entrano come fonti secondarie con il loro stato
  documentale (scansioni a 150 ppi, senza livello di testo) e con il rimando a
  questo atto.
- **§4.9 (nuova sottosezione)**: sintesi dei tre confronti e delle due
  confutazioni che ne derivano (chiavi che non combaciano ⇒ il nostro null non è
  conclusivo; gibberish ≠ un solo tipo di cifrario ⇒ non si identifica la
  tecnica). La numerazione dei capitoli non cambia: 4.8 resta la PCA, 7 Dracula,
  8 Limiti, 9 Riproducibilità, 10 Riferimenti.
- **§9 Riproducibilità**: `_extract_pdf.py` e `_pdf_pages.py` entrano fra gli
  strumenti; `report/atti/manifest.json` e questo documento entrano fra gli
  artefatti; l'estratto `palma_histocrypt2023.txt` è dichiarato **non
  riproducibile** dai PDF agli atti.
- **§10 Riferimenti**: aggiunte le due voci nuove (Antal et al.; Layfield et al.)
  più King 2001 e Rosenmeyer 2019 già presenti.

## 7. Limiti di questo atto

- **Pagine lette, non documenti letti.** Le affermazioni della sezione 2-4 si
  riferiscono alle pagine elencate nella sezione 1.3; il resto è agli atti ma non
  letto. Un giudizio sul complesso dei tre lavori richiederebbe le pagine
  rimanenti (24 su 28) e, per Palma, la tesi e il dataset `MaLaNova`.
- **Citazioni da raster a 150 ppi.** I virgolettati sono stati trascritti a
  vista: errori sui singoli caratteri sono possibili, il senso no. Per una
  citazione formale serve la versione Tipografica/HTML dei saggi.
- **Nessun OCR.** Non è stato possibile indicizzare i tre PDF, quindi non è
  escluso che contengano affermazioni rilevanti in pagine non lette (per esempio
  sui simboli o sulla datazione).
- **Antal et al. riguarda la carta, non la pietra.** Il corpus è di documenti
  diplomatici su carta, con chiavi; le conclusioni sul repertorio numerico e
  sulla sorte delle chiavi valgono per quel corpus, non per l'epigrafia.
- **Layfield et al. è un rapporto di conferenza**, non un articolo di ricerca:
  vale come indicazione di metodo (revisione, paleografia, "hoax") e come
  rassegna, non come risultato.
- **Il dato "le chiavi non combaciano"** viene da un solo fondo archivistico
  (13 scatole, 96 documenti): è un fatto locale, non una legge.
