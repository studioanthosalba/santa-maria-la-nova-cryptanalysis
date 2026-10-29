# -*- coding: utf-8 -*-
"""common.py -- shared utilities for the Santa Maria la Nova epigraph project.

The epigraph of the Turbolo chapel (Naples) is a ~600-glyph inscription written
in an otherwise unknown alphabet.  This module holds every reusable primitive
of the analysis pipeline: text normalisation, transcription alignment, and the
descriptive / inferential statistics used by the numbered scripts.

Only the standard library is required.  scipy is used when importable (exact
chi-square tail probabilities) with a pure-python fallback otherwise, so the
pipeline is reproducible on a bare interpreter.
"""

from __future__ import annotations

import json
import math
import os
import random
import re
import sys
import unicodedata
from collections import Counter

# --------------------------------------------------------------------------
# paths
# --------------------------------------------------------------------------
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCES = os.path.join(BASE, "sources")
CORPUS = os.path.join(BASE, "corpus")
REPORT = os.path.join(BASE, "report")
REPO = os.path.join(SOURCES, "MaLaNova-master")
REPO_CORPORA = os.path.join(REPO, "corpora")

#: marker used for an illegible glyph (the '?' of Palma's transcriptions)
GAP = "#"

#: separator characters that carry no phonological information
SEPARATORS = set(" .,;:/-|_()[]{}\t\r\n\"'`~*+=<>!?0123456789")


def utf8_stdout() -> None:
    """Make Greek/Czech output survive a cp1252 Windows console."""
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # pragma: no cover - old interpreters
        pass


def stable_hash(text: str) -> int:
    """Deterministic seed from a string (``hash()`` is salted per process)."""
    import zlib
    return zlib.crc32(text.encode("utf-8")) % 100000


def read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        return fh.read()


