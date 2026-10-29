# Phase 1 -- descriptive statistics of the epigraph

Readings analysed: `palma_A`, `palma_B`, `gemini_full`

---

# Reading `palma_A`

*repo:stringaoriginale.txt -- Palma 2023, arbitrary Latin-letter transliteration with word gaps ('.'=separator, '?'=illegible)*

## palma_A -- single symbols

| statistic | value |
|---|---|
| length n | 584 |
| distinct glyphs K | 24 |
| IC | 0.0595 |
| IC x 26 (Palma's scale) | 1.5480 |
| IC x K (1.0 = random over K) | 1.4290 |
| entropy H (bits) | 4.2685 |
| H_max = log2 K | 4.5850 |
| redundancy 1 - H/H_max | 0.0690 |
| effective alphabet 2^H | 19.2700 |
| most frequent glyph share % | 13.0100 |
| top-5 share % | 42.8100 |
| hapax glyphs (count = 1) | 0 |
| chi-square vs uniform | 273.0000 |
| df | 23 |
| p(chi2 >= x) | <1e-12 |

| glyph | count | % | cumulative % |
|---|---|---|---|
| `i` | 76 | 13.0100 | 13.0100 |
| `a` | 50 | 8.5600 | 21.5800 |
| `u` | 48 | 8.2200 | 29.7900 |
| `r` | 40 | 6.8500 | 36.6400 |
| `m` | 36 | 6.1600 | 42.8100 |
| `t` | 34 | 5.8200 | 48.6300 |
| `n` | 30 | 5.1400 | 53.7700 |
| `e` | 29 | 4.9700 | 58.7300 |
| `c` | 25 | 4.2800 | 63.0100 |
| `f` | 25 | 4.2800 | 67.2900 |
| `b` | 23 | 3.9400 | 71.2300 |
| `d` | 22 | 3.7700 | 75.0000 |
| `l` | 22 | 3.7700 | 78.7700 |
| `s` | 19 | 3.2500 | 82.0200 |
| `p` | 18 | 3.0800 | 85.1000 |
| `q` | 16 | 2.7400 | 87.8400 |
| `g` | 16 | 2.7400 | 90.5800 |
| `v` | 15 | 2.5700 | 93.1500 |
| `o` | 12 | 2.0500 | 95.2100 |
| `j` | 8 | 1.3700 | 96.5800 |
| `k` | 6 | 1.0300 | 97.6000 |
| `z` | 6 | 1.0300 | 98.6300 |
| `w` | 4 | 0.6800 | 99.3200 |
| `x` | 4 | 0.6800 | 100.0000 |

## palma_A -- n-grams

| n | distinct | mean count | most frequent | repeat rate | top-10 share % | H(X|prev) |
|---|---|---|---|---|---|---|
| 2 | 277 | 2.1000 | `mi` (8) | 0.7530 | 12.7000 | 3.5130 |
| 3 | 536 | 1.0900 | `uba` (3) | 0.1546 | 3.8000 | 1.2440 |
| 4 | 576 | 1.0100 | `litd` (2) | 0.0172 | 2.6000 | 0.1440 |

Repeat rate = share of n-gram tokens occurring more than once; in a random text over K glyphs it is close to 0.

Top 2-grams of palma_A:

| 2-gram | count | % |
|---|---|---|
| `mi` | 8 | 1.3700 |
| `um` | 8 | 1.3700 |
| `ai` | 8 | 1.3700 |
| `iu` | 8 | 1.3700 |
| `ia` | 8 | 1.3700 |
| `ri` | 7 | 1.2000 |
| `it` | 7 | 1.2000 |
| `ti` | 7 | 1.2000 |
| `mu` | 7 | 1.2000 |
| `ir` | 6 | 1.0300 |

Top 3-grams of palma_A:

| 3-gram | count | % |
|---|---|---|
| `uba` | 3 | 0.5200 |
| `ail` | 3 | 0.5200 |
| `rda` | 2 | 0.3400 |
| `mib` | 2 | 0.3400 |
| `lit` | 2 | 0.3400 |
| `itd` | 2 | 0.3400 |
| `bum` | 2 | 0.3400 |
| `vil` | 2 | 0.3400 |
| `bfi` | 2 | 0.3400 |
| `bir` | 2 | 0.3400 |

## palma_A -- word structure

| statistic | value |
|---|---|
| tokens | 123 |
| mean length | 4.9100 |
| sd length | 2.7700 |
| min / max length | 1 / 19 |
| hapax tokens | 120 |
| types / tokens | 0.9840 |
| 1-2 letter tokens % | 18.7000 |
| tokens containing an illegible mark | 10 |

| length | tokens | % |
|---|---|---|
| 1 | 12 | 9.8000 |
| 2 | 11 | 8.9000 |
| 3 | 15 | 12.2000 |
| 4 | 19 | 15.4000 |
| 5 | 20 | 16.3000 |
| 6 | 18 | 14.6000 |
| 7 | 15 | 12.2000 |
| 8 | 3 | 2.4000 |
| 9 | 3 | 2.4000 |
| 10 | 2 | 1.6000 |
| 11 | 2 | 1.6000 |
| 12 | 2 | 1.6000 |
| 19 | 1 | 0.8000 |

Longest tokens: `equrfitiaslnvtrenac`, `grvilni#gfb#`, `aeiucu#tu#ck`, `if##g#wagiu`, `fdreicnoqgi`, `edra##mi#r`, `abumituvad`, `rpifcqpaq`

Isomorph collisions (distinct tokens sharing a repetition pattern): **11** patterns covering 97 tokens.  They are the raw material of pattern-based crib attacks.

| pattern | tokens |
|---|---|
| ABCDE | `aceuf`, `antsi`, `ard#s`, `audti`, `eszra`, `iamub` |
| ABC | `abn`, `amx`, `atd`, `ate`, `cmr`, `iau` |
| ABCD | `atqx`, `czae`, `fiua`, `igsc`, `isqe`, `iuae` |
| AB | `at`, `au`, `bi`, `ct`, `fi`, `il` |
| ABCDEF | `ctorni`, `fdirne`, `gwnbir`, `ifpcua`, `iluoqa`, `iserdu` |
| A | `a`, `e`, `m`, `n`, `o`, `p` |
| ABCDEFG | `#bugawi`, `aendcsi`, `aizmtqf`, `ilcfsgx`, `lnrceba`, `mudivtr` |
| ABCA | `eiue`, `mntm` |
| ABCDAEF | `altiaud`, `efsierl` |
| ABCDED | `outnmn`, `zmlfpf` |
| ABCDEFGH | `biwceag#`, `vntimqbf` |

Word-level palindromes: `rcfcr`

## palma_A -- palindromes and ABABA motifs

| quantity | observed | null mean | null sd | p (>= observed) |
|---|---|---|---|---|
| palindromic runs (len 4-8) | 6 | 4.3100 | 2.2200 | 0.2699 |
| ABABA motifs (len 5) | 0 | 0.1300 | 0.3800 | 1.0000 |

Positions of ABABA motifs: *none*

## palma_A -- positions

| statistic | value |
|---|---|
| lines | 37 |
| mean line length | 16.3000 |
| sd line length | 5.0000 |
| mean per-line IC | 0.0621 |
| lines with IC = 0 (all glyphs distinct) | 1 |

| line | glyphs | first | last | has gap mark |
|---|---|---|---|---|
| 1 | 10 | `e` | `r` | True |
| 2 | 8 | `d` | `#` | True |
| 3 | 8 | `n` | `r` | False |
| 4 | 20 | `i` | `a` | False |
| 5 | 17 | `n` | `b` | True |
| 6 | 20 | `g` | `r` | True |
| 7 | 21 | `z` | `#` | True |
| 8 | 21 | `n` | `u` | True |
| 9 | 22 | `e` | `i` | True |
| 10 | 22 | `r` | `e` | False |
| 11 | 18 | `n` | `q` | False |
| 12 | 20 | `p` | `m` | False |
| 13 | 17 | `l` | `i` | False |
| 14 | 20 | `v` | `i` | False |
| 15 | 20 | `a` | `r` | False |
| 16 | 23 | `e` | `e` | False |
| 17 | 19 | `v` | `r` | False |
| 18 | 24 | `a` | `i` | True |
| 19 | 22 | `t` | `l` | False |
| 20 | 21 | `s` | `i` | False |
| 21 | 21 | `i` | `e` | False |
| 22 | 20 | `v` | `i` | False |
| 23 | 18 | `a` | `a` | False |
| 24 | 18 | `i` | `e` | True |
| 25 | 10 | `k` | `u` | False |
| 26 | 10 | `m` | `e` | False |
| 27 | 9 | `v` | `r` | False |
| 28 | 14 | `i` | `e` | False |
| 29 | 11 | `p` | `i` | False |
| 30 | 12 | `u` | `b` | False |
| 31 | 9 | `u` | `m` | False |
| 32 | 14 | `i` | `a` | False |
| 33 | 10 | `t` | `i` | False |
| 34 | 14 | `i` | `a` | False |
| 35 | 17 | `a` | `i` | False |
| 36 | 13 | `c` | `n` | False |
| 37 | 11 | `c` | `u` | False |

- line initials: `edningznernplvaevatsivaikmvipuuitiacc` -- 17 distinct over 37 lines
- line finals:  `r#rabr#uieqmiirerilieiaeuereibmaiainu` -- 11 distinct

A text hiding an acrostic would show repeated line initials; here the most frequent initial covers 6/37 lines.

## palma_A -- periodicity tests

| period k | pooled IC | IC x 26 | delta vs global |
|---|---|---|---|
| 1 | 0.0595 | 1.5480 | 0 |
| 2 | 0.0599 | 1.5560 | 3.200e-04 |
| 3 | 0.0611 | 1.5880 | 0.0016 |
| 4 | 0.0594 | 1.5440 | -1.600e-04 |
| 5 | 0.0586 | 1.5250 | -8.900e-04 |
| 6 | 0.0614 | 1.5970 | 0.0019 |
| 7 | 0.0582 | 1.5120 | -0.0014 |
| 8 | 0.0582 | 1.5140 | -0.0013 |
| 9 | 0.0602 | 1.5660 | 7.100e-04 |
| 10 | 0.0586 | 1.5230 | -9.500e-04 |
| 11 | 0.0617 | 1.6030 | 0.0021 |
| 12 | 0.0608 | 1.5800 | 0.0012 |
| 13 | 0.0597 | 1.5530 | 1.900e-04 |
| 14 | 0.0558 | 1.4500 | -0.0038 |
| 15 | 0.0598 | 1.5540 | 2.300e-04 |
| 16 | 0.0583 | 1.5150 | -0.0013 |
| 17 | 0.0632 | 1.6440 | 0.0037 |
| 18 | 0.0608 | 1.5800 | 0.0012 |
| 19 | 0.0595 | 1.5480 | -1.000e-05 |
| 20 | 0.0578 | 1.5030 | -0.0017 |

Largest IC gain at k = **17** (+0.00370); a monoalphabetic text shows no peak, a periodic polyalphabetic one peaks at the key length.

| Friedman quantity | value |
|---|---|
| kappa | 0.0186 |
| chi2 | 250.0100 |
| df | 23 |
| p(chi2 >= x) | <1e-12 |

Kasiski (repeated trigrams): 24 repeat pairs, GCD of distances = 1, most frequent divisors: 2(9), 3(9), 4(6), 5(5), 6(5), 7(5)

## palma_A -- illegible marks

| statistic | value |
|---|---|
| gap marks | 20 |
| runs | 14 |
| mean run | 1.4300 |
| max run | 5 |
| share of the string % | 3.3000 |

| run length | count |
|---|---|
| 1 | 11 |
| 2 | 2 |
| 5 | 1 |

---

# Reading `palma_B`

*repo:soluzione.txt -- Palma 2023, final glyph string in Greek letter labels*

## palma_B -- single symbols

| statistic | value |
|---|---|
| length n | 678 |
| distinct glyphs K | 23 |
| IC | 0.0813 |
| IC x 26 (Palma's scale) | 2.1140 |
| IC x K (1.0 = random over K) | 1.8700 |
| entropy H (bits) | 3.9903 |
| H_max = log2 K | 4.5240 |
| redundancy 1 - H/H_max | 0.1180 |
| effective alphabet 2^H | 15.8900 |
| most frequent glyph share % | 17.1100 |
| top-5 share % | 54.7200 |
| hapax glyphs (count = 1) | 0 |
| chi-square vs uniform | 611.2000 |
| df | 22 |
| p(chi2 >= x) | <1e-12 |

| glyph | count | % | cumulative % |
|---|---|---|---|
| `ρ` | 116 | 17.1100 | 17.1100 |
| `α` | 85 | 12.5400 | 29.6500 |
| `ω` | 82 | 12.0900 | 41.7400 |
| `δ` | 46 | 6.7800 | 48.5300 |
| `φ` | 42 | 6.1900 | 54.7200 |
| `τ` | 31 | 4.5700 | 59.2900 |
| `κ` | 30 | 4.4200 | 63.7200 |
| `ε` | 27 | 3.9800 | 67.7000 |
| `θ` | 27 | 3.9800 | 71.6800 |
| `χ` | 25 | 3.6900 | 75.3700 |
| `ζ` | 24 | 3.5400 | 78.9100 |
| `υ` | 22 | 3.2400 | 82.1500 |
| `λ` | 18 | 2.6500 | 84.8100 |
| `μ` | 18 | 2.6500 | 87.4600 |
| `β` | 17 | 2.5100 | 89.9700 |
| `ν` | 16 | 2.3600 | 92.3300 |
| `π` | 15 | 2.2100 | 94.5400 |
| `ψ` | 12 | 1.7700 | 96.3100 |
| `γ` | 8 | 1.1800 | 97.4900 |
| `η` | 7 | 1.0300 | 98.5300 |
| `ξ` | 5 | 0.7400 | 99.2600 |
| `σ` | 3 | 0.4400 | 99.7100 |
| `ι` | 2 | 0.2900 | 100.0000 |

## palma_B -- n-grams

| n | distinct | mean count | most frequent | repeat rate | top-10 share % | H(X|prev) |
|---|---|---|---|---|---|---|
| 2 | 252 | 2.6900 | `ρα` (23) | 0.8198 | 20.8000 | 3.4180 |
| 3 | 569 | 1.1900 | `ρφρ` (6) | 0.2722 | 6.4000 | 1.6310 |
| 4 | 666 | 1.0100 | `ρφρα` (3) | 0.0252 | 2.8000 | 0.3360 |

Repeat rate = share of n-gram tokens occurring more than once; in a random text over K glyphs it is close to 0.

Top 2-grams of palma_B:

| 2-gram | count | % |
|---|---|---|
| `ρα` | 23 | 3.4000 |
| `φρ` | 17 | 2.5100 |
| `ρω` | 16 | 2.3600 |
| `ωρ` | 16 | 2.3600 |
| `αρ` | 16 | 2.3600 |
| `ρφ` | 15 | 2.2200 |
| `ρρ` | 11 | 1.6200 |
| `ρτ` | 9 | 1.3300 |
| `ωδ` | 9 | 1.3300 |
| `δρ` | 9 | 1.3300 |

Top 3-grams of palma_B:

| 3-gram | count | % |
|---|---|---|
| `ρφρ` | 6 | 0.8900 |
| `ρρα` | 6 | 0.8900 |
| `ωρα` | 5 | 0.7400 |
| `ωαρ` | 4 | 0.5900 |
| `ραρ` | 4 | 0.5900 |
| `ραυ` | 4 | 0.5900 |
| `αρφ` | 4 | 0.5900 |
| `φρα` | 4 | 0.5900 |
| `φωδ` | 3 | 0.4400 |
| `φρρ` | 3 | 0.4400 |

## palma_B -- word structure

*skipped: this reading preserves no word separators*

## palma_B -- palindromes and ABABA motifs

| quantity | observed | null mean | null sd | p (>= observed) |
|---|---|---|---|---|
| palindromic runs (len 4-8) | 15 | 9.6000 | 3.3800 | 0.0810 |
| ABABA motifs (len 5) | 2 | 0.4100 | 0.7100 | 0.0755 |

Positions of ABABA motifs: `ρφρφρ`@510, `ραραρ`@514

## palma_B -- positions

*skipped: this reading is a single continuous string*

## palma_B -- periodicity tests

| period k | pooled IC | IC x 26 | delta vs global |
|---|---|---|---|
| 1 | 0.0813 | 2.1140 | 0 |
| 2 | 0.0808 | 2.0990 | -5.700e-04 |
| 3 | 0.0809 | 2.1020 | -4.500e-04 |
| 4 | 0.0801 | 2.0820 | -0.0012 |
| 5 | 0.0801 | 2.0830 | -0.0012 |
| 6 | 0.0800 | 2.0810 | -0.0013 |
| 7 | 0.0824 | 2.1430 | 0.0011 |
| 8 | 0.0796 | 2.0710 | -0.0017 |
| 9 | 0.0816 | 2.1210 | 2.700e-04 |
| 10 | 0.0770 | 2.0020 | -0.0043 |
| 11 | 0.0830 | 2.1590 | 0.0017 |
| 12 | 0.0779 | 2.0240 | -0.0035 |
| 13 | 0.0813 | 2.1140 | -1.000e-05 |
| 14 | 0.0804 | 2.0910 | -9.000e-04 |
| 15 | 0.0794 | 2.0650 | -0.0019 |
| 16 | 0.0783 | 2.0350 | -0.0030 |
| 17 | 0.0798 | 2.0750 | -0.0015 |
| 18 | 0.0796 | 2.0700 | -0.0017 |
| 19 | 0.0820 | 2.1310 | 6.600e-04 |
| 20 | 0.0765 | 1.9880 | -0.0048 |

Largest IC gain at k = **11** (+0.00172); a monoalphabetic text shows no peak, a periodic polyalphabetic one peaks at the key length.

| Friedman quantity | value |
|---|---|
| kappa | 0.0396 |
| chi2 | 589.1500 |
| df | 22 |
| p(chi2 >= x) | <1e-12 |

Kasiski (repeated trigrams): 64 repeat pairs, GCD of distances = 1, most frequent divisors: 2(34), 3(17), 5(15), 4(13), 7(9), 6(8)

## palma_B -- illegible marks

| statistic | value |
|---|---|
| gap marks | 93 |
| runs | 75 |
| mean run | 1.2400 |
| max run | 4 |
| share of the string % | 12.1000 |

| run length | count |
|---|---|
| 1 | 59 |
| 2 | 15 |
| 4 | 1 |

---

# Reading `gemini_full`

*Gemini log (dracula_epigrafe.md), 33-line transcription embedded in testo_epigrafe_completo; the archived conversation describes it as a simulation of the slab's rows (not an independent transcription), so it is used here as a comparison term only*

## gemini_full -- single symbols

| statistic | value |
|---|---|
| length n | 569 |
| distinct glyphs K | 23 |
| IC | 0.1147 |
| IC x 26 (Palma's scale) | 2.9820 |
| IC x K (1.0 = random over K) | 2.6380 |
| entropy H (bits) | 3.5495 |
| H_max = log2 K | 4.5240 |
| redundancy 1 - H/H_max | 0.2150 |
| effective alphabet 2^H | 11.7100 |
| most frequent glyph share % | 21.4400 |
| top-5 share % | 68.1900 |
| hapax glyphs (count = 1) | 1 |
| chi-square vs uniform | 952.4000 |
| df | 22 |
| p(chi2 >= x) | <1e-12 |

| glyph | count | % | cumulative % |
|---|---|---|---|
| `a` | 122 | 21.4400 | 21.4400 |
| `i` | 87 | 15.2900 | 36.7300 |
| `v` | 75 | 13.1800 | 49.9100 |
| `o` | 70 | 12.3000 | 62.2100 |
| `p` | 34 | 5.9800 | 68.1900 |
| `e` | 34 | 5.9800 | 74.1700 |
| `l` | 25 | 4.3900 | 78.5600 |
| `d` | 24 | 4.2200 | 82.7800 |
| `b` | 20 | 3.5100 | 86.2900 |
| `n` | 18 | 3.1600 | 89.4600 |
| `t` | 14 | 2.4600 | 91.9200 |
| `f` | 7 | 1.2300 | 93.1500 |
| `z` | 7 | 1.2300 | 94.3800 |
| `g` | 6 | 1.0500 | 95.4300 |
| `r` | 5 | 0.8800 | 96.3100 |
| `h` | 5 | 0.8800 | 97.1900 |
| `c` | 4 | 0.7000 | 97.8900 |
| `m` | 3 | 0.5300 | 98.4200 |
| `y` | 2 | 0.3500 | 98.7700 |
| `δ` | 2 | 0.3500 | 99.1200 |
| `π` | 2 | 0.3500 | 99.4700 |
| `q` | 2 | 0.3500 | 99.8200 |
| `φ` | 1 | 0.1800 | 100.0000 |

## gemini_full -- n-grams

| n | distinct | mean count | most frequent | repeat rate | top-10 share % | H(X|prev) |
|---|---|---|---|---|---|---|
| 2 | 159 | 3.5700 | `ai` (27) | 0.8873 | 30.1000 | 3.0640 |
| 3 | 404 | 1.4000 | `vai` (8) | 0.4586 | 9.7000 | 1.8310 |
| 4 | 535 | 1.0600 | `viov` (3) | 0.1025 | 4.2000 | 0.5880 |

Repeat rate = share of n-gram tokens occurring more than once; in a random text over K glyphs it is close to 0.

Top 2-grams of gemini_full:

| 2-gram | count | % |
|---|---|---|
| `ai` | 27 | 4.7500 |
| `ia` | 24 | 4.2300 |
| `va` | 23 | 4.0500 |
| `av` | 23 | 4.0500 |
| `io` | 18 | 3.1700 |
| `vi` | 13 | 2.2900 |
| `pa` | 11 | 1.9400 |
| `al` | 11 | 1.9400 |
| `vo` | 11 | 1.9400 |
| `ov` | 10 | 1.7600 |

Top 3-grams of gemini_full:

| 3-gram | count | % |
|---|---|---|
| `vai` | 8 | 1.4100 |
| `aia` | 7 | 1.2300 |
| `iia` | 6 | 1.0600 |
| `avo` | 6 | 1.0600 |
| `vio` | 5 | 0.8800 |
| `iov` | 5 | 0.8800 |
| `pav` | 5 | 0.8800 |
| `iav` | 5 | 0.8800 |
| `avi` | 4 | 0.7100 |
| `ovi` | 4 | 0.7100 |

## gemini_full -- word structure

| statistic | value |
|---|---|
| tokens | 124 |
| mean length | 4.5900 |
| sd length | 2.5800 |
| min / max length | 1 / 19 |
| hapax tokens | 107 |
| types / tokens | 0.9030 |
| 1-2 letter tokens % | 24.2000 |
| tokens containing an illegible mark | 0 |

| length | tokens | % |
|---|---|---|
| 1 | 14 | 11.3000 |
| 2 | 16 | 12.9000 |
| 3 | 13 | 10.5000 |
| 4 | 18 | 14.5000 |
| 5 | 20 | 16.1000 |
| 6 | 14 | 11.3000 |
| 7 | 21 | 16.9000 |
| 8 | 2 | 1.6000 |
| 9 | 4 | 3.2000 |
| 10 | 1 | 0.8000 |
| 19 | 1 | 0.8000 |

Longest tokens: `iaaddogorivameliape`, `pvaioganbv`, `vaviovipa`, `tvadfovai`, `aildfaiai`, `baviehaφδ`, `loniliad`, `hacolavv`

Isomorph collisions (distinct tokens sharing a repetition pattern): **13** patterns covering 75 tokens.  They are the raw material of pattern-based crib attacks.

| pattern | tokens |
|---|---|
| ABCD | `biav`, `boia`, `cpav`, `ehpπ`, `have`, `ioyq` |
| ABC | `aie`, `cai`, `eva`, `iav`, `iov`, `oar` |
| AB | `an`, `ao`, `av`, `et`, `ia`, `io` |
| ABCDE | `anioz`, `bavio`, `ibnap`, `ieavo`, `iveoa`, `omtal` |
| A | `a`, `b`, `i`, `n`, `p`, `v` |
| ABCDEF | `ateofi`, `elidao`, `obidva`, `ovaipf` |
| ABCA | `eane`, `iali`, `ioai` |
| ABCDBEF | `pagdavo`, `piavibo` |
| ABCDC | `oebib`, `ohvbv` |
| ABCDEAF | `apolead`, `idvalin` |
| ABCDEC | `bvaiga`, `nvadma` |
| ABCDEFB | `latroda`, `lavonea` |

Word-level palindromes: `deded`

## gemini_full -- palindromes and ABABA motifs

| quantity | observed | null mean | null sd | p (>= observed) |
|---|---|---|---|---|
| palindromic runs (len 4-8) | 23 | 16.7400 | 4.4600 | 0.1024 |
| ABABA motifs (len 5) | 4 | 0.8700 | 1.0700 | 0.0295 |

Positions of ABABA motifs: `aiaia`@145, `iaiai`@146, `edede`@362, `deded`@363

## gemini_full -- positions

| statistic | value |
|---|---|
| lines | 36 |
| mean line length | 15.8000 |
| sd line length | 5.5000 |
| mean per-line IC | 0.1154 |
| lines with IC = 0 (all glyphs distinct) | 0 |

| line | glyphs | first | last | has gap mark |
|---|---|---|---|---|
| 1 | 9 | `v` | `a` | False |
| 2 | 22 | `o` | `p` | False |
| 3 | 6 | `a` | `o` | False |
| 4 | 12 | `o` | `i` | False |
| 5 | 19 | `i` | `a` | False |
| 6 | 22 | `n` | `e` | False |
| 7 | 17 | `a` | `a` | False |
| 8 | 21 | `i` | `o` | False |
| 9 | 21 | `a` | `i` | False |
| 10 | 19 | `a` | `a` | False |
| 11 | 23 | `p` | `i` | False |
| 12 | 17 | `v` | `o` | False |
| 13 | 20 | `h` | `o` | False |
| 14 | 20 | `p` | `a` | False |
| 15 | 23 | `i` | `i` | False |
| 16 | 19 | `h` | `δ` | False |
| 17 | 19 | `p` | `o` | False |
| 18 | 22 | `l` | `v` | False |
| 19 | 20 | `b` | `o` | False |
| 20 | 21 | `o` | `i` | False |
| 21 | 21 | `n` | `o` | False |
| 22 | 20 | `p` | `i` | False |
| 23 | 18 | `o` | `π` | False |
| 24 | 10 | `z` | `a` | False |
| 25 | 8 | `i` | `p` | False |
| 26 | 13 | `n` | `a` | False |
| 27 | 12 | `o` | `r` | False |
| 28 | 10 | `t` | `q` | False |
| 29 | 9 | `a` | `v` | False |
| 30 | 6 | `a` | `i` | False |
| 31 | 12 | `o` | `l` | False |
| 32 | 8 | `a` | `q` | False |
| 33 | 13 | `a` | `p` | False |
| 34 | 17 | `p` | `o` | False |
| 35 | 12 | `i` | `a` | False |
| 36 | 8 | `c` | `a` | False |

- line initials: `voaoinaiaapvhpihplbonpozinotaaoaapic` -- 12 distinct over 36 lines
- line finals:  `apoiaeaoiaiooaiδovoioiπaparqvilqpoaa` -- 11 distinct

A text hiding an acrostic would show repeated line initials; here the most frequent initial covers 8/36 lines.

## gemini_full -- periodicity tests

| period k | pooled IC | IC x 26 | delta vs global |
|---|---|---|---|
| 1 | 0.1147 | 2.9820 | 0 |
| 2 | 0.1140 | 2.9630 | -7.300e-04 |
| 3 | 0.1154 | 3.0000 | 6.800e-04 |
| 4 | 0.1140 | 2.9650 | -6.700e-04 |
| 5 | 0.1143 | 2.9710 | -4.300e-04 |
| 6 | 0.1148 | 2.9860 | 1.600e-04 |
| 7 | 0.1129 | 2.9370 | -0.0017 |
| 8 | 0.1128 | 2.9320 | -0.0019 |
| 9 | 0.1145 | 2.9770 | -1.900e-04 |
| 10 | 0.1156 | 3.0060 | 9.400e-04 |
| 11 | 0.1200 | 3.1200 | 0.0053 |
| 12 | 0.1146 | 2.9810 | -6.000e-05 |
| 13 | 0.1155 | 3.0020 | 7.600e-04 |
| 14 | 0.1127 | 2.9300 | -0.0020 |
| 15 | 0.1111 | 2.8900 | -0.0035 |
| 16 | 0.1156 | 3.0060 | 9.100e-04 |
| 17 | 0.1152 | 2.9940 | 4.600e-04 |
| 18 | 0.1159 | 3.0150 | 0.0013 |
| 19 | 0.1153 | 2.9990 | 6.500e-04 |
| 20 | 0.1119 | 2.9090 | -0.0028 |

Largest IC gain at k = **11** (+0.00531); a monoalphabetic text shows no peak, a periodic polyalphabetic one peaks at the key length.

| Friedman quantity | value |
|---|---|
| kappa | 0.0745 |
| chi2 | 930.3600 |
| df | 22 |
| p(chi2 >= x) | <1e-12 |

Kasiski (repeated trigrams): 106 repeat pairs, GCD of distances = 1, most frequent divisors: 2(47), 3(35), 4(24), 5(21), 7(20), 6(18)

## gemini_full -- illegible marks

*no illegible marks in this reading*

