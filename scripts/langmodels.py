# -*- coding: utf-8 -*-
"""langmodels.py -- reference language models for the epigraph analysis.

The candidate plaintext languages are represented by *parallel-genre* texts
(biblical / religious prose) so that register is held constant while language
varies.  Two further directories are used:

* ``sources/external``  -- downloaded by ``_fetch_external.py``;
* ``sources/MaLaNova-master/corpora`` -- Palma's own corpora, several of which
  are double-encoded UTF-8 (they must be repaired before use).

Everything is reduced to lower-case ASCII letters, so that the statistics are
comparable with a transliterated ciphertext.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C

EXTERNAL = os.path.join(C.SOURCES, "external")

#: Greek letters -> distinct Latin letters (injective, so n-grams survive)
GREEK_TRANSLIT = {
    "\u03b1": "a", "\u03b2": "b", "\u03b3": "g", "\u03b4": "d", "\u03b5": "e",
    "\u03b6": "z", "\u03b7": "h", "\u03b8": "q", "\u03b9": "i", "\u03ba": "k",
    "\u03bb": "l", "\u03bc": "m", "\u03bd": "n", "\u03be": "c", "\u03bf": "o",
    "\u03c0": "p", "\u03c1": "r", "\u03c3": "s", "\u03c2": "s", "\u03c4": "t",
    "\u03c5": "u", "\u03c6": "f", "\u03c7": "x", "\u03c8": "y", "\u03c9": "w",
}

#: reference languages: label -> loader specification
LANGUAGES = {
    "Latin (Vulgate)": {"file": "bible_latin_vulgate.txt"},
    "Latin (humanist corpus)": {"repo": "latincorpus.txt", "mojibake": True},
    "Czech (Bible Kralicka 1613)": {"file": "bible_czech_kralicka_1613.txt"},
    "Czech (catechism)": {"file": "czech_catechism.txt"},
    "Italian (Riveduta)": {"file": "bible_italian_riveduta.txt"},
    "Italian (Dante)": {"file": "italian_dante.txt"},
    "Hungarian (Karoli)": {"file": "bible_hungarian_karoli.txt"},
    "Hungarian (Erdy codex, XV c.)": {"repo": "erdycodex.txt", "mojibake": True},
    "Old Hungarian (Funeral Sermon)": {
        "repo": "oldhungarianfuneralsermon.txt", "mojibake": True},
    "Old Hungarian (Lamentation of Mary)": {
        "repo": "oldhungarianlamentationofmary.txt", "mojibake": True},
    "Old Czech (Bohemian 2)": {"repo": "bohemian2.txt"},
    "Old Czech (Bohemian 3)": {"repo": "bohemian3.txt"},
    "Old Luxembourgish (Codex Mariendalensis)": {"repo": "oldlux2.txt"},
    "Romanian": {"file": "bible_romanian.txt"},
    "Albanian": {"file": "bible_albanian.txt"},
    "Croatian": {"file": "bible_croatian.txt"},
    "Slovak": {"file": "bible_slovak.txt"},
    "Polish": {"file": "bible_polish.txt"},
    "German (Schlachter)": {"file": "bible_german_schlachter.txt"},
    "English (KJV)": {"file": "bible_english_kjv.txt"},
    "Greek (Brenton, translit.)": {"file": "bible_greek_brenton.txt",
                                   "greek": True},
}

#: how many letters of each reference text are used (memory/speed trade-off)
MAX_LETTERS = 1_500_000

#: cache of normalised reference texts, keyed by (label, max_letters)
_TEXT_CACHE = {}

#: vowel inventory of each reference language (after ASCII folding)
VOWELS = {
    "Latin (Vulgate)": set("aeiou"),
    "Latin (humanist corpus)": set("aeiou"),
    "Czech (Bible Kralicka 1613)": set("aeiouy"),
    "Czech (catechism)": set("aeiouy"),
    "Italian (Riveduta)": set("aeiou"),
    "Italian (Dante)": set("aeiou"),
    "Hungarian (Karoli)": set("aeiou"),
    "Hungarian (Erdy codex, XV c.)": set("aeiou"),
    "Old Hungarian (Funeral Sermon)": set("aeiou"),
    "Old Hungarian (Lamentation of Mary)": set("aeiou"),
    "Old Czech (Bohemian 2)": set("aeiouy"),
    "Old Czech (Bohemian 3)": set("aeiouy"),
    "Old Luxembourgish (Codex Mariendalensis)": set("aeiou"),
    "Romanian": set("aeiou"),
    "Albanian": set("aeiouy"),
    "Croatian": set("aeiou"),
    "Slovak": set("aeiouy"),
    "Polish": set("aeiouy"),
    "German (Schlachter)": set("aeiou"),
    "English (KJV)": set("aeiouy"),
    "Greek (Brenton, translit.)": set("aehiouw"),
}


def fix_mojibake(text: str) -> str:
    """Repair UTF-8 read as cp437 and re-saved (Palma's corpora are damaged)."""
    try:
        fixed = text.encode("cp437").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return text
    # accept the repair only if it removes the mojibake markers
    bad = ("\u251c", "\u252c", "\u253c", "\u255a", "\u256c")
    if sum(text.count(b) for b in bad) > sum(fixed.count(b) for b in bad):
        return fixed
    return text


def normalize(text: str, greek: bool = False) -> str:
    if greek:
        text = "".join(GREEK_TRANSLIT.get(ch, ch) for ch in text.lower())
    return C.normalize_latin(text)


def _path(spec: dict) -> str:
    if "file" in spec:
        return os.path.join(EXTERNAL, spec["file"])
    return os.path.join(C.REPO_CORPORA, spec["repo"])


def load_language(label: str, max_letters: int = MAX_LETTERS) -> str:
    key = (label, max_letters)
    if key in _TEXT_CACHE:
        return _TEXT_CACHE[key]
    spec = LANGUAGES[label]
    path = _path(spec)
    text = C.read_text(path)
    if spec.get("mojibake"):
        text = fix_mojibake(text)
    letters = normalize(text, greek=spec.get("greek", False))[:max_letters]
    _TEXT_CACHE[key] = letters
    return letters


def load_all(max_letters: int = MAX_LETTERS, verbose: bool = True) -> dict:
    out = {}
    for label in LANGUAGES:
        try:
            out[label] = load_language(label, max_letters)
            if verbose:
                print(f"  {label:32s} {len(out[label]):>8d} letters "
                      f"K={len(set(out[label])):2d} "
                      f"IC={C.ic(out[label][:200000]):.4f}")
        except Exception as exc:  # pragma: no cover - missing corpus
            if verbose:
                print(f"  {label:32s} SKIPPED ({exc})")
    return out


#: minimum size of a corpus to enter the *comparative* analyses (2-5).  The
#: threshold fixes the reference set at 16 corpora independently of the length
#: of the reading under test: the five short texts of Palma's repository
#: (0.7k-15k letters: Old Czech 2 and 3, the two Old Hungarian sermons, Old
#: Luxembourgish) are listed in ``LANGUAGES`` and can be loaded, but a
#: distribution of length-matched windows drawn from them would consist of a
#: handful of overlapping windows, not of a sample.
MIN_REFERENCE = 30_000


def load_reference(max_letters: int = MAX_LETTERS, verbose: bool = True,
                   min_letters: int = MIN_REFERENCE) -> dict:
    """The reference set actually used by the comparisons (16 corpora)."""
    everything = load_all(max_letters=max_letters, verbose=verbose)
    return {k: v for k, v in everything.items() if len(v) >= min_letters}


# --------------------------------------------------------------------------
# n-gram language models (used by the substitution attack)
# --------------------------------------------------------------------------
def build_ngram_model(seq: str, n: int, top_k: int = 200_000) -> dict:
    """Log-probability table for the ``top_k`` most frequent n-grams."""
    import math
    counts = C.ngrams(seq, n)
    total = sum(c for _, c in counts.most_common(top_k))
    logp = {g: math.log(c / total) for g, c in counts.most_common(top_k)}
    return {"n": n, "logp": logp, "floor": math.log(0.5 / total)}


def score_text(text: str, model: dict) -> float:
    """Mean log-probability per n-gram (higher = more language-like)."""
    n = model["n"]
    logp = model["logp"]
    floor = model["floor"]
    total = 0.0
    cnt = 0
    for i in range(len(text) - n + 1):
        g = tuple(text[i:i + n])
        total += logp.get(g, floor)
        cnt += 1
    return total / cnt if cnt else float("-inf")


if __name__ == "__main__":
    C.utf8_stdout()
    print("loading reference languages ...")
    langs = load_all()
    print(f"\n{len(langs)} languages loaded")
    for label, seq in langs.items():
        print(f"{label:34s} n={len(seq):>8d} IC={C.ic(seq[:100000]):.5f} "
              f"IC26={C.ic26(seq[:100000]):.3f} H={C.entropy(seq[:100000]):.3f}")
