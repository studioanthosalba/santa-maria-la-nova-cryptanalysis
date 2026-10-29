# Phase 1b -- inferential statistics

Readings analysed: `palma_A`, `palma_B`, `gemini_full`

All tests are run on the glyph strings with the illegible marks removed unless stated otherwise.

## Permutation and bootstrap tests

## palma_A -- is the repetition compatible with chance?

| test | observed | null mean | null sd | statistic | p |
|---|---|---|---|---|---|
| IC, permutation null (10 000 shuffles) | 0.0595 | 0.0595 | 0 | -1.0000 | 1.0000 |
| IC, bootstrap CI95 (5 000 resamples) | 0.0595 | 0.0611 | 0.0028 | [0.0560, 0.0669] | - |
| Friedman kappa (uniform null) | 0.0186 | - | - | chi2=250.0, df=23 | <1e-12 |

The permutation null keeps the unigram distribution fixed and destroys only the order, so a significant result means that the sequence is more repetitive than its own frequency profile allows by chance: the text carries serial structure (it is not a random list of glyphs).

## palma_A -- is there a hidden period?

| quantity | value |
|---|---|
| best period k | 17 |
| IC gain at that k | 0.0037 |
| mean IC gain of the best k under shuffling | 0.0036 |
| 95th percentile of the null | 0.0063 |
| p (null max >= observed max) | 0.4351 |

This is the correct test for 'Kasiski found a period': the maximum IC gain is itself a random variable, and at n ~ 600 its null distribution is wide.  A non-significant p means the apparent periodicity is an artefact of small samples.

## palma_B -- is the repetition compatible with chance?

| test | observed | null mean | null sd | statistic | p |
|---|---|---|---|---|---|
| IC, permutation null (10 000 shuffles) | 0.0813 | 0.0813 | 0 | 0 | 1.0000 |
| IC, bootstrap CI95 (5 000 resamples) | 0.0813 | 0.0826 | 0.0042 | [0.0749, 0.0912] | - |
| Friedman kappa (uniform null) | 0.0396 | - | - | chi2=589.2, df=22 | <1e-12 |

The permutation null keeps the unigram distribution fixed and destroys only the order, so a significant result means that the sequence is more repetitive than its own frequency profile allows by chance: the text carries serial structure (it is not a random list of glyphs).

## palma_B -- is there a hidden period?

| quantity | value |
|---|---|
| best period k | 11 |
| IC gain at that k | 0.0017 |
| mean IC gain of the best k under shuffling | 0.0034 |
| 95th percentile of the null | 0.0060 |
| p (null max >= observed max) | 0.9341 |

This is the correct test for 'Kasiski found a period': the maximum IC gain is itself a random variable, and at n ~ 600 its null distribution is wide.  A non-significant p means the apparent periodicity is an artefact of small samples.

## gemini_full -- is the repetition compatible with chance?

| test | observed | null mean | null sd | statistic | p |
|---|---|---|---|---|---|
| IC, permutation null (10 000 shuffles) | 0.1147 | 0.1147 | 0 | -1.0000 | 1.0000 |
| IC, bootstrap CI95 (5 000 resamples) | 0.1147 | 0.1162 | 0.0057 | [0.1055, 0.1284] | - |
| Friedman kappa (uniform null) | 0.0745 | - | - | chi2=930.4, df=22 | <1e-12 |

The permutation null keeps the unigram distribution fixed and destroys only the order, so a significant result means that the sequence is more repetitive than its own frequency profile allows by chance: the text carries serial structure (it is not a random list of glyphs).

## gemini_full -- is there a hidden period?

| quantity | value |
|---|---|
| best period k | 11 |
| IC gain at that k | 0.0053 |
| mean IC gain of the best k under shuffling | 0.0047 |
| 95th percentile of the null | 0.0086 |
| p (null max >= observed max) | 0.3253 |

This is the correct test for 'Kasiski found a period': the maximum IC gain is itself a random variable, and at n ~ 600 its null distribution is wide.  A non-significant p means the apparent periodicity is an artefact of small samples.

## Reference fingerprint (plaintext languages vs the epigraph)

