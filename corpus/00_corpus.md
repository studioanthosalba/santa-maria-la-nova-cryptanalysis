# Phase 0 -- canonical corpus of the Santa Maria la Nova epigraph

## 3.1 Transcription inventory

| key | lines | symbols | letters | gaps | #glyphs | IC | ICx26 | H | tokens |
|---|---|---|---|---|---|---|---|---|---|
| palma_A | 38 | 604 | 584 | 20 | 24 | 0.0595 | 1.5479 | 4.2690 | 123 |
| palma_A2 | 19 | 366 | 357 | 9 | 24 | 0.0567 | 1.4754 | 4.2810 | 63 |
| palma_A_nosp | 1 | 604 | 584 | 20 | 24 | 0.0595 | 1.5479 | 4.2690 | 27 |
| palma_B | 1 | 771 | 678 | 93 | 23 | 0.0813 | 2.1142 | 3.9900 | 1 |
| palma_C | 1 | 855 | 681 | 174 | 17 | 0.0941 | 2.4475 | 3.6730 | 1 |
| palma_B2 | 1 | 862 | 678 | 184 | 24 | 0.0806 | 2.0959 | 4.0250 | 1 |
| palma_B3 | 3 | 730 | 641 | 89 | 24 | 0.0797 | 2.0723 | 4.0340 | 3 |
| palma_B4 | 52 | 589 | 589 | 0 | 24 | 0.0779 | 2.0267 | 4.0430 | 52 |
| palma_C_nq | 1 | 681 | 681 | 0 | 17 | 0.0941 | 2.4475 | 3.6730 | 1 |
| gemini_full | 36 | 569 | 569 | 0 | 23 | 0.1147 | 2.9820 | 3.5500 | 124 |
| gemini_central | 8 | 164 | 164 | 0 | 18 | 0.1096 | 2.8498 | 3.4680 | 27 |
| gemini_central_in_full | 8 | 165 | 165 | 0 | 17 | 0.1091 | 2.8364 | 3.4560 | 27 |
| drac_raw | 68 | 863 | 863 | 0 | 24 | 0.1048 | 2.7249 | 3.7450 | 201 |

Provenance:
- **palma_A** -- repo:stringaoriginale.txt -- Palma 2023, arbitrary Latin-letter transliteration with word gaps ('.'=separator, '?'=illegible)
- **palma_A2** -- repo:stringaoriginale2.txt -- Palma 2023, subset of palma_A (rows kept for the AZdecrypt run)
- **palma_A_nosp** -- repo:stringanospaces.txt -- Palma 2023, same as palma_A without spaces (scriptio continua)
- **palma_B** -- repo:soluzione.txt -- Palma 2023, final glyph string in Greek letter labels
- **palma_C** -- repo:scriptiocontinua.txt -- Palma 2023, 17-class merged variant with gaps
- **palma_B2** -- repo:scriptiocontinua2.txt -- Palma 2023, filled Latin-letter variant (same letter count as palma_B)
- **palma_B3** -- repo:scriptiocontinua3.txt -- Palma 2023, shortened filled variant
- **palma_B4** -- repo:scriptiocontinua4.txt -- Palma 2023, filled variant split one chunk per line
- **palma_C_nq** -- repo:scriptiocontinuanoq.txt -- Palma 2023, 17-class merged variant, gaps removed
- **gemini_full** -- Gemini log (dracula_epigrafe.md), 33-line transcription embedded in testo_epigrafe_completo; the archived conversation describes it as a simulation of the slab's rows (not an independent transcription), so it is used here as a comparison term only
- **gemini_central** -- Gemini log, standalone 8-line central block (declared simulation)
- **gemini_central_in_full** -- Gemini log, central 8 lines inside the 33-line transcription (declared simulation)
- **drac_raw** -- epigrafe drac.md -- degraded/OCR-like reading

Note: `ICx26` is Palma's normalised IC (cf. his Table 1, value 1.72 for the inscription).

## 3.2 Pairwise alignment after frequency-rank relabeling

Transcriptions of the same slab use unrelated label alphabets, so a naive alignment scores 2% identity by construction.  Each pair is therefore compared after mapping the k-th most frequent symbol of reading A onto the k-th most frequent symbol of reading B (a substitution preserves the frequency order); the residual mismatches are then real disagreements.

| pair | len A | len B | columns | identity | chance | score |
|---|---|---|---|---|---|---|
| palma_A ~ palma_B | 604 | 771 | 835 | 0.3006 | 0.0656 | -333.0000 |
| palma_A ~ gemini_full | 604 | 569 | 690 | 0.3058 | 0.0755 | -268.0000 |
| palma_B ~ gemini_full | 771 | 569 | 834 | 0.3285 | 0.0935 | -286.0000 |
| palma_B ~ palma_C_nq | 771 | 681 | 879 | 0.3345 | 0.0854 | -291.0000 |
| gemini_central ~ gemini_central_in_full | 164 | 165 | 165 | 0.9273 | 0.1147 | 141.0000 |
| gemini_full ~ drac_raw | 569 | 863 | 900 | 0.3444 | 0.1081 | -280.0000 |

