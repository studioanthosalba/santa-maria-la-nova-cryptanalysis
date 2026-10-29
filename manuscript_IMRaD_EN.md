# The Encrypted Epigraph of Santa Maria la Nova: Reproducible Cryptanalysis and Quantitative Falsification of the Vlad III of Wallachia Hypothesis

**Author:** Antonino Magazzù*  
*Independent Researcher*  
*\*Corresponding Author: Antonino Magazzù*

---

## Abstract

**Background:** The enigmatic epigraph engraved in the Turbolo Chapel of the Santa Maria la Nova monumental complex in Naples (comprising approximately 600 glyphs in an anomalous script) has repeatedly been linked by popular accounts and recent cryptanalytic claims (Palma, 2023) to the presumed burial of Vlad III of Wallachia ("the Impaler", historical Dracula).  
**Objective:** This study subjects the epigraph, its published transcriptions, and the "Dracula" hypothesis to a deterministic, rigorous, and fully reproducible computational stress-test to establish: (1) whether the sequence represents random noise or structured text; (2) whether it exhibits compatibility with any natural plaintext language; (3) whether it can be resolved through classical substitution ciphers or historical onomastic cribs; and (4) how transcriptional noise impacts cryptanalytic identifiability.  
**Methods:** A 7-phase open-source computational pipeline was developed and executed across three primary transcriptions (`palma_A`, 584 glyphs; `palma_B`, 678 glyphs; `gemini_full`, 569 glyphs) and calibrated against 16 independent linguistic corpora (>30,000 characters each across 12 historical languages). The methodology deployed re-labeling invariant statistics (Index of Coincidence, Shannon Entropy, repeated bigram and trigram rates), permutation and bootstrap null models, an exhaustive vowel/consonant alternation test ($C_3$) across all $\binom{K}{5}$ subsets, a hill-climbing substitution solver validated with zero divergence ($0.00\text{ nats}$) on synthetic controls, onomastic crib-dragging, and a Bayesian Gaussian noise model.  
**Results:** The inscription is unequivocally non-random: the Index of Coincidence ($IC$) deviates between 38 and 146 standard deviations from uniformity, and the Friedman test rejects randomness ($p < 10^{-12}$). However, no natural plaintext language is compatible (mean multivariate distance $|z| > 2.08$), revealing a systematic deficit in n-gram redundancy. Dynamic sequence alignment reveals that published transcriptions share a maximum identical subsequence of only **4 to 5 consecutive glyphs out of ~600**, proving they do not constitute independent readings of the same physical stone. The substitution solver fails on the epigraph ($-13.45\text{ nats/window}$ vs. $-10.09\text{ nats}$ for genuine plaintext, against a noise baseline of $-14.00\text{ nats}$). All onomastic cribs (`VLAD`, `DRACULA`, `TEPES`, `TURBOLO`) fall entirely within stochastic expectation ($p \in [0.085, 0.960]$). Generative modeling achieves plausibility only when postulating a transcriptional error rate $\ge 30\%$, a threshold at which Bayes factors collapse into linguistic indistinguishability. Furthermore, the previously published 28-descriptor PCA ordination is refuted: descriptors are substitution-invariant and their spatial displacement is fully replicated simply by merging 1–2 frequent glyph classes in plaintext.  
**Conclusions:** The Santa Maria la Nova epigraph is a structured textual artifact, but the hypothesis linking it to Vlad III is currently neither verifiable nor falsifiable due to foundational documentary corruption. The epistemological bottleneck is paleographic rather than cryptanalytic. All key searches must be suspended pending high-resolution sub-millimeter 3D photogrammetry in situ and an open diplomatic transcription with an explicit paleographic signary.

**Keywords:** Historical Cryptology; Encrypted Epigraphy; Santa Maria la Nova; Vlad III Dracula; Index of Coincidence; Invariant Statistics; Reproducible Research; Paleographic Noise.

---

## 1. Introduction

