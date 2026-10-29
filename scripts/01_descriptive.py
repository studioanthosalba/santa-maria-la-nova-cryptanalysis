# -*- coding: utf-8 -*-
"""01_descriptive.py -- Phase 1a: descriptive statistics of the epigraph.

For the three independent readings that matter (Palma's two glyph strings and
the 33-line Gemini transcription) the script computes:

* unigram table, Index of Coincidence, Shannon entropy, redundancy,
  effective alphabet size, chi-square against uniformity;
* bigram / trigram inventories, repeat rates, conditional entropies;
* word-level structure (only ``palma_A`` preserves word separators):
  length distribution, hapax ratio, pattern collisions (isomorphs),
  word-internal palindromes;
* character-level palindromes and ABABA-type motifs (the ``DEDED`` motif that
  first attracted attention);
* positional statistics (line initials/finals, acrostic check, per-line IC);
* Friedman period profile and Kasiski divisors, i.e. the classical tests for
  transposition / polyalphabetic ciphers;
* distribution of the illegible runs.

Output: ``corpus/01_descriptive.md``.
"""

from __future__ import annotations

import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C

C.utf8_stdout()

KEY_READINGS = ["palma_A", "palma_B", "gemini_full"]


# --------------------------------------------------------------------------
# small helpers
# --------------------------------------------------------------------------
def pct(x: int, n: int) -> float:
    return 100.0 * x / n if n else 0.0


def top_rows(counter: Counter, n: int, total: int) -> list:
    rows = []
    cum = 0
    for sym, c in counter.most_common(n):
        cum += c
        rows.append([f"`{sym}`", c, round(pct(c, total), 2),
                     round(pct(cum, total), 2)])
    return rows


def gram_str(gram) -> str:
    return "".join(gram)


def unigram_section(rec: dict) -> list:
    letters = rec["letters"]
    n = len(letters)
    fr = C.freq(letters)
    k = len(fr)
    h = C.entropy(letters)
    hm = C.entropy_max(k)
    x2, df, p = C.chi_square_uniform(letters)
    out = [f"## {rec['key']} -- single symbols", ""]
    out.append(C.md_table(
        ["statistic", "value"],
        [["length n", n], ["distinct glyphs K", k],
         ["IC", round(C.ic(letters), 5)],
         ["IC x 26 (Palma's scale)", round(C.ic26(letters), 3)],
         ["IC x K (1.0 = random over K)", round(C.ic(letters) * k, 3)],
         ["entropy H (bits)", round(h, 4)],
         ["H_max = log2 K", round(hm, 3)],
         ["redundancy 1 - H/H_max", round(1 - h / hm, 3) if hm else 0],
         ["effective alphabet 2^H", round(2 ** h, 2)],
         ["most frequent glyph share %",
          round(pct(fr.most_common(1)[0][1], n), 2)],
         ["top-5 share %",
          round(pct(sum(c for _, c in fr.most_common(5)), n), 2)],
         ["hapax glyphs (count = 1)",
          sum(1 for c in fr.values() if c == 1)],
         ["chi-square vs uniform", round(x2, 1)],
         ["df", df], ["p(chi2 >= x)", C.fmt_p(p)]]))
    out.append("")
    out.append(C.md_table(["glyph", "count", "%", "cumulative %"],
                          top_rows(fr, min(k, 26), n)))
    out.append("")
    return out


def ngram_section(rec: dict) -> list:
    letters = rec["letters"]
    out = [f"## {rec['key']} -- n-grams", ""]
    rows = []
    for n in (2, 3, 4):
        g = C.ngrams(letters, n)
        tot = sum(g.values())
        top = g.most_common(1)[0]
        top10 = sum(c for _, c in g.most_common(10))
        rows.append([n, len(g), round(tot / len(g), 2),
                     f"`{gram_str(top[0])}` ({top[1]})",
                     round(C.repeat_rate(letters, n), 4),
                     round(pct(top10, tot), 1),
                     round(C.conditional_entropy(letters, n - 1), 3)])
    out.append(C.md_table(
        ["n", "distinct", "mean count", "most frequent", "repeat rate",
         "top-10 share %", "H(X|prev)"], rows))
    out.append("")
    out.append("Repeat rate = share of n-gram tokens occurring more than once; "
               "in a random text over K glyphs it is close to 0.")
    out.append("")
    for n in (2, 3):
        g = C.ngrams(letters, n)
        tot = sum(g.values())
        rows = [[f"`{gram_str(gr)}`", c, round(pct(c, tot), 2)]
                for gr, c in g.most_common(10)]
        out.append(f"Top {n}-grams of {rec['key']}:")
        out.append("")
        out.append(C.md_table([f"{n}-gram", "count", "%"], rows))
        out.append("")
    return out


