# -*- coding: utf-8 -*-
"""00_corpus.py -- Phase 0: build the canonical corpus of transcriptions.

Sources handled
---------------
1. Palma 2023 repository (``sources/MaLaNova-master``), 9 transcription files;
2. the Gemini conversation log (``dracula_epigrafe.md``) which embeds a 33-line
   transcription of the slab and a repeated 8-line "central block";
3. ``epigrafe drac.md``, a degraded/OCR-like alternative reading.

Outputs
-------
``corpus/corpora.json``  normalised sequences + provenance
``corpus/00_corpus.md``  human readable report (stats, alignment, confusion)
"""

from __future__ import annotations

import importlib.util
import os
import re
import shutil
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C

C.utf8_stdout()

# --------------------------------------------------------------------------
# 1. registry of sources
# --------------------------------------------------------------------------
REPO_FILES = [
    ("palma_A", "stringaoriginale.txt",
     "Palma 2023, arbitrary Latin-letter transliteration with word gaps "
     "('.'=separator, '?'=illegible)"),
    ("palma_A2", "stringaoriginale2.txt",
     "Palma 2023, subset of palma_A (rows kept for the AZdecrypt run)"),
    ("palma_A_nosp", "stringanospaces.txt",
     "Palma 2023, same as palma_A without spaces (scriptio continua)"),
    ("palma_B", "soluzione.txt",
     "Palma 2023, final glyph string in Greek letter labels"),
    ("palma_C", "scriptiocontinua.txt",
     "Palma 2023, 17-class merged variant with gaps"),
    ("palma_B2", "scriptiocontinua2.txt",
     "Palma 2023, filled Latin-letter variant (same letter count as palma_B)"),
    ("palma_B3", "scriptiocontinua3.txt",
     "Palma 2023, shortened filled variant"),
    ("palma_B4", "scriptiocontinua4.txt",
     "Palma 2023, filled variant split one chunk per line"),
    ("palma_C_nq", "scriptiocontinuanoq.txt",
     "Palma 2023, 17-class merged variant, gaps removed"),
]

#: characters allowed inside a glyph line of the Gemini log
GLYPH_CHARS = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                  "\u0391\u0392\u0393\u0394\u0395\u0396\u0397\u0398\u0399"
                  "\u039a\u039b\u039c\u039d\u039e\u039f\u03a0\u03a1\u03a3"
                  "\u03a4\u03a5\u03a6\u03a7\u03a8\u03a9"
                  "\u2200\u2021\u2020+\u00b7.,-\\' ")

NOISE = [re.compile(p) for p in (
    r"^##\s*Page", r"^\d+/\d+$", r"^https?://", r"^\d{1,2}/\d{1,2}/\d{2},",
    r"^L.enigma dell.epigrafe", r"^User prompt:", r"^Response:",
)]


def is_glyph_line(line: str) -> bool:
    s = line.strip()
    if any(p.match(s) for p in NOISE):
        return False
    if len(s) < 6:
        return False
    body = [ch for ch in s if not ch.isspace()]
    if not body:
        return False
    letters = [ch for ch in body if ch.isalpha()]
    if len(letters) < 6:
        return False
    allowed = sum(1 for ch in body if ch in GLYPH_CHARS)
    if allowed / len(body) < 0.95:
        return False
    upper = sum(1 for ch in letters if ch.isupper()) / len(letters)
    return upper > 0.75


def glyph_groups(text: str) -> list:
    """Consecutive runs of glyph lines; page headers are transparent."""
    groups, cur = [], []
    for line in text.splitlines():
        s = line.strip()
        if any(p.match(s) for p in NOISE) or not s:
            continue  # page headers/footers do not break a run
        if is_glyph_line(line):
            cur.append(s)
        else:
            if len(cur) >= 3:
                groups.append(cur)
            cur = []
    if len(cur) >= 3:
        groups.append(cur)
    return groups


def extract_gemini(md_path: str) -> dict:
    text = C.read_text(md_path)
    groups = glyph_groups(text)
    full = max(groups, key=len)
    central = None
    for g in groups:  # the standalone 8-line block, first reading
        if len(g) == 8 and g[0].startswith("PEVPIV"):
            central = g
            break
    if central is None:  # fall back: window around the DEDED palindrome
        for g in groups:
            for i, ln in enumerate(g):
                if "DEDED" in ln:
                    central = g[max(0, i - 5):i + 3]
                    break
            if central:
                break
    inner = None  # the central block *inside* the 33-line transcription
    for i, ln in enumerate(full):
        if "DEDED" in ln:
            inner = full[max(0, i - 6):i + 2]
            break
    return {"gemini_full": full, "gemini_central": central or [],
            "gemini_central_in_full": inner or [],
            "all_groups": groups}


