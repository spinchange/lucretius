#!/usr/bin/env python3
"""Build the print interior of De Rerum Natura as a press-ready PDF.

A print edition, not the web pages paginated. Trim 7 x 10 in (Lulu's
"Executive", hardcover casewrap or paperback), chosen so that the English
verse has a measure of about 65 characters beside a 1.4 in outer column:

  - Machiavelli's reading marks from Vatican MS Ross. 884 stand in the
    OUTER margin, level with the line they stand against, as they stand
    in his copy: his Latin (or Greek) in a red-brown like iron-gall ink,
    the English beneath it, the folio after. The pointing hand at 2.82 and
    his dashes and crosses are set as glyphs, not described. On a verso
    the column is on the left and the notes range right, toward the text.
  - Line numbers every fifth line in the INNER margin, so the outer one
    belongs to him.
  - Each book opens on a recto with its argument; the translator's notes
    follow the book; the translator's commentary on the books and the
    state of the copy (corrections, variants, omissions, catchwords: the
    entries that record the copy rather than a reading) are back matter,
    on a wider measure.
  - --mono prints his marks in a dark grey instead of colour, for a
    black-and-white interior, which costs much less per copy.

Pipeline: translation/, latin/ is not needed; margin/marginalia.tsv ->
print-build/work/data-<tag>.json -> tools/print/interior.typ (Typst) ->
print-build/<name>.pdf. The parsers are shared with tools/build_web.py.
translation/ and margin/ are never modified.

Usage:
    python tools/build_print.py                 # all six books, colour
    python tools/build_print.py --books 2       # Book II only (sample)
    python tools/build_print.py --mono          # black-and-white interior
"""
from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_web import (GLYPH, MARGIN_INTRO, REF_RE, ROMAN, TOTAL_LINES,  # noqa: E402
                       brown_label, entry_order, parse_book, parse_margin)

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "translation"
TEMPLATE = ROOT / "tools" / "print" / "interior.typ"
BUILD = ROOT / "print-build"
WORK = BUILD / "work"
GREEK = re.compile(r"[Ͱ-Ͽἀ-῿]")


def parts(text: str, alias: dict[int, int]) -> list[list]:
    """A verse line as runs of text and note numbers: [["t", s], ["n", 3]]."""
    out: list[list] = []
    pos = 0
    for m in REF_RE.finditer(text):
        if m.start() > pos:
            out.append(["t", text[pos:m.start()]])
        n = int(m.group(1))
        out.append(["n", alias.get(n, n)])
        pos = m.end()
    if pos < len(text):
        out.append(["t", text[pos:]])
    return out


def mark(r: dict) -> dict:
    exp = r["expanded"]
    if r["kind"] in ("mark", "manicule"):
        return {"glyph": GLYPH.get(exp, exp), "fol": r["folio"]}
    return {"lat": exp, "greek": bool(GREEK.search(exp)),
            "en": r["english"], "fol": r["folio"]}


def copy_row(r: dict) -> dict:
    note = r["english"]
    if r["remarks"]:
        note += f" {r['remarks']}"
    label = html.unescape(brown_label(r))
    if label:
        note += f" ({label})"
    return {"line": r["book.line"], "fol": r["folio"], "kind": r["kind"],
            "dipl": r["diplomatic"], "exp": r["expanded"],
            "greek": bool(GREEK.search(r["expanded"])), "note": note}


def book_data(n: int, margin: list[dict]) -> dict:
    bk = parse_book(SRC / f"book_{n:02d}.txt")
    beside: dict[str, list[dict]] = {}
    for r in margin:
        if r["reading"]:
            for b, key in r["anchors"]:
                if b == n:
                    beside.setdefault(key, []).append(r)
    stanzas = []
    used = set()
    for st in bk["stanzas"]:
        lines = []
        for it in st:
            if it[0] == "lacuna":
                lines.append({"lacuna": True})
                continue
            _, key, text = it
            m = re.match(r"(\d+)([a-z]?)$", key)
            shown = (int(m.group(1)) % 5 == 0 and not m.group(2)) or key == "1"
            mg = [mark(r) for r in beside.get(key, [])]
            if mg:
                used.add(key)
            lines.append({"k": key, "show": shown,
                          "p": parts(text, bk["alias"]), "mg": mg})
        stanzas.append(lines)
    missing = set(beside) - used
    if missing:
        raise SystemExit(f"book {n}: marks keyed to lines not in the verse: {sorted(missing)}")
    notes = []
    for nt in bk["notes"]:
        where = ""
        if nt["line"] is not None:
            where = f'{n}.{nt["line"]}{nt["span"].replace("-", "–")}'
        notes.append({"num": nt["num"], "where": where, "body": nt["body"]})
    copy = sorted((r for r in margin if not r["reading"] and r["book"] == n),
                  key=entry_order)
    return {"n": n, "roman": ROMAN[n - 1], "argument": bk["argument"],
            "commentary": bk["commentary"], "stanzas": stanzas,
            "notes": notes, "copy": [copy_row(r) for r in copy],
            "marks": sum(len(x["mg"]) for s in stanzas for x in s if "mg" in x)}


