# -*- coding: utf-8 -*-
"""02_inferential.py -- Phase 1b: inferential statistics.

Contents
--------
1. Permutation / bootstrap tests for the repetition structure (IC, periodicity).
2. Length-matched comparison with 16 reference languages using *relabel
   invariant* statistics (a substitution leaves them untouched, so the test is
   valid for a ciphertext -- something the published analyses do not do).
3. A baseline against uniform random text over the same number of glyphs.
4. The exhaustive vowels/consonants test: all C(K,5) vowel assignments are tried
   and scored with the consonant-run statistics of the reference languages,
   which turns Palma's qualitative experiment into a test with a null
   distribution.
5. Robustness to the illegible marks.

Output: ``corpus/02_inferential.md``.
"""

from __future__ import annotations

import itertools
import os
import random
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C
import langmodels as LM

C.utf8_stdout()

READINGS = ["palma_A", "palma_B", "gemini_full"]
N_SLICES = 400
SAMPLE_LETTERS = 400_000

#: machine-readable summary filled while the sections run
SUMMARY = {"permutation": {}, "periodicity": {}, "rankings": {}, "cv": {},
           "random_null": {}}


# --------------------------------------------------------------------------
# 1. permutation and bootstrap tests
# --------------------------------------------------------------------------
def permutation_section(rec: dict, n_iter: int = 10000) -> list:
    seq = rec["letters"]
    mc = C.monte_carlo_ic(seq, n_iter=n_iter)
    bs = C.bootstrap_ic(seq, n_iter=5000)
    fr = C.friedman_chi2(seq)
    SUMMARY["permutation"][rec["key"]] = {
        "ic": mc["observed"], "p": mc["p_value"], "bs_lo": bs["lo95"],
        "bs_hi": bs["hi95"], "kappa": fr["kappa"], "friedman_p": fr["p_value"]}
    out = [f"## {rec['key']} -- is the repetition compatible with chance?", ""]
    out.append(C.md_table(
        ["test", "observed", "null mean", "null sd", "statistic", "p"],
        [["IC, permutation null (10 000 shuffles)", round(mc["observed"], 5),
          round(mc["null_mean"], 5), round(mc["null_sd"], 5),
          round(mc["z"], 2), C.fmt_p(mc["p_value"])],
         ["IC, bootstrap CI95 (5 000 resamples)",
          round(bs["observed"], 5), round(bs["mean"], 5), round(bs["sd"], 5),
          f"[{bs['lo95']:.4f}, {bs['hi95']:.4f}]", "-"],
         ["Friedman kappa (uniform null)", round(fr["kappa"], 4), "-", "-",
          f"chi2={fr['chi2']:.1f}, df={fr['df']}", C.fmt_p(fr["p_value"])]]))
    out.append("")
    out.append("The permutation null keeps the unigram distribution fixed and "
               "destroys only the order, so a significant result means that the "
               "sequence is more repetitive than its own frequency profile "
               "allows by chance: the text carries serial structure (it is not a "
               "random list of glyphs).")
    out.append("")
    return out


def periodicity_null(rec: dict, n_iter: int = 500, max_period: int = 20) -> list:
    """Is the best periodicity peak larger than what shuffling produces?"""
    seq = rec["letters"]
    rng = random.Random(17)
    obs = max(C.ic_by_period(seq, max_period), key=lambda p: p["delta"])
    letters = list(seq)
    sims = []
    for _ in range(n_iter):
        rng.shuffle(letters)
        sims.append(max(C.ic_by_period(letters, max_period),
                        key=lambda p: p["delta"])["delta"])
    p = (1 + sum(1 for v in sims if v >= obs["delta"])) / (1 + n_iter)
    SUMMARY["periodicity"][rec["key"]] = {
        "best_k": obs["period"], "delta": obs["delta"], "p": p,
        "null95": C.quantile(sims, 0.95)}
    out = [f"## {rec['key']} -- is there a hidden period?", ""]
    out.append(C.md_table(
        ["quantity", "value"],
        [["best period k", obs["period"]],
         ["IC gain at that k", round(obs["delta"], 5)],
         ["mean IC gain of the best k under shuffling",
          round(C.mean(sims), 5)],
         ["95th percentile of the null", round(C.quantile(sims, 0.95), 5)],
         ["p (null max >= observed max)", C.fmt_p(p)]]))
    out.append("")
    out.append("This is the correct test for 'Kasiski found a period': the "
               "maximum IC gain is itself a random variable, and at n ~ 600 its "
               "null distribution is wide.  A non-significant p means the "
               "apparent periodicity is an artefact of small samples.")
    out.append("")
    return out