def write_text(path: str, text: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def save_json(path: str, obj) -> None:
    write_text(path, json.dumps(obj, ensure_ascii=False, indent=1, sort_keys=True))


def load_json(path: str):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


# --------------------------------------------------------------------------
# normalisation
# --------------------------------------------------------------------------
#: characters of historical corpora that NFD does not decompose usefully
SPECIAL_MAP = {
    "æ": "ae", "Æ": "ae", "œ": "oe", "Œ": "oe", "ß": "ss", "ø": "o",
    "Ø": "o", "đ": "d", "Đ": "d", "ð": "d", "Ð": "d", "ł": "l", "Ł": "l",
    "þ": "th", "Þ": "th", "ı": "i", "ȷ": "j", "ſ": "s", "ʒ": "z",
    "ǧ": "g", "ǫ": "o", "ȩ": "e", "ę": "e", "ą": "a", "ų": "u", "ū": "u",
    "ō": "o", "ā": "a", "ē": "e", "ī": "i", "ǎ": "a", "ě": "e", "ǐ": "i",
    "ǒ": "o", "ǔ": "u", "ř": "r", "Ř": "r", "č": "c", "Č": "c", "š": "s",
    "Š": "s", "ž": "z", "Ž": "z", "ť": "t", "Ť": "t", "ď": "d", "Ď": "d",
    "ň": "n", "Ň": "n", "ů": "u", "Ů": "u",
}


def strip_diacritics(s: str) -> str:
    """ASCII-fold a string (used for the Old Czech / Old Hungarian corpora)."""
    s = "".join(SPECIAL_MAP.get(ch, ch) for ch in s)
    return "".join(ch for ch in unicodedata.normalize("NFD", s)
                   if unicodedata.category(ch) != "Mn")


def normalize_latin(s: str) -> str:
    """Lower-case ASCII-folded letters only."""
    s = strip_diacritics(s.lower())
    return re.sub(r"[^a-z]", "", s)


def normalize_cipher(s: str, gap: str = GAP) -> str:
    """Normalise a transcription of the epigraph.

    Every non letter is dropped except '?' which becomes ``gap`` (illegible
    glyph).  Case is folded; the Greek glyph labels used by Palma's
    ``soluzione.txt`` are kept as they are.
    """
    out = []
    for ch in s:
        if ch == "?":
            out.append(gap)
        elif ch.isspace() or ch in SEPARATORS:
            continue
        elif ch.isalpha():
            out.append(ch.lower())
    return "".join(out)


def is_greek(s: str) -> bool:
    return bool(s) and sum(1 for ch in s if "\u0370" <= ch <= "\u03ff") > len(s) / 2


def words(s: str) -> list:
    """Split a transcription into word tokens, dropping empty / gap-only ones."""
    toks = re.split(r"[\s.,;:]+", s)
    return [t for t in toks if any(c.isalpha() for c in t)]


def word_tokens(s: str, gap: str = GAP) -> list:
    """Word tokens cleaned to letters+gap only."""
    out = []
    for t in words(s):
        c = normalize_cipher(t, gap)
        if c:
            out.append(c)
    return out



# --------------------------------------------------------------------------
# descriptive statistics
# --------------------------------------------------------------------------
def freq(seq) -> Counter:
    return Counter(seq)


def ngrams(seq, n: int) -> Counter:
    return Counter(tuple(seq[i:i + n]) for i in range(len(seq) - n + 1))


def ic(seq) -> float:
    """Friedman's index of coincidence (n(n-1) denominator)."""
    n = len(seq)
    if n < 2:
        return 0.0
    return sum(c * (c - 1) for c in Counter(seq).values()) / (n * (n - 1))


def ic26(seq) -> float:
    """Palma's "normalized IC" = IC * 26 (so that random text ~ 1.0)."""
    return ic(seq) * 26.0


def ic_random(k: int) -> float:
    """Expected IC of a uniform random text over ``k`` symbols: 1/k."""
    return 1.0 / k if k else 0.0


def entropy(seq) -> float:
    n = len(seq)
    if n == 0:
        return 0.0
    tot = 0.0
    for c in Counter(seq).values():
        p = c / n
        tot -= p * math.log2(p)
    return tot


def entropy_max(k: int) -> float:
    return math.log2(k) if k > 1 else 0.0


def conditional_entropy(seq, order: int = 1) -> float:
    """H(X_t | previous ``order`` symbols), in bits."""
    if len(seq) <= order + 1:
        return 0.0
    ctx = ngrams(seq, order)
    joint = ngrams(seq, order + 1)
    total = sum(joint.values())
    h = 0.0
    for gram, c in joint.items():
        h -= (c / total) * math.log2(c / ctx[gram[:order]])
    return h


def redundancy(seq) -> float:
    k = len(set(seq))
    hm = entropy_max(k)
    return 0.0 if hm == 0 else 1.0 - entropy(seq) / hm


def repeat_rate(seq, n: int) -> float:
    """Share of ``n``-grams that occur more than once."""
    g = ngrams(seq, n)
    if not g:
        return 0.0
    return sum(c for c in g.values() if c > 1) / sum(g.values())


def type_token_ratio(seq) -> float:
    return len(set(seq)) / len(seq) if seq else 0.0


def chi_square_uniform(seq) -> tuple:
    """Pearson chi-square of the unigram distribution against uniformity."""
    n = len(seq)
    obs = list(Counter(seq).values())
    k = len(obs)
    if k < 2 or n == 0:
        return 0.0, max(k - 1, 1), 1.0
    exp = n / k
    x2 = sum((o - exp) ** 2 / exp for o in obs)
    return x2, k - 1, chi2_sf(x2, k - 1)


def chi_square(obs_counts, exp_probs) -> tuple:
    """Pearson chi-square of observed counts against expected probabilities.

    ``exp_probs`` maps symbol->probability; probability mass on symbols that
    were never observed is still counted in chi-square (they are real evidence
    against the hypothesis), and observed symbols missing from the reference
    are pooled into a single neutral cell.
    """
    n = sum(obs_counts.values())
    if n == 0:
        return 0.0, 0, 1.0
    x2 = 0.0
    cells = 0
    other = 0
    for sym, c in obs_counts.items():
        p = exp_probs.get(sym, 0.0)
        if p <= 0:
            other += c
        else:
            x2 += (c - n * p) ** 2 / (n * p)
            cells += 1
    if other:
        cells += 1  # pooled "symbol absent from the reference" cell
    for sym, p in exp_probs.items():
        if p > 0 and sym not in obs_counts:
            x2 += n * p
            cells += 1
    df = max(cells - 1, 1)
    return x2, df, chi2_sf(x2, df)


# --------------------------------------------------------------------------
# chi-square tail probability (scipy when available, else own gamma code)
# --------------------------------------------------------------------------
try:  # pragma: no cover - depends on the environment
    from scipy import stats as _scipy_stats
except Exception:  # pragma: no cover
    _scipy_stats = None


def _gammainc_q(a: float, x: float) -> float:
    """Regularized upper incomplete gamma Q(a, x) -- Numerical Recipes style."""
    if x < 0 or a <= 0:
        return float("nan")
    if x == 0:
        return 1.0
    gln = math.lgamma(a)
    if x < a + 1.0:  # series for P(a,x)
        ap = a
        total = 1.0 / a
        delta = total
        for _ in range(1000):
            ap += 1.0
            delta *= x / ap
            total += delta
            if abs(delta) < abs(total) * 1e-15:
                break
        return 1.0 - total * math.exp(-x + a * math.log(x) - gln)
    tiny = 1e-300  # continued fraction for Q(a,x)
    b = x + 1.0 - a
    c = 1.0 / tiny
    d = 1.0 / b
    h = d
    for i in range(1, 1000):
        an = -i * (i - a)
        b += 2.0
        d = an * d + b
        if abs(d) < tiny:
            d = tiny
        c = b + an / c
        if abs(c) < tiny:
            c = tiny
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < 1e-15:
            break
    return math.exp(-x + a * math.log(x) - gln) * h


def chi2_sf(x: float, df: int) -> float:
    """P(chi2_df >= x)."""
    if df <= 0:
        return 1.0
    if _scipy_stats is not None:
        return float(_scipy_stats.chi2.sf(x, df))
    return max(0.0, min(1.0, _gammainc_q(df / 2.0, x / 2.0)))


def norm_sf(z: float) -> float:
    """P(Z >= z) for a standard normal."""
    return 0.5 * math.erfc(z / math.sqrt(2.0))


def mean(xs):
    xs = list(xs)
    return sum(xs) / len(xs) if xs else 0.0


def stdev(xs):
    xs = list(xs)
    if len(xs) < 2:
        return 0.0
    m = mean(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - 1))