def extract_drac(path: str) -> list:
    out = []
    for line in C.read_text(path).splitlines():
        s = line.replace("\\+", "+").replace("\\-", "-").strip()
        s = re.sub(r"\bp\.\s*\d+$", "", s).strip(" ,;")
        if not s:
            continue
        if sum(1 for ch in s if ch.isalpha()) < 2:
            continue
        out.append(s)
    return out


# --------------------------------------------------------------------------
# 2. normalisation of one transcription into a record
# --------------------------------------------------------------------------
def make_record(key: str, lines, provenance: str) -> dict:
    raw = "\n".join(lines)
    clean = C.normalize_cipher(raw)
    letters = clean.replace(C.GAP, "")
    toks = C.word_tokens(raw)
    return {
        "key": key,
        "provenance": provenance,
        "n_lines": len(lines),
        "n_symbols": len(clean),
        "n_letters": len(letters),
        "n_gaps": clean.count(C.GAP),
        "K": len(set(letters)),
        "ic": round(C.ic(letters), 6),
        "ic26": round(C.ic26(letters), 4),
        "entropy": round(C.entropy(letters), 4),
        "n_tokens": len(toks),
        "tokens": toks,
        "lines": lines,
        "clean": clean,
        "letters": letters,
        "alphabet": "".join(sorted(set(letters))),
    }


def build() -> dict:
    records = {}
    for key, fname, prov in REPO_FILES:
        path = os.path.join(C.REPO, fname)
        records[key] = make_record(key, C.read_text(path).splitlines(),
                                   f"repo:{fname} -- {prov}")

    gem = extract_gemini(os.path.join(C.BASE, "dracula_epigrafe.md"))
    records["gemini_full"] = make_record(
        "gemini_full", gem["gemini_full"],
        "Gemini log (dracula_epigrafe.md), 33-line transcription embedded in "
        "testo_epigrafe_completo; the archived conversation describes it as a "
        "simulation of the slab's rows (not an independent transcription), so "
        "it is used here as a comparison term only")
    records["gemini_central"] = make_record(
        "gemini_central", gem["gemini_central"],
        "Gemini log, standalone 8-line central block (declared simulation)")
    records["gemini_central_in_full"] = make_record(
        "gemini_central_in_full", gem["gemini_central_in_full"],
        "Gemini log, central 8 lines inside the 33-line transcription "
        "(declared simulation)")

    drac = extract_drac(os.path.join(C.BASE, "epigrafe drac.md"))
    records["drac_raw"] = make_record(
        "drac_raw", drac, "epigrafe drac.md -- degraded/OCR-like reading")
    return records


# --------------------------------------------------------------------------
# 3. pairwise comparison
# --------------------------------------------------------------------------
PAIRS = [
    ("palma_A", "palma_B"),
    ("palma_A", "gemini_full"),
    ("palma_B", "gemini_full"),
    ("palma_B", "palma_C_nq"),
    ("gemini_central", "gemini_central_in_full"),
    ("gemini_full", "drac_raw"),
]


def confusion_rows(cols, top: int = 30, inv=None) -> list:
    """For each left-hand symbol, the right-hand symbols it aligns with."""
    by_a = {}
    for (x, y), n in C.confusion_matrix(cols).items():
        if x == "-" or y == "-":
            continue
        by_a.setdefault(x, {})
        by_a[x][y] = n
    rows = []
    for x in sorted(by_a, key=lambda s: -sum(by_a[s].values()))[:top]:
        tot = sum(by_a[x].values())
        best = sorted(by_a[x].items(), key=lambda kv: -kv[1])[:3]
        name = f"{x} (<- {inv[x]})" if inv and x in inv else x
        rows.append([name, " ".join(f"{y}({n})" for y, n in best), tot,
                     round(best[0][1] / tot, 2)])
    return rows