| text | IC | H | top1 | bi_rep | tri_rep | n |
|---|---|---|---|---|---|---|
| epigraph `palma_A` | 0.0595 | 4.2685 | 0.1301 | 0.7530 | 0.1546 | 584 |
| epigraph `palma_B` | 0.0813 | 3.9903 | 0.1711 | 0.8198 | 0.2722 | 678 |
| epigraph `gemini_full` | 0.1147 | 3.5495 | 0.2144 | 0.8873 | 0.4586 | 569 |
| Latin (Vulgate) | 0.0726 | 3.9968 | 0.1272 | 0.9085 | 0.5401 | 678 |
| Latin (humanist corpus) | 0.0717 | 3.9862 | 0.1168 | 0.8965 | 0.4103 | 678 |
| Czech (Bible Kralicka 1613) | 0.0594 | 4.2226 | 0.1161 | 0.8911 | 0.5214 | 678 |
| Czech (catechism) | 0.0611 | 4.1989 | 0.1136 | 0.8812 | 0.5095 | 678 |
| Italian (Riveduta) | 0.0779 | 3.9132 | 0.1380 | 0.9397 | 0.6146 | 678 |
| Italian (Dante) | 0.0728 | 3.9841 | 0.1274 | 0.9277 | 0.4819 | 678 |
| Hungarian (Karoli) | 0.0760 | 4.0383 | 0.1618 | 0.9044 | 0.6025 | 678 |
| Hungarian (Erdy codex, XV c.) | 0.0805 | 3.9813 | 0.1815 | 0.8867 | 0.5178 | 678 |
| Romanian | 0.0835 | 3.8390 | 0.1602 | 0.9319 | 0.6317 | 678 |
| Albanian | 0.0799 | 4.0260 | 0.1884 | 0.8997 | 0.6056 | 678 |
| Croatian | 0.0659 | 4.1087 | 0.1181 | 0.9084 | 0.4771 | 678 |
| Slovak | 0.0621 | 4.1803 | 0.1178 | 0.8797 | 0.4401 | 678 |
| Polish | 0.0628 | 4.1832 | 0.1147 | 0.8909 | 0.5628 | 678 |
| German (Schlachter) | 0.0773 | 3.9960 | 0.1670 | 0.9014 | 0.6260 | 678 |
| English (KJV) | 0.0709 | 4.0442 | 0.1285 | 0.8975 | 0.6309 | 678 |
| Greek (Brenton, translit.) | 0.0751 | 3.9880 | 0.1305 | 0.8892 | 0.5764 | 678 |

Language values are means over 200 windows of 678 glyphs; the epigraph values are computed on its own length.

## Length-matched language comparison

### palma_A (n = 584) against length-matched language models

| reference language | z(IC) | z(H) | z(top1) | z(bi_rep) | z(tri_rep) | mean |z| | min p |
|---|---|---|---|---|---|---|---|
| Czech (Bible Kralicka 1613) | 0.0600 | 1.2500 | 1.0000 | -6.5500 | -4.1700 | 2.6070 | 0.0025 |
| Czech (catechism) | -0.4500 | 1.8500 | 1.3900 | -6.3200 | -4.6500 | 2.9310 | 0.0025 |
| Polish | -1.1400 | 2.0400 | 1.1800 | -5.7800 | -4.5500 | 2.9390 | 0.0025 |
| Greek (Brenton, translit.) | -2.9700 | 3.9200 | -0.1100 | -4.7400 | -4.1900 | 3.1840 | 0.0025 |
| Slovak | -1.0900 | 2.6900 | 1.0900 | -6.6700 | -5.0000 | 3.3060 | 0.0025 |
| English (KJV) | -3.1700 | 4.2600 | 0.1200 | -5.7000 | -5.4800 | 3.7460 | 0.0025 |
| Hungarian (Karoli) | -3.3500 | 3.9400 | -1.7100 | -6.6600 | -5.3300 | 4.1990 | 0.0025 |
| Albanian | -3.6000 | 4.4300 | -2.8700 | -6.2500 | -5.4100 | 4.5130 | 0.0025 |
| German (Schlachter) | -3.5200 | 4.3800 | -2.1800 | -6.4900 | -6.0500 | 4.5260 | 0.0025 |
| Croatian | -2.9700 | 4.7100 | 1.0500 | -9.9700 | -4.9300 | 4.7250 | 0.0025 |
| Hungarian (Erdy codex, XV c.) | -3.8000 | 4.0900 | -2.4200 | -6.7700 | -7.3600 | 4.8870 | 0.0025 |
| Latin (Vulgate) | -5.1600 | 6.8300 | 0.2300 | -8.5300 | -5.2300 | 5.1970 | 0.0025 |
| Romanian | -5.0600 | 9.1400 | -1.4300 | -9.8900 | -5.5000 | 6.2040 | 0.0025 |
| Latin (humanist corpus) | -6.3400 | 8.6800 | 1.4700 | -9.9500 | -6.9100 | 6.6700 | 0.0025 |
| Italian (Riveduta) | -6.8000 | 8.2300 | -0.6400 | -13.6300 | -6.2000 | 7.1000 | 0.0025 |
| Italian (Dante) | -6.4300 | 9.0400 | 0.1300 | -14.3800 | -8.3000 | 7.6580 | 0.0025 |