# The note on the margin, for print: the web page's introduction
# (build_web.MARGIN_INTRO), with what it says about links and the right
# margin said for paper instead.
PRINT_INTRO = [
    MARGIN_INTRO[0],
    "This edition prints everything written in the margins and between the "
    "lines of the 133 folios of the poem, in two places. The reading marks "
    "stand in the outer margin of each page, level with the English of the "
    "line they stand against: the verbal notes, nearly all of them beside "
    "Book II on the motion of the first-beginnings, the swerve, the free "
    "mind that follows from it, and the gods’ indifference; the Greek "
    "glosses; the single words in a lighter ink that gloss a hard Latin "
    "word; the pointing hand at 2.82; and the dashes, crosses and other "
    "marks that show where the reader stopped. Everything else, the "
    "copyist’s own corrections, the variants written in the margin, the "
    "lines he dropped and the lines he supplied, the order marks, "
    "catchwords and colophons, is the state of the copy rather than a "
    "record of reading, and is tabulated at the back of the book.",
    "The images of the manuscript belong to the Vatican Library and are not "
    "reproduced. Each entry gives its folio, and the whole manuscript can be "
    "seen on DigiVatLib, the Library’s digital collection, at "
    "digi.vatlib.it/view/MSS_Ross.884 (a recto NNr is image NN+11 there, a "
    "verso NNv is image NN+12). The transcription keeps the diplomatic form "
    "of each note, expands its abbreviations, and keys it to the line of the "
    "poem by the words it stands against rather than by counting. The copy "
    "was written at twenty-eight lines a page.",
]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--books", nargs="*", type=int)
    ap.add_argument("--mono", action="store_true",
                    help="Machiavelli's marks in grey, for a black-and-white interior")
    args = ap.parse_args(argv)
    books = args.books or list(range(1, 7))
    typst = shutil.which("typst")
    if not typst:
        raise SystemExit("typst is required (winget install Typst.Typst)")

    margin = parse_margin()
    data = {
        "colour": not args.mono,
        "sample": books != list(range(1, 7)),
        "total_lines": f"{TOTAL_LINES:,}",
        "intro": PRINT_INTRO,
        "books": [book_data(n, margin) for n in books],
    }
    tag = ("book" + "-".join(f"{n:02d}" for n in books)
           if data["sample"] else "complete") + ("-mono" if args.mono else "")
    WORK.mkdir(parents=True, exist_ok=True)
    data_path = WORK / f"data-{tag}.json"
    data_path.write_text(json.dumps(data, ensure_ascii=False, indent=1),
                         encoding="utf-8")
    out = BUILD / f"de-rerum-natura-7x10-{tag}.pdf"
    # typst resolves the template's paths against --root
    rel = data_path.relative_to(ROOT).as_posix()
    cmd = [typst, "compile", "--root", str(ROOT), "--input", f"data=/{rel}",
           str(TEMPLATE), str(out)]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    if res.returncode:
        sys.stderr.write(res.stderr)
        raise SystemExit("typst failed")
    if res.stderr.strip():
        print(res.stderr.strip())
    pages = 0
    try:
        from pypdf import PdfReader
        pages = len(PdfReader(str(out)).pages)
    except ImportError:
        pass
    marks = sum(b["marks"] for b in data["books"])
    print(f"{out.relative_to(ROOT)}: {pages} pages; books "
          f"{', '.join(ROMAN[n - 1] for n in books)}; {marks} marks in the margin")
    return 0


if __name__ == "__main__":
    sys.exit(main())
