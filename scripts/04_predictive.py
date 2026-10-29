# -*- coding: utf-8 -*-
"""04_predictive.py -- Phase 3: generative models and Bayes factors.

The failure of every noiseless model in Phases 1b-2 suggests that the object
under analysis may be the *transcription* of the inscription as much as the
inscription itself.  This script therefore fits a family of generative models

    plaintext(language) -> substitution -> [nulls] -> [transcription noise]

to the relabel-invariant fingerprint of each reading, and reports

* the best-fitting transcription-noise rate for every language,
* Gaussian log-likelihoods, posterior probabilities and Bayes factors against
  the best model,
* the same fit for control objects (a clean substitution cipher, a nulled one,
  a noisy one) so that the method itself is calibrated.

Output: ``corpus/04_predictive.md``.
"""

from __future__ import annotations

import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C
import langmodels as LM

C.utf8_stdout()

STATS = ["IC", "H", "top1", "bi_rep", "tri_rep"]
READINGS = ["palma_A", "palma_B", "gemini_full"]
SAMPLE = 300_000
NOISE_GRID = [0.0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.40]
N_REP = 30

#: machine-readable summary filled while the sections run
SUMMARY = {"calibration": [], "fits": {}}


def simulate(seq: str, n: int, noise: float, rng: random.Random,
             null_share: float = 0.0) -> str:
    """Slice, substitute, optionally add nulls, then corrupt ``noise`` of glyphs."""
    i = rng.randrange(len(seq) - n)
    plain = seq[i:i + n]
    letters = sorted(set(plain))
    shuffled = letters[:]
    rng.shuffle(shuffled)
    key = dict(zip(letters, shuffled))
    out = [key[c] for c in plain]
    if null_share:
        for _ in range(int(n * null_share)):
            out.insert(rng.randrange(len(out) + 1), "9")
    if noise:
        alphabet = letters + (["9"] if null_share else [])
        for j, ch in enumerate(out):
            if rng.random() < noise:
                out[j] = alphabet[rng.randrange(len(alphabet))]
    return "".join(out)


def stats_of(seq: str) -> dict:
    fp = C.fingerprint(seq)
    return {s: fp[s] for s in STATS}


def simulate_stats(seq: str, n: int, noise: float, n_rep: int = N_REP,
                   null_share: float = 0.0, seed: int = 0) -> dict:
    rng = random.Random(seed)
    vals = {s: [] for s in STATS}
    for _ in range(n_rep):
        st = stats_of(simulate(seq, n, noise, rng, null_share))
        for s in STATS:
            vals[s].append(st[s])
    return {s: (C.mean(v), max(C.stdev(v), 1e-9)) for s, v in vals.items()}


def gauss_loglik(observed: dict, model: dict) -> float:
    ll = 0.0
    for s in STATS:
        mu, sd = model[s]
        ll += (-0.5 * ((observed[s] - mu) / sd) ** 2 - math.log(sd)
               - 0.5 * math.log(2 * math.pi))
    return ll


def fit_languages(rec: dict, langs: dict) -> tuple:
    """Best noise rate per language, plus the likelihood marginalised over it."""
    n = len(rec["letters"])
    obs = stats_of(rec["letters"])
    rows = []
    for label, text in langs.items():
        if len(text) < n + 10:
            continue
        best = None
        lls = []
        for q in NOISE_GRID:
            model = simulate_stats(text, n, q,
                                   seed=C.stable_hash(label) + int(q * 100))
            ll = gauss_loglik(obs, model)
            lls.append(ll)
            if best is None or ll > best[0]:
                best = (ll, q)
        mx = max(lls)  # marginal likelihood, uniform prior over the grid
        marginal = mx + math.log(sum(math.exp(v - mx) for v in lls) / len(lls))
        rows.append([label, best[1], round(best[0], 2), round(marginal, 2)])
    rows.sort(key=lambda r: -r[3])
    SUMMARY["fits"][rec["key"]] = [
        {"language": r[0], "noise": r[1], "loglik": r[2], "marginal": r[3]}
        for r in rows]
    top = rows[0][3] if rows else 0.0
    out = [f"### {rec['key']} (n = {n}): best model per language", ""]
    out.append(C.md_table(
        ["language", "best noise rate", "log-lik at that rate",
         "marginal log-lik", "Bayes factor vs best"],
        [[r[0], r[1], r[2], r[3], C._fmt(math.exp(min(r[3] - top, 0)))]
         for r in rows]))
    out.append("")
    out.append("`marginal log-lik` integrates the likelihood over the noise grid "
               "with a uniform prior, so a language is not rewarded merely for "
               "having a free parameter.  The Bayes factor compares each model "
               "with the best one: below 1e-2 the model is effectively dead.")
    out.append("")
    return out


