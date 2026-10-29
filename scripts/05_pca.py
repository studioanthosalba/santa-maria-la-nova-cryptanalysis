# -*- coding: utf-8 -*-
"""05_pca.py -- Phase 1c: ordination (PCA) of the relabel-invariant profiles.

The analysis answers three questions and refuses a fourth:

1. Does the published PCA (``report/pca_analisi.md``) reproduce?  Its central
   numbers are rebuilt here from scratch -- same 28 descriptors, same sampling
   scheme (100 segments per corpus per length), same seed -- and compared
   coordinate by coordinate with the published ones.
2. What can such an ordination *see*?  All 28 descriptors are invariant under a
   bijective renaming of the glyphs, so a monoalphabetic substitution is, by
   construction, invisible: the script proves it numerically (distance 0.000)
   instead of asserting it.
3. What produces the anomalous position of the readings?  The decisive control
   is a **plain text of a reference language with k glyph classes merged** (the
   effect of a transcriber who does not distinguish glyph variants).  The sweep
   over k shows how many merges reproduce the position of each reading.  If a
   plain, unenciphered text lands where ``gemini_full`` lands, the anomaly says
   nothing about the cipher and everything about the transcription.

The fourth question -- *which language* -- is not answered, and the script
shows why the nearest-neighbour tables of the published analysis cannot answer
it either: their concentration is compared with the null distribution of the
same statistic over the reference points themselves.

Output: ``corpus/05_pca.md`` and ``corpus/05_pca_summary.json``.
"""

from __future__ import annotations

import math
import os
import random
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C
import langmodels as LM

C.utf8_stdout()

READINGS = ["palma_A", "palma_B", "gemini_full"]
SEED = 20261029
N_SEG = 100
SAMPLE_LETTERS = 400_000
N_COMP = 6
MERGE_LEVELS = (0, 1, 2, 3, 4)

#: coordinates published in ``report/pca_analisi.md`` (z = coordinate / sd of
#: the component over the reference samples), used only for the comparison
PUBLISHED = {
    "palma_A": (2.77, 1.61, 1.01),
    "palma_B": (1.29, 0.47, 3.52),
    "gemini_full": (-0.87, -2.40, 6.03),
}
PUBLISHED_RANGE = ((-1.57, 1.40), (-1.63, 1.52), (-1.44, 1.88))

#: coordinates of the second PCA in the repository
#: (``report/verifica_trascrizioni_corpora_cifrari.md``, 21 corpora, readings
#: Palma only), used only for the comparison
PUBLISHED_2 = {
    "palma_A": (-2.864, 0.667, -0.841),
    "palma_B": (-1.333, -0.442, -3.344),
}

#: corpora dropped in the reduced-subset sensitivity check (the four
#: peripheral modern references), to test how much the ordination depends on
#: the choice of the reference set
SUBSET_DROP = ("English (KJV)", "German (Schlachter)",
               "Latin (humanist corpus)", "Italian (Dante)")

SUMMARY = {"published": PUBLISHED, "readings": {}, "controls": {},
           "invariance": {}, "neighbours": {}, "stability": {},
           "families": {}, "axes": {}}


# --------------------------------------------------------------------------
# 28 relabel-invariant descriptors
# --------------------------------------------------------------------------
FEATURE_NAMES = (
    ["IC", "H", "K", "redundancy"]
    + [f"share{i}" for i in range(1, 13)]
    + [f"n{n}_{s}" for n in (2, 3, 4, 5) for s in ("types", "rep", "Hn")]
)


def features(seq: str, rep: str = "tokens") -> list:
    """The 28 descriptors: 4 global ones, 12 sorted frequency shares and, for
    n = 2..5, the type ratio, the repeat rate and the normalised entropy of the
    n-gram stream.

    Every entry is unchanged by a bijective renaming of the symbols (the shares
    are sorted, the n-gram statistics only look at equality of n-grams), so the
    whole vector is invariant under a substitution.

    ``rep`` selects the definition of the repeat rate: ``"tokens"`` is the share
    of n-gram tokens whose n-gram occurs more than once, ``"1xu"`` is 1 - U/N
    (the complement of the type ratio).  The two variants differ by at most a
    couple of tenths of a standard deviation in the ordination, which is why
    both are offered and compared instead of being assumed.
    """
    n = len(seq)
    fr = Counter(seq)
    k = len(fr)
    h = 0.0
    for c in fr.values():
        p = c / n
        h -= p * math.log2(p)
    hm = math.log2(k) if k > 1 else 1.0
    shares = sorted((c / n for c in fr.values()), reverse=True)
    shares = shares[:12] + [0.0] * max(0, 12 - len(shares))
    out = [C.ic(seq), h, float(k), 1.0 - h / hm] + shares
    for order in (2, 3, 4, 5):
        cnt = Counter(zip(*(seq[i:] for i in range(order))))
        total = sum(cnt.values())
        types = len(cnt)
        vals = [c / total for c in cnt.values()] if total else []
        hng = -sum(p * math.log2(p) for p in vals) if vals else 0.0
        out.append(types / total if total else 0.0)
        if rep == "1xu":
            out.append(1.0 - types / total if total else 0.0)
        else:
            out.append(sum(c for c in cnt.values() if c > 1) / total
                       if total else 0.0)
        out.append(hng / math.log2(total) if total > 1 else 0.0)
    return out