def chance_identity(seq_a, seq_b, mapping) -> float:
    """Identity expected if the two strings were independent over the same classes."""
    n = len(seq_a)
    pa = {s: c / n for s, c in C.freq(seq_a).items()}
    m = len(seq_b)
    pb = {s: c / m for s, c in C.freq(seq_b).items()}
    return sum(p * pb.get(mapping.get(s), 0.0) for s, p in pa.items())


# --------------------------------------------------------------------------
# imaging / OCR probe
# --------------------------------------------------------------------------
#: extensions of the photographs that could in principle carry the inscription
IMAGE_EXT = (".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff",
             ".bmp", ".heic", ".dng")
#: OCR command line tools (``pytesseract`` alone is only a wrapper)
OCR_BINARIES = ("tesseract", "ocrmypdf")
#: python OCR packages, wrapper first
OCR_MODULES = ("pytesseract", "easyocr", "paddleocr", "doctr",
               "rapidocr_onnxruntime", "keras_ocr")
#: packages that cannot run without the tesseract binary
OCR_WRAPPERS = {"pytesseract"}
#: SOFn markers that carry the frame size in a JPEG stream
JPEG_SOF = set(range(0xC0, 0xD0)) - {0xC4, 0xC8, 0xCC}


def _jpeg_size(data: bytes):
    """Width and height from the first SOFn segment, without Pillow."""
    i, n = 2, len(data)
    while i + 9 < n:
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        if marker in JPEG_SOF:
            h, w = struct.unpack(">HH", data[i + 5:i + 9])
            return w, h
        if marker in (0x01, 0xD8) or 0xD0 <= marker <= 0xD7:
            i += 2
            continue
        i += 2 + struct.unpack(">H", data[i + 2:i + 4])[0]
    return None


def _webp_size(data: bytes):
    """Width and height of a RIFF/WEBP container (VP8, VP8L or VP8X)."""
    chunk = data[12:16]
    if chunk == b"VP8X":
        return (1 + int.from_bytes(data[24:27], "little"),
                1 + int.from_bytes(data[27:30], "little"))
    if chunk == b"VP8 ":
        return (int.from_bytes(data[26:28], "little") & 0x3FFF,
                int.from_bytes(data[28:30], "little") & 0x3FFF)
    if chunk == b"VP8L":
        bits = int.from_bytes(data[21:25], "little")
        return (bits & 0x3FFF) + 1, ((bits >> 14) & 0x3FFF) + 1
    return None


def image_size(path: str):
    """Pixel size of a JPEG, WEBP or PNG file (``None`` if not decodable)."""
    with open(path, "rb") as fh:
        data = fh.read(1 << 20)
    if data[:2] == b"\xff\xd8":
        return _jpeg_size(data)
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return _webp_size(data)
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return struct.unpack(">II", data[16:24])
    return None


def _has_module(name: str) -> bool:
    try:
        return importlib.util.find_spec(name) is not None
    except (ImportError, ValueError):
        return False


def ocr_state() -> dict:
    """Which OCR path, if any, this environment can actually execute."""
    binaries = [b for b in OCR_BINARIES if shutil.which(b)]
    modules = [m for m in OCR_MODULES if _has_module(m)]
    runnable = list(binaries) + [m for m in modules if m not in OCR_WRAPPERS]
    return {"binaries": binaries, "modules": modules, "runnable": runnable}


def imaging_report(recs: dict):
    """Measure what the available photographs support, and what they do not.

    Glyph cell and row pitch are *optimistic upper bounds*: they assume the
    inscription fills the whole frame with perfectly uniform rows, so the real
    values are smaller.  They are reported because turning "the photographs are
    not good enough" into a number is what makes the claim checkable.
    """
    ref = recs.get("gemini_full") or {}
    rows_n = ref.get("n_lines") or 0
    glyphs = ref.get("n_letters") or 0
    per_line = glyphs / rows_n if rows_n else 0.0

    names = sorted(f for f in os.listdir(C.BASE)
                   if f.lower().endswith(IMAGE_EXT))
    images = []
    for name in names:
        path = os.path.join(C.BASE, name)
        size = image_size(path)
        rec = {"file": name, "bytes": os.path.getsize(path),
               "width": None, "height": None}
        if size:
            w, h = size
            rec.update({"width": w, "height": h, "pixels": w * h,
                        "bytes_per_pixel": round(rec["bytes"] / float(w * h), 3)})
            if per_line:
                rec["cell_px_upper"] = round(w / per_line, 1)
                rec["line_px_upper"] = round(h / rows_n, 1)
        images.append(rec)

    payload = {
        "images": images,
        "reference_geometry": {
            "key": "gemini_full", "rows": rows_n, "glyphs": glyphs,
            "glyphs_per_line": round(per_line, 1),
            "basis": "optimistic upper bound: inscription filling the frame, "
                     "uniform rows"},
        "ocr": ocr_state(),
    }
    return payload, _imaging_md(payload)