def quantile(xs, q: float):
    """Linear-interpolated quantile (q in [0,1]) of an unsorted sequence."""
    ys = sorted(xs)
    if not ys:
        return float("nan")
    pos = q * (len(ys) - 1)
    lo = int(math.floor(pos))
    hi = min(lo + 1, len(ys) - 1)
    return ys[lo] + (ys[hi] - ys[lo]) * (pos - lo)


# --------------------------------------------------------------------------
# inferential statistics
# --------------------------------------------------------------------------
def monte_carlo_ic(seq, n_iter: int = 10000, seed: int = 12345) -> dict:
    """Permutation test: is the observed IC compatible with a random shuffle?

    H0: the sequence is exchangeable, i.e. its only structure is the unigram
    distribution (a weak null: it already fixes the alphabet and its skew).
    The test therefore asks whether the *serial* structure of the text is more
    repetitive than chance.
    """
    rng = random.Random(seed)
    obs = ic(seq)
    letters = list(seq)
    ge = 0
    sims = []
    for _ in range(n_iter):
        rng.shuffle(letters)
        v = ic(letters)
        sims.append(v)
        if v >= obs:
            ge += 1
    mu, sd = mean(sims), stdev(sims)
    return {"observed": obs, "p_value": (1 + ge) / (1 + n_iter),
            "null_mean": mu, "null_sd": sd, "n_iter": n_iter,
            "z": (obs - mu) / (sd or 1e-12)}