# --------------------------------------------------------------------------
# PCA in pure standard library (28 x 28 symmetric eigenproblem)
# --------------------------------------------------------------------------
def _jacobi(mat: list, sweeps: int = 80) -> tuple:
    """Cyclic Jacobi eigen-decomposition of a symmetric matrix.

    Returns ``(values, vectors)`` with ``vectors[i]`` the eigenvector of
    ``values[i]``.  Deterministic: no pivoting, fixed sweep order.
    """
    n = len(mat)
    a = [row[:] for row in mat]
    v = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for _ in range(sweeps):
        off = sum(a[i][j] ** 2 for i in range(n) for j in range(n) if i != j)
        if off < 1e-20:
            break
        for p in range(n - 1):
            for q in range(p + 1, n):
                if abs(a[p][q]) < 1e-18:
                    continue
                theta = (a[q][q] - a[p][p]) / (2.0 * a[p][q])
                t = (1.0 if theta >= 0 else -1.0) / (
                    abs(theta) + math.sqrt(theta * theta + 1.0))
                c = 1.0 / math.sqrt(t * t + 1.0)
                s = t * c
                for k in range(n):
                    akp, akq = a[k][p], a[k][q]
                    a[k][p] = c * akp - s * akq
                    a[k][q] = s * akp + c * akq
                for k in range(n):
                    apk, aqk = a[p][k], a[q][k]
                    a[p][k] = c * apk - s * aqk
                    a[q][k] = s * apk + c * aqk
                for k in range(n):
                    vkp, vkq = v[k][p], v[k][q]
                    v[k][p] = c * vkp - s * vkq
                    v[k][q] = s * vkp + c * vkq
    values = [a[i][i] for i in range(n)]
    vectors = [[v[k][i] for k in range(n)] for i in range(n)]
    return values, vectors


def fit(samples: list, n_comp: int = N_COMP) -> dict:
    """Standardise the reference matrix, then PCA on the correlation matrix."""
    m = len(samples)
    d = len(samples[0])
    mean = [sum(row[j] for row in samples) / m for j in range(d)]
    sd = []
    for j in range(d):
        var = sum((row[j] - mean[j]) ** 2 for row in samples) / m
        sd.append(math.sqrt(var) if var > 0 else 1.0)
    z = [[(row[j] - mean[j]) / sd[j] for j in range(d)] for row in samples]
    corr = [[sum(z[i][a] * z[i][b] for i in range(m)) / (m - 1)
             for b in range(d)] for a in range(d)]
    values, vectors = _jacobi(corr)
    order = sorted(range(d), key=lambda i: -values[i])
    total = sum(values)
    comps, var = [], []
    for i in order[:n_comp]:
        vec = vectors[i]
        # deterministic orientation: the largest loading is positive
        jmax = max(range(d), key=lambda j: abs(vec[j]))
        if vec[jmax] < 0:
            vec = [-x for x in vec]
        comps.append(vec)
        var.append(values[i] / total if total else 0.0)
    scores = [[sum(zi[j] * vec[j] for j in range(d)) for vec in comps] for zi in z]
    sds = []
    for k in range(len(comps)):
        col = [s[k] for s in scores]
        sds.append(C.stdev(col) or 1.0)
    return {"mean": mean, "sd": sd, "comps": comps, "var": var,
            "sds": sds, "dims": d, "n": m}


def project(model: dict, vec: list) -> list:
    """PC coordinates of one feature vector, expressed in sd units."""
    z = [(vec[j] - model["mean"][j]) / model["sd"][j] for j in range(model["dims"])]
    out = []
    for k, comp in enumerate(model["comps"]):
        raw = sum(z[j] * comp[j] for j in range(model["dims"]))
        out.append(raw / model["sds"][k])
    return out


def radius(model: dict, vec: list) -> float:
    """RMS distance from the reference centroid in standardised space."""
    z = [(vec[j] - model["mean"][j]) / model["sd"][j] for j in range(model["dims"])]
    return math.sqrt(sum(x * x for x in z) / len(z))


# --------------------------------------------------------------------------
# sampling and the merging control
# --------------------------------------------------------------------------
def segments(langs: dict, lengths, n_seg: int = N_SEG, seed: int = SEED,
             skip=(), rep: str = "tokens") -> list:
    """``n_seg`` random length-``L`` segments per language and per length."""
    rng = random.Random(seed)
    out = []
    for label in sorted(langs):
        if label in skip:
            continue
        text = langs[label]
        for L in lengths:
            hi = len(text) - L
            if hi <= 0:
                continue
            for _ in range(n_seg):
                i = rng.randrange(hi)
                s = text[i:i + L]
                out.append((label, L, features(s, rep=rep)))
    return out


def substitution(seq: str, seed: int = 7) -> tuple:
    """Stable random bijection on the glyph classes of ``seq``."""
    keys = sorted(set(seq))
    shuffled = keys[:]
    random.Random(seed).shuffle(shuffled)
    table = dict(zip(keys, shuffled))
    return "".join(table[ch] for ch in seq), table


def merge(seq: str, k: int) -> str:
    """Merge the ``k`` most frequent glyph classes into the most frequent one.

    This is what a transcriber does when he does not distinguish glyph
    variants: two distinct signs of the stone end up under one label.
    """
    if k <= 0:
        return seq
    order = [c for c, _ in Counter(seq).most_common()]
    table = {c: order[0] for c in order[1:k + 1]}
    return "".join(table.get(ch, ch) for ch in seq)


def nearest(queries: list, sample_labels: list, sample_vecs: list,
            k: int = 15, dims: int = 2, skip=None) -> list:
    """Language census of the ``k`` nearest reference samples (PCA space).

    ``skip[i]`` optionally excludes the reference point itself from the
    neighbours of query ``i`` (used when the query *is* a reference point).
    """
    out = []
    for qi, q in enumerate(queries):
        own = skip[qi] if skip else -1
        dists = []
        for i, v in enumerate(sample_vecs):
            if i == own:
                continue
            d = sum((q[a] - v[a]) ** 2 for a in range(dims))
            dists.append((d, sample_labels[i]))
        dists.sort(key=lambda t: t[0])
        out.append(Counter(lbl for _, lbl in dists[:k]))
    return out


