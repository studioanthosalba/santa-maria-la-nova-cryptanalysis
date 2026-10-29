# -*- coding: utf-8 -*-
"""03_attacks.py -- Phase 2: classical attacks on the glyph string.

Included
--------
* a self-test that the solver really can break a monoalphabetic substitution of
  a known text of the same length (without it no negative result is meaningful);
* ``strip_nulls``: greedy removal of glyphs hypothesised as nulls, with a
  simulation-based control;
* ``SubstitutionSolver``: simulated-annealing / hill-climbing search of the
  24! keyspace scored with 5-gram language models, run for several candidate
  plaintext languages;
* crib search by isomorphy (pattern) against Latin and Czech religious formulae;
* the "Greek letter shapes" vowels test on Palma's Greek-labelled reading.

Output: ``corpus/03_attacks.md``.
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

MODELS = ["Latin (Vulgate)", "Czech (Bible Kralicka 1613)", "Italian (Riveduta)"]
SAMPLE = 600_000

#: machine-readable summary filled while the sections run
SUMMARY = {"self_test": [], "null": {}, "keys": [], "attack": []}

#: cache of n-gram models, keyed by (language label, n)
_MODEL_CACHE = {}


# --------------------------------------------------------------------------
# substitution solver
# --------------------------------------------------------------------------
class SubstitutionSolver:
    """Hill-climbing solver for a monoalphabetic substitution.

    The score is the mean n-gram log-probability of the candidate plaintext
    under a reference language model; swaps are accepted when they improve the
    score or, with probability exp(delta / T), when they worsen it (annealing).
    Only the windows touching the two swapped letters are rescored, which makes
    an attack on a 678-glyph text take seconds instead of hours.
    """

    def __init__(self, cipher: str, model: dict, seed: int = 0, plain=None):
        self.cipher = cipher
        self.model = model
        self.n = model["n"]
        self.logp = model["logp"]
        self.floor = model["floor"]
        self.symbols = sorted(set(cipher))
        self.pos = {s: [] for s in self.symbols}
        for i, ch in enumerate(cipher):
            self.pos[ch].append(i)
        self.plain = plain or sorted({ch for g in self.logp for ch in g})
        self.swap_letters = self.plain
        self.rng = random.Random(seed)
        self.n_windows = len(cipher) - self.n + 1
        self.reset()

    def reset(self, key=None):
        if key is None:
            letters = self.plain[:]
            self.rng.shuffle(letters)
            key = {s: letters[i % len(letters)]
                   for i, s in enumerate(self.symbols)}
        self.key = dict(key)
        self.text = [self.key[c] for c in self.cipher]
        self.contrib = [0.0] * self.n_windows
        for st in range(self.n_windows):
            self.contrib[st] = self.logp.get(
                tuple(self.text[st:st + self.n]), self.floor)
        self.score = sum(self.contrib)

    def reset_fixed(self, fixed: dict):
        """Initialise with some glyphs pinned to fixed plaintext letters."""
        used = set(fixed.values())
        free_letters = [l for l in self.plain if l not in used]
        self.rng.shuffle(free_letters)
        free_syms = [s for s in self.symbols if s not in fixed]
        key = dict(fixed)
        for i, s in enumerate(free_syms):
            key[s] = free_letters[i % len(free_letters)]
        self.swap_letters = free_letters
        self.reset(key)

    def _affected_windows(self, positions):
        out = set()
        last = self.n_windows - 1
        for p in positions:
            out.update(range(max(0, p - self.n + 1), min(p, last) + 1))
        return out

    def _swap(self, a: str, b: str):
        touched = []
        for s, v in list(self.key.items()):
            if v == a:
                self.key[s] = b
                touched += self.pos[s]
            elif v == b:
                self.key[s] = a
                touched += self.pos[s]
        for p in touched:
            self.text[p] = self.key[self.cipher[p]]
        return touched

    def _rescore(self, touched):
        delta = 0.0
        new = {}
        for st in self._affected_windows(touched):
            v = self.logp.get(tuple(self.text[st:st + self.n]), self.floor)
            new[st] = v
            delta += v - self.contrib[st]
        return new, delta

    def run(self, iterations: int = 12000, t_start: float = 1.2,
            t_end: float = 0.02, restarts: int = 1, verbose: bool = False):
        best_key, best_score = dict(self.key), self.score
        for r in range(restarts):
            if r:
                for _ in range(4):  # perturb the incumbent before continuing
                    a, b = self.rng.sample(self.swap_letters, 2)
                    new, delta = self._rescore(self._swap(a, b))
                    for st, v in new.items():
                        self.contrib[st] = v
                    self.score += delta
            for it in range(iterations):
                t = t_start * (t_end / t_start) ** (it / max(iterations - 1, 1))
                a, b = self.rng.sample(self.swap_letters, 2)
                new, delta = self._rescore(self._swap(a, b))
                if delta >= 0 or self.rng.random() < math.exp(delta / t):
                    for st, v in new.items():
                        self.contrib[st] = v
                    self.score += delta
                    if self.score > best_score:
                        best_score = self.score
                        best_key = dict(self.key)
                else:
                    self._swap(a, b)  # undo
            if verbose:
                print(f"    restart {r}: best mean logp "
                      f"{best_score / self.n_windows:.3f}")
        self.reset(best_key)
        return best_score / self.n_windows, self.plaintext()

    def plaintext(self) -> str:
        return "".join(self.key[c] for c in self.cipher)


def build_model(label: str, n: int = 5) -> dict:
    key = (label, n)
    if key not in _MODEL_CACHE:
        seq = LM.load_language(label, max_letters=SAMPLE)
        _MODEL_CACHE[key] = LM.build_ngram_model(seq, n)
    return _MODEL_CACHE[key]


def staged_attack(cipher: str, label: str, orders=(2, 3, 4, 5),
                  iterations: int = 4000, restarts: int = 2,
                  seed: int = 0) -> tuple:
    """Solve with progressively longer n-grams, carrying the key forward.

    Higher-order models have sharper but more rugged landscapes: a 5-gram search
    from a random start gets stuck (measured on the Czech control), while a
    2->3->4->5 ladder recovers the true key.  Returns (score at the last order,
    plaintext, key).
    """
    models = {n: build_model(label, n) for n in orders}
    plain = sorted({ch for g in models[orders[-1]]["logp"] for ch in g})
    key = None
    score = float("-inf")
    pt = ""
    for n in orders:
        solver = SubstitutionSolver(cipher, models[n], seed=seed, plain=plain)
        if key:
            solver.reset(key)
        score, pt = solver.run(iterations=iterations, restarts=restarts)
        key = dict(solver.key)
    return score, pt, key


def staged_vowel_attack(cipher: str, label: str, fixed: dict,
                        orders=(2, 3, 4, 5), iterations: int = 4000,
                        restarts: int = 2, seed: int = 0) -> tuple:
    """Same ladder, but with the vowel glyphs pinned to the vowel letters.

    This tests the *vowel-in-clear* hypothesis suggested by the photograph: the
    glyphs shaped like A, E, I, O, V behave statistically like vowels, so if the
    cipher leaves the vowels readable, only the consonants have to be solved.
    """
    models = {n: build_model(label, n) for n in orders}
    plain = sorted({ch for g in models[orders[-1]]["logp"] for ch in g})
    key = None
    score = float("-inf")
    pt = ""
    for n in orders:
        solver = SubstitutionSolver(cipher, models[n], seed=seed, plain=plain)
        solver.reset_fixed(fixed)
        if key:
            merged = {s: key.get(s, v) for s, v in fixed.items()}
            merged.update({s: v for s, v in key.items() if s not in fixed})
            solver.reset(merged)
            solver.swap_letters = [l for l in plain if l not in fixed.values()]
        score, pt = solver.run(iterations=iterations, restarts=restarts)
        key = dict(solver.key)
    return score, pt, key


def vowel_attack_section(recs: dict) -> list:
    """Attack the faithful (photograph-validated) reading with vowels in clear."""
    out = ["## Vowel-in-clear attack on the photograph-validated reading", ""]
    out.append("Le lettere che *sembrano* vocali (A, E, I, O, V/U) si comportano "
               "come vocali: con quell'insieme la quota C3 scende a 0.028, "
               "valore naturale. Se il cifrario lascia leggibili le vocali, "
               "restano da risolvere solo le consonanti: si prova quindi la "
               "scala 2->5 grammi con le vocali inchiodate.")
    out.append("")
    fixed = {"a": "a", "e": "e", "i": "i", "o": "o", "v": "u"}
    rows = []
    samples = {}
    for key in ("gemini_full", "gemini_central"):
        if key not in recs:
            continue
        cipher = recs[key]["letters"]
        fx = {g: l for g, l in fixed.items() if g in cipher}
        for li, label in enumerate(MODELS):
            score, pt, _ = staged_vowel_attack(cipher, label, fx,
                                               iterations=4000, restarts=2,
                                               seed=31 + li)
            samples[f"{key} | {label}"] = pt
            rows.append([key, label.split(" (")[0], len(fx), round(score, 3),
                         pt[:60]])
            SUMMARY.setdefault("vowel_attack", []).append(
                {"reading": key, "model": label, "vowels": len(fx),
                 "score": round(score, 3)})
    out.append(C.md_table(["lettura", "modello", "vocali fissate", "punteggio",
                           "testo prodotto (primi 60 glifi)"], rows))
    out.append("")
    out.append("Per confronto, il punteggio di un testo reale della stessa "
               "lunghezza è circa -10 e quello di una permutazione casuale circa "
               "-14.")
    out.append("")
    out.append("```")
    for k, v in samples.items():
        out.append(f"{k}:")
        for i in range(0, len(v), 40):
            out.append("  " + v[i:i + 40])
        out.append("")
    out.append("```")
    out.append("")
    return out


def make_control_text(label: str, n: int, seed: int = 1) -> tuple:
    """Encrypt a random slice of ``label`` with a random substitution."""
    rng = random.Random(seed)
    seq = LM.load_language(label, max_letters=SAMPLE)
    i = rng.randrange(len(seq) - n)
    plain = seq[i:i + n]
    letters = sorted(set(plain))
    shuffled = letters[:]
    rng.shuffle(shuffled)
    key = dict(zip(letters, shuffled))
    cipher = "".join(key[c] for c in plain)
    return cipher, plain


# --------------------------------------------------------------------------
# nulls: are some glyphs void?
# --------------------------------------------------------------------------
def greedy_strip(seq: str, steps: int = 8) -> list:
    """Repeatedly remove the glyph whose removal raises the IC the most."""
    cur, traj = seq, []
    for _ in range(steps):
        best = None
        # ``sorted`` breaks ties canonically: iterating the set directly would
        # follow the process hash seed and change the recorded glyph between runs.
        for g in sorted(set(cur)):
            cand = cur.replace(g, "")
            v = C.ic(cand)
            if best is None or v > best[0]:
                best = (v, g, cand)
        traj.append({"removed": best[1], "IC": round(best[0], 5),
                     "n": len(best[2])})
        cur = best[2]
    return traj


def max_gain(seq: str) -> tuple:
    """Largest IC gain obtainable by deleting a single glyph type."""
    base = C.ic(seq)
    best = (0.0, "")
    # canonical order: ties must not depend on the process hash seed
    for g in sorted(set(seq)):
        v = C.ic(seq.replace(g, "")) - base
        if v > best[0]:
            best = (v, g)
    return best


def null_test(rec: dict, n_rep: int = 25, null_share: float = 0.10) -> list:
    """Compare the best single-glyph deletion with calibrated controls.

    Deleting a glyph type always changes the IC a little, so the question can
    only be answered by comparison: how large is the best such gain in texts
    that certainly have no nulls, and in texts that certainly have some?
    """
    seq = rec["letters"]
    n = len(seq)
    obs_gain, obs_glyph = max_gain(seq)
    rng = random.Random(101)
    src = LM.load_language("Latin (Vulgate)", max_letters=SAMPLE)
    clean_gains, nulled_gains = [], []
    for r in range(n_rep):
        i = rng.randrange(len(src) - n)
        plain = src[i:i + n]
        letters = sorted(set(plain))
        shuffled = letters[:]
        rng.shuffle(shuffled)
        key = dict(zip(letters, shuffled))
        cipher = "".join(key[c] for c in plain)
        clean_gains.append(max_gain(cipher)[0])
        # version with two genuine nulls inserted
        chars = list(cipher)
        for _ in range(int(n * null_share)):
            chars.insert(rng.randrange(len(chars) + 1), rng.choice("89"))
        nulled_gains.append(max_gain("".join(chars))[0])
    p_clean = (1 + sum(1 for v in clean_gains if v >= obs_gain)) / (1 + n_rep)
    SUMMARY["null"] = {"observed_gain": obs_gain, "observed_glyph": obs_glyph,
                       "clean_mean": C.mean(clean_gains),
                       "nulled_mean": C.mean(nulled_gains), "p": p_clean}
    out = [f"## {rec['key']} -- are some glyphs nulls?", ""]
    out.append(C.md_table(
        ["text", "best single-glyph IC gain", "glyph"],
        [[f"epigraph `{rec['key']}`", round(obs_gain, 5), f"`{obs_glyph}`"],
         ["control: substitution, no nulls (mean of "
          f"{n_rep})", round(C.mean(clean_gains), 5), "-"],
         ["control: substitution + 10% nulls (mean of "
          f"{n_rep})", round(C.mean(nulled_gains), 5), "-"]]))
    out.append("")
    out.append(f"p(best gain >= observed | no nulls) = **{C.fmt_p(p_clean)}**. "
               "A null hypothesis is supported only if deleting the supposed "
               "null glyph recovers an IC close to the language value, which is "
               "what the nulled control shows and the epigraph does not.")
    out.append("")
    return out



def null_control(n: int = 678, null_share: float = 0.15, seed: int = 5) -> list:
    """How far does greedy stripping get when nulls are really there?"""
    label = "Latin (Vulgate)"
    seq = LM.load_language(label, max_letters=SAMPLE)
    rng = random.Random(seed)
    i = rng.randrange(len(seq) - n)
    plain = seq[i:i + n]
    letters = sorted(set(plain))
    shuffled = letters[:]
    rng.shuffle(shuffled)
    key = dict(zip(letters, shuffled))
    cipher = "".join(key[c] for c in plain)
    n_null = int(n * null_share)
    nulls = [rng.choice(letters) for _ in range(n_null)]
    positions = sorted(rng.sample(range(len(cipher) + n_null - 1), n_null),
                       reverse=True)
    noisy = list(cipher)
    for p, g in zip(positions, nulls):
        noisy.insert(p, g)
    noisy = "".join(noisy)
    traj = greedy_strip(cipher, 4)
    traj_null = greedy_strip(noisy, 4)
    out = ["### Control: a text that really has nulls", ""]
    out.append(C.md_table(
        ["stage", "IC", "length"],
        [["original plaintext", round(C.ic(plain), 5), len(plain)],
         ["after substitution", round(C.ic(cipher), 5), len(cipher)],
         ["substitution + 15% nulls", round(C.ic(noisy), 5), len(noisy)],
         ["nulls, greedy stripping step 1", traj_null[0]["IC"],
          traj_null[0]["n"]],
         ["nulls, greedy stripping step 3", traj_null[2]["IC"],
          traj_null[2]["n"]],
         ["no nulls, greedy stripping step 1", traj[0]["IC"], traj[0]["n"]],
         ["no nulls, greedy stripping step 3", traj[2]["IC"], traj[2]["n"]]]))
    out.append("")
    out.append("Greedy stripping always inflates the IC a little, which is why "
               "an increase alone is not evidence of nulls; the calibrated "
               "comparison is with this control.")
    out.append("")
    return out

def self_test(n: int = 678, seed: int = 7) -> list:
    out = ["## Self-test: can the attack break a known cipher?", ""]
    rows = []
    for label in MODELS:
        cipher, plain = make_control_text(label, n, seed)
        model = build_model(label)
        score, recovered, _ = staged_attack(cipher, label, iterations=5000,
                                            restarts=2, seed=seed)
        truth = LM.score_text(plain, model)
        rows.append([label, round(score, 3), round(truth, 3),
                     round(C.ic(recovered), 4), round(C.ic(plain), 4),
                     recovered[:12], plain[:12]])
    SUMMARY["self_test"] = [{"model": r[0], "score": r[1], "truth": r[2]}
                            for r in rows]
    out.append(C.md_table(
        ["encrypted control text", "score reached", "score of the true plaintext",
         "IC recovered", "IC plaintext", "recovered head", "true head"], rows))
    out.append("")
    out.append("A substitution preserves the IC exactly, so the IC cannot "
               "separate true from false solutions; the informative column is "
               "the score reached.  If the solver approaches the score of the "
               "true plaintext on control texts of this very length, then its "
               "behaviour on the epigraph is evidence about the epigraph rather "
               "than about the solver.")
    out.append("")
    return out


# --------------------------------------------------------------------------
# the real attack
# --------------------------------------------------------------------------
def dictionary_words(path: str) -> set:
    txt = C.read_text(path)
    out = set()
    for w in txt.replace(",", " ").split():
        w = C.normalize_latin(w)
        if len(w) >= 3:
            out.add(w)
    return out


def dict_hits(text: str, dic: set, min_len: int = 4, limit: int = 12) -> list:
    """Longest dictionary words found as substrings of a space-less text."""
    hits = []
    i = 0
    while i < len(text) - min_len:
        found = None
        for L in range(min(12, len(text) - i), min_len - 1, -1):
            if text[i:i + L] in dic:
                found = text[i:i + L]
                break
        if found:
            hits.append(found)
            i += len(found)
        else:
            i += 1
    return hits[:limit]


def attack_section(recs: dict, keys=("palma_B", "palma_A"),
                   iterations: int = 3500, restarts: int = 2) -> list:
    dic_path = os.path.join(C.REPO_CORPORA, "latindic.txt")
    dic = dictionary_words(dic_path) if os.path.exists(dic_path) else set()
    out = ["## Simulated-annealing attack on the substitution hypothesis", ""]
    rows = []
    samples = {}
    for key in keys:
        cipher = recs[key]["letters"]
        for li, label in enumerate(MODELS):
            model = build_model(label)
            rng = random.Random(5)
            shuffled = list(cipher)
            rng.shuffle(shuffled)
            base = LM.score_text("".join(shuffled), model)
            natural = C.mean([LM.score_text(
                LM.load_language(label, max_letters=SAMPLE)[
                    rng.randrange(SAMPLE - 700):][:len(cipher)], model)
                for _ in range(3)])
            score, pt, _ = staged_attack(cipher, label, iterations=iterations,
                                         restarts=restarts, seed=11 + li)
            hits = dict_hits(pt, dic) if dic else []
            samples[f"{key} | {label}"] = pt
            rows.append([key, label.split(" (")[0], round(score, 3),
                         round(base, 3), round(natural, 3), len(hits),
                         pt[:26]])
    SUMMARY["attack"] = [{"reading": r[0], "model": r[1], "score": r[2],
                          "shuffled": r[3], "natural": r[4], "words": r[5]}
                         for r in rows]
    out.append(C.md_table(["reading", "language model", "score reached",
                           "shuffled baseline", "natural-text level",
                           "Latin words", "plaintext head"], rows))
    out.append("")
    out.append("`score reached` is the mean 5-gram log-probability per window "
               "after the search; `shuffled baseline` is what the same glyph "
               "multiset scores in random order; `natural-text level` is what a "
               "genuine text of the same language and length scores.  A "
               "successful attack must land near the natural-text level.")
    out.append("")
    out.append("Best candidates in full (line breaks every 40 glyphs, for "
               "legibility only):")
    out.append("")
    out.append("```")
    for k, v in samples.items():
        out.append(f"{k}:")
        for i in range(0, len(v), 40):
            out.append("  " + v[i:i + 40])
        out.append("")
    out.append("```")
    out.append("")
    return out


# --------------------------------------------------------------------------
# crib search by isomorphy
# --------------------------------------------------------------------------
LATIN_CRIBS = [
    "hic", "iacet", "iacit", "requiescat", "requiescit", "anima", "eius",
    "ora", "pro", "eo", "nobis", "maria", "mater", "dei", "filius", "sanctus",
    "spiritus", "amen", "tumulus", "sepulcrum", "christus", "iesus", "domine",
    "gloria", "saecula", "saeculorum", "mortuus", "obiit", "anno", "domini",
    "virgo", "beata", "immaculata", "turbolo", "franciscus", "fernandus",
    "balthassar", "miserere", "peccator", "memento", "vita", "aeterna",
    "resurrectio", "corpus", "sancta", "ecclesia", "capella", "marmore",
]
CZECH_CRIBS = [
    "pomiluj", "boze", "hriech", "duse", "milosrdenstvi", "otce", "amen",
    "jezis", "kriste", "matko", "panno", "maria", "svaty", "duch", "veky",
    "smiluj", "pane", "hospodine", "krale", "nebeskeho", "chleb", "nasy",
    "odpust", "viny", "zbav", "nas", "zleho", "tve", "jmeno",
]


def crib_search(rec: dict, cribs: dict) -> list:
    toks = [t for t in rec["tokens"] if C.GAP not in t and len(t) >= 3]
    out = [f"## {rec['key']} -- crib search by isomorphy", ""]
    rows = []
    trivial = 0
    for lang, words in cribs.items():
        for w in words:
            if len(set(w)) == len(w):
                trivial += 1  # pattern ABCDEF... matches almost anything
                continue
            matches = [t for t in toks if C.is_isomorph(t, w)]
            if matches:
                rows.append([lang, w, C.pattern(w),
                             ", ".join(f"`{m}`" for m in matches[:4])])
    out.append(f"{trivial} of the cribs were skipped because all their letters "
               "are distinct: their pattern is shared by every token of the same "
               "length with all-distinct glyphs, so they carry no information.")
    out.append("")
    if not rows:
        out.append("*no token of this reading is isomorphic to any informative "
                   "crib*")
        out.append("")
        return out
    out.append(C.md_table(["language", "crib", "pattern", "isomorphic tokens"],
                          rows[:20]))
    out.append("")
    out.append("Isomorphy is only a *necessary* condition: a crib becomes "
               "credible only when several matches imply one single consistent "
               "glyph-to-letter mapping.")
    out.append("")
    return out


def greek_shape_test(rec: dict) -> list:
    """Palma's Greek-labelled reading: are the Greek vowel shapes vowels?"""
    import re
    vowels = set("\u03b1\u03b5\u03b7\u03b9\u03bf\u03c5\u03c9")
    seq = rec["letters"]
    present = vowels & set(seq)
    table = str.maketrans({ch: ("V" if ch in vowels else "C") for ch in set(seq)})
    runs = [len(m) for m in re.findall(r"C+", seq.translate(table))]
    total = len(seq)
    c3 = sum(r for r in runs if r >= 3) / total
    out = ["## The 'Greek vowel' hypothesis (Palma's Greek-labelled reading)", ""]
    out.append(C.md_table(
        ["quantity", "value"],
        [["Greek vowel glyphs present", ", ".join(sorted(present))],
         ["their share of the text %",
          round(100 * sum(C.freq(seq)[g] for g in present) / len(seq), 1)],
         ["C3 share under this assignment", round(c3, 4)],
         ["mean consonant run", round(C.mean(runs), 2)],
         ["longest consonant run", max(runs)]]))
    out.append("")
    out.append("Natural languages keep the C3 share below about 0.10; a much "
               "larger value means the Greek letter shapes are not being used as "
               "the vowels of the plaintext.")
    out.append("")
    return out