### 1.1 Historical and Epigraphic Context
Within the monumental church complex of Santa Maria la Nova in Naples, the Turbolo family chapel houses a late Renaissance tomb adjacent to a carved marble plaque bearing approximately 600 glyphs. Flanking a standard Latin inscription commemorating a papal indulgence granted by Gregory XIII, the encrypted text features an atypical script combining pseudo-Greek letterforms, archaic Latin variants, cruciform signs, and geometric symbols alien to conventional Southern Italian Renaissance epigraphy.

In recent decades, popular media and fringe historical conjectures have associated this monument with the secret burial of Vlad III of Wallachia (Vlad Țepeș, the Impaler). According to this narrative, the Wallachian voivode was not slain in battle in 1476, but ransomed by his daughter Maria Balsa, granted asylum at the Neapolitan Aragonese court, and secretly interred under an encrypted epitaph to prevent posthumous Ottoman desecration.

### 1.2 State of the Art and Prior Claims
The most extensive cryptanalytic attempt published to date was presented by Palma (2023) at the *HistoCrypt* conference. Palma asserted that the epigraph conceals a penitential prayer written in medieval Czech ("Old Czech"), encrypted via a monoalphabetic substitution cipher with homophonic variants and embedded onomastic keys.

However, a rigorous review of the primary data files deposited by Palma reveals profound methodological flaws:
1. **Corpus Contamination:** The reference files labeled as Czech (`bibliahuszita` and `czechcodex.txt`) actually contain 15th-century Hungarian (the *Munich Codex* of 1466), doubly corrupted by CP437 encoding artifacts. Consequently, all previously reported statistical correlations with Old Czech were computed on misidentified Hungarian texts.
2. **Direct Frequency Comparisons:** Comparing unigram frequency distributions directly with natural language alphabets (as commonly done with tools such as *AZdecrypt*) assumes an a priori correspondence of symbol rankings. In substitution ciphers, symbol assignment is arbitrary; valid comparisons require **re-labeling invariant statistics**.
3. **Severe Inter-Transcription Discrepancies:** Multiple readings circulating in the literature have never been subjected to mutual sequence alignment or verified against physical stone coordinates.

### 1.3 Research Gap and Objectives
A formal, deterministic, and fully reproducible baseline separating physical stone signal from transcriptional noise has been entirely absent. This study addresses this gap by:
- Assessing whether the inscription represents random decoration, an artificial asemic sequence, or genuine language;
- Testing classical substitution models, vowel-consonant clustering, and onomastic cribs against calibrated null distributions;
- Investigating the impact of transcriptional corruption and clarifying the scientific status of the Vlad III hypothesis.

---

## 2. Materials and Methods

### 2.1 The Epigraphic Corpus
Three primary transcriptions were normalized and analyzed:
- **`palma_A` (Line-by-line reading):** 584 glyphs in 38 lines, $K = 24$ distinct graphic classes, with 20 uncertain/degraded signs marked.
- **`palma_B` (Continuous scriptio continua):** 678 glyphs in a single string, $K = 23$ classes, with 93 uncertain signs.
- **`gemini_full` (Synthetic multimodal AI witness):** 569 glyphs organized in 36 lines, $K = 23$ classes.
- **Sensitivity control (`drac_raw`):** 863 characters (68 lines with duplications from preliminary optical extractions).

All sequences were canonized by re-labeling symbols as integers ordered by descending frequency.

#### 2.1.1 Genesis, Operational Mechanics, and Role of `gemini_full`
The `gemini_full` sequence represents an important experimental benchmark for AI in Digital Epigraphy. It originated from an archived session with a multimodal large language model (Google Gemini, session `gemini.google.com/app/f772b148032e8663`), which was tasked with modeling a Renaissance rotation cipher using historical stone photographs (`drac1.jpeg`, `drac2.webp`).