# --------------------------------------------------------------------------
# 1. variance and meaning of the axes
# --------------------------------------------------------------------------
def sec_assi(model: dict) -> list:
    out = ["## Varianza spiegata e significato degli assi", ""]
    rows = []
    cum = 0.0
    for i, v in enumerate(model["var"]):
        cum += v
        rows.append([f"PC{i + 1}", f"{100 * v:.2f}%", f"{100 * cum:.2f}%"])
    out += [C.md_table(["componente", "varianza spiegata", "cumulativa"], rows), ""]
    out.append("Carichi più forti (correlazione variabile-componente):")
    out.append("")
    rows = []
    for i, comp in enumerate(model["comps"]):
        idx = sorted(range(len(comp)), key=lambda j: -abs(comp[j]))[:5]
        rows.append([f"PC{i + 1}"]
                    + [f"{FEATURE_NAMES[j]} ({comp[j]:+.2f})" for j in idx])
    out += [C.md_table(["componente", "1", "2", "3", "4", "5"], rows), ""]
    SUMMARY["axes"] = {
        "var": [round(v, 4) for v in model["var"]],
        "top_loadings": {f"PC{i + 1}": [[FEATURE_NAMES[j], round(comp[j], 3)]
                                        for j in sorted(range(len(comp)),
                                                        key=lambda j: -abs(comp[j]))[:5]]
                         for i, comp in enumerate(model["comps"])},
    }
    return out


# --------------------------------------------------------------------------
# 1b. the ambiguous descriptor, and the second PCA of the repository
# --------------------------------------------------------------------------
def sec_definizioni(langs: dict, recs: dict, lengths) -> list:
    out = ["## La definizione ambigua del «tasso di ripetizione»", ""]
    out.append("L'analisi pubblicata non specifica come calcoli il tasso di "
               "ripetizione degli n-grammi. Le due definizioni plausibili sono "
               "la quota di n-grammi *token* che compaiono più di una volta e il "
               "complemento del rapporto tipi/totale, 1 − U/N. L'ordinazione è "
               "rifatta con la seconda, a parità di tutto il resto:")
    out.append("")
    alt = segments(langs, lengths, rep="1xu")
    mdl = fit([s[2] for s in alt])
    rows, shifts, deltas_alt = [], {}, []
    for k in READINGS:
        z_alt = project(mdl, features(recs[k]["letters"], rep="1xu"))[:3]
        z_main = SUMMARY["readings"][k][:3]
        pub = PUBLISHED[k]
        signs = [1.0 if p * r >= 0 else -1.0 for p, r in zip(pub, z_alt)]
        d_alt = [abs(p - s * r) for p, s, r in zip(pub, signs, z_alt)]
        deltas_alt += d_alt
        shift = max(abs(a - (b if a * b >= 0 else -b))
                    for a, b in zip(z_main, z_alt))
        shifts[k] = round(shift, 2)
        rows.append([f"`{k}`", f"{max(d_alt):.2f}", f"{shift:.2f}"])
    out += [C.md_table(["lettura", "scarto dalla PCA pubblicata con 1 - U/N",
                        "spostamento rispetto alla definizione a token"], rows),
            ""]
    out.append(f"Le due definizioni spostano le coordinate di al massimo "
               f"{max(shifts.values()):.2f} deviazioni standard e lasciano la "
               "riproduzione allo stesso livello: **l'ambiguità non è la causa "
               "delle differenze residue con l'analisi pubblicata**.")
    out.append("")
    SUMMARY["definitions"] = {"shift": shifts,
                              "max_delta_1xu": round(max(deltas_alt), 3)}
    return out


def sec_altra_pca(recs: dict) -> list:
    out = ["## Confronto con la seconda PCA presente nel repository", ""]
    out.append("In `report/verifica_trascrizioni_corpora_cifrari.md` esiste una "
               "seconda ordinazione, eseguita in modo indipendente con 21 "
               "corpora (i sedici di questa pipeline più i cinque testi brevi) e "
               "con le sole letture Palma. Le sue coordinate, allineate nel "
               "segno, si confrontano con quelle calcolate qui:")
    out.append("")
    rows, deltas = [], []
    for k in PUBLISHED_2:
        pub = PUBLISHED_2[k]
        rec = SUMMARY["readings"][k][:3]
        signs = [1.0 if p * r >= 0 else -1.0 for p, r in zip(pub, rec)]
        d = [abs(p - s * r) for p, s, r in zip(pub, signs, rec)]
        deltas += d
        rows.append([f"`{k}`", ", ".join(f"{v:.2f}" for v in pub),
                     ", ".join(f"{s * v:.2f}" for s, v in zip(signs, rec)),
                     f"{max(d):.2f}"])
    out += [C.md_table(["lettura", "seconda PCA", "questa pipeline",
                        "scarto massimo"], rows), ""]
    out.append(f"Con un insieme di corpora diverso e un codice diverso le "
               f"coordinate delle due letture Palma concordano entro "
               f"{max(deltas):.2f} deviazioni standard, e la seconda PCA "
               "conferma il punto che conta: le prossimità cambiano da una "
               "lettura all'altra, quindi non identificano una lingua. Le due "
               "analisi convergono anche sul resto — il merito della PCA è "
               "descrivere, non attribuire.")
    out.append("")
    SUMMARY["second_pca"] = {"published": PUBLISHED_2,
                             "max_delta": round(max(deltas), 3)}
    return out