Each reference language is sampled with windows of exactly the same length, so sampling error is identical on both sides.  z = (observed - language mean) / language sd; the languages are ordered by mean |z| over the five invariant statistics.  A mean |z| below ~1 means the inscription is indistinguishable from that language at this length; above ~2 it is unlikely.

### palma_B (n = 678) against length-matched language models

| reference language | z(IC) | z(H) | z(top1) | z(bi_rep) | z(tri_rep) | mean |z| | min p |
|---|---|---|---|---|---|---|---|
| Greek (Brenton, translit.) | 1.1700 | 0.0900 | 2.7900 | -3.0500 | -3.3100 | 2.0810 | 0.0100 |
| Albanian | 0.2200 | -0.6300 | -0.9100 | -4.3500 | -4.5800 | 2.1380 | 0.0025 |
| Hungarian (Erdy codex, XV c.) | 0.2400 | 0.1300 | -0.4300 | -4.4800 | -5.8000 | 2.2170 | 0.0025 |
| German (Schlachter) | 0.8600 | -0.1400 | 0.2300 | -4.7600 | -5.1800 | 2.2350 | 0.0025 |
| Hungarian (Karoli) | 1.0600 | -0.8100 | 0.4700 | -4.7900 | -4.3300 | 2.2900 | 0.0025 |
| English (KJV) | 3.1600 | -1.1200 | 3.3300 | -4.0900 | -4.7000 | 3.2790 | 0.0025 |
| Romanian | -0.4500 | 3.3200 | 0.5500 | -7.8700 | -4.7100 | 3.3810 | 0.0025 |
| Latin (Vulgate) | 3.6100 | -0.1500 | 3.6700 | -6.4700 | -4.0800 | 3.5960 | 0.0025 |
| Italian (Riveduta) | 1.2800 | 1.8500 | 2.5500 | -10.8300 | -5.1300 | 4.3280 | 0.0025 |
| Polish | 6.6000 | -4.6000 | 4.5900 | -3.9400 | -3.5200 | 4.6490 | 0.0025 |
| Latin (humanist corpus) | 5.3800 | 0.0400 | 6.9600 | -6.8700 | -4.8900 | 4.8290 | 0.0025 |
| Czech (catechism) | 6.0300 | -5.5600 | 5.1000 | -4.0600 | -3.4200 | 4.8340 | 0.0025 |
| Czech (Bible Kralicka 1613) | 8.1900 | -5.9400 | 4.0800 | -4.6500 | -3.2300 | 5.2190 | 0.0025 |
| Italian (Dante) | 4.6100 | 0.2200 | 4.1900 | -11.2100 | -6.6300 | 5.3720 | 0.0025 |
| Slovak | 8.9000 | -5.9900 | 5.1600 | -4.3400 | -3.4900 | 5.5750 | 0.0025 |
| Croatian | 7.3800 | -3.5200 | 5.7900 | -7.5900 | -3.8400 | 5.6230 | 0.0025 |

Each reference language is sampled with windows of exactly the same length, so sampling error is identical on both sides.  z = (observed - language mean) / language sd; the languages are ordered by mean |z| over the five invariant statistics.  A mean |z| below ~1 means the inscription is indistinguishable from that language at this length; above ~2 it is unlikely.

### gemini_full (n = 569) against length-matched language models