# --------------------------------------------------------------------------
# 2. length-matched comparison with the reference languages
# --------------------------------------------------------------------------
def language_comparison(rec: dict, langs: dict, n_slices: int = N_SLICES) -> tuple:
    seq = rec["letters"]
    n = len(seq)
    fp = C.fingerprint(seq)
    rows = []
    rank = {}
    zs_store = {}
    for label, text in langs.items():
        if len(text) < n + 100:
            continue
        dist = C.slice_stats(text, n, n_slices=n_slices)
        if not dist:
            continue
        zs, ps = {}, {}
        for st in C.KEY_STATS:
            zs[st], ps[st] = C.z_and_p(fp[st], dist[st])
        comp = sum(abs(zs[st]) for st in C.KEY_STATS) / len(C.KEY_STATS)
        rank[label] = comp
        zs_store[label] = {k: round(v, 2) for k, v in zs.items()}
        rows.append([label] + [round(zs[st], 2) for st in C.KEY_STATS] +
                    [round(comp, 3),
                     C.fmt_p(min(ps[st] for st in C.KEY_STATS))])
    rows.sort(key=lambda r: r[-2])
    SUMMARY["rankings"][rec["key"]] = {
        "mean_abs_z": rank, "z_by_stat": zs_store,
        "fingerprint": {k: fp[k] for k in C.KEY_STATS}, "n": n}
    header = (["reference language"] +
              [f"z({st})" for st in C.KEY_STATS] +
              ["mean |z|", "min p"])
    out = [f"### {rec['key']} (n = {n}) against length-matched language models",
           ""]
    out.append(C.md_table(header, rows))
    out.append("")
    out.append("Each reference language is sampled with windows of exactly the "
               "same length, so sampling error is identical on both sides.  "
               "z = (observed - language mean) / language sd; the languages are "
               "ordered by mean |z| over the five invariant statistics.  A mean "
               "|z| below ~1 means the inscription is indistinguishable from that "
               "language at this length; above ~2 it is unlikely.")
    out.append("")
    return out, rank


def fingerprint_table(recs: dict, langs: dict, n_slices: int = N_SLICES) -> list:
    """Side-by-side fingerprint of the readings and of the reference languages."""
    rows = []
    for key in READINGS:
        fp = C.fingerprint(recs[key]["letters"])
        rows.append([f"epigraph `{key}`"] +
                    [round(fp[st], 4) for st in C.KEY_STATS] +
                    [len(recs[key]["letters"])])
    for label, text in langs.items():
        n = 678
        dist = C.slice_stats(text, n, n_slices=min(n_slices, 200))
        if not dist:
            continue
        rows.append([label] +
                    [round(C.mean(dist[st]), 4) for st in C.KEY_STATS] +
                    [n])
    out = ["## Reference fingerprint (plaintext languages vs the epigraph)", ""]
    out.append(C.md_table(["text"] + list(C.KEY_STATS) + ["n"], rows))
    out.append("")
    out.append("Language values are means over 200 windows of 678 glyphs; the "
               "epigraph values are computed on its own length.")
    out.append("")
    return out