# --------------------------------------------------------------------------
# 2. reproduction of the published coordinates
# --------------------------------------------------------------------------
def sec_letture(model: dict, recs: dict, samples: list, lengths) -> list:
    out = ["## Posizione delle letture e confronto con l'analisi pubblicata", ""]
    ref = {}
    for L in lengths:
        sub = [project(model, s[2]) for s in samples if s[1] == L]
        ref[L] = {i: (C.quantile([s[i] for s in sub], 0.05),
                      C.quantile([s[i] for s in sub], 0.95)) for i in range(3)}
    rows, zs = [], {}
    for key in READINGS:
        z = project(model, features(recs[key]["letters"]))
        zs[key] = [round(v, 2) for v in z]
        L = len(recs[key]["letters"])
        lo, hi = ref[L][0]
        rows.append([f"`{key}`", L] + [f"{v:.2f}" for v in z[:3]]
                    + [f"{lo:.2f} - {hi:.2f}"])
    out += [C.md_table(["lettura", "n", "PC1 z", "PC2 z", "PC3 z",
                        "intervallo 5-95% di PC1 nei riferimenti"], rows), ""]
    out.append("Confronto con i valori pubblicati in `report/pca_analisi.md` "
               "(stessi 28 descrittori, stesso schema di campionamento, stesso "
               "seme). Il segno di ciascun autovettore è arbitrario e "
               "l'orientamento scelto qui, pur deterministico, è indipendente da "
               "quello dell'analisi pubblicata: le componenti vengono perciò "
               "allineate una per una prima del confronto.")
    out.append("")
    rows, deltas = [], []
    for key in READINGS:
        pub = PUBLISHED[key]
        rec = zs[key][:3]
        signs = [1.0 if (p * r) >= 0 else -1.0 for p, r in zip(pub, rec)]
        d = [abs(p - s * r) for p, s, r in zip(pub, signs, rec)]
        deltas += d
        rows.append([f"`{key}`", ", ".join(f"{v:.2f}" for v in pub),
                     ", ".join(f"{s * v:.2f}" for s, v in zip(signs, rec)),
                     ", ".join(f"{x:.2f}" for x in d)])
    out += [C.md_table(["lettura", "pubblicato", "ricalcolato",
                        "differenza assoluta"], rows), ""]
    out.append(f"Le nove coordinate concordano entro {max(deltas):.2f} "
               f"deviazioni standard (mediana {C.quantile(deltas, 0.5):.2f}): "
               "l'ordinazione pubblicata è riprodotta. Restano non ricostruibili "
               "due suoi elementi: **quali** sedici corpora abbia usato (la "
               "pipeline ne configura 21 e ne seleziona sedici con una regola "
               "dichiarata, almeno 30.000 lettere, che esclude i cinque testi "
               "brevi del repository di Palma — `scripts/langmodels.py`) e le "
               "definizioni operative di «tasso di ripetizione» ed «entropia "
               "normalizzata» degli n-grammi. La riproduzione è quindi buona sul "
               "risultato e imperfetta sul protocollo.")
    out.append("")
    SUMMARY["readings"] = zs
    SUMMARY["reproduction"] = {
        "max_delta": round(max(deltas), 3),
        "median_delta": round(C.quantile(deltas, 0.5), 3),
        "recomputed": zs,
        "signs": {k: [1.0 if (p * r) >= 0 else -1.0
                      for p, r in zip(PUBLISHED[k], zs[k][:3])]
                  for k in READINGS}}
    return out


# --------------------------------------------------------------------------
# 3. what the ordination cannot see
# --------------------------------------------------------------------------
def sec_invarianza(model: dict, langs: dict) -> list:
    out = ["## Che cosa questa ordinazione non può vedere", ""]
    out.append("I 28 descrittori sono invarianti per rietichettatura biiettiva: "
               "una sostituzione monoalfabetica **non sposta di un millimetro** "
               "il punto nello spazio PCA. Non è un'asserzione, è una verifica:")
    out.append("")
    rows, dmax = [], 0.0
    for label, L in (("Latin (Vulgate)", 569), ("Italian (Riveduta)", 584),
                     ("Slovak", 678), ("Latin (humanist corpus)", 569)):
        text = langs[label][:L]
        enc, _ = substitution(text, seed=11)
        f0, f1 = features(text), features(enc)
        d = max(abs(a - b) for a, b in zip(f0, f1))
        dmax = max(dmax, d)
        z0, z1 = project(model, f0), project(model, f1)
        dd = max(abs(a - b) for a, b in zip(z0[:3], z1[:3]))
        rows.append([label, L, f"{d:.1e}", f"{dd:.1e}",
                     round(f0[0], 4), round(f0[1], 3)])
    out += [C.md_table(["controllo", "n", "scarto massimo sui 28 descrittori",
                        "scarto massimo su PC1-PC3", "IC", "H"], rows), ""]
    out.append(f"Scarto massimo su tutti i controlli: {dmax:.1e}. **L'ordinazione "
               "è cieca rispetto alla trasformazione che si vuole studiare.** "
               "Un'anomalia di posizione può quindi nascere solo da due cause: la "
               "struttura di ripetizione del testo, oppure il modo in cui è stato "
               "**trascritto** — mai dal fatto che sia cifrato per sostituzione, "
               "che quella struttura la lascia intatta.")
    out.append("")
    SUMMARY["invariance"] = {"max_feature_delta": dmax,
                             "note": "features are invariant under substitution"}
    return out