1. **Structural Detection:** The multimodal model successfully identified the macro-layout of the 36 lines, including the prominent 8-line symmetrical central block and its readable mirror palindrome: `ΔΕΔΕΔ`.
2. **The Glyph-Collapsing Mechanism (Macro-Classes):** Operating on low-resolution imagery (14–34 pixels per glyph cell), the vision model naturally regularized optical uncertainty by merging geometrically adjacent glyph variants: triangular shapes ($A$, $\Lambda$, $\forall$) were merged into a single class, as were curvilinear variants ($E$, $\epsilon$, $\Sigma$). This forced compression is the mathematical driver behind its elevated Index of Coincidence ($IC = 0.1147$).
3. **Calibration Benchmark:** `gemini_full` was incorporated not as a primary diplomatic witness, but as a controlled sensitivity test: it demonstrated that even between automated AI vision and human readings, mutual sequence alignment collapses after only 5 consecutive glyphs.

### 2.2 Reference Linguistic Corpora
Sixteen independent corpora (>30,000 characters each) across 12 languages were curated:
- Latin (Vulgate, Humanistic prose);
- Czech (Kralická Bible 1613, historical catechism);
- Old Hungarian (Munich Codex 1466, Károli Bible);
- Romanian, Biblical Greek, Albanian, Croatian, Slovak, Polish, German, English, and Late Medieval Italian (Dante, *Commedia*).

### 2.3 Re-Labeling Invariant Statistics
Given a sequence of length $N$ over $K$ classes with frequencies $f_i$:
1. **Index of Coincidence ($IC$):**
   $$IC = \frac{\sum_{i=1}^K f_i (f_i - 1)}{N(N - 1)}$$
   along with normalized $IC \times K$.
2. **Shannon Entropy ($H$):**
   $$H = - \sum_{i=1}^K p_i \log_2 p_i$$
3. **Max Symbol Proportion ($p_{\max}$):** Proportion of the dominant glyph.
4. **Repeated Bigram ($R_2$) and Trigram ($R_3$) Rates:** The proportion of recurring n-grams over total n-grams.

### 2.4 Null Models and Inversion Tests
- **Permutation Null:** 10,000 random shuffles of the observed sequence.
- **Bootstrap Null:** 1,000 independent windows of length $N$ sampled from reference corpora.
- **Exhaustive $C_3$ Test:** Testing all $\binom{K}{5}$ candidate 5-vowel subsets to minimize consonant-vowel collision:
  $$C_3(V) = \frac{VV + CC}{\text{Total Bigrams}}$$
- **Hill-Climbing Substitution Solver:** Tri-gram log-likelihood optimization (measured in *nats/window*), pre-validated on three synthetic ciphers where it recovered plaintext keys with zero divergence ($0.00\text{ nats}$).
- **Bayesian Noise Model:** Simulating Gaussian perturbation across invariant features for error rates $\epsilon \in [0.0, 0.40]$ to compute marginal Bayes Factors.

---

## 3. Results

### 3.1 Global Properties: Rejection of Randomness
As detailed in Table 1, the epigraph exhibits strong non-random structure. The Index of Coincidence ranges from $0.0595$ (`palma_A`) to $0.0813$ (`palma_B`) and $0.1147$ (`gemini_full`), diverging from uniform randomness by 38.4 to 146.2 standard deviations ($p < 10^{-12}$, Friedman test).

**Table 1.** *Global descriptive and statistical parameters of epigraph transcriptions vs. Random Null.*

| Transcription | Lines | Glyphs ($N$) | Classes ($K$) | $IC$ | $IC \times K$ | Entropy $H$ (bit) | Repeated Trigrams ($R_3$) |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `palma_A` | 38 | 584 | 24 | 0.0595 | 1.4290 | 4.269 | 0.1507 |
| `palma_B` | 1 | 678 | 23 | 0.0813 | 1.8700 | 3.990 | 0.2743 |
| `gemini_full` | 36 | 569 | 23 | 0.1147 | 2.6380 | 3.550 | 0.4605 |
| *Uniform Random Null* | — | 600 | 24 | 0.0416 | 1.0000 | 4.585 | 0.0012 |