def word_section(rec: dict) -> list:
    toks = [t for t in rec["tokens"] if t.replace(C.GAP, "")]
    out = [f"## {rec['key']} -- word structure", ""]
    if len(toks) < 20:
        out.append("*skipped: this reading preserves no word separators*")
        out.append("")
        return out
    lens = [len(t) for t in toks]
    n = len(toks)
    fr = C.freq(toks)
    hapax = sum(1 for c in fr.values() if c == 1)
    dist = Counter(lens)
    out.append(C.md_table(
        ["statistic", "value"],
        [["tokens", n], ["mean length", round(C.mean(lens), 2)],
         ["sd length", round(C.stdev(lens), 2)],
         ["min / max length", f"{min(lens)} / {max(lens)}"],
         ["hapax tokens", hapax],
         ["types / tokens", round(len(fr) / n, 3)],
         ["1-2 letter tokens %",
          round(pct(sum(1 for x in lens if x <= 2), n), 1)],
         ["tokens containing an illegible mark",
          sum(1 for t in toks if C.GAP in t)]]))
    out.append("")
    out.append(C.md_table(["length", "tokens", "%"],
                          [[L, dist[L], round(pct(dist[L], n), 1)]
                           for L in sorted(dist)]))
    out.append("")
    out.append("Longest tokens: " + ", ".join(
        f"`{t}`" for t in sorted(toks, key=len, reverse=True)[:8]))
    out.append("")
    by_pat = {}
    for t in sorted(set(toks)):
        by_pat.setdefault(C.pattern(t), []).append(t)
    coll = {p: v for p, v in by_pat.items() if len(v) > 1}
    out.append(f"Isomorph collisions (distinct tokens sharing a repetition "
               f"pattern): **{len(coll)}** patterns covering "
               f"{sum(len(v) for v in coll.values())} tokens.  They are the "
               "raw material of pattern-based crib attacks.")
    out.append("")
    rows = [[p, ", ".join(f"`{t}`" for t in sorted(v)[:6])]
            for p, v in sorted(coll.items(),
                               key=lambda kv: (-len(kv[1]), kv[0]))[:12]]
    if rows:
        out.append(C.md_table(["pattern", "tokens"], rows))
        out.append("")
    pals = sorted({t for t in toks if len(t) >= 3 and t == t[::-1]})
    out.append("Word-level palindromes: " +
               (", ".join(f"`{t}`" for t in pals) if pals else "*none*"))
    out.append("")
    return out


def motif_section(rec: dict, n_iter: int = 2000) -> list:
    """Palindromes and ABABA motifs, with a permutation null."""
    import random
    seq = rec["letters"]
    rng = random.Random(2024)

    def scan(s):
        pals = []
        for i in range(len(s)):
            for L in range(4, 9):
                sub = s[i:i + L]
                if len(sub) == L and sub == sub[::-1]:
                    pals.append(sub)
        aba = sum(1 for i in range(len(s) - 4)
                  if len(set(s[i:i + 5])) == 2
                  and s[i] == s[i + 2] == s[i + 4]
                  and s[i + 1] == s[i + 3] and s[i] != s[i + 1])
        return len(pals), aba

    obs_pal, obs_aba = scan(seq)
    sims_pal, sims_aba = [], []
    letters = list(seq)
    for _ in range(n_iter):
        rng.shuffle(letters)
        p, a = scan(letters)
        sims_pal.append(p)
        sims_aba.append(a)
    p_pal = (1 + sum(1 for v in sims_pal if v >= obs_pal)) / (1 + n_iter)
    p_aba = (1 + sum(1 for v in sims_aba if v >= obs_aba)) / (1 + n_iter)
    out = [f"## {rec['key']} -- palindromes and ABABA motifs", ""]
    out.append(C.md_table(
        ["quantity", "observed", "null mean", "null sd", "p (>= observed)"],
        [["palindromic runs (len 4-8)", obs_pal, round(C.mean(sims_pal), 2),
          round(C.stdev(sims_pal), 2), C.fmt_p(p_pal)],
         ["ABABA motifs (len 5)", obs_aba, round(C.mean(sims_aba), 2),
          round(C.stdev(sims_aba), 2), C.fmt_p(p_aba)]]))
    out.append("")
    hits = []
    for i in range(len(seq) - 4):
        w = seq[i:i + 5]
        if len(set(w)) == 2 and w[0] == w[2] == w[4] and w[1] == w[3] and w[0] != w[1]:
            hits.append((i, w))
    out.append("Positions of ABABA motifs: " +
               (", ".join(f"`{w}`@{i}" for i, w in hits) if hits else "*none*"))
    out.append("")
    return out