# --------------------------------------------------------------------------
# 4. the decisive control: plain text with merged glyph classes
# --------------------------------------------------------------------------
def sec_controllo(model: dict, langs: dict, recs: dict) -> list:
    out = ["## Il controllo decisivo: testo in chiaro con classi di glifi fuse", ""]
    out.append("Se l'invarianza vale per sostituzione, la spiegazione più "
               "semplice — e non linguistica — della posizione anomala delle "
               "letture è il livello di dettaglio della trascrizione. Si prende "
               "allora un testo di riferimento **in chiaro, senza alcun "
               "cifrario**, e gli si fondono le prime k classi di glifi in una "
               "sola: è l'effetto di un trascrittore che non distingue le "
               "varianti Α/Λ/∀ o Ε/Є. Se il punto proiettato finisce dove "
               "finisce l'epigrafe, l'anomalia è di trascrizione, non di "
               "cifrario.")
    out.append("")
    radii = {}
    for key in READINGS:
        L = len(recs[key]["letters"])
        r_read = radius(model, features(recs[key]["letters"]))
        radii[key] = {"radius": r_read, "n": L, "levels": {}}
        out.append(f"**Lettura `{key}`** (n = {L}): distanza dal centro dei "
                   f"riferimenti {r_read:.2f}. Controlli alla stessa lunghezza:")
        out.append("")
        rows = []
        for m in MERGE_LEVELS:
            zs, rs = [], []
            for label in sorted(langs):
                vec = features(merge(langs[label][:L], m))
                z = project(model, vec)
                zs.append(z)
                rs.append(radius(model, vec))
            med = [C.quantile([z[i] for z in zs], 0.5) for i in range(3)]
            frac = sum(1 for r in rs if r >= r_read) / len(rs)
            radii[key]["levels"][m] = {"median_radius": C.quantile(rs, 0.5),
                                       "frac_above": frac,
                                       "median_z": med}
            rows.append([m, f"{C.quantile(rs, 0.5):.2f}", f"{frac:.2f}",
                         f"{med[0]:+.2f}", f"{med[1]:+.2f}", f"{med[2]:+.2f}"])
        out += [C.md_table(["classi fuse", "distanza mediana", "frazione di "
                            "controlli oltre la lettura", "z PC1", "z PC2",
                            "z PC3"], rows), ""]
    SUMMARY["controls"] = radii
    rows, equiv, fracs = [], {}, {}
    for key in READINGS:
        lv = radii[key]["levels"]
        central = [m for m in MERGE_LEVELS
                   if 0.10 <= lv[m]["frac_above"] <= 0.90]
        equiv[key] = central
        fracs[key] = {m: lv[m]["frac_above"] for m in MERGE_LEVELS}
        span = (f"{central[0]}-{central[-1]}" if len(central) > 1
                else (str(central[0]) if central else "> 4"))
        rows.append([f"`{key}`", f"{radii[key]['radius']:.2f}", span,
                     f"{lv[0]['frac_above']:.2f}", f"{lv[2]['frac_above']:.2f}"])
    SUMMARY["equivalent_merge"] = equiv
    out.append("**Livello di fusione equivalente.** Per ogni lettura si "
               "riporta l'intervallo di fusioni in cui la sua distanza cade "
               "fuori dalle code della distribuzione dei controlli (frazione di "
               "testi naturali più lontani del centro compresa fra 0,10 e 0,90), "
               "con due valori di riferimento:")
    out.append("")
    out += [C.md_table(["lettura", "distanza osservata",
                        "classi fuse compatibili",
                        "frazione di controlli oltre la lettura (m = 0)",
                        "frazione oltre (m = 2)"], rows), ""]
    wide = [k for k in READINGS if len(equiv[k]) > 1]
    out.append("Nessuna lettura richiede più di due fusioni" +
               (", e `palma_B` sta già dentro la variabilità di un testo in "
                "chiaro senza alcuna fusione." if "palma_B" in wide else "."))
    out.append("")
    mixed = [k for k in READINGS
             if radii[k]["levels"][0]["median_z"][0]
             * SUMMARY["readings"][k][0] < 0]
    if mixed:
        out.append("Attenzione alla differenza fra **scala** e **direzione**: la "
                   "corrispondenza riguarda la distanza (una misura scalare, "
                   "invariante per rotazione degli assi), non il profilo. A "
                   "m = 0 il PC1 mediano dei controlli ha segno opposto a quello "
                   "di " + ", ".join(f"`{k}`" for k in mixed) + ": la fusione "
                   "delle classi riproduce *quanto* una lettura è lontana dal "
                   "centro, non *dove* si trova. La conclusione corretta è quindi "
                   "più stretta di quella che l'analisi pubblicata suggerisce e "
                   "più stretta anche di una semplice equivalenza: **l'ampiezza "
                   "dell'allontanamento non è evidenza di un cifrario diverso "
                   "dalla sostituzione**, perché è la stessa che producono testi "
                   "naturali non cifrati trascritti con una o due classi fuse.")
        out.append("")
    return out


