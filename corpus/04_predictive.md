# Phase 3 -- predictive models and Bayes factors

Statistics used (all invariant under substitution): `IC`, `H`, `top1`, `bi_rep`, `tri_rep`.

Generative model: `plaintext(language) -> substitution -> [nulls] -> [transcription noise]`, with the language drawn from the 16 reference corpora and the noise rate from a fixed grid; the likelihood is a diagonal Gaussian on the five statistics, whose mean and sd are estimated from 30 replicates per cell.

## Calibration: fitting objects of known origin

| object | true generating language | best-fitting language | noise inferred | log-lik |
|---|---|---|---|---|
| clean substitution of Latin | Latin (Vulgate) | Latin (Vulgate) | 0.0500 | 15.1800 |
| Latin + 10% nulls | Latin (Vulgate) | Croatian | 0.0500 | 16.2300 |
| Latin, 10% transcription noise | Latin (Vulgate) | Latin (Vulgate) | 0.1000 | 14.2600 |
| Latin, 25% transcription noise | Latin (Vulgate) | Croatian | 0.3000 | 16.1800 |
| uniform random glyphs | uniform | Czech (catechism) | 0.4000 | -13.0500 |

The calibration shows the envelope of the method: a clean or nulled substitution is attributed to the right language with a low inferred noise, while a heavily corrupted text drifts towards languages with sparse consonant structure.  Conclusions about the epigraph must stay inside this envelope.

## Fitting the readings

### palma_A (n = 584): best model per language

| language | best noise rate | log-lik at that rate | marginal log-lik | Bayes factor vs best |
|---|---|---|---|---|
| Hungarian (Karoli) | 0.3000 | 15.0500 | 13.0600 | 1.0000 |
| German (Schlachter) | 0.4000 | 13.9900 | 12.5000 | 0.5712 |
| Hungarian (Erdy codex, XV c.) | 0.3000 | 13.6100 | 11.9500 | 0.3296 |
| Albanian | 0.3000 | 13.2600 | 11.4000 | 0.1901 |
| Greek (Brenton, translit.) | 0.3000 | 12.8400 | 11.1500 | 0.1481 |
| Latin (Vulgate) | 0.3000 | 11.9300 | 9.9100 | 0.0429 |
| Italian (Dante) | 0.3000 | 11.7800 | 9.7300 | 0.0358 |
| Italian (Riveduta) | 0.4000 | 11.6100 | 9.5400 | 0.0296 |
| Polish | 0.2500 | 11.1700 | 9.2100 | 0.0213 |
| English (KJV) | 0.2500 | 11.1800 | 9.1500 | 0.0200 |
| Slovak | 0.2000 | 10.7600 | 9.1200 | 0.0194 |
| Latin (humanist corpus) | 0.3000 | 10.8000 | 8.8000 | 0.0141 |
| Czech (Bible Kralicka 1613) | 0.2000 | 9.3000 | 8.1300 | 0.0072 |
| Romanian | 0.4000 | 9.0600 | 7.1000 | 0.0026 |
| Croatian | 0.2500 | 8.7400 | 6.9300 | 0.0022 |
| Czech (catechism) | 0.2000 | 7.2300 | 5.2700 | 4.139e-04 |

`marginal log-lik` integrates the likelihood over the noise grid with a uniform prior, so a language is not rewarded merely for having a free parameter.  The Bayes factor compares each model with the best one: below 1e-2 the model is effectively dead.

### palma_B (n = 678): best model per language

| language | best noise rate | log-lik at that rate | marginal log-lik | Bayes factor vs best |
|---|---|---|---|---|
| Hungarian (Erdy codex, XV c.) | 0.1500 | 8.8700 | 6.8800 | 1.0000 |
| Romanian | 0.2000 | 7.4000 | 5.6800 | 0.3012 |
| Greek (Brenton, translit.) | 0.1000 | 4.4800 | 2.5300 | 0.0129 |
| Albanian | 0.1000 | 2.2800 | 0.9500 | 0.0027 |
| Hungarian (Karoli) | 0.1000 | 1.0100 | -1.0600 | 3.562e-04 |
| German (Schlachter) | 0.1500 | -2.0500 | -4.1000 | 1.704e-05 |
| English (KJV) | 0 | -6.5700 | -8.6400 | 1.819e-07 |
| Italian (Riveduta) | 0.1000 | -13.3500 | -15.4300 | 2.046e-10 |
| Latin (Vulgate) | 0 | -18.7600 | -20.8300 | 9.241e-13 |
| Latin (humanist corpus) | 0.0500 | -30.1500 | -32.2300 | 1.035e-17 |
| Polish | 0.1000 | -35.2500 | -37.3300 | 6.307e-20 |
| Czech (catechism) | 0 | -37.2300 | -39.3100 | 8.708e-21 |
| Croatian | 0 | -40.3900 | -41.8200 | 7.077e-22 |
| Italian (Dante) | 0.1500 | -42.7300 | -44.7900 | 3.631e-23 |
| Slovak | 0.0500 | -44.3400 | -46.4200 | 7.114e-24 |
| Czech (Bible Kralicka 1613) | 0 | -53.5000 | -55.4200 | 8.779e-28 |

`marginal log-lik` integrates the likelihood over the noise grid with a uniform prior, so a language is not rewarded merely for having a free parameter.  The Bayes factor compares each model with the best one: below 1e-2 the model is effectively dead.

### gemini_full (n = 569): best model per language

| language | best noise rate | log-lik at that rate | marginal log-lik | Bayes factor vs best |
|---|---|---|---|---|
| German (Schlachter) | 0 | -26.1000 | -28.1800 | 1.0000 |
| Hungarian (Erdy codex, XV c.) | 0 | -26.1600 | -28.2400 | 0.9418 |
| Romanian | 0.0500 | -46.5500 | -48.6200 | 1.327e-09 |
| Greek (Brenton, translit.) | 0.0500 | -51.3400 | -53.4200 | 1.092e-11 |
| Albanian | 0.0500 | -52.7600 | -54.8400 | 2.641e-12 |
| Hungarian (Karoli) | 0 | -60.7900 | -62.8700 | 8.597e-16 |
| Italian (Riveduta) | 0 | -79.9700 | -82.0500 | 4.023e-24 |
| English (KJV) | 0 | -82.7100 | -84.7900 | 2.598e-25 |
| Latin (Vulgate) | 0 | -142.0700 | -144.1500 | 4.314e-51 |
| Croatian | 0 | -207.0900 | -209.1700 | 2.495e-79 |
| Polish | 0.0500 | -219.3700 | -221.4500 | 1.159e-84 |
| Latin (humanist corpus) | 0.1000 | -270.0100 | -272.0900 | 1.178e-106 |
| Czech (catechism) | 0 | -296.3300 | -298.4100 | 4.371e-118 |
| Italian (Dante) | 0.0500 | -303.4500 | -305.5300 | 3.535e-121 |
| Czech (Bible Kralicka 1613) | 0.0500 | -308.3700 | -310.4500 | 2.580e-123 |
| Slovak | 0.1000 | -464.0900 | -466.1700 | 6.072e-191 |

`marginal log-lik` integrates the likelihood over the noise grid with a uniform prior, so a language is not rewarded merely for having a free parameter.  The Bayes factor compares each model with the best one: below 1e-2 the model is effectively dead.