`chance` is the identity expected between two independent strings sharing the same class distribution: it is the null model for 'these readings are unrelated'.

### Glyph confusion, palma_A~palma_B

| symbol of palma_A -> palma_B | top matches in palma_B | n | purity |
|---|---|---|---|
| ρ (<- i) | ρ(39) ω(15) #(4) | 70 | 0.5600 |
| α (<- u) | α(41) ω(2) τ(1) | 47 | 0.8700 |
| # (<- a) | #(32) α(2) ζ(2) | 45 | 0.7100 |
| ω (<- r) | ω(27) ρ(2) ξ(1) | 36 | 0.7500 |
| δ (<- m) | δ(15) μ(4) ρ(3) | 32 | 0.4700 |
| τ (<- n) | τ(10) α(9) δ(2) | 29 | 0.3400 |
| φ (<- t) | φ(8) ζ(7) ε(3) | 27 | 0.3000 |
| θ (<- f) | θ(20) ρ(2) μ(1) | 24 | 0.8300 |
| κ (<- e) | κ(6) φ(4) τ(3) | 23 | 0.2600 |
| χ (<- b) | χ(11) σ(2) δ(1) | 22 | 0.5000 |
| ε (<- c) | ε(15) ω(2) σ(1) | 22 | 0.6800 |
| υ (<- l) | κ(6) υ(5) ρ(2) | 19 | 0.3200 |
| λ (<- #) | #(5) ρ(3) λ(2) | 18 | 0.2800 |
| ζ (<- d) | ζ(4) υ(3) ρ(3) | 18 | 0.2200 |
| β (<- p) | δ(2) π(2) ω(2) | 15 | 0.1300 |
| π (<- g) | ω(4) π(2) #(2) | 15 | 0.2700 |
| μ (<- s) | β(6) ρ(2) τ(2) | 15 | 0.4000 |
| ν (<- q) | #(3) π(2) λ(2) | 14 | 0.2100 |
| ψ (<- v) | ψ(8) #(1) ρ(1) | 11 | 0.7300 |
| γ (<- o) | ρ(3) #(2) η(1) | 11 | 0.2700 |
| η (<- j) | ρ(2) λ(1) #(1) | 8 | 0.2500 |
| ξ (<- k) | #(2) π(1) ω(1) | 6 | 0.3300 |
| σ (<- z) | φ(2) ρ(1) #(1) | 5 | 0.4000 |
| ι (<- w) | κ(2) η(1) ε(1) | 4 | 0.5000 |

### Glyph confusion, palma_B~gemini_full

| symbol of palma_B -> gemini_full | top matches in gemini_full | n | purity |
|---|---|---|---|
| a (<- ρ) | a(75) v(3) p(3) | 93 | 0.8100 |
| i (<- #) | i(46) a(4) f(3) | 70 | 0.6600 |
| v (<- α) | v(40) i(6) a(4) | 61 | 0.6600 |
| o (<- ω) | o(48) v(2) t(2) | 58 | 0.8300 |
| p (<- δ) | p(11) a(6) v(4) | 29 | 0.3800 |
| e (<- φ) | e(14) i(3) n(3) | 28 | 0.5000 |
| t (<- χ) | t(4) a(4) v(2) | 16 | 0.2500 |
| d (<- κ) | d(6) i(2) v(2) | 16 | 0.3800 |
| n (<- θ) | n(5) e(2) b(2) | 16 | 0.3100 |
| l (<- τ) | l(6) i(3) o(3) | 16 | 0.3800 |
| z (<- υ) | z(5) v(5) a(1) | 14 | 0.3600 |
| g (<- λ) | v(2) a(2) i(2) | 13 | 0.1500 |
| b (<- ε) | b(4) a(4) t(1) | 12 | 0.3300 |
| h (<- β) | a(3) h(2) b(2) | 12 | 0.2500 |
| f (<- ζ) | i(4) l(2) p(2) | 12 | 0.3300 |
| r (<- μ) | r(3) i(2) n(1) | 11 | 0.2700 |
| c (<- ν) | l(1) t(1) o(1) | 7 | 0.1400 |
| y (<- ψ) | i(4) l(1) δ(1) | 7 | 0.5700 |
| δ (<- γ) | a(1) v(1) n(1) | 5 | 0.2000 |
| m (<- π) | a(1) t(1) q(1) | 4 | 0.2500 |
| φ (<- σ) | a(1) φ(1) | 2 | 0.5000 |
| π (<- η) | z(1) d(1) | 2 | 0.5000 |
| q (<- ξ) | q(1) | 1 | 1.0000 |

## 3.3 Where the readings agree

`palma_A ~ palma_B`: letter where both readings coincide, `·` where they differ.

```
·····λ·ρ·ω···#···λ·····ρ···ω····ω·χ··ρ···ω·ρχ····υ·ω···#··αδ···ρ············ω·ρ···ρ···ω·ρ········θχ·
··θ······ω·δ···θ·θ#ρ····φ·θ····ε···#·π····ρ·θ···φ········#·ρα·κ··ω··#····ρ···α··χ···α····#···γ·ω··ω·
·θε··········ε·ω··αδτ··τ······#··ε··θ··ω··τ·····#·π······θ········ζω·ρ·········υρ··#··εθ···#·····ψ··
·ρ···θ···α···#ε····ω····τ·#··φ·····ρ·υ·ψ·δ·α···ζ·ρ···κ·α··ρ···ρ·#··τ··ω·τ··κρ·······ω·····α···ψα·ω··
ρ··α··α·ε·······#·τ··ε··φ·τκ···χα···αψ··#··θ···ω······α·ζ·υφ··ρ··α·#··α·θα·······α··μ·αχ#····εθε··ω·
···κ·····ρ·δ·#····τ·εθ··α·κ··ρ·ε·αθ#·χ··········θ··ρ#·ψ······υ··#·········ω···ρ··μ······#······#·β·ρ
·α·····φ·δ·····αχ#···ψ··δ····α·ρφ·ρ··#···α····ω········θ·#··αρ··α·····δν··ψ·····δ····α··α·β···δ··α·ρ
··αχα·φ··········δ···ω··ρ·χ·ρ·ρ······θ······α·#····εω·ω·θ·ρ··δ·····δ··ω····ρα·#α···ρ··α···δ#··ψ#·α·ζ
··ε·δ··ω·ρ·α·α··τ··ε····χ#·ρ······α
```

## 3.4 Relabel-invariant agreement between readings

Different transcriptions label the same glyphs with different alphabets (Latin letters vs Greek letters), so symbol-by-symbol identity is meaningless across sources.  What *is* comparable is the repetition pattern: after canonical relabeling two readings of the same text must give nearly the same string.

| pair | len A | len B | common block | share of shorter | relabel identity |
|---|---|---|---|---|---|
| palma_A ~ palma_B | 584 | 678 | 4 | 0.0070 | 0.2450 |
| palma_A ~ gemini_full | 584 | 569 | 4 | 0.0070 | 0.2620 |
| palma_B ~ gemini_full | 678 | 569 | 5 | 0.0090 | 0.2550 |
| palma_B ~ palma_C_nq | 678 | 681 | 5 | 0.0070 | 0.2840 |
| gemini_central ~ gemini_central_in_full | 164 | 165 | 69 | 0.4210 | 0.9450 |
| gemini_full ~ drac_raw | 569 | 863 | 5 | 0.0090 | 0.3120 |

## 3.5 Excess repetitiveness relative to a random text

The IC of a ciphertext is invariant under substitution, but it *does* depend on how many glyph classes the transcriber distinguished: merging glyphs concentrates the distribution and inflates the IC.  The scale-free measure is IC x K, which equals 1.0 for a uniform random text over K glyphs and ~1.9 for Latin letters (see 01_descriptive.md).

| key | n | K | IC | IC x K | excess over random |
|---|---|---|---|---|---|
| palma_A | 584 | 24 | 0.0595 | 1.4290 | 0.4290 |
| palma_A2 | 357 | 24 | 0.0567 | 1.3620 | 0.3620 |
| palma_A_nosp | 584 | 24 | 0.0595 | 1.4290 | 0.4290 |
| palma_B | 678 | 23 | 0.0813 | 1.8700 | 0.8700 |
| palma_C | 681 | 17 | 0.0941 | 1.6000 | 0.6000 |
| palma_B2 | 678 | 24 | 0.0806 | 1.9350 | 0.9350 |
| palma_B3 | 641 | 24 | 0.0797 | 1.9130 | 0.9130 |
| palma_B4 | 589 | 24 | 0.0779 | 1.8710 | 0.8710 |
| palma_C_nq | 681 | 17 | 0.0941 | 1.6000 | 0.6000 |
| gemini_full | 569 | 23 | 0.1147 | 2.6380 | 1.6380 |
| gemini_central | 164 | 18 | 0.1096 | 1.9730 | 0.9730 |
| gemini_central_in_full | 165 | 17 | 0.1091 | 1.8550 | 0.8550 |
| drac_raw | 863 | 24 | 0.1048 | 2.5150 | 1.5150 |

## 3.6 Imaging and OCR probe

What the photographs physically support, measured instead of asserted. Glyph cell and row pitch are an **optimistic upper bound**: the inscription is assumed to fill the whole frame with 36 uniform rows enclosing 569 glyphs (15.8 per row), so the real values are smaller.

| file | pixels | total px | bytes | bytes/px | glyph cell (max) | row pitch (max) |
|---|---|---|---|---|---|---|
| `drac1.jpeg` | 225x225 | 50625 | 11932 | 0.24 | 14.2 | 6.2 |
| `drac2.webp` | 544x1024 | 557056 | 162504 | 0.29 | 34.4 | 28.4 |

**No runnable OCR engine**: the `tesseract` binary is not on PATH; `pytesseract` is installed but only wraps that binary. This phase produces no machine transcription, and none is simulated in its place: the strings analysed downstream remain the published ones (section 3.1).