| reference language | z(IC) | z(H) | z(top1) | z(bi_rep) | z(tri_rep) | mean |z| | min p |
|---|---|---|---|---|---|---|---|
| Hungarian (Erdy codex, XV c.) | 6.2600 | -5.8800 | 1.6700 | 1.0900 | -0.4200 | 3.0630 | 0.0025 |
| Albanian | 5.9900 | -8.2300 | 1.2200 | 0.2000 | -1.4700 | 3.4220 | 0.0025 |
| Romanian | 6.6100 | -5.9300 | 2.5800 | -1.7500 | -1.6500 | 3.7020 | 0.0025 |
| German (Schlachter) | 7.4400 | -7.1000 | 2.7500 | 0.2000 | -1.8000 | 3.8570 | 0.0025 |
| Hungarian (Karoli) | 7.7300 | -8.0100 | 2.6800 | 0.1400 | -1.3100 | 3.9740 | 0.0025 |
| Greek (Brenton, translit.) | 7.2300 | -5.7500 | 5.4700 | 0.7000 | -0.9200 | 4.0110 | 0.0025 |
| English (KJV) | 12.1400 | -9.1100 | 6.3600 | 0.3400 | -1.7200 | 5.9340 | 0.0025 |
| Italian (Riveduta) | 13.3100 | -8.0900 | 5.4600 | -2.7800 | -1.7000 | 6.2680 | 0.0025 |
| Latin (Vulgate) | 16.2700 | -10.7600 | 6.9100 | -0.0100 | -0.5700 | 6.9050 | 0.0025 |
| Polish | 17.4300 | -14.0800 | 7.9100 | 0.7900 | -0.8500 | 8.2110 | 0.0025 |
| Czech (catechism) | 15.8100 | -16.3900 | 8.5300 | 1.6100 | -0.2500 | 8.5170 | 0.0025 |
| Italian (Dante) | 19.6300 | -13.2000 | 7.5500 | -1.8800 | 0.5100 | 8.5550 | 0.0025 |
| Czech (Bible Kralicka 1613) | 19.4200 | -16.2300 | 6.8200 | 0.9900 | -0.3300 | 8.7590 | 0.0025 |
| Croatian | 21.4900 | -15.6100 | 9.5900 | -0.0400 | 0.2300 | 9.3900 | 0.0025 |
| Latin (humanist corpus) | 22.4400 | -13.2800 | 11.3400 | 0.9800 | 2.8900 | 10.1860 | 0.0025 |
| Slovak | 22.8700 | -18.7600 | 8.8000 | 1.8900 | 1.2300 | 10.7090 | 0.0025 |

Each reference language is sampled with windows of exactly the same length, so sampling error is identical on both sides.  z = (observed - language mean) / language sd; the languages are ordered by mean |z| over the five invariant statistics.  A mean |z| below ~1 means the inscription is indistinguishable from that language at this length; above ~2 it is unlikely.

## Comparison with uniform random text

## palma_A -- distance from a uniform random string

| statistic | observed | random mean | random sd | z | p |
|---|---|---|---|---|---|
| IC | 0.0595 | 0.0417 | 5.000e-04 | 37.1500 | 0.0020 |
| H | 4.2685 | 4.5566 | 0.0085 | -34.0100 | 0.0020 |
| top1 | 0.1301 | 0.0590 | 0.0045 | 15.9400 | 0.0020 |
| bi_rep | 0.7530 | 0.6356 | 0.0207 | 5.6700 | 0.0020 |
| tri_rep | 0.1546 | 0.0408 | 0.0119 | 9.5600 | 0.0020 |

Uniform text over the same K glyphs is the 'meaningless decoration' hypothesis: at least two statistics must reject it for the inscription to be worth attacking at all.

## palma_B -- distance from a uniform random string

| statistic | observed | random mean | random sd | z | p |
|---|---|---|---|---|---|
| IC | 0.0813 | 0.0435 | 4.000e-04 | 85.2300 | 0.0020 |
| H | 3.9903 | 4.4999 | 0.0075 | -67.5600 | 0.0020 |
| top1 | 0.1711 | 0.0596 | 0.0041 | 27.2800 | 0.0020 |
| bi_rep | 0.8198 | 0.7221 | 0.0158 | 6.1900 | 0.0020 |
| tri_rep | 0.2722 | 0.0526 | 0.0133 | 16.4500 | 0.0020 |

Uniform text over the same K glyphs is the 'meaningless decoration' hypothesis: at least two statistics must reject it for the inscription to be worth attacking at all.

## gemini_full -- distance from a uniform random string

| statistic | observed | random mean | random sd | z | p |
|---|---|---|---|---|---|
| IC | 0.1147 | 0.0435 | 5.000e-04 | 136.0500 | 0.0020 |
| H | 3.5495 | 4.4956 | 0.0088 | -107.7200 | 0.0020 |
| top1 | 0.2144 | 0.0611 | 0.0046 | 33.6400 | 0.0020 |
| bi_rep | 0.8873 | 0.6560 | 0.0207 | 11.1800 | 0.0020 |
| tri_rep | 0.4586 | 0.0442 | 0.0129 | 32.1700 | 0.0020 |

