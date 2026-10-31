"""Build a segment's accepted text (sKK.review.txt) from the translate draft
plus the translator's line patches, and record the review stage.

Usage: python tools/review.py b01s02 segments/b01/s02.patch.tsv
       python tools/review.py b01s02 segments/b01/s02.patch2.tsv --round 2
With --round 2 the base text is the existing review file (not the Opus
draft), the result overwrites the review file, and the stage recorded is
"review2" (the full second read); the first review record is kept.
Patch file: one line per change, key<TAB>new text (tab-separated; a key may
appear once). Keys must exist in the segment. A patch line whose text is
empty is rejected.
"""
import sys
from datetime import datetime, timezone
from common import load_manifest, update_stage, parse_lines, seg_path, fmt_line

def main():
    seg_id, patch = sys.argv[1], sys.argv[2]
    rnd = int(sys.argv[sys.argv.index("--round") + 1]) if "--round" in sys.argv else 1
    m = load_manifest(); e = [x for x in m["segments"] if x["id"] == seg_id][0]
    base = "translate" if rnd == 1 else "review"
    rows = parse_lines(seg_path(e, base).read_text(encoding="utf-8"))
    keys = [k for k, _ in rows]
    patches = {}
    for ln in open(patch, encoding="utf-8").read().replace("\r\n", "\n").split("\n"):
        if not ln.strip() or ln.startswith("#"): continue
        k, t = ln.split("\t", 1)
        assert k in keys, f"unknown key {k}"
        assert k not in patches, f"duplicate key {k}"
        assert t.strip(), f"empty text for {k}"
        patches[k] = t.strip()
    out = [fmt_line(k, patches.get(k, t)) if t != "[lacuna]" else "       [lacuna]" for k, t in rows]
    seg_path(e, "review").write_text("\n".join(out) + "\n", encoding="utf-8")
    update_stage(seg_id, "review" if rnd == 1 else f"review{rnd}", {"status": "done", "model": "fable (translator)",
        "finished": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "patched": sorted(patches, key=keys.index), "n_patched": len(patches)})
    print(f"{seg_id}: review written (round {rnd}), {len(patches)} lines patched")

if __name__ == "__main__":
    main()