def bootstrap_ic(seq, n_iter: int = 5000, seed: int = 999) -> dict:
    """Non-parametric bootstrap CI of the IC (resampling characters)."""
    rng = random.Random(seed)
    n = len(seq)
    vals = []
    for _ in range(n_iter):
        sample = [seq[rng.randrange(n)] for _ in range(n)]
        vals.append(ic(sample))
    return {"observed": ic(seq), "mean": mean(vals), "sd": stdev(vals),
            "lo95": quantile(vals, 0.025), "hi95": quantile(vals, 0.975)}


def bootstrap_stat(seq, stat, n_iter: int = 5000, seed: int = 777) -> dict:
    """Generic bootstrap of an arbitrary statistic of the character sequence."""
    rng = random.Random(seed)
    n = len(seq)
    vals = []
    for _ in range(n_iter):
        sample = [seq[rng.randrange(n)] for _ in range(n)]
        vals.append(stat(sample))
    return {"observed": stat(seq), "mean": mean(vals), "sd": stdev(vals),
            "lo95": quantile(vals, 0.025), "hi95": quantile(vals, 0.975)}


def ic_by_period(seq, max_period: int = 20) -> list:
    """Friedman: IC of the sub-sequences at stride k.

    A monoalphabetic text keeps IC constant in k; a polyalphabetic one shows
    the IC rising towards the plaintext value exactly at k = key length.
    """
    out = []
    for k in range(1, max_period + 1):
        cols = [seq[i::k] for i in range(k)]
        num = 0.0
        den = 0.0
        for c in cols:
            m = len(c)
            if m < 2:
                continue
            num += sum(v * (v - 1) for v in Counter(c).values())
            den += m * (m - 1)
        val = (num / den) if den else 0.0
        out.append({"period": k, "ic": val, "delta": val - ic(seq)})
    return out


def friedman_chi2(seq) -> dict:
    """Friedman's kappa test (shift of coincidence) for monoalphabeticity."""
    n = len(seq)
    k = len(set(seq))
    if n < 3 or k < 2:
        return {"kappa": 0.0, "chi2": 0.0, "df": 0, "p_value": 1.0}
    kap = (k * ic(seq) - 1.0) / (k - 1.0)
    x2 = (k - 1.0) * (n - 1.0) * kap
    df = k - 1
    return {"kappa": kap, "chi2": x2, "df": df, "p_value": chi2_sf(x2, df)}


def kasiski(seq, n: int = 3, max_gap: int = 150) -> dict:
    """Kasiski examination: distances between repeated n-grams and their GCDs."""
    pos = {}
    for i in range(len(seq) - n + 1):
        pos.setdefault(seq[i:i + n], []).append(i)
    gaps = []
    for gram, ps in pos.items():
        if len(ps) < 2:
            continue
        for a, b in zip(ps, ps[1:]):
            d = b - a
            if 0 < d <= max_gap:
                gaps.append((d, gram))
    divisor_hits = Counter()
    for d, _ in gaps:
        for f in range(2, 21):
            if d % f == 0:
                divisor_hits[f] += 1
    return {"n_repeats": len(gaps), "gaps": gaps[:200],
            "divisors": divisor_hits.most_common(10),
            "gcd": _gcd_list([d for d, _ in gaps])}


def _gcd_list(xs) -> int:
    from math import gcd
    g = 0
    for x in xs:
        g = gcd(g, x)
    return g


# --------------------------------------------------------------------------
# word-shape helpers
# --------------------------------------------------------------------------
def pattern(word: str) -> str:
    """Canonical repetition pattern: 'stare' -> 'ABCDE', 'toto' -> 'ABAB'."""
    seen = {}
    out = []
    for ch in word:
        if ch not in seen:
            seen[ch] = chr(ord("A") + len(seen))
        out.append(seen[ch])
    return "".join(out)