def _imaging_md(payload: dict) -> list:
    geo = payload["reference_geometry"]
    ocr = payload["ocr"]
    md = ["## 3.6 Imaging and OCR probe", ""]
    md.append("What the photographs physically support, measured instead of "
              "asserted. Glyph cell and row pitch are an **optimistic upper "
              "bound**: the inscription is assumed to fill the whole frame with "
              f"{geo['rows']} uniform rows enclosing {geo['glyphs']} glyphs "
              f"({geo['glyphs_per_line']} per row), so the real values are "
              "smaller.")
    md.append("")
    md.append(C.md_table(
        ["file", "pixels", "total px", "bytes", "bytes/px",
         "glyph cell (max)", "row pitch (max)"],
        [[f"`{r['file']}`",
          f"{r['width']}x{r['height']}" if r["width"] else "?",
          f"{r.get('pixels', '?')}", f"{r['bytes']}",
          f"{r['bytes_per_pixel']:.2f}" if "bytes_per_pixel" in r else "?",
          f"{r['cell_px_upper']:.1f}" if "cell_px_upper" in r else "?",
          f"{r['line_px_upper']:.1f}" if "line_px_upper" in r else "?"]
         for r in payload["images"]]))
    md.append("")
    if ocr["runnable"]:
        md.append("OCR engine available: " + ", ".join(ocr["runnable"]) + ".")
    else:
        why = []
        if not ocr["binaries"]:
            why.append("the `tesseract` binary is not on PATH")
        if "pytesseract" in ocr["modules"]:
            why.append("`pytesseract` is installed but only wraps that binary")
        md.append("**No runnable OCR engine**: " + "; ".join(why) +
                  ". This phase produces no machine transcription, and none is "
                  "simulated in its place: the strings analysed downstream "
                  "remain the published ones (section 3.1).")
    md.append("")
    return md