Uniform text over the same K glyphs is the 'meaningless decoration' hypothesis: at least two statistics must reject it for the inscription to be worth attacking at all.

## Vowels and consonants

## palma_A -- exhaustive vowels/consonants test

Every one of the 42504 possible 5-glyph vowel sets is tried.  In any natural language vowels and consonants alternate, so the fraction of the text sitting inside runs of three or more consonants (`C3`) is small; a good vowel set minimises it.

| 5-glyph vowel set | C3 share | mean C run | longest C run | glyph counts |
|---|---|---|---|---|
| `i`, `a`, `u`, `r`, `n` | 0.3048 | 2.0120 | 6 | i:76a:50u:48r:40n:30 |
| `i`, `a`, `u`, `r`, `m` | 0.3219 | 2.2270 | 9 | i:76a:50u:48r:40m:36 |
| `i`, `a`, `u`, `r`, `f` | 0.3408 | 2.1840 | 10 | i:76a:50u:48r:40f:25 |
| `i`, `a`, `u`, `r`, `c` | 0.3408 | 2.1970 | 10 | i:76a:50u:48r:40c:25 |
| `i`, `a`, `u`, `r`, `q` | 0.3425 | 2.1850 | 10 | i:76a:50u:48r:40q:16 |
| --- reference languages --- | - | - | - | - |
| Italian (Riveduta) | 0.0250 | 1.3830 | - | - |
| Italian (Dante) | 0.0414 | 1.4590 | - | - |
| Romanian | 0.0478 | 1.3360 | - | - |
| Latin (Vulgate) | 0.0581 | 1.4710 | - | - |
| Croatian | 0.0606 | 1.3460 | - | - |
| Latin (humanist corpus) | 0.0831 | 1.5080 | - | - |
| Slovak | 0.0993 | 1.4660 | - | - |
| Hungarian (Karoli) | 0.1042 | 1.5530 | - | - |
| Czech (Bible Kralicka 1613) | 0.1214 | 1.5070 | - | - |
| Albanian | 0.1281 | 1.5320 | - | - |
| Polish | 0.1367 | 1.5860 | - | - |
| Czech (catechism) | 0.1638 | 1.6350 | - | - |
| German (Schlachter) | 0.2274 | 1.9400 | - | - |
| English (KJV) | 0.2691 | 1.9060 | - | - |
| Hungarian (Erdy codex, XV c.) | 0.2726 | 2.0350 | - | - |
| Greek (Brenton, translit.) | 0.3077 | 2.0230 | - | - |

- best achievable C3 share: **0.3048**
- median over all vowel sets: 0.7123
- best natural-language reference: 0.0250

If the best achievable value is far above the reference range, then no substitution can turn this glyph string into a text with natural vowel/consonant alternation -- which rules out plain monoalphabetic substitution of an alphabetic language and points to nulls, transposition or a different segmentation.

## palma_B -- exhaustive vowels/consonants test

Every one of the 33649 possible 5-glyph vowel sets is tried.  In any natural language vowels and consonants alternate, so the fraction of the text sitting inside runs of three or more consonants (`C3`) is small; a good vowel set minimises it.

| 5-glyph vowel set | C3 share | mean C run | longest C run | glyph counts |
|---|---|---|---|---|
| `ρ`, `α`, `ω`, `δ`, `λ` | 0.1652 | 1.6890 | 6 | ρ:116α:85ω:82δ:46λ:18 |
| `ρ`, `α`, `ω`, `δ`, `θ` | 0.1740 | 1.6770 | 7 | ρ:116α:85ω:82δ:46θ:27 |
| `ρ`, `α`, `ω`, `δ`, `ε` | 0.1755 | 1.6510 | 6 | ρ:116α:85ω:82δ:46ε:27 |
| `ρ`, `α`, `ω`, `δ`, `τ` | 0.1799 | 1.7190 | 8 | ρ:116α:85ω:82δ:46τ:31 |
| `ρ`, `α`, `ω`, `δ`, `β` | 0.1888 | 1.7200 | 8 | ρ:116α:85ω:82δ:46β:17 |
| --- reference languages --- | - | - | - | - |
| Italian (Riveduta) | 0.0253 | 1.3830 | - | - |
| Italian (Dante) | 0.0417 | 1.4580 | - | - |
| Romanian | 0.0481 | 1.3370 | - | - |
| Latin (Vulgate) | 0.0591 | 1.4730 | - | - |
| Croatian | 0.0612 | 1.3490 | - | - |
| Latin (humanist corpus) | 0.0830 | 1.5090 | - | - |
| Slovak | 0.0990 | 1.4660 | - | - |
| Hungarian (Karoli) | 0.1036 | 1.5520 | - | - |
| Czech (Bible Kralicka 1613) | 0.1208 | 1.5080 | - | - |
| Albanian | 0.1284 | 1.5310 | - | - |
| Polish | 0.1379 | 1.5890 | - | - |
| Czech (catechism) | 0.1634 | 1.6340 | - | - |
| German (Schlachter) | 0.2252 | 1.9360 | - | - |
| English (KJV) | 0.2683 | 1.9040 | - | - |
| Hungarian (Erdy codex, XV c.) | 0.2717 | 2.0340 | - | - |
| Greek (Brenton, translit.) | 0.3063 | 2.0190 | - | - |