def is_isomorph(a: str, b: str) -> bool:
    return len(a) == len(b) and pattern(a) == pattern(b)


#: alphabet of labels for canonical relabeling of long sequences
_LABELS = ("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")


def relabel(seq) -> str:
    """Canonical relabeling by order of first occurrence (relabel-invariant)."""
    seen = {}
    out = []
    for ch in seq:
        if ch not in seen:
            seen[ch] = _LABELS[len(seen) % len(_LABELS)]
        out.append(seen[ch])
    return "".join(out)


def longest_common_substring(a: str, b: str) -> tuple:
    """(length, start_in_a, start_in_b) of the longest common substring."""
    if not a or not b:
        return 0, 0, 0
    prev = [0] * (len(b) + 1)
    best, bi, bj = 0, 0, 0
    for i in range(1, len(a) + 1):
        cur = [0] * (len(b) + 1)
        ai = a[i - 1]
        for j in range(1, len(b) + 1):
            if ai == b[j - 1]:
                v = prev[j - 1] + 1
                cur[j] = v
                if v > best:
                    best, bi, bj = v, i - v, j - v
        prev = cur
    return best, bi, bj


def sorted_profile(seq, k: int) -> list:
    """Descending normalised frequency vector, zero-padded to length k.

    Invariant under any bijective relabeling of the alphabet, therefore the
    correct way to compare a ciphertext with a plaintext language model.
    """
    n = len(seq)
    vals = sorted((c / n for c in Counter(seq).values()), reverse=True)
    return vals + [0.0] * (k - len(vals))


def l1_profile_distance(p, q) -> float:
    return sum(abs(x - y) for x, y in zip(p, q))


def profile_map(seq_a, seq_b) -> dict:
    """Heuristic symbol correspondence by descending frequency rank.

    Two transcriptions of the same inscription label the glyphs with unrelated
    alphabets, so no symbol can be matched by name.  Since a substitution
    preserves the frequency order of the classes, the k-th most frequent symbol
    of one reading is a sensible prior for the k-th most frequent of the other.
    Used only to *initialise* an alignment that is then scored empirically.
    """
    fa = [s for s, _ in Counter(seq_a).most_common()]
    fb = [s for s, _ in Counter(seq_b).most_common()]
    return {s: fb[i] for i, s in enumerate(fa) if i < len(fb)}


def apply_map(seq, mapping, default: str = "-") -> str:
    return "".join(mapping.get(ch, default) for ch in seq)


def word_lengths(tokens) -> list:
    return [len(t) for t in tokens]


