# GUIDA PRATICA OPEN SCIENCE: COME RENDERE DISPONIBILE IL CODICE COMPUTAZIONALE PYTHON

**Autore:** Antonino Magazzù  
**Progetto:** Crittanalisi Riproducibile dell'Epigrafe di Santa Maria la Nova  
**Obiettivo:** Ottenere un DOI accademico permanente, garantire la riproducibilità totale e permettere ai revisori e al pubblico di eseguire il codice con un click.

---

## 1. IL GOLD STANDARD ACCADEMICO: GITHUB + ZENODO (Con DOI Permanente)

Le riviste scientifiche internazionali di fascia alta (*Cryptologia*, *Digital Scholarship in the Humanities*, *Springer Nature*) richiedono nel paragrafo **Data & Code Availability** un link a un repository permanente dotato di **DOI (Digital Object Identifier)**.

### Come configurarlo in 5 minuti:
1. **Crea un Repository GitHub Pubblico:**
   - Nome consigliato: `santa-maria-la-nova-cryptanalysis`
   - Carica l'intera struttura del progetto:
     ```text
     scripts/       <- I file da 00_corpus.py a 06_report.py
     corpus/        <- I file JSON e markdown con tutti i dati
     report/        <- I report e la documentazione agli atti
     README.md      <- Istruzioni chiare di esecuzione
     requirements.txt
     LICENSE        <- Consigliata: MIT License (per il codice) o CC-BY 4.0 (per i dati)
     ```
2. **Collega GitHub a Zenodo (CERN / OpenAIRE):**
   - Vai su [zenodo.org](https://zenodo.org/) (l'archivio Open Science gestito dal CERN e finanziato dalla Commissione Europea).
   - Accedi cliccando su **"Log in with GitHub"**.
   - Vai nella sezione **GitHub** del tuo profilo Zenodo e attiva l'interruttore sul tuo repository `santa-maria-la-nova-cryptanalysis`.
3. **Genera il DOI con una Release:**
   - Su GitHub, clicca su **"Create a new release"** (es. Tag: `v1.0.0`, Titolo: *First Scientific Release - Santa Maria la Nova Epigraph Analysis*).
   - Istantaneamente, Zenodo "congela" lo snapshot del codice, genera un archivio permanente e ti assegna un **DOI ufficiale** (es. `10.5281/zenodo.10892341`).
4. **Inserisci il DOI nel Paper:**
   - Nel tuo manoscritto IMRaD, nella sezione *Data & Code Availability Statement*, scriverai:
     > *"All analytical code, data matrices, and cryptographic logs are openly accessible on Zenodo under DOI: 10.5281/zenodo.XXXXXXX."*

---

## 2. ESECUZIONE INTERATTIVA CON 1 CLICK: GOOGLE COLAB

Per permettere a chiunque (revisori, colleghi o appassionati) di **verificare i risultati senza installare nulla sul proprio computer**:

1. Crea un notebook Jupyter (`Santa_Maria_La_Nova_Interactive.ipynb`) che clona il tuo repo GitHub ed esegue le fasi della pipeline:
   ```python
   !git clone https://github.com/tuo-username/santa-maria-la-nova-cryptanalysis.git
   %cd santa-maria-la-nova-cryptanalysis
   !python scripts/00_corpus.py
   !python scripts/01_descriptive.py
   !python scripts/02_inferential.py
   ```
2. Inserisci in cima al tuo `README.md` di GitHub il badge ufficiale di Google Colab:
   ```markdown
   [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tuo-username/santa-maria-la-nova-cryptanalysis/blob/main/Santa_Maria_La_Nova_Interactive.ipynb)
   ```
3. Chiunque clicchi sul pulsante aprirà una macchina virtuale gratuita Google nel proprio browser ed eseguirà la pipeline in tempo reale.

---

## 3. OPEN SCIENCE FRAMEWORK (OSF.IO)

In alternativa o in aggiunta a Zenodo, puoi usare [OSF (Open Science Framework)](https://osf.io/):
- Piattaforma pensata specificamente per la ricerca umanistica e computazionale indipendente.
- Permette di registrare un progetto (*Preregistration*), caricare codice e allegati di grandi dimensioni (anche immagini e modelli 3D) e genera anch'essa un DOI citable.

---

## 4. CHECKLIST FINALE PRIMA DELLA PUBBLICAZIONE

- [ ] File `requirements.txt` pulito (nel nostro caso basta Python standard e `requests`).
- [ ] File `README.md` con la sezione *"How to reproduce"* (il comando `python scripts/00_corpus.py ...`).
- [ ] Registro delle impronte crittografiche SHA256 dei file per dimostrare l'integrità dei dati (già presente in `report/atti/manifest.json`).
- [ ] Licenza open source chiara (MIT per codice, CC-BY per testo e tabelle).