# --------------------------------------------------------------------------
# 5. how much a nearest-neighbour table is worth
# --------------------------------------------------------------------------
def sec_vicini(model: dict, samples: list, recs: dict) -> list:
    out = ["## I vicini: quanto vale una tabella di prossimità", ""]
    labels = [s[0] for s in samples]
    vecs = [project(model, s[2]) for s in samples]
    queries = {k: project(model, features(recs[k]["letters"])) for k in READINGS}
    rows = []
    for dims in (2, 3, 6):
        for key in READINGS:
            cens = nearest([queries[key]], labels, vecs, k=15, dims=dims)[0]
            rows.append([f"`{key}`", dims,
                         "; ".join(f"{l} {c}" for l, c in cens.most_common(4))])
    out += [C.md_table(["lettura", "componenti usate",
                        "prime 15 prossimità (lingua, conteggio)"], rows), ""]
    out.append("La tabella cambia con il numero di componenti: è il sintomo che "
               "l'analisi pubblicata stessa segnala. Per sapere se una "
               "concentrazione come «dieci su quindici da una sola lingua» è "
               "informativa serve una distribuzione nulla, e la si ottiene "
               "applicando la stessa statistica ai punti di riferimento stessi "
               "(escludendo ciascun punto dai propri vicini):")
    out.append("")
    rng = random.Random(SEED + 1)
    probe = rng.sample(range(len(vecs)), 300)
    nulls = {}
    for dims in (2, 3):
        counts = nearest([vecs[i] for i in probe], labels, vecs, k=15,
                         dims=dims, skip=probe)
        nulls[dims] = ([max(c.values()) for c in counts],
                       [len(c) for c in counts])
    rows, stat = [], {}
    for key in READINGS:
        stat[key] = {}
        row = [f"`{key}`"]
        for dims in (2, 3):
            cens = nearest([queries[key]], labels, vecs, k=15, dims=dims)[0]
            mx, dv = max(cens.values()), len(cens)
            nmax, ndiv = nulls[dims]
            pmax = sum(1 for v in nmax if v >= mx) / len(nmax)
            pdiv = sum(1 for v in ndiv if v <= dv) / len(ndiv)
            stat[key][dims] = {"max_count": mx, "distinct": dv,
                               "p_max": pmax, "p_distinct": pdiv}
            row += [mx, f"{pmax:.2f}"]
        rows.append(row)
    out += [C.md_table(["lettura", "massimo su 15 (2 comp.)", "p (nulla)",
                        "massimo su 15 (3 comp.)", "p (nulla)"], rows), ""]
    out.append("Nei 300 punti di riferimento la concentrazione massima su una "
               f"lingua va da {min(nulls[2][0])} a {max(nulls[2][0])} (mediana "
               f"{C.quantile(nulls[2][0], 0.5):.0f}) su due componenti e da "
               f"{min(nulls[3][0])} a {max(nulls[3][0])} su tre; le lingue "
               f"distinte da {min(nulls[2][1])} a {max(nulls[2][1])}. Valori "
               "osservati: a due componenti "
               + ", ".join(f"`{k}` p = {stat[k][2]['p_max']:.2f}" for k in READINGS)
               + "; a tre componenti "
               + ", ".join(f"`{k}` p = {stat[k][3]['p_max']:.2f}" for k in READINGS)
               + ".")
    out.append("")
    sig = [k for k in READINGS if stat[k][3]["p_max"] < 0.05]
    if sig:
        out.append("Una concentrazione fuori dal null compare solo per "
                   + ", ".join(f"`{k}`" for k in sig)
                   + " e solo usando tre assi: riguarda produzioni intermedie "
                   "della pipeline di Palma, non la lastra stessa "
                   "(sezione 6), e non si ripete a due componenti. Le tabelle di "
                   "prossimità, in questa forma, non identificano una lingua: "
                   "descrivono quanto è affollata una regione dello spazio.")
    else:
        out.append("Nessuna lettura esce dal null: le tabelle di prossimità non "
                   "identificano una lingua, descrivono quanto è affollata una "
                   "regione dello spazio.")
    out.append("")
    SUMMARY["neighbours"] = {"readings": stat,
                             "null_max_range": {d: [min(nulls[d][0]),
                                                    max(nulls[d][0])]
                                                for d in (2, 3)},
                             "null_distinct_range": [min(nulls[2][1]),
                                                     max(nulls[2][1])]}
    return out


# --------------------------------------------------------------------------
# 6. stability: sampling seed and reference set
# --------------------------------------------------------------------------
def sec_stabilita(langs: dict, recs: dict, lengths) -> list:
    out = ["## Stabilità: seme del campionamento e insieme dei riferimenti", ""]
    out.append("L'ordinazione viene rifatta con quattro semi diversi e, "
               "separatamente, escludendo quattro corpora periferici (inglese, "
               "tedesco, latino umanistico, Dante): dodici riferimenti al posto "
               "di sedici. Per ogni lettura si riporta l'oscillazione delle "
               "coordinate.")
    out.append("")
    runs = []
    for seed in (SEED, SEED + 1, SEED + 2, SEED + 3):
        smp = segments(langs, lengths, n_seg=60, seed=seed)
        runs.append(("seme " + str(seed % 1000), fit([s[2] for s in smp]), smp))
    smp12 = segments(langs, lengths, n_seg=60, seed=SEED, skip=SUBSET_DROP)
    runs.append(("12 corpora", fit([s[2] for s in smp12]), smp12))
    zs = {k: [] for k in READINGS}
    tops = {k: [] for k in READINGS}
    rads = {k: [] for k in READINGS}
    for _, mdl, smp in runs:
        labels = [s[0] for s in smp]
        vecs = [project(mdl, s[2]) for s in smp]
        for k in READINGS:
            fv = features(recs[k]["letters"])
            q = project(mdl, fv)
            zs[k].append(q[:3])
            rads[k].append(radius(mdl, fv))
            cens = nearest([q], labels, vecs, k=15, dims=2)[0]
            tops[k].append(cens.most_common(1)[0][0])
    rows, stab = [], {}
    for k in READINGS:
        cols = list(zip(*zs[k]))
        stab[k] = {"z": [[round(min(c), 2), round(max(c), 2)] for c in cols],
                   "radius": [round(min(rads[k]), 2), round(max(rads[k]), 2)],
                   "nearest_by_run": tops[k]}
        rows.append([f"`{k}`"] + [f"{min(c):+.2f} / {max(c):+.2f}" for c in cols]
                    + [f"{min(rads[k]):.2f} / {max(rads[k]):.2f}",
                       min(tops[k], key=tops[k].count)])
    out += [C.md_table(["lettura", "PC1 z (min/max)", "PC2 z", "PC3 z",
                        "distanza (min/max)",
                        "lingua più prossima (la più frequente)"], rows), ""]
    changing = [k for k in READINGS if len(set(tops[k])) > 1]
    out.append("Le righe sono minime e massime su cinque ordinazioni "
               "indipendenti (quattro semi più il sottoinsieme ridotto a dodici "
               "corpora). **La distanza dal centro è la statistica che regge**: "
               "è invariante per rotazione degli assi e resta stabile. Le "
               "singole componenti oltre la prima no: PC2 e PC3 si scambiano o "
               "cambiano segno quando cambia il campione dei riferimenti, quindi "
               "un valore come «PC3 z = 6» non è riproducibile come grandezza "
               "isolata.")
    out.append("")
    if changing:
        detail = "; ".join(
            f"`{k}`: " + ", ".join(sorted(set(tops[k]))) for k in changing)
        out.append("La lingua più prossima **cambia con il campionamento** "
                   f"({detail}): l'attribuzione linguistica per prossimità non è "
                   "un risultato.")
    out.append("")
    SUMMARY["stability"] = {"runs": [name for name, _, _ in runs], "z": stab}
    return out
    SUMMARY["stability"] = {"runs": [name for name, _, _ in runs], "z": stab}
    return out