def main() -> None:
    recs = build()
    C.save_json(os.path.join(C.CORPUS, "corpora.json"),
                {k: {kk: vv for kk, vv in v.items() if kk != "lines"}
                 for k, v in recs.items()})
    C.save_json(os.path.join(C.CORPUS, "lines.json"),
                {k: v["lines"] for k, v in recs.items()})

    out = ["# Phase 0 -- canonical corpus of the Santa Maria la Nova epigraph",
           "", "## 3.1 Transcription inventory", ""]
    rows = [[k, v["n_lines"], v["n_symbols"], v["n_letters"], v["n_gaps"],
             v["K"], round(v["ic"], 4), v["ic26"], round(v["entropy"], 3),
             v["n_tokens"]] for k, v in recs.items()]
    out.append(C.md_table(["key", "lines", "symbols", "letters", "gaps",
                           "#glyphs", "IC", "ICx26", "H", "tokens"], rows))
    out.append("")
    out.append("Provenance:")
    for k, v in recs.items():
        out.append(f"- **{k}** -- {v['provenance']}")
    out.append("")
    out.append("Note: `ICx26` is Palma's normalised IC (cf. his Table 1, "
               "value 1.72 for the inscription).")
    out.append("")

    out.append("## 3.2 Pairwise alignment after frequency-rank relabeling")
    out.append("")
    out.append("Transcriptions of the same slab use unrelated label alphabets, so "
               "a naive alignment scores 2% identity by construction.  Each pair "
               "is therefore compared after mapping the k-th most frequent symbol "
               "of reading A onto the k-th most frequent symbol of reading B (a "
               "substitution preserves the frequency order); the residual "
               "mismatches are then real disagreements.")
    out.append("")
    aligns = {}
    rows = []
    for a, b in PAIRS:
        sa, sb = recs[a]["clean"], recs[b]["clean"]
        mp = C.profile_map(sa, sb)
        r = C.align(C.apply_map(sa, mp), sb)
        aligns[f"{a}~{b}"] = r
        rows.append([f"{a} ~ {b}", len(sa), len(sb), r["n_columns"],
                     round(r["identity"], 4),
                     round(chance_identity(sa, sb, mp), 4),
                     round(r["score"], 1)])
    out.append(C.md_table(["pair", "len A", "len B", "columns", "identity",
                           "chance", "score"], rows))
    out.append("")
    out.append("`chance` is the identity expected between two independent "
               "strings sharing the same class distribution: it is the null "
               "model for 'these readings are unrelated'.")
    out.append("")

    for pair in ("palma_A~palma_B", "palma_B~gemini_full"):
        a, b = pair.split("~")
        inv = {v: k for k, v in
               C.profile_map(recs[a]["clean"], recs[b]["clean"]).items()}
        out.append(f"### Glyph confusion, {pair}")
        out.append("")
        out.append(C.md_table(
            [f"symbol of {a} -> {b}", f"top matches in {b}", "n", "purity"],
            confusion_rows(aligns[pair]["columns"], inv=inv)))
        out.append("")

    out.append("## 3.3 Where the readings agree")
    out.append("")
    cols = aligns["palma_A~palma_B"]["columns"]
    same = "".join(x if x == y else "\u00b7" for x, y in cols)
    out.append("`palma_A ~ palma_B`: letter where both readings coincide, "
               "`\u00b7` where they differ.")
    out.append("")
    out.append("```")
    for i in range(0, len(same), 100):
        out.append(same[i:i + 100])
    out.append("```")
    out.append("")

    out.append("## 3.4 Relabel-invariant agreement between readings")
    out.append("")
    out.append("Different transcriptions label the same glyphs with different "
               "alphabets (Latin letters vs Greek letters), so symbol-by-symbol "
               "identity is meaningless across sources.  What *is* comparable is "
               "the repetition pattern: after canonical relabeling two readings of "
               "the same text must give nearly the same string.")
    out.append("")
    rows = []
    for a, b in PAIRS:
        pa = C.relabel(recs[a]["letters"])
        pb = C.relabel(recs[b]["letters"])
        L, ia, ib = C.longest_common_substring(pa, pb)
        al = C.align(pa, pb)
        rows.append([f"{a} ~ {b}", len(pa), len(pb), L,
                     round(L / min(len(pa), len(pb)), 3),
                     round(al["identity"], 3)])
    out.append(C.md_table(["pair", "len A", "len B", "common block",
                           "share of shorter", "relabel identity"], rows))
    out.append("")
    out.append("## 3.5 Excess repetitiveness relative to a random text")
    out.append("")
    out.append("The IC of a ciphertext is invariant under substitution, but it "
               "*does* depend on how many glyph classes the transcriber "
               "distinguished: merging glyphs concentrates the distribution and "
               "inflates the IC.  The scale-free measure is IC x K, which equals "
               "1.0 for a uniform random text over K glyphs and ~1.9 for Latin "
               "letters (see 01_descriptive.md).")
    out.append("")
    rows = []
    for k, v in recs.items():
        rows.append([k, v["n_letters"], v["K"], round(v["ic"], 4),
                     round(v["ic"] * v["K"], 3),
                     round(v["ic"] * max(v["K"], 1) - 1.0, 3)])
    out.append(C.md_table(["key", "n", "K", "IC", "IC x K",
                           "excess over random"], rows))
    out.append("")

    img_payload, img_md = imaging_report(recs)
    C.save_json(os.path.join(C.CORPUS, "imaging.json"), img_payload)
    out += img_md

    C.write_text(os.path.join(C.CORPUS, "00_corpus.md"), "\n".join(out) + "\n")

    for k, v in recs.items():
        print(f"{k:24s} lines={v['n_lines']:3d} symbols={v['n_symbols']:4d} "
              f"letters={v['n_letters']:4d} gaps={v['n_gaps']:3d} "
              f"K={v['K']:2d} IC={v['ic']:.4f} IC26={v['ic26']:.3f} "
              f"tokens={v['n_tokens']:3d}")
    print()
    for pair, r in aligns.items():
        print(f"{pair:40s} identity={r['identity']:.4f} cols={r['n_columns']}")
    print("\nwrote corpus/corpora.json, corpus/lines.json, corpus/imaging.json "
          "and corpus/00_corpus.md")


if __name__ == "__main__":
    main()