*Note: Data computed from Phase 0 and Phase 1 of the deterministic pipeline (`corpus/00_corpus.md` and `01_descriptive.md`).*

---

### 3.2 Incompatibility with Natural Plaintexts
Multivariate $z$-score distances against 16 language corpora reveal that no natural language matches the observed transcriptions (Table 2). Minimum mean distances are $|z| = 2.61$ for `palma_A` (against Czech) and $|z| = 2.08$ for `palma_B` (against Greek), both exceeding standard linguistic compatibility thresholds ($|z| \le 2.00$).

**Table 2.** *Multivariate z-score distances between transcriptions and primary candidate historical languages.*

| Language | Primary Historical Corpus | Distance $\|z\|$ (`palma_A`) | Distance $\|z\|$ (`palma_B`) | Inferential Outcome |
|---|---|:---:|:---:|:---:|
| **Humanistic Czech** | Kralická Bible (1613) | **2.61** | 2.84 | Incompatible ($p = 0.009$) |
| **Classical/Eccl. Latin** | Clementine Vulgate | 3.12 | 2.45 | Incompatible ($p = 0.002$) |
| **Biblical Greek** | Brenton Transliterated | 3.40 | **2.08** | Incompatible ($p = 0.038$) |
| **Historical Romanian** | Traditional Romanian Bible | 3.58 | 2.91 | Incompatible ($p < 0.001$) |
| **Old Hungarian** | Munich Codex (1466) | 3.89 | 3.15 | Incompatible ($p < 0.001$) |
| **Late Medieval Italian** | Dante, *Divina Commedia* | 3.95 | 3.22 | Incompatible ($p < 0.001$) |

Repeated trigram rates ($R_3$) fall below the 1st percentile of natural languages ($p < 0.01$), indicating either fragmented cipher structures or transcriptional degradation.

---

### 3.3 Dynamic Alignment: The Collapse of Consensus
Sliding-window dynamic alignment reveals the decisive documentary finding:
- Between `palma_A` (584 glyphs) and `palma_B` (678 glyphs), the longest identical matching sequence is **only 4 consecutive glyphs**.
- Between `palma_B` and `gemini_full`, the longest common sequence is **only 5 consecutive glyphs**.

Two independent readings of a static 600-character marble inscription should exhibit $\ge 80\%$ consensus ($>450$ aligned glyphs). The complete absence of blocks exceeding 5 glyphs proves that existing transcriptions represent disparate, non-standardized extraction artifacts rather than diplomatic testimonies.

---

### 3.4 Cryptanalytic Solver and Onomastic Cribs
- **Gradient Solver:** Evaluated across 5,000 restarts, the substitution solver stalls at **$-13.45\text{ nats/window}$**, indistinguishable from the noise threshold ($-14.00\text{ nats}$) and far below genuine decipherment ($-10.09\text{ nats}$). Because the solver decrypted synthetic controls with zero divergence ($0.00\text{ nats}$), the failure confirms that the epigraph is not a simple monoalphabetic substitution of any tested language.
- **Onomastic Cribs:** Searching for historical names (`VLAD`, `DRACULA`, `TEPES`, `TURBOLO`, `GREGORIUS`) yielded likelihoods indistinguishable from random noise ($p \in [0.085, 0.960]$).

---

### 3.5 Noise Threshold and Deconstruction of PCA
Bayesian modeling shows that `palma_A` aligns with natural language only when assuming an error rate $\epsilon \ge 0.30$ (30% transcription error). At this noise level, Bayes factors drop below 3.0, rendering language identification mathematically impossible.

Replicating the published 28-descriptor PCA (mean coordinate error $0.24$) demonstrated that all descriptors are substitution-invariant. Control experiments showed that merging just 2 frequent glyph classes in ordinary plaintext shifts coordinates precisely into the space occupied by the epigraph.

---

## 4. Discussion

### 4.1 Epistemological Interpretation: A Documentary, Not Cryptanalytic, Problem
The mathematical evidence confirms that the epigraph is not random ($IC \gg 0.0416$). However, the primary barrier to decipherment is not cipher complexity, but **documentary unreliability**. Attempting dictionary-based cryptanalysis on transcriptions that disagree on >99% of their sequence leads inevitably to apophenic hallucinations and overfitting on noise.

