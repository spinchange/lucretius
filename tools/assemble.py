"""Assemble a book from its segments into translation/book_NN.txt.

Uses sKK.review.txt where it exists (the translator's accepted text), else
sKK.translate.txt. Draft notes from sKK.annotate.txt are appended in a
"Notes (DRAFT)" section; the translator numbers and finalizes them in Pass 2.
Usage:  python tools/assemble.py 1
"""
import sys
from common import ROOT, load_manifest, seg_path


def main():
    n = int(sys.argv[1]); m = load_manifest()
    segs = [e for e in m["segments"] if e["book"] == n]
    verse, notes, missing = [], [], []
    for e in segs:
        p = seg_path(e, "review") if seg_path(e, "review").exists() else seg_path(e, "translate")
        if not p.exists():
            missing.append(e["id"]); continue
        verse.append(p.read_text(encoding="utf-8").rstrip("\n"))
        a = seg_path(e, "annotate")
        if a.exists(): notes.append(a.read_text(encoding="utf-8").rstrip("\n"))
    if missing:
        print("not assembled; segments without translation:", ", ".join(missing)); sys.exit(1)
    out = [f"BOOK {n}", "", "[argument: one sentence, to be written]", "", "TRANSLATOR'S COMMENTARY", "",
           "[to be written]", "", "-" * 60, "", "\n\n".join(verse), "", "-" * 60, "", "Notes (DRAFT)", ""]
    out.append("\n\n".join(notes) if notes else "[no draft notes yet]")
    dest = ROOT / "translation" / f"book_{n:02d}.txt"
    dest.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"wrote {dest} from {len(segs)} segments")


if __name__ == "__main__":
    main()
