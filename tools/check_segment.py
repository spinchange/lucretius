"""Mechanical hygiene check of a segment's translation against its Latin.

Checks: every Latin line key appears once, in order, with nothing extra;
lacuna lines preserved; no Latin left in the English; syllable band (9-16)
reported with outliers; note placeholders counted. Exit 0 if clean, 1
otherwise.

Usage:  python tools/check_segment.py b01s03 [b01s04 ...] | --all
"""
import re, sys
from common import load_manifest, parse_lines, seg_path
from beatcheck import line_syllables

LATIN_HINT = re.compile(r"\b(atque|quoniam|enim|igitur|rerum|naturam?|primordia|corpora|quae|sunt)\b")


def check(entry, quiet=False):
    probs = []
    lat = parse_lines(seg_path(entry, "latin").read_text(encoding="utf-8"))
    p = seg_path(entry, "review") if seg_path(entry, "review").exists() else seg_path(entry, "translate")
    if not p.exists():
        return [f"{entry['id']}: no translation file"]
    eng = parse_lines(p.read_text(encoding="utf-8"))
    lk = [k for k, _ in lat]; ek = [k for k, _ in eng]
    if lk != ek:
        probs.append(f"key sequence differs: latin {len(lk)} lines, english {len(ek)} lines")
        missing = [k for k in lk if k not in ek]; extra = [k for k in ek if k not in lk]
        if missing: probs.append(f"  missing keys: {missing[:15]}")
        if extra: probs.append(f"  extra keys: {extra[:15]}")
        if not missing and not extra: probs.append("  same keys, different order")
    sylls = []
    for (lkey, ltxt), (ekey, etxt) in zip(lat, eng):
        if ltxt == "[lacuna]":
            if etxt.strip() != "[lacuna]": probs.append(f"  lacuna line after {lkey!r} not preserved as [lacuna]")
            continue
        body = re.sub(r"\{\{NOTE:.*?\}\}", "", etxt).strip()
        if not body: probs.append(f"  {ekey}: empty line")
        if len(LATIN_HINT.findall(body)) >= 2:
            probs.append(f"  {ekey}: looks like untranslated Latin: {body[:50]}")
        sylls.append((ekey, line_syllables(body)))
    if sylls:
        n = len(sylls); inband = sum(1 for _, s in sylls if 9 <= s <= 16)
        srt = sorted(s for _, s in sylls); med = srt[n // 2]
        outl = [(k, s) for k, s in sylls if s < 7 or s > 19]
        notes = sum(1 for _, t in eng if "{{NOTE" in t)
        info = f"{entry['id']}: {n} lines, median {med} syll, {100*inband/n:.0f}% in 9-16 band, {notes} note placeholders"
        if outl: info += f", outliers {outl[:8]}"
        if not quiet: print(info)
        if 100 * inband / n < 80: probs.append(f"  only {100*inband/n:.0f}% of lines in the 9-16 syllable band")
    return [p if p.startswith("  ") else f"{entry['id']}: {p}" for p in probs]


def main():
    m = load_manifest(); ids = sys.argv[1:]
    todo = [e for e in m["segments"] if "--all" in ids or e["id"] in ids]
    bad = 0
    for e in todo:
        probs = check(e)
        for p in probs: print(p)
        bad += bool(probs)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
