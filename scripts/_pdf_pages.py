# -*- coding: utf-8 -*-
"""_pdf_pages.py -- rasterise an image-only PDF page to PNG (standard library).

The three PDFs on the record have no text layer: each page is a single
``/Image`` XObject, Flate-encoded, 8-bit, ICCBased RGB, 1240x1753 px (~150 dpi
A4).  There is no OCR engine in this environment, so the only way to read them
is to look at them.  This tool writes one page as PNG so that it can be
inspected (and so that any statement about the documents can be traced back to
a page number).

It handles the two encodings actually present in these files plus the common
ones, and refuses anything else instead of guessing:

    /FlateDecode + 8-bit gray / RGB   -> decoded, re-encoded as PNG
    /DCTDecode                        -> dumped as .jpg, untouched
    anything else                     -> error, no output

Usage
-----
    python scripts/_pdf_pages.py FILE.pdf PAGE [PAGE ...] [--scale N]
    python scripts/_pdf_pages.py FILE.pdf --info

Output goes to ``report/atti/pages/`` as ``<slug>-p<N>.png``.
"""

from __future__ import annotations

import os
import struct
import sys
import zlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C

C.utf8_stdout()

OUT_DIR = os.path.join(C.BASE, "report", "atti", "pages")


def _reader(path):
    from PyPDF2 import PdfReader  # optional, tooling only
    return PdfReader(path)


def page_image(page):
    """Return the single image XObject of a page (name, object) or None."""
    res = page.get("/Resources") or {}
    xobj = res.get("/XObject")
    if not xobj:
        return None
    for name, ref in xobj.items():
        obj = ref.get_object()
        if obj.get("/Subtype") == "/Image":
            return name, obj
    return None


def _components(img):
    cs = img.get("/ColorSpace")
    if isinstance(cs, list) and cs:
        head = cs[0]
        if head == "/ICCBased":
            n = cs[1].get_object().get("/N", 3)
            return {1: 1, 3: 3, 4: 3}[n]
        if head in ("/Indexed", "/Separation"):
            raise ValueError(f"colour space {head} not supported")
    if cs in ("/DeviceRGB", "/CalRGB"):
        return 3
    if cs == "/DeviceGray":
        return 1
    raise ValueError(f"colour space {cs} not supported")


def write_png(path, width, height, ncomp, data, scale=1):
    """Minimal PNG writer; ``scale`` > 1 subsamples (nearest neighbour)."""
    stride = width * ncomp
    if scale > 1:
        rows = []
        for y in range(0, height, scale):
            row = data[y * stride:(y + 1) * stride]
            rows.append(bytes(row[x * ncomp + c]
                              for x in range(0, width, scale)
                              for c in range(ncomp)))
        width = len(rows[0]) // ncomp
        height = len(rows)
        raw = b"".join(b"\x00" + r for r in rows)
    else:
        raw = b"".join(b"\x00" + data[y * stride:(y + 1) * stride]
                       for y in range(height))
    ctype = {1: 0, 3: 2}[ncomp]

    def chunk(tag, payload):
        return (struct.pack(">I", len(payload)) + tag + payload +
                struct.pack(">I", zlib.crc32(tag + payload) & 0xFFFFFFFF))

    png = (b"\x89PNG\r\n\x1a\n" +
           chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, ctype, 0, 0, 0)) +
           chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))
    with open(path, "wb") as fh:
        fh.write(png)
    return width, height, len(png)


def render(pdf_path, page_no, scale=2):
    reader = _reader(pdf_path)
    page = reader.pages[page_no - 1]
    found = page_image(page)
    if not found:
        raise ValueError(f"page {page_no} has no image XObject "
                         f"(text layer? use _extract_pdf.py)")
    name, img = found
    filt = img.get("/Filter")
    filt = filt if isinstance(filt, list) else [filt]
    if "/DCTDecode" in filt:
        data = img.get_data()
        ext, ncomp, w, h = "jpg", 0, img["/Width"], img["/Height"]
        slug = os.path.splitext(os.path.basename(pdf_path))[0][:20]
        slug = "".join(ch if ch.isalnum() else "-" for ch in slug).strip("-")
        path = os.path.join(OUT_DIR, f"{slug}-p{page_no}.{ext}")
        os.makedirs(OUT_DIR, exist_ok=True)
        with open(path, "wb") as fh:
            fh.write(data)
        return path, w, h, os.path.getsize(path)
    if set(filt) - {"/FlateDecode"}:
        raise ValueError(f"filters {filt} not supported")
    ncomp = _components(img)
    width, height = int(img["/Width"]), int(img["/Height"])
    data = img.get_data()  # PyPDF2 already applies /FlateDecode
    if len(data) != width * height * ncomp and "/FlateDecode" in filt:
        data = zlib.decompress(data)
    if len(data) != width * height * ncomp:
        raise ValueError(f"unexpected pixel buffer {len(data)} != "
                         f"{width}*{height}*{ncomp}")
    slug = "".join(ch if ch.isalnum() else "-"
                   for ch in os.path.splitext(os.path.basename(pdf_path))[0][:20])
    path = os.path.join(OUT_DIR, f"{slug.strip('-')}-p{page_no}.png")
    os.makedirs(OUT_DIR, exist_ok=True)
    w, h, size = write_png(path, width, height, ncomp, data, scale)
    return path, w, h, size


def main() -> None:
    argv = sys.argv[1:]
    scale, info, rest = 1, False, []
    i = 0
    while i < len(argv):
        if argv[i] == "--scale":
            scale = int(argv[i + 1])
            i += 2
            continue
        if argv[i] == "--info":
            info = True
        else:
            rest.append(argv[i])
        i += 1
    if not rest:
        print(__doc__)
        return
    pdf = os.path.join(C.BASE, rest[0])
    pages = [p for p in rest[1:]]
    if info:
        for n, page in enumerate(_reader(pdf).pages, 1):
            res = page.get("/Resources") or {}
            fonts = res.get("/Font")
            nfont = len(fonts) if fonts else 0
            found = page_image(page)
            if not found:
                print(f"p{n}: {nfont} font(s), no image (text layer present)")
                continue
            _, img = found
            print(f"p{n}: {nfont} font(s), {img.get('/Filter')} "
                  f"{img['/Width']}x{img['/Height']} {img.get('/ColorSpace')}")
        return
    if not pages:
        print(__doc__)
        return
    for p in pages:
        path, w, h, size = render(pdf, int(p), scale)
        print(f"{os.path.relpath(path, C.BASE)}  {w}x{h}  {size // 1024} kB")


if __name__ == "__main__":
    main()