def levenshtein(a: str, b: str) -> int:
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1,
                           prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def align(a: str, b: str, match: float = 1.0, mismatch: float = -1.0,
          gap: float = -1.0) -> dict:
    """Needleman-Wunsch global alignment; returns columns and identity."""
    n, m = len(a), len(b)
    score = [[0.0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        score[i][0] = gap * i
    for j in range(1, m + 1):
        score[0][j] = gap * j
    for i in range(1, n + 1):
        ai = a[i - 1]
        for j in range(1, m + 1):
            s = match if ai == b[j - 1] else mismatch
            score[i][j] = max(score[i - 1][j - 1] + s,
                              score[i - 1][j] + gap,
                              score[i][j - 1] + gap)
    i, j = n, m
    cols = []
    while i > 0 or j > 0:
        if i > 0 and j > 0:
            s = match if a[i - 1] == b[j - 1] else mismatch
            if abs(score[i][j] - (score[i - 1][j - 1] + s)) < 1e-9:
                cols.append((a[i - 1], b[j - 1]))
                i, j = i - 1, j - 1
                continue
        if i > 0 and abs(score[i][j] - (score[i - 1][j] + gap)) < 1e-9:
            cols.append((a[i - 1], "-"))
            i -= 1
        else:
            cols.append(("-", b[j - 1]))
            j -= 1
    cols.reverse()
    same = sum(1 for x, y in cols if x == y and x != "-")
    return {"columns": cols, "identity": same / max(len(cols), 1),
            "n_columns": len(cols), "score": score[n][m]}


def confusion_matrix(pairs) -> Counter:
    """Count co-occurring symbol pairs (glyph confusion) from aligned columns."""
    return Counter(pairs)


# --------------------------------------------------------------------------
# reporting helpers
# --------------------------------------------------------------------------
def md_table(header, rows) -> str:
    out = ["| " + " | ".join(str(h) for h in header) + " |",
           "|" + "|".join("---" for _ in header) + "|"]
    for r in rows:
        out.append("| " + " | ".join(_fmt(c) for c in r) + " |")
    return "\n".join(out)


def _fmt(c) -> str:
    if isinstance(c, float):
        if c != c:  # NaN
            return "n/a"
        if c == 0:
            return "0"
        if abs(c) >= 1000 or abs(c) < 1e-3:
            return f"{c:.3e}"
        return f"{c:.4f}"
    return str(c)


def fmt_p(p: float) -> str:
    if p != p:
        return "n/a"
    if p < 1e-12:
        return "<1e-12"
    if p < 1e-4:
        return f"{p:.2e}"
    return f"{p:.4f}"


# --------------------------------------------------------------------------
# relabel-invariant fingerprint (the workhorse of the language comparison)
# --------------------------------------------------------------------------
def fingerprint(seq) -> dict:
    """Relabel-invariant fingerprint of a string.

    Every statistic here is unchanged by any bijective renaming of the symbols,
    hence it can be compared directly between a ciphertext and a plaintext
    language model.  (This corrects the common practice of comparing ciphertext
    letter frequencies with plaintext letter frequencies, which is invalid
    under substitution.)
    """
    n = len(seq)
    if n < 6:
        return {}
    fr = Counter(seq)
    k = len(fr)
    h = 0.0
    for c in fr.values():
        p = c / n
        h -= p * math.log2(p)
    top = sorted((c / n for c in fr.values()), reverse=True)
    bi = Counter(zip(seq, seq[1:]))
    tri = Counter(zip(seq, seq[1:], seq[2:]))
    nbi = sum(bi.values())
    ntri = sum(tri.values())

    def rr(counter, total):
        return sum(c for c in counter.values() if c > 1) / total if total else 0.0

    return {
        "IC": ic(seq),
        "H": h,
        "Hrel": h / entropy_max(k) if k > 1 else 0.0,
        "top1": top[0],
        "top3": sum(top[:3]),
        "top5": sum(top[:5]),
        "bi_rep": rr(bi, nbi),
        "tri_rep": rr(tri, ntri),
        "bi_types": len(bi) / nbi,
        "tri_types": len(tri) / ntri,
        "mean_bi": nbi / len(bi),
    }


#: statistics used for cross-language inference, chosen for low sensitivity to
#: the number of glyph classes the transcriber happened to distinguish
KEY_STATS = ("IC", "H", "top1", "bi_rep", "tri_rep")


def slice_stats(seq, n: int, n_slices: int = 500, seed: int = 4321) -> dict:
    """Distributions of the fingerprint statistics over length-``n`` windows."""
    rng = random.Random(seed)
    hi = len(seq) - n
    if hi <= 0:
        return {}
    out = {k: [] for k in KEY_STATS}
    for _ in range(n_slices):
        s = seq[rng.randrange(hi):][:n]
        fp = fingerprint(s)
        for k in KEY_STATS:
            out[k].append(fp[k])
    return out


def z_and_p(observed: float, dist) -> tuple:
    """Two-sided z-score and empirical two-sided p-value of ``observed``."""
    mu, sd = mean(dist), stdev(dist)
    if sd == 0:
        return 0.0, 1.0
    z = (observed - mu) / sd
    tail = sum(1 for v in dist if abs(v - mu) >= abs(observed - mu))
    return z, (1 + tail) / (1 + len(dist))
