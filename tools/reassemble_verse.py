"""Update the verse of a finished book file from its review segments, keeping
the argument, commentary, [n] markers and final notes in place.

assemble.py rebuilds translation/book_NN.txt from scratch and so cannot be
used once a book's notes are final. This tool reads the book file, and for
every numbered verse line replaces the text with the current text of the
segment review file for that key. A marker [n] that sat at the end of the
old line goes to the end of the new line; a marker anchored after a word
inside the line is kept after that word if the word still occurs in the new
line, else moved to the end of the line (and reported). Lines whose text is
unchanged are left alone. Lacuna lines are not touched.

Usage: python tools/reassemble_verse.py 2 [--dry-run]
Afterwards: python tools/check_narration.py 2 (expect a mismatch until the
narration source is regenerated with make_narration.py), then
python tools/make_narration.py 2.
"""
import re, sys
from common import ROOT, load_manifest, parse_lines, seg_path

RULE = "-" * 60
LINE = re.compile(r"^(\s*)(\d+[a-z]?)(\s\s)(.*)$")
MARK = re.compile(r"\[(\d+)\]")


def main():
    n = int(sys.argv[1]); dry = "--dry-run" in sys.argv
    m = load_manifest()
    new = {}
    for e in m["segments"]:
        if e["book"] != n: continue
        p = seg_path(e, "review")
        for k, t in parse_lines(p.read_text(encoding="utf-8")):
            if k: new[k] = re.sub(r"\s*\{\{NOTE:.*?\}\}", "", t).strip()
    dest = ROOT / "translation" / f"book_{n:02d}.txt"
    text = dest.read_text(encoding="utf-8").replace("\r\n", "\n")
    parts = text.split(RULE)
    assert len(parts) >= 3, "expected two rule lines around the verse"
    out, changed, moved = [], 0, []
    for raw in parts[1].split("\n"):
        mm = LINE.match(raw)
        if not mm:
            out.append(raw); continue
        ind, key, sep, body = mm.groups()
        marks = [(x.group(1), x.start()) for x in MARK.finditer(body)]
        old = MARK.sub("", body).strip()
        if key not in new or new[key] == old:
            out.append(raw); continue
        line = new[key]
        for num, pos in marks:
            tag = f"[{num}]"
            if pos >= len(MARK.sub("", body).rstrip()) :  # was at the end
                line = line.rstrip() + tag if not line.rstrip()[-1] in ".,;:?!" else line.rstrip() + tag
                continue
            # anchored after a word inside the line
            before = MARK.sub("", body[:pos])
            word = re.findall(r"[\w'’-]+[.,;:?!]*$", before)
            word = word[0] if word else ""
            if word and word in line:
                i = line.index(word) + len(word)
                line = line[:i] + tag + line[i:]
            else:
                line = line.rstrip() + tag
                moved.append((key, tag))
        out.append(f"{ind}{key}{sep}{line}")
        changed += 1
        print(f"{key}: {old}\n{' ' * (len(key) + 2)}-> {line}")
    parts[1] = "\n".join(out)
    if not dry:
        dest.write_text(RULE.join(parts), encoding="utf-8")
    print(f"{'would change' if dry else 'changed'} {changed} lines in {dest.name}")
    for key, tag in moved:
        print(f"  marker {tag} on line {key} moved to the end of the line; check the anchor")


if __name__ == "__main__":
    main()