def positional_section(rec: dict) -> list:
    """Line geometry, line-initial/final glyphs, per-line IC, acrostic check."""
    lines = [C.normalize_cipher(li) for li in rec["lines"]]
    lines = [li for li in lines if len(li) >= 2]
    out = [f"## {rec['key']} -- positions", ""]
    if len(lines) < 3:
        out.append("*skipped: this reading is a single continuous string*")
        out.append("")
        return out
    lens = [len(li) for li in lines]
    ics = [C.ic(li) for li in lines]
    out.append(C.md_table(
        ["statistic", "value"],
        [["lines", len(lines)], ["mean line length", round(C.mean(lens), 1)],
         ["sd line length", round(C.stdev(lens), 1)],
         ["mean per-line IC", round(C.mean(ics), 4)],
         ["lines with IC = 0 (all glyphs distinct)",
          sum(1 for v in ics if v == 0)]]))
    out.append("")
    rows = [[i + 1, len(li), f"`{li[0]}`", f"`{li[-1]}`",
             C.GAP in li] for i, li in enumerate(lines)]
    out.append(C.md_table(["line", "glyphs", "first", "last",
                           "has gap mark"], rows))
    out.append("")
    initials = "".join(li[0] for li in lines)
    finals = "".join(li[-1] for li in lines)
    out.append(f"- line initials: `{initials}` -- {len(set(initials))} distinct "
               f"over {len(initials)} lines")
    out.append(f"- line finals:  `{finals}` -- {len(set(finals))} distinct")
    out.append("")
    # crude acrostic test: are initials concentrated on few glyphs?
    fr = C.freq(initials)
    out.append("A text hiding an acrostic would show repeated line initials; "
               f"here the most frequent initial covers "
               f"{fr.most_common(1)[0][1]}/{len(initials)} lines.")
    out.append("")
    return out


def periodicity_section(rec: dict, max_period: int = 20) -> list:
    seq = rec["letters"]
    out = [f"## {rec['key']} -- periodicity tests", ""]
    prof = C.ic_by_period(seq, max_period)
    rows = [[p["period"], round(p["ic"], 5),
             round(p["ic"] * 26, 3), round(p["delta"], 5)] for p in prof]
    out.append(C.md_table(["period k", "pooled IC", "IC x 26", "delta vs global"],
                          rows))
    out.append("")
    best = max(prof, key=lambda p: p["delta"])
    out.append(f"Largest IC gain at k = **{best['period']}** "
               f"(+{best['delta']:.5f}); a monoalphabetic text shows no peak, "
               "a periodic polyalphabetic one peaks at the key length.")
    out.append("")
    fr = C.friedman_chi2(seq)
    out.append(C.md_table(
        ["Friedman quantity", "value"],
        [["kappa", round(fr["kappa"], 4)], ["chi2", round(fr["chi2"], 2)],
         ["df", fr["df"]], ["p(chi2 >= x)", C.fmt_p(fr["p_value"])]]))
    out.append("")
    kas = C.kasiski(seq, 3)
    out.append(f"Kasiski (repeated trigrams): {kas['n_repeats']} repeat pairs, "
               f"GCD of distances = {kas['gcd']}, most frequent divisors: " +
               ", ".join(f"{d}({c})" for d, c in kas["divisors"][:6]))
    out.append("")
    return out


def gap_section(rec: dict) -> list:
    seq = rec["clean"]
    runs = [len(r) for r in seq.split("#") if r == ""]
    # run-length encoding of the gap marks
    lengths = []
    cur = 0
    for ch in seq:
        if ch == C.GAP:
            cur += 1
        elif cur:
            lengths.append(cur)
            cur = 0
    if cur:
        lengths.append(cur)
    out = [f"## {rec['key']} -- illegible marks", ""]
    if not lengths:
        out.append("*no illegible marks in this reading*")
        out.append("")
        return out
    dist = Counter(lengths)
    out.append(C.md_table(
        ["statistic", "value"],
        [["gap marks", sum(lengths)], ["runs", len(lengths)],
         ["mean run", round(C.mean(lengths), 2)],
         ["max run", max(lengths)],
         ["share of the string %",
          round(pct(sum(lengths), len(seq)), 1)]]))
    out.append("")
    out.append(C.md_table(["run length", "count"],
                          [[L, dist[L]] for L in sorted(dist)]))
    out.append("")
    return out


def main() -> None:
    recs = C.load_json(os.path.join(C.CORPUS, "corpora.json"))
    lines = C.load_json(os.path.join(C.CORPUS, "lines.json"))
    out = ["# Phase 1 -- descriptive statistics of the epigraph", "",
           "Readings analysed: " + ", ".join(f"`{k}`" for k in KEY_READINGS),
           ""]
    for key in KEY_READINGS:
        rec = dict(recs[key])
        rec["lines"] = lines[key]
        out += ["---", "", f"# Reading `{key}`", "",
                f"*{rec['provenance']}*", ""]
        out += unigram_section(rec)
        out += ngram_section(rec)
        out += word_section(rec)
        out += motif_section(rec)
        out += positional_section(rec)
        out += periodicity_section(rec)
        out += gap_section(rec)
    C.write_text(os.path.join(C.CORPUS, "01_descriptive.md"),
                 "\n".join(out) + "\n")
    print("wrote corpus/01_descriptive.md")
    for key in KEY_READINGS:
        rec = recs[key]
        print(f"{key:14s} n={rec['n_letters']:4d} K={rec['K']:2d} "
              f"IC={rec['ic']:.4f} IC26={rec['ic26']:.3f} "
              f"H={rec['entropy']:.3f} ICK={rec['ic'] * rec['K']:.3f}")


if __name__ == "__main__":
    main()


