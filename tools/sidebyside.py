"""Print a segment's Latin and English interleaved, for the translator's review.
Usage: python tools/sidebyside.py b01s02 [first last]"""
import sys
from common import load_manifest, parse_lines, seg_path
m = load_manifest(); e = [x for x in m["segments"] if x["id"] == sys.argv[1]][0]
lat = parse_lines(seg_path(e, "latin").read_text(encoding="utf-8"))
p = seg_path(e, "review") if seg_path(e, "review").exists() else seg_path(e, "translate")
eng = dict(parse_lines(p.read_text(encoding="utf-8")))
lo, hi = (sys.argv[2], sys.argv[3]) if len(sys.argv) > 3 else (None, None)
on = lo is None
for k, t in lat:
    if lo and k == lo: on = True
    if on:
        print(f"{k:>5}  {t}")
        print(f"       > {eng.get(k, '???')}")
    if hi and k == hi: break
