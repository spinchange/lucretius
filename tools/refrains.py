"""List the Latin lines of one book that recur verbatim elsewhere in the poem,
with the current English of every occurrence (review text where it exists,
else the Opus draft). The translator uses it before a book's review to make
the English repeat its own earlier lines where the Latin repeats.

Usage: python tools/refrains.py 3          (all repeated lines of Book 3)
       python tools/refrains.py 3 --earlier (only those shared with Books 1-2)
Lacuna markers and orthographic variants (nilum/nihilum) are not matched;
grep for those by hand."""
import re, sys
from pathlib import Path
from common import load_manifest, parse_lines, read_book, seg_path

book = int(sys.argv[1]); earlier = "--earlier" in sys.argv
lat = {}
for b in range(1, 7):
    for k, t in read_book(b):
        if t != "[lacuna]" and not t.startswith("*"):
            lat[(b, k)] = t
norm = lambda s: re.sub(r"[^a-z]", "", s.lower().replace("nihil", "nil"))
by = {}
for (b, k), t in lat.items():
    by.setdefault(norm(t), []).append((b, k))
eng = {}
for e in load_manifest()["segments"]:
    p = seg_path(e, "review") if seg_path(e, "review").exists() else seg_path(e, "translate")
    if p.exists():
        for k, t in parse_lines(p.read_text(encoding="utf-8")):
            eng[(e["book"], k)] = t
order = lambda k: float(re.sub(r"[a-z]", ".5", k) or 0)
for (b, k), t in sorted(lat.items(), key=lambda x: (x[0][0], order(x[0][1]))):
    if b != book: continue
    occ = by[norm(t)]
    if len(occ) < 2: continue
    if earlier and not any(ob < book for ob, _ in occ): continue
    print(f"{b}.{k}  {t}")
    for ob, ok in occ:
        print(f"    {ob}.{ok}: {eng.get((ob, ok), '???')}")
