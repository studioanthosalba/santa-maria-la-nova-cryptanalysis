# -*- coding: utf-8 -*-
"""_fetch_external.py -- download the plain-text corpora used as language models.

Everything lands in ``sources/external`` (UTF-8) so the pipeline never needs
the network again.  Failures are reported, not fatal: the analysis falls back to
whatever corpora are available.
"""
import json
import os
import sys

import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C

OUT = os.path.join(C.SOURCES, "external")
os.makedirs(OUT, exist_ok=True)

BIBLE = {
    "czech_kralicka_1613": "cs_bkr",
    "latin_vulgate": "la_vulg",
    "italian_riveduta": "it_irb20",
    "hungarian_karoli": "hu_hunk",
    "romanian": "ro_vdc",
    "albanian": "sq_albb",
    "croatian": "hr_okok",
    "slovak": "sk_onpk",
    "greek_brenton": "grc_grcbrent",
    "german_schlachter": "de_sch1951",
    "polish": "pl_ubg",
    "english_kjv": "en_kjv",
}
BIBLE_URL = "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/{}.json"

TEXTS = {
    "italian_dante.txt": "https://www.gutenberg.org/cache/epub/1012/pg1012.txt",
    "czech_dostoevsky.txt": "https://www.gutenberg.org/cache/epub/34225/pg34225.txt",
    "czech_catechism.txt": "https://www.gutenberg.org/cache/epub/16843/pg16843.txt",
}

HEADERS = {"User-Agent": "Mozilla/5.0 (research; epigraph cryptanalysis)"}


def get(url, timeout=60):
    r = requests.get(url, timeout=timeout, headers=HEADERS)
    r.raise_for_status()
    return r


def fetch_bibles():
    for name, code in BIBLE.items():
        dest = os.path.join(OUT, f"bible_{name}.txt")
        if os.path.exists(dest) and os.path.getsize(dest) > 100000:
            print(f"skip (cached) {name}")
            continue
        try:
            r = get(BIBLE_URL.format(code))
            data = json.loads(r.content.decode("utf-8"))
            chunks = []
            for book in data:
                chunks.append(book.get("name", ""))
                for ch in book.get("chapters", []):
                    chunks.extend(ch)
            txt = "\n".join(chunks)
            C.write_text(dest, txt)
            print(f"ok {name}: {len(txt)} chars -> {dest}")
        except Exception as exc:  # pragma: no cover - network dependent
            print(f"FAIL {name}: {exc}")


def fetch_texts():
    for name, url in TEXTS.items():
        dest = os.path.join(OUT, name)
        if os.path.exists(dest) and os.path.getsize(dest) > 100000:
            print(f"skip (cached) {name}")
            continue
        try:
            r = get(url)
            txt = r.content.decode("utf-8", errors="replace")
            C.write_text(dest, txt)
            print(f"ok {name}: {len(txt)} chars -> {dest}")
        except Exception as exc:  # pragma: no cover - network dependent
            print(f"FAIL {name}: {exc}")


if __name__ == "__main__":
    C.utf8_stdout()
    fetch_bibles()
    fetch_texts()
    print("\nnow in sources/external:")
    for f in sorted(os.listdir(OUT)):
        print(f"  {os.path.getsize(os.path.join(OUT, f)):>10} {f}")
