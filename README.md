# Santa Maria la Nova: Reproducible Epigraph Cryptanalysis & Hypothesis Stress-Test

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](https://www.python.org/)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/studioanthosalba/santa-maria-la-nova-cryptanalysis/blob/main/Santa_Maria_La_Nova_Interactive.ipynb)
[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.pending-blue)](https://zenodo.org)
[![Author: Antonino Magazzù](https://img.shields.io/badge/Author-Antonino%20Magazzù-orange.svg)](#author)

> **Author:** Antonino Magazzù (*Independent Researcher*)  
> **Official Papers (PDF):**  
> 📄 [Italian Full Report & Divulgative Summary](Santa_Maria_La_Nova_Studio_Completo.pdf)  
> 📄 [English Academic Manuscript (IMRaD)](Santa_Maria_La_Nova_Cryptanalysis_EN.pdf)

---

## 🏛️ Project Overview

This repository provides the complete, deterministic, and 100% reproducible computational pipeline for the cryptanalytic and paleographic investigation of the late Renaissance encrypted inscription in the **Turbolo Chapel** of the **Santa Maria la Nova monumental complex (Naples, Italy)**.

The inscription (comprising ~600 glyphs in an anomalous, unclassified script) has repeatedly been connected by popular accounts and recent publications (Palma, *HistoCrypt 2023*) to the secret tomb of **Vlad III of Wallachia (Vlad Țepeș, "Dracula")**.

### 🔍 Core Findings (TL;DR)
1. **The inscription is non-random:** The Index of Coincidence ($IC$) diverges between 38 and 146 standard deviations from uniform randomness ($p < 10^{-12}$). A deliberate system exists.
2. **The documentary breakdown:** When comparing published transcriptions (`palma_A` and `palma_B`), the longest identical substring is **only 4 to 5 consecutive characters out of 600**. Scholars have been analyzing disparate, unaligned extraction artifacts.
3. **Refutation of the Dracula claim:** The hypothesis of an "Old Czech prayer containing Dracula's name" was calculated against a misidentified 15th-century Hungarian codex (*Munich Codex*, 1466) with encoding bugs. Onomastic cribs (`VLAD`, `DRACULA`) do not exceed random noise ($p \in [0.085, 0.960]$).
4. **The role of AI (`gemini_full`):** Multimodal AI vision on low-resolution imagery regularized ambiguity by merging glyph variants ($A/\Lambda/\forall$, $E/\epsilon/\Sigma$), creating an artificial jump in the Index of Coincidence ($IC = 0.1147$) and proving that photographic resolution is the ultimate barrier.
5. **The scientific verdict:** The impasse is documentary, not cryptanalytic. Key searches must be suspended until high-resolution in situ 3D laser photogrammetry and an open diplomatic transcription are produced.

---

## ⚡ 1-Click Interactive Execution (Google Colab)

To reproduce all 7 analytical phases directly in your browser without installing anything on your computer, click the button below:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/studioanthosalba/santa-maria-la-nova-cryptanalysis/blob/main/Santa_Maria_La_Nova_Interactive.ipynb)

---

## 💻 Local Installation & Reproduction

### Prerequisites
- Python 3.10 or higher.
- Standard library only (`requests` optional for downloading external corpora).

```bash
# 1. Clone repository
git clone https://github.com/studioanthosalba/santa-maria-la-nova-cryptanalysis.git
cd santa-maria-la-nova-cryptanalysis

# 2. Run the deterministic 7-phase pipeline (~7 minutes total)
python scripts/00_corpus.py         # Phase 0: Corpus canonization & sequence alignment
python scripts/01_descriptive.py     # Phase 1a: Descriptive statistics (IC, Entropy, n-grams)
python scripts/02_inferential.py     # Phase 1b: Inferential tests (16 languages, C3 vowels)
python scripts/03_attacks.py         # Phase 2: Hill-climbing solver & onomastic cribs
python scripts/04_predictive.py      # Phase 3: Bayesian noise model & Bayes factors
python scripts/05_pca.py             # Phase 1c: 28-descriptor PCA refutation
python scripts/06_report.py          # Summary: Deterministic report generation
```

Every number reported in the scientific manuscripts is deterministically generated from verified JSON summaries in `corpus/`—no figure is estimated by hand.

---

## 📁 Repository Structure

```text
├── Santa_Maria_La_Nova_Studio_Completo.pdf  <- Italian Master Publication PDF
├── Santa_Maria_La_Nova_Cryptanalysis_EN.pdf <- English Academic Manuscript PDF
├── manuscript_IMRaD.md                     <- IMRaD Source Text (Italian)
├── manuscript_IMRaD_EN.md                  <- IMRaD Source Text (English)
├── stress_test_ipotesi_elenchos.md          <- 12-Lens Epistemological Stress-Test
├── Santa_Maria_La_Nova_Interactive.ipynb    <- Interactive Google Colab Notebook
├── CITATION.cff                            <- Standard Citation Format
├── .zenodo.json                            <- CERN Zenodo Metadata Integration
├── LICENSE                                 <- MIT (Code) & CC-BY 4.0 (Data/Papers)
├── scripts/                                <- 7-Phase Python analytical pipeline
├── corpus/                                 <- Processed matrices, JSON data & markdown summaries
├── report/                                 <- Technical logs, manifests, and documentation
└── drac1.jpeg, drac2.webp, drac2.jpg       <- Photographic documentation of the plaque
```

---

## 📖 Citation

If you use this dataset, computational pipeline, or findings in academic research, please cite:

```bibtex
@software{magazzu2026santamaria,
  author = {Magazzù, Antonino},
  title = {The Encrypted Epigraph of Santa Maria la Nova: Reproducible Cryptanalysis and Quantitative Falsification of the Vlad III Hypothesis},
  year = {2026},
  url = {https://github.com/antoninomagazzu/santa-maria-la-nova-cryptanalysis},
  version = {1.0.0}
}
```

---

## ⚖️ License
- **Code:** [MIT License](LICENSE)
- **Data & Manuscripts:** Creative Commons Attribution 4.0 International ([CC BY 4.0](https://creativecommons.org/licenses/by/4.0/))  
© 2026 Antonino Magazzù. All rights reserved.