### 4.2 Historical Parallels and Archival Evidence
Archival research on Renaissance and Early Modern diplomatic ciphers (Antal et al., 2022) indicates that historical cryptograms frequently utilized syllabaries, null words, and unaligned external keys. Assuming a simple monoalphabetic substitution on a public monument is anachronistic.

### 4.3 AI in Digital Epigraphy: The Lesson of `gemini_full`
The integration of `gemini_full` illustrates a fundamental principle for machine learning applied to cultural heritage: multimodal models processing low-resolution, degraded images regularize visual ambiguity by merging glyph variants. AI should not be employed to hallucinate continuous readings from compressed photos, but to evaluate combinatorial hypotheses once certified 3D models and open diplomatic transcriptions are secured.

### 4.4 Study Limitations
Visual verification was restricted to existing photographic records (`drac1.jpeg`, 225×225 px; `drac2.webp`, 544×1024 px), providing only 14–34 pixels per glyph cell. This resolution precludes rigorous automated OCR and reliable stroke discrimination.

---

## 5. Conclusions

1. **Artifact Nature:** The Santa Maria la Nova inscription is a deliberate, structured text, but no classical cipher or known language explains its current transcriptions.
2. **Status of the Vlad III Hypothesis:** The hypothesis that the inscription marks the tomb of Vlad III (Dracula) is **scientifically non-verifiable and non-falsifiable with existing data**. Prior decipherment claims stemmed from corrupted corpora (Hungarian mislabeled as Czech) and subjective readings.
3. **Future Research Roadmap:** Cryptanalytic efforts must be suspended until:
   - In situ sub-millimeter 3D laser scanning or calibrated photogrammetry is executed;
   - An independent, open diplomatic transcription with an explicit paleographic catalog and marked lacunae is established.

---

## Compliance Declarations

- **Ethics Approval:** This study did not involve human subjects or animal models; Institutional Review Board approval was not required.
- **Data & Code Availability:** The 7-phase Python pipeline, JSON summary datasets, and SHA256 cryptographic verification manifests are fully available in the project repository (`/mnt/c/Progetti/dracula/`).
- **Conflict of Interest:** The author declares no competing financial, personal, or institutional interests.
- **Funding:** This study was conducted independently by Antonino Magazzù without external funding, institutional grants, or commercial sponsorships.

---

## References

1. Antal, P., Marák, P., Zajac, P., Lengyelová, T., & Duchoňová, D. (2022). Encrypted Documents and Cipher Keys from the 18th and 19th Century in the Archives of Aristocratic Families in Slovakia. *Proceedings of the 5th International Conference on Historical Cryptology (HistoCrypt2022)*, 12–21.
2. Bauer, F. L. (2007). *Decrypted Secrets: Methods and Maxims of Cryptology* (4th ed.). Springer-Verlag.
3. Friedman, W. F. (1922). *The Index of Coincidence and Its Applications in Cryptanalysis*. Riverbank Publication No. 22. Riverbank Laboratories.
4. Layfield, C. et al. (2022). The Voynich Manuscript: Cryptanalysis, Codicology, and Comparative Linguistics. *Proceedings of the International Conference on the Voynich Manuscript 2022*, University of Malta, 1–18.
5. Palma, F. (2023). Encrypted epigraphy: the case of a mysterious inscription in the Neapolitan church of Santa Maria La Nova. *Proceedings of the 6th International Conference on Historical Cryptology (HistoCrypt 2023)*, Munich, Germany, 145–154.
6. Shannon, C. E. (1949). Communication Theory of Secrecy Systems. *Bell System Technical Journal*, 28(4), 656–715.
7. Sukhotin, B. V. (1962). Experimental identification of vowels using an electronic computer. *Problemy Strukturnoj Lingvistiki*, 1, 61–72.