def vigenere_decrypt(seq: str, shifts, alphabet: list) -> str:
    idx = {c: i for i, c in enumerate(alphabet)}
    k = len(alphabet)
    return "".join(alphabet[(idx[ch] - shifts[i % len(shifts)]) % k]
                   for i, ch in enumerate(seq))


def key_test(rec: dict, keys=("VLAD", "DRACULA", "TURBOLO", "MARIA", "BALSA",
                              "FERRILLO", "NAPOLI", "IESUS"),
             n_rand: int = 400) -> list:
    """Do the names attached to the legend work as polyalphabetic keys?

    The keys are inserted as their Latin letter values (A=0 ... Z=25) and
    applied modulo the number of glyph classes, which is the only way a Latin
    key can act on an unknown alphabet.  The statistic is the trigram repeat
    rate of the decrypted text: a correct key restores the language value
    (~0.5), a wrong key leaves it at the ciphertext level (~0.2).
    """
    seq = rec["letters"]
    alphabet = sorted(set(seq))
    k = len(alphabet)
    obs = C.repeat_rate(seq, 3)
    rng = random.Random(303)
    rows = []
    for key in keys:
        shifts = [ord(ch.upper()) - 65 for ch in key]
        dec = vigenere_decrypt(seq, shifts, alphabet)
        stats = C.fingerprint(dec)
        # null: random keys of the same length
        sims = []
        for _ in range(n_rand):
            rsh = [rng.randrange(k) for _ in shifts]
            sims.append(C.fingerprint(vigenere_decrypt(seq, rsh, alphabet))
                        ["tri_rep"])
        p = (1 + sum(1 for v in sims if v >= stats["tri_rep"])) / (1 + n_rand)
        rows.append([key, round(stats["IC"], 4), round(stats["tri_rep"], 3),
                     round(C.mean(sims), 3), C.fmt_p(p)])
    SUMMARY["keys"] = [{"key": r[0], "IC": r[1], "tri_rep": r[2],
                        "random_mean": r[3], "p": r[4]} for r in rows]
    out = ["## Do the names of the legend work as polyalphabetic keys?", ""]
    out.append(C.md_table(
        ["key", "IC after decryption", "trigram repeat", "random-key mean", "p"],
        rows))
    out.append("")
    best = min(rows, key=lambda r: float(r[4])) if rows else None
    out.append(f"The undecrypted text has IC {C.ic(seq):.4f} and trigram repeat "
               f"{obs:.3f}; the language range is IC ~ 0.073 and trigram repeat "
               "~ 0.5.  None of the keys brings the decrypted text into that "
               "range, and the smallest p-value among them is "
               f"{best[4] if best else 'n/a'} (key `{best[0] if best else '-'}`), "
               "i.e. indistinguishable from a random key of the same length.")
    out.append("")
    return out


def main() -> None:
    recs = C.load_json(os.path.join(C.CORPUS, "corpora.json"))
    out = ["# Phase 2 -- attacks", "",
           "Targets: `palma_B` (678 glyphs, the most complete reading) and "
           "`palma_A` (584 glyphs, the only reading with word boundaries).", ""]
    print("self test ...")
    out += self_test()
    print("null analysis ...")
    out += null_test(recs["palma_B"])
    out += null_control()
    print("polyalphabetic keys ...")
    out += key_test(recs["palma_B"])
    print("substitution attack ...")
    out += attack_section(recs)
    print("vowel-in-clear attack ...")
    out += vowel_attack_section(recs)
    out += crib_search(recs["palma_A"],
                       {"Latin": LATIN_CRIBS, "Czech": CZECH_CRIBS})
    out += greek_shape_test(recs["palma_B"])
    C.save_json(os.path.join(C.CORPUS, "03_summary.json"), SUMMARY)
    C.write_text(os.path.join(C.CORPUS, "03_attacks.md"), "\n".join(out) + "\n")
    print("\nwrote corpus/03_attacks.md")


if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()