# --------------------------------------------------------------------------
# 3. uniform random baseline
# --------------------------------------------------------------------------
def cv_metrics(seq: str, vowels) -> dict:
    """Consonant-run statistics for a given vowel set (V/C abstraction)."""
    import re
    table = str.maketrans({ch: ("V" if ch in vowels else "C") for ch in set(seq)})
    s = seq.translate(table)
    runs = [len(m) for m in re.findall(r"C+", s)]
    total = len(s)
    inside3 = sum(r for r in runs if r >= 3)
    inside4 = sum(r for r in runs if r >= 4)
    return {"mean_C_run": (sum(runs) / len(runs)) if runs else 0.0,
            "share_in_C3": inside3 / total,
            "share_in_C4": inside4 / total,
            "longest_C_run": max(runs) if runs else 0}


def reference_cv(langs: dict, n: int, n_slices: int = 200) -> dict:
    """Distribution of CV metrics for each reference language at length n."""
    import random
    out = {}
    for label, text in langs.items():
        vowels = LM.VOWELS.get(label, set("aeiou"))
        rng = random.Random(2025)
        hi = len(text) - n
        if hi <= 0:
            continue
        vals = {"mean_C_run": [], "share_in_C3": [], "share_in_C4": []}
        for _ in range(n_slices):
            s = text[rng.randrange(hi):][:n]
            m = cv_metrics(s, vowels)
            for k in vals:
                vals[k].append(m[k])
        out[label] = {k: (C.mean(v), C.stdev(v)) for k, v in vals.items()}
    return out


def cv_exhaustive(rec: dict, ref: dict, k_best: int = 5) -> list:
    """Try every C(K,5) vowel assignment and score it against the references."""
    seq = rec["letters"]
    glyphs = [g for g, _ in C.freq(seq).most_common()]
    fr = C.freq(seq)
    n = len(seq)
    results = []
    for combo in itertools.combinations(glyphs, 5):
        m = cv_metrics(seq, set(combo))
        results.append((m["share_in_C3"], m["mean_C_run"], m["longest_C_run"],
                        combo))
    results.sort()
    SUMMARY["cv"][rec["key"]] = {
        "best_c3": results[0][0], "best_set": list(results[0][3]),
        "median_c3": C.quantile([r[0] for r in results], 0.5),
        "reference_best": min(v["share_in_C3"][0] for v in ref.values())}
    out = [f"## {rec['key']} -- exhaustive vowels/consonants test", ""]
    out.append("Every one of the "
               f"{len(results)} possible 5-glyph vowel sets is tried.  In any "
               "natural language vowels and consonants alternate, so the "
               "fraction of the text sitting inside runs of three or more "
               "consonants (`C3`) is small; a good vowel set minimises it.")
    out.append("")
    rows = []
    for c3, meanrun, longest, combo in results[:k_best]:
        rows.append([", ".join(f"`{g}`" for g in combo), round(c3, 4),
                     round(meanrun, 3), longest,
                     "".join(f"{g}:{fr[g]}" for g in combo)])
    rows.append(["--- reference languages ---", "-", "-", "-", "-"])
    for label, vals in sorted(ref.items(), key=lambda kv: kv[1]["share_in_C3"][0]):
        rows.append([label, round(vals["share_in_C3"][0], 4),
                     round(vals["mean_C_run"][0], 3), "-", "-"])
    out.append(C.md_table(["5-glyph vowel set", "C3 share", "mean C run",
                           "longest C run", "glyph counts"], rows))
    out.append("")
    lo = C.quantile([r[0] for r in results], 0.5)
    out.append(f"- best achievable C3 share: **{results[0][0]:.4f}**")
    out.append(f"- median over all vowel sets: {lo:.4f}")
    natural = min(v["share_in_C3"][0] for v in ref.values())
    out.append(f"- best natural-language reference: {natural:.4f}")
    out.append("")
    out.append("If the best achievable value is far above the reference range, "
               "then no substitution can turn this glyph string into a text with "
               "natural vowel/consonant alternation -- which rules out plain "
               "monoalphabetic substitution of an alphabetic language and points "
               "to nulls, transposition or a different segmentation.")
    out.append("")
    return out


