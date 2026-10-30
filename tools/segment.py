"""Cut each book into translation segments at paragraph boundaries and build
segments/manifest.json plus one Latin file per segment.

Paragraph boundaries come from the Perseus XML's <milestone unit="card">
markers, so segments start at sense units rather than arbitrary line counts.
A segment closes at the first paragraph start after it reaches --target
lines, or by force once it reaches 1.6x --target. The translator's own
sample (translation/proem_sample.txt) is installed as Book 1 segment 00.

Re-running is safe: existing stage outputs in segments/ are kept and the
manifest's stage records are preserved for segments whose line range is
unchanged. Usage:  python tools/segment.py [--target 110]
"""
import argparse, json, shutil
from datetime import datetime, timezone
from xml.etree import ElementTree as ET
from common import ROOT, LATIN, MANIFEST, read_book, fmt_line, seg_path

NS = {"t": "http://www.tei-c.org/ns/1.0"}
XML = LATIN / "source" / "drn_perseus_lat1.xml"
FIRST_CUT = {1: "146"}  # book 1: the proem (1-145) is the translator's sample


def para_starts():
    root = ET.parse(XML).getroot()
    out = {}
    for book in root.findall('.//t:div[@subtype="book"]', NS):
        n = int(book.get("n")); keys = set(); pending = False
        for el in book:
            tag = el.tag.split("}")[-1]
            if tag == "milestone" and el.get("unit") == "card":
                pending = True
            elif tag == "l" and pending and el.get("n"):
                keys.add(el.get("n")); pending = False
        out[n] = keys
    return out


def cut(rows, starts, target, first_cut=None):
    segs, cur = [], []
    for i, (key, _) in enumerate(rows):
        if first_cut:
            do_cut = key == first_cut
        else:
            do_cut = bool(cur) and ((len(cur) >= target and key in starts) or len(cur) >= int(target * 1.6))
        if do_cut and cur:
            segs.append(cur); cur = []
            if first_cut and key == first_cut:
                first_cut = None
        cur.append(i)
    if cur:
        if segs and len(cur) < 40:
            segs[-1].extend(cur)  # fold a short tail into the previous segment
        else:
            segs.append(cur)
    return segs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", type=int, default=110)
    a = ap.parse_args()
    old = {}
    if MANIFEST.exists():
        old = {e["id"]: e for e in json.loads(MANIFEST.read_text(encoding="utf-8"))["segments"]}
    starts = para_starts()
    entries = []
    for n in range(1, 7):
        rows = read_book(n)
        for s, idxs in enumerate(cut(rows, starts[n], a.target, FIRST_CUT.get(n))):
            keys = [rows[i][0] for i in idxs]
            e = {"id": f"b{n:02d}s{s:02d}", "book": n, "seg": s,
                 "start_idx": idxs[0], "end_idx": idxs[-1],
                 "first": next(k for k in keys if k), "last": next(k for k in reversed(keys) if k),
                 "n": len(idxs), "stages": {}}
            o = old.get(e["id"])
            if o and (o["start_idx"], o["end_idx"]) == (e["start_idx"], e["end_idx"]):
                e["stages"] = o["stages"]
            entries.append(e)
            p = seg_path(e, "latin")
            p.write_text("\n".join(fmt_line(rows[i][0], rows[i][1]) for i in idxs) + "\n", encoding="utf-8")
    # install the translator's sample as b01s00
    sample = ROOT / "translation" / "proem_sample.txt"
    e0 = entries[0]
    if sample.exists() and e0["id"] == "b01s00":
        shutil.copy(sample, seg_path(e0, "translate"))
        e0["stages"]["translate"] = {"status": "done", "model": "fable (translator)",
                                     "finished": datetime.now(timezone.utc).isoformat(timespec="seconds")}
        e0["stages"]["review"] = {"status": "done", "note": "translator's own sample; the register was set from it"}
    m = {"created": datetime.now(timezone.utc).isoformat(timespec="seconds"), "target": a.target,
         "segments": entries}
    MANIFEST.write_text(json.dumps(m, indent=1, ensure_ascii=False), encoding="utf-8")
    by_book = {}
    for e in entries:
        by_book.setdefault(e["book"], []).append(e["n"])
    for n, sizes in by_book.items():
        print(f"book {n}: {len(sizes)} segments, lines/segment min {min(sizes)} max {max(sizes)} mean {sum(sizes)/len(sizes):.0f}")
    print(f"total segments {len(entries)}")


if __name__ == "__main__":
    main()