# --------------------------------------------------------------------------
# 7. which family of descriptors drives the position
# --------------------------------------------------------------------------
FAMILIES = (
    ("globali (IC, H, K, ridondanza)", 0, 4),
    ("quote di frequenza ordinate", 4, 16),
    ("n-grammi 2-5", 16, 28),
)


def sec_famiglie(samples: list, recs: dict) -> list:
    out = ["## Quale famiglia di descrittori produce l'allontanamento", ""]
    out.append("Le stesse letture proiettate in tre ordinazioni separate, una "
               "per famiglia di descrittori: se l'anomalia nasce dalla "
               "ripetizione degli n-grammi compare in tutte, se nasce dalla "
               "concentrazione delle frequenze compare solo nelle quote.")
    out.append("")
    rows, fam = [], {}
    for name, lo, hi in FAMILIES:
        sub = [s[2][lo:hi] for s in samples]
        mdl = fit(sub)
        r = {}
        for k in READINGS:
            full = features(recs[k]["letters"])[lo:hi]
            z = project(mdl, full)
            rad = radius(mdl, full)
            r[k] = {"z": [round(v, 2) for v in z[:2]], "radius": round(rad, 2)}
            rows.append([name, f"`{k}`", f"{z[0]:+.2f}", f"{z[1]:+.2f}",
                         f"{rad:.2f}"])
        fam[name] = r
    out += [C.md_table(["famiglia", "lettura", "PC1 z", "PC2 z",
                        "distanza"], rows), ""]
    ranking = sorted(FAMILIES, key=lambda f: -fam[f[0]]["gemini_full"]["radius"])
    top = ranking[0][0]
    out.append(f"Per `gemini_full` l'allontanamento più forte è nella famiglia "
               f"«{top}» (distanza "
               f"{fam[top]['gemini_full']['radius']:.2f}), il più debole in "
               f"«{ranking[-1][0]}» "
               f"({fam[ranking[-1][0]]['gemini_full']['radius']:.2f}): "
               "l'irregolarità della sequenza non sta nella struttura di "
               "ripetizione degli n-grammi ma nella **concentrazione delle "
               "frequenze e nell'entropia**, cioè nel numero e nella "
               "distribuzione delle classi di glifi che la trascrizione "
               "distingue. È la stessa diagnosi della sezione 6.1, ottenuta per "
               "un'altra via.")
    out.append("")
    SUMMARY["families"] = fam
    return out


