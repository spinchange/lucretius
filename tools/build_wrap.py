#!/usr/bin/env python3
"""Build the one-piece cover wrap (back, spine, front) for the 7 x 10 in
print edition, as a single vector PDF from tools/print/wrap.typ.

    python tools/build_wrap.py                         # hardcover, spine estimated
    python tools/build_wrap.py --spine 0.875           # Lulu's figure from its template
    python tools/build_wrap.py --kind paperback        # paperback, Lulu's formula

Hardcover (Lulu casewrap): boards 7.125 x 10.25 in (trim plus 0.125 in
overhang), 0.75 in wrap round every edge, hinge about 0.25 in from the
spine. Lulu publishes the casewrap spine width only in the custom template
it makes once the interior is uploaded, so without --spine the hardcover
spine is an ESTIMATE (the paperback formula plus 0.25 in for the board)
and the wrap is marked provisional in its filename. Replace it with the
template's figure before ordering.

Paperback (Lulu): spine = pages / 444 + 0.06 in, 0.125 in bleed.

The page count is read from the built interior
(print-build/de-rerum-natura-7x10-complete.pdf) unless --pages is given.
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "tools" / "print" / "wrap.typ"
INTERIOR = ROOT / "print-build" / "de-rerum-natura-7x10-complete.pdf"
MEDALLION = "illustrations/cover_medallion.jpg"
# Lulu's barcode for the hardcover ISBN 978-0-557-67921-8, downloaded from
# the Lulu wizard. A paperback has its own ISBN and needs its own file.
BARCODE = ROOT / "print-build" / "isbn-barcode.svg"
# Hardcover spine widths Lulu gave (from its print-ready cover), by page count
LULU_SPINE = {266: 0.87}
OUT = ROOT / "print-build"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--kind", choices=("hardcover", "paperback"), default="hardcover")
    ap.add_argument("--pages", type=int)
    ap.add_argument("--spine", type=float, help="spine width in inches (Lulu's template)")
    args = ap.parse_args(argv)

    pages = args.pages
    if pages is None:
        from pypdf import PdfReader
        if not INTERIOR.exists():
            raise SystemExit(f"build the interior first: python tools/build_print.py")
        pages = len(PdfReader(str(INTERIOR)).pages)
    paper = pages / 444 + 0.06
    provisional = False
    if args.spine:
        spine = args.spine
    elif args.kind == "hardcover" and pages in LULU_SPINE:
        spine = LULU_SPINE[pages]
    elif args.kind == "paperback":
        spine = paper
    else:
        spine = paper + 0.25
        provisional = True
    spine = round(spine, 3)

    edge = 0.75 if args.kind == "hardcover" else 0.125
    panel_w, panel_h = (7.125, 10.25) if args.kind == "hardcover" else (7.0, 10.0)
    width = 2 * edge + 2 * panel_w + spine
    height = 2 * edge + panel_h
    name = f"de-rerum-natura-7x10-{args.kind}-wrap" + ("-PROVISIONAL" if provisional else "")
    out = OUT / f"{name}.pdf"
    typst = shutil.which("typst") or "typst"
    cmd = [typst, "compile", "--root", str(ROOT),
           "--input", f"kind={args.kind}", "--input", f"spine={spine}",
           "--input", f"medallion=/{MEDALLION}", str(TEMPLATE), str(out)]
    barcode = args.kind == "hardcover" and BARCODE.exists()
    if barcode:
        cmd[-2:-2] = ["--input", f"barcode=/{BARCODE.relative_to(ROOT).as_posix()}"]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    if res.returncode:
        sys.stderr.write(res.stderr)
        raise SystemExit("typst failed")
    print(f"{out.relative_to(ROOT)}: {width:.3f} x {height:.3f} in; {pages} pages; "
          f"spine {spine:.3f} in; " + ("barcode placed" if barcode else
          "NO BARCODE (save Lulu's SVG as print-build/isbn-barcode.svg)") + (" (ESTIMATE: replace with Lulu's template figure)"
                                      if provisional else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