- best achievable C3 share: **0.1652**
- median over all vowel sets: 0.6947
- best natural-language reference: 0.0253

If the best achievable value is far above the reference range, then no substitution can turn this glyph string into a text with natural vowel/consonant alternation -- which rules out plain monoalphabetic substitution of an alphabetic language and points to nulls, transposition or a different segmentation.

## gemini_full -- exhaustive vowels/consonants test

Every one of the 33649 possible 5-glyph vowel sets is tried.  In any natural language vowels and consonants alternate, so the fraction of the text sitting inside runs of three or more consonants (`C3`) is small; a good vowel set minimises it.

| 5-glyph vowel set | C3 share | mean C run | longest C run | glyph counts |
|---|---|---|---|---|
| `a`, `i`, `v`, `o`, `e` | 0.0281 | 1.2480 | 4 | a:122i:87v:75o:70e:34 |
| `a`, `i`, `v`, `o`, `p` | 0.0475 | 1.3920 | 6 | a:122i:87v:75o:70p:34 |
| `a`, `i`, `v`, `o`, `l` | 0.0492 | 1.4180 | 7 | a:122i:87v:75o:70l:25 |
| `a`, `i`, `o`, `p`, `e` | 0.0527 | 1.3450 | 4 | a:122i:87o:70p:34e:34 |
| `a`, `i`, `v`, `o`, `d` | 0.0545 | 1.3840 | 6 | a:122i:87v:75o:70d:24 |
| --- reference languages --- | - | - | - | - |
| Italian (Riveduta) | 0.0251 | 1.3830 | - | - |
| Italian (Dante) | 0.0413 | 1.4590 | - | - |
| Romanian | 0.0479 | 1.3370 | - | - |
| Latin (Vulgate) | 0.0584 | 1.4710 | - | - |
| Croatian | 0.0606 | 1.3460 | - | - |
| Latin (humanist corpus) | 0.0829 | 1.5080 | - | - |
| Slovak | 0.0994 | 1.4660 | - | - |
| Hungarian (Karoli) | 0.1039 | 1.5530 | - | - |
| Czech (Bible Kralicka 1613) | 0.1212 | 1.5070 | - | - |
| Albanian | 0.1283 | 1.5320 | - | - |
| Polish | 0.1360 | 1.5840 | - | - |
| Czech (catechism) | 0.1642 | 1.6360 | - | - |
| German (Schlachter) | 0.2266 | 1.9390 | - | - |
| English (KJV) | 0.2691 | 1.9070 | - | - |
| Hungarian (Erdy codex, XV c.) | 0.2716 | 2.0350 | - | - |
| Greek (Brenton, translit.) | 0.3072 | 2.0220 | - | - |

- best achievable C3 share: **0.0281**
- median over all vowel sets: 0.6942
- best natural-language reference: 0.0251

If the best achievable value is far above the reference range, then no substitution can turn this glyph string into a text with natural vowel/consonant alternation -- which rules out plain monoalphabetic substitution of an alphabetic language and points to nulls, transposition or a different segmentation.

## Robustness to the illegible marks

| reading | gap marks | IC (gaps kept) | IC (gaps dropped) | H (gaps kept) | H (gaps dropped) |
|---|---|---|---|---|---|
| palma_A | 20 | 0.0567 | 0.0595 | 4.3370 | 4.2690 |
| palma_B | 93 | 0.0773 | 0.0813 | 4.0400 | 3.9900 |
| gemini_full | 0 | 0.1147 | 0.1147 | 3.5500 | 3.5500 |

Treating '?' as a glyph in its own right barely moves the statistics, so the conclusions do not depend on dropping the illegible positions.