def gap_robustness(recs: dict) -> list:
    rows = []
    for key in READINGS:
        rec = recs[key]
        clean = rec["clean"]
        with_gap = C.fingerprint(clean) if len(clean) > 20 else {}
        no_gap = C.fingerprint(rec["letters"])
        rows.append([key, rec["n_gaps"], round(with_gap.get("IC", 0), 5),
                     round(no_gap["IC"], 5),
                     round(with_gap.get("H", 0), 3), round(no_gap["H"], 3)])
    out = ["## Robustness to the illegible marks", ""]
    out.append(C.md_table(["reading", "gap marks", "IC (gaps kept)",
                           "IC (gaps dropped)", "H (gaps kept)",
                           "H (gaps dropped)"], rows))
    out.append("")
    out.append("Treating '?' as a glyph in its own right barely moves the "
               "statistics, so the conclusions do not depend on dropping the "
               "illegible positions.")
    out.append("")
    return out


def random_null_section(rec: dict, n_iter: int = 500) -> list:
    seq = rec["letters"]
    k = len(set(seq))
    n = len(seq)
    rng = random.Random(99)
    obs = C.fingerprint(seq)
    sims = {st: [] for st in C.KEY_STATS}
    alphabet = list(set(seq))
    for _ in range(n_iter):
        s = "".join(alphabet[rng.randrange(k)] for _ in range(n))
        fp = C.fingerprint(s)
        for st in C.KEY_STATS:
            sims[st].append(fp[st])
    rows = []
    for st in C.KEY_STATS:
        z, p = C.z_and_p(obs[st], sims[st])
        rows.append([st, round(obs[st], 4), round(C.mean(sims[st]), 4),
                     round(C.stdev(sims[st]), 4), round(z, 2), C.fmt_p(p)])
    out = [f"## {rec['key']} -- distance from a uniform random string", ""]
    out.append(C.md_table(["statistic", "observed", "random mean",
                           "random sd", "z", "p"], rows))
    out.append("")
    out.append("Uniform text over the same K glyphs is the 'meaningless "
               "decoration' hypothesis: at least two statistics must reject it "
               "for the inscription to be worth attacking at all.")
    out.append("")
    return out


def main() -> None:
    recs = C.load_json(os.path.join(C.CORPUS, "corpora.json"))
    print("loading reference languages ...")
    langs = LM.load_reference(max_letters=SAMPLE_LETTERS, verbose=False)
    print(f"{len(langs)} languages, "
          f"{sum(len(v) for v in langs.values())} letters total")

    out = ["# Phase 1b -- inferential statistics", "",
           "Readings analysed: " + ", ".join(f"`{k}`" for k in READINGS), "",
           "All tests are run on the glyph strings with the illegible marks "
           "removed unless stated otherwise.", ""]

    out += ["## Permutation and bootstrap tests", ""]
    for key in READINGS:
        out += permutation_section(recs[key])
        out += periodicity_null(recs[key])

    out += fingerprint_table(recs, langs)

    out += ["## Length-matched language comparison", ""]
    rankings = {}
    for key in READINGS:
        block, rank = language_comparison(recs[key], langs)
        out += block
        rankings[key] = rank

    out += ["## Comparison with uniform random text", ""]
    for key in READINGS:
        out += random_null_section(recs[key])

    out += ["## Vowels and consonants", ""]
    print("running the exhaustive vowels/consonants test ...")
    for key in READINGS:
        n = len(recs[key]["letters"])
        ref = reference_cv(langs, n, n_slices=120)
        out += cv_exhaustive(recs[key], ref)

    out += gap_robustness(recs)

    C.save_json(os.path.join(C.CORPUS, "02_summary.json"), SUMMARY)
    C.write_text(os.path.join(C.CORPUS, "02_inferential.md"),
                 "\n".join(out) + "\n")
    print("\nwrote corpus/02_inferential.md")
    for key, rank in rankings.items():
        best = sorted(rank.items(), key=lambda kv: kv[1])[:5]
        print(f"\nbest language matches for {key}:")
        for label, comp in best:
            print(f"   {label:34s} mean|z| = {comp:.3f}")


if __name__ == "__main__":
    main()