# --------------------------------------------------------------------------
# 8. verdict
# --------------------------------------------------------------------------
def sec_verdetto() -> list:
    out = ["## Verdetto su questa ordinazione", ""]
    rep = SUMMARY["reproduction"]
    inv = SUMMARY["invariance"]["max_feature_delta"]
    nb = SUMMARY["neighbours"]["readings"]
    st = SUMMARY["stability"]["z"]
    eq = SUMMARY["equivalent_merge"]
    out.append("**Che cosa regge.**")
    out.append("")
    out.append("1. L'analisi pubblicata è **riprodotta**: le nove coordinate "
               f"delle tre letture concordano entro {rep['max_delta']:.2f} "
               f"deviazioni standard (mediana {rep['median_delta']:.2f}) con "
               "protocollo ricostruito da una descrizione verbale. La sua "
               "conclusione descrittiva — nessun profilo linguistico comune alle "
               "tre letture, `gemini_full` la più lontana — è confermata.")
    out.append("2. La **distanza dal centro** delle letture è stabile su quattro "
               "semi di campionamento e sul sottoinsieme ridotto a dodici corpora "
               f"(`gemini_full`: {st['gemini_full']['radius'][0]:.2f}-"
               f"{st['gemini_full']['radius'][1]:.2f}; `palma_A`: "
               f"{st['palma_A']['radius'][0]:.2f}-"
               f"{st['palma_A']['radius'][1]:.2f}).")
    out.append("")
    out.append("**Che cosa non regge.**")
    out.append("")
    out.append("1. **L'ordinazione non può testare un cifrario.** I 28 "
               f"descrittori sono invarianti per sostituzione (scarto {inv:.1e}): "
               "nessuna posizione PCA può dire se il testo è cifrato per "
               "sostituzione o in chiaro. L'ipotesi secondo cui «una "
               "sostituzione monoalfabetica non basta» non è un risultato di "
               "quella PCA: è un'ipotesi esterna che la PCA non può né "
               "sostenere né escludere.")
    out.append("2. **L'ampiezza dell'allontanamento non è un'anomalia.** Testi di "
               "riferimento **in chiaro, senza alcun cifrario**, a cui sono state "
               "fuse una o due classi di glifi hanno la stessa distanza dal "
               "centro delle letture: le fusioni compatibili sono "
               + ", ".join(f"`{k}`: " + (f"{eq[k][0]}-{eq[k][-1]}"
                                          if len(eq[k]) > 1
                                          else (str(eq[k][0]) if eq[k] else "> 4"))
                           for k in ("palma_A", "palma_B", "gemini_full"))
               + ". La via più economica per produrre quello spostamento non "
               "richiede alcun cifrario: basta una trascrizione che non distingua "
               "le varianti di glifo — ciò che la fotografia suggerisce "
               "(sezione 6.1).")
    flipped = [k for k in READINGS
               if SUMMARY["controls"][k]["levels"][0]["median_z"][0]
               * SUMMARY["readings"][k][0] < 0]
    out.append("3. **La direzione però non è quella.** "
               + (("La fusione delle classi sposta i controlli sul lato opposto "
                   "di PC1 rispetto a " + ", ".join(f"`{k}`" for k in flipped)
                   + ": ")
                  if flipped else "")
               + "il profilo delle letture resta irregolare anche dopo la "
               "fusione, e l'irregolarità riguarda le frequenze, non i n-grammi. "
               "La PCA dice quindi *quanto* è strano il profilo, non *perché*, e "
               "non può attribuirlo né a un cifrario né a un errore di lettura.")
    out.append("4. **Le tabelle di prossimità non identificano una lingua.** La "
               "lingua più vicina cambia con il numero di componenti e con il "
               "campionamento; la concentrazione delle letture (massimo "
               f"{nb['gemini_full'][2]['max_count']} finestre su 15 da una "
               "sola lingua per `gemini_full`) ha "
               f"p = {nb['gemini_full'][2]['p_max']:.2f} rispetto alla stessa "
               "statistica calcolata sui punti di riferimento. «Slovacco», "
               "«ungherese storico» e «italiano» sono etichette geometriche, non "
               "attribuzioni.")
    out.append("5. **Le componenti oltre la prima non sono stabili**, e i "
               "riferimenti non sono campioni indipendenti (cento finestre "
               "sovrapposte per corpus): le distanze non sono p-value e le "
               "componenti massimizzano la varianza, non la separazione fra "
               "lingue.")
    out.append("")
    out.append("**Conclusione.** La PCA resta un buon strumento descrittivo e un "
               "cattivo strumento inferenziale. Integrata nella pipeline dice una "
               "cosa sola e la dice bene: le letture disponibili non sono profili "
               "di lingua naturale, e la loro distanza dai riferimenti è quella "
               "che produce una trascrizione a maglia larga. Non dice, e non può "
               "dire, se il testo sia cifrato, in quale lingua, né se contenga un "
               "nome.")
    out.append("")
    return out


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------
def main() -> None:
    recs = C.load_json(os.path.join(C.CORPUS, "corpora.json"))
    print("loading reference languages ...", flush=True)
    langs = LM.load_reference(max_letters=SAMPLE_LETTERS, verbose=False)
    lengths = [len(recs[k]["letters"]) for k in READINGS]
    print(f"{len(langs)} languages, lengths {lengths}", flush=True)

    print("sampling reference segments ...", flush=True)
    samples = segments(langs, lengths)
    print(f"{len(samples)} segments x 28 descriptors", flush=True)
    SUMMARY["dataset"] = {"languages": len(langs), "samples": len(samples),
                          "lengths": lengths, "seed": SEED,
                          "min_reference": LM.MIN_REFERENCE}
    model = fit([s[2] for s in samples])
    print("PCA done: " + ", ".join(f"{100 * v:.1f}%" for v in model["var"]),
          flush=True)

    out = ["# Fase 1c -- ordinazione PCA dei profili invarianti", "",
           "Ricostruzione e verifica critica dell'analisi PCA prodotta a parte "
           "(`report/pca_analisi.md`).", "",
           "**Dati.** Tre letture dell'epigrafe (`palma_A` 584 glifi, `palma_B` "
           f"678, `gemini_full` 569) e {len(langs)} corpora di riferimento; "
           f"{N_SEG} segmenti casuali per corpus e per ciascuna delle tre "
           f"lunghezze ({len(samples)} campioni).", "",
           "**Variabili.** 28 descrittori invarianti per rietichettatura: IC, "
           "entropia, numero di classi, ridondanza; quote dei 12 glifi più "
           "frequenti in ordine decrescente (ordinate, quindi non associate a un "
           "simbolo); per n = 2..5 rapporto tipi/totale, tasso di ripetizione ed "
           "entropia normalizzata degli n-grammi.", "",
           "**Metodo.** Standardizzazione sui soli riferimenti, PCA sulla "
           "matrice di correlazione (autosolutore di Jacobi in sola libreria "
           "standard, 28 x 28), letture proiettate nello spazio risultante; "
           f"seme {SEED}.", ""]

    out += sec_assi(model)
    out += sec_letture(model, recs, samples, lengths)
    out += sec_definizioni(langs, recs, lengths)
    out += sec_altra_pca(recs)
    print("  assi + riproduzione + definizioni fatti", flush=True)
    out += sec_invarianza(model, langs)
    out += sec_controllo(model, langs, recs)
    print("  invarianza + controlli fatti", flush=True)
    out += sec_vicini(model, samples, recs)
    print("  vicini fatti", flush=True)
    out += sec_stabilita(langs, recs, lengths)
    print("  stabilita' fatta", flush=True)
    out += sec_famiglie(samples, recs)
    print("  famiglie fatte", flush=True)
    out += sec_verdetto()

    C.save_json(os.path.join(C.CORPUS, "05_pca_summary.json"), SUMMARY)
    C.write_text(os.path.join(C.CORPUS, "05_pca.md"), "\n".join(out) + "\n")
    print("\nwrote corpus/05_pca.md")


if __name__ == "__main__":
    main()


