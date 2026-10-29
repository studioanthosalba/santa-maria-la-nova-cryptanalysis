# -*- coding: utf-8 -*-
"""_extract_pdf.py -- put the external PDFs on the record.

Tooling, like ``_fetch_external.py``: it is *not* part of the analysis pipeline
and needs an optional package (``PyPDF2``).  The pipeline keeps reading only
the ``.txt`` files it produces.

For each PDF on the record it writes a manifest entry (size, SHA256, pages) and
inspects every page:

* page has a text layer -> text is extracted (with mojibake repair) and written
  to the ``.txt`` target, but **only if it is long enough to be real**;
* page is a single image  -> nothing is extracted; the raster is described
  (filter, pixel size, colour space) and the document is flagged
  ``image_only``, because the text can then only be read page by page with
  ``_pdf_pages.py``.

It never overwrites an existing extract with an empty or truncated one: that is
the failure it is written to avoid.  Use ``--force`` to overwrite on purpose.

Output: ``report/atti/manifest.json``.

Usage
-----
    python scripts/_extract_pdf.py [--force] [--check]
"""

from __future__ import annotations

import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C

C.utf8_stdout()

from _pdf_pages import page_image  # noqa: E402  (tooling import, same folder)

#: source PDF -> (output path relative to the repository root, human label)
PDFS = [
    ("View of Encrypted epigraphy - the case of a mysterious inscription in "
     "the Neapolitan church of Santa Maria La Nova.pdf",
     "report/atti/palma_histocrypt2023.txt",
     "Palma 2023, HistoCrypt -- the paper under examination"),
    ("View of Encrypted Documents and Cipher Keys From the 18th and 19th "
     "Century in the Archives of Aristocratic Families in Slovakia.pdf",
     "report/atti/slovakia_cipher_keys.txt",
     "Antal, Marak, Zajac, Lengyelova, Duchonova -- encrypted documents and "
     "surviving cipher keys, Slovak National Archive"),
    ("View of International Conference on the Voynich Manuscript 2022.pdf",
     "report/atti/voynich2022.txt",
     "Layfield et al. 2022 -- Voynich conference report (methodology)"),
]

MANIFEST_OUT = "report/atti/manifest.json"

#: below this, an "extract" is a failure, not a text
MIN_CHARS = 500

#: substrings that betray a latin-1/cp1252 mis-decode
MOJIBAKE = ("â€", "Ã¢", "Ã¨", "Ã¹", "Ã ", "Â«", "Â»", "Â°", "â€™", "â€œ")


def repair_mojibake(line: str) -> str:
    """Undo a latin-1/cp1252 round trip, but only if it actually helps."""
    if not any(m in line for m in MOJIBAKE):
        return line
    try:
        fixed = line.encode("cp1252", "strict").decode("utf-8", "strict")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return line
    bad = lambda s: (s.count("\ufffd") + sum(s.count(m) for m in MOJIBAKE))
    return fixed if bad(fixed) < bad(line) else line


def sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 16), b""):
            h.update(block)
    return h.hexdigest()


def inspect(path: str) -> dict:
    """Return what the PDF contains, page by page."""
    from PyPDF2 import PdfReader
    reader = PdfReader(path)
    pages, texts = [], []
    for n, page in enumerate(reader.pages, 1):
        found = page_image(page)
        entry = {"page": n}
        if found:
            _, img = found
            filt = img.get("/Filter")
            entry["raster"] = {
                "filter": filt if isinstance(filt, str)
                else [str(f) for f in filt],
                "px": f"{img['/Width']}x{img['/Height']}",
                "bits": img.get("/BitsPerComponent"),
            }
        else:
            raw = page.extract_text() or ""
            text = "\n".join(repair_mojibake(l) for l in raw.splitlines())
            entry["text_chars"] = len(text)
            texts.append(text)
        pages.append(entry)
    page_px = None
    if pages and "raster" in pages[0]:
        page_px = pages[0]["raster"]["px"]
    w = int(page_px.split("x")[0]) if page_px else 0
    return {"n_pages": len(pages), "pages": pages, "text": "\n\n".join(texts),
            "page_px": page_px,
            "image_only": all("raster" in p for p in pages),
            "ppi_at_a4": round(w / (210 / 25.4)) if w else None}


def main() -> None:
    force = "--force" in sys.argv
    check_only = "--check" in sys.argv
    manifest, problems = [], []
    for src, rel_out, label in PDFS:
        path = os.path.join(C.BASE, src)
        if not os.path.exists(path):
            problems.append(f"missing source: {src}")
            continue
        rec = {"source": src, "label": label, "pdf_bytes": os.path.getsize(path),
               "pdf_sha256": sha256(path), "text_out": rel_out}
        try:
            info = inspect(path)
        except ImportError as exc:
            print(exc)
            return
        text = info.pop("text")
        rec.update(info)
        out_path = os.path.join(C.BASE, rel_out)
        rec["extract_written"] = False
        if text.strip() and len(text) >= MIN_CHARS:
            if (force or not os.path.exists(out_path)) and not check_only:
                C.write_text(out_path, text.strip() + "\n")
                rec["extract_written"] = True
            rec["extract_chars"] = len(text)
        else:
            rec["note"] = ("no text layer: page images only, read with "
                           "_pdf_pages.py")
        manifest.append(rec)
        kind = ("image-only" if rec["image_only"] else "text layer")
        print(f"{os.path.basename(src)[:46]:46s} {kind} {rec['n_pages']}p "
              f"{rec.get('page_px') or '':10s} {rec.get('extract_chars') or 0:6d} chars")
    if not check_only:
        os.makedirs(os.path.join(C.BASE, "report", "atti"), exist_ok=True)
        C.save_json(os.path.join(C.BASE, MANIFEST_OUT), {"documents": manifest})
        print(f"\nwrote {MANIFEST_OUT}")
    for p in problems:
        print(p)


if __name__ == "__main__":
    main()