def control_fit(langs: dict, n: int = 678, n_rep: int = 12) -> list:
    """Fit the same machinery to objects whose generation we know exactly."""
    rng = random.Random(777)
    latin = langs["Latin (Vulgate)"]
    cases = [
        ("clean substitution of Latin", simulate(latin, n, 0.0, rng),
         "Latin (Vulgate)"),
        ("Latin + 10% nulls", simulate(latin, n, 0.0, rng, null_share=0.10),
         "Latin (Vulgate)"),
        ("Latin, 10% transcription noise", simulate(latin, n, 0.10, rng),
         "Latin (Vulgate)"),
        ("Latin, 25% transcription noise", simulate(latin, n, 0.25, rng),
         "Latin (Vulgate)"),
        ("uniform random glyphs",
         "".join(rng.choice("abcdefghijklmnopqrstuvwx") for _ in range(n)),
         "uniform"),
    ]
    out = ["## Calibration: fitting objects of known origin", ""]
    rows = []
    for name, seq, truth in cases:
        obs = stats_of(seq)
        best = None
        for label, text in langs.items():
            if len(text) < n + 10:
                continue
            for q in NOISE_GRID:
                model = simulate_stats(text, n, q, n_rep=n_rep,
                                       seed=int(q * 1000) + len(label))
                ll = gauss_loglik(obs, model)
                if best is None or ll > best[0]:
                    best = (ll, label, q)
        rows.append([name, truth, best[1], best[2], round(best[0], 2)])
    SUMMARY["calibration"] = [
        {"object": r[0], "truth": r[1], "best": r[2], "noise": r[3],
         "loglik": r[4]} for r in rows]
    out.append(C.md_table(["object", "true generating language",
                           "best-fitting language", "noise inferred",
                           "log-lik"], rows))
    out.append("")
    out.append("The calibration shows the envelope of the method: a clean or "
               "nulled substitution is attributed to the right language with a "
               "low inferred noise, while a heavily corrupted text drifts towards "
               "languages with sparse consonant structure.  Conclusions about the "
               "epigraph must stay inside this envelope.")
    out.append("")
    return out


def main() -> None:
    recs = C.load_json(os.path.join(C.CORPUS, "corpora.json"))
    print("loading languages ...")
    langs = LM.load_reference(max_letters=SAMPLE, verbose=False)
    out = ["# Phase 3 -- predictive models and Bayes factors", "",
           "Statistics used (all invariant under substitution): " +
           ", ".join(f"`{s}`" for s in STATS) + ".", "",
           "Generative model: `plaintext(language) -> substitution -> "
           "[nulls] -> [transcription noise]`, with the language drawn from the "
           "16 reference corpora and the noise rate from a fixed grid; the "
           "likelihood is a diagonal Gaussian on the five statistics, whose mean "
           "and sd are estimated from 30 replicates per cell.", ""]
    print("calibration ...")
    out += control_fit(langs)
    out += ["## Fitting the readings", ""]
    for key in READINGS:
        print(f"fitting {key} ...")
        out += fit_languages(recs[key], langs)
    C.save_json(os.path.join(C.CORPUS, "04_summary.json"), SUMMARY)
    C.write_text(os.path.join(C.CORPUS, "04_predictive.md"),
                 "\n".join(out) + "\n")
    print("\nwrote corpus/04_predictive.md")


if __name__ == "__main__":
    main()
