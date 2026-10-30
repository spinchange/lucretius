"""Turn a book's draft notes into the final numbered notes (one-shot).

Reads translation/book_NN.txt as assemble.py wrote it (placeholders in the
verse, a "Notes (DRAFT)" section) and a notes spec, and writes the book
file in the Iliad format: argument line, translator's commentary, [n]
markers in the verse, a "Notes" section with the numbered notes, each
opening with its (book.line). Every {{NOTE: ...}} placeholder is removed
from the verse; the verse wording itself is never touched (check with
tools/check_narration.py afterwards).

Spec format (plain text):

    ARGUMENT
    one or two sentences

    COMMENTARY
    paragraphs separated by blank lines

    NOTES
    @22 | shores of light
    (1.22) The note text, any number of lines, joined into one paragraph.

    @156
    (1.155-158) A note whose marker goes at the end of line 156.

"@KEY" names the verse line (key as printed, e.g. 860a) that carries the
marker; "| anchor" puts the marker right after that text in the line,
otherwise it goes at the end of the line. Notes are numbered in verse order.

Usage: python tools/apply_notes.py 1 path/to/book_01.notes.txt
"""
import re, sys, textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RULE = "-" * 60
NOTE = re.compile(r"\s*\{\{NOTE:.*?\}\}")
LINE = re.compile(r"^(\s*)(\d+[a-z]?)(\s\s)(.*)$")
WIDTH = 76


def parse_spec(text):
    text = text.replace("\r\n", "\n")
    m = re.match(r"\s*ARGUMENT\n(.*?)\n\s*COMMENTARY\n(.*?)\n\s*NOTES\n(.*)", text, re.S)
    if not m:
        sys.exit("spec needs ARGUMENT, COMMENTARY and NOTES sections")
    argument = " ".join(m.group(1).split())
    commentary = [" ".join(p.split()) for p in re.split(r"\n\s*\n", m.group(2).strip()) if p.strip()]
    notes = []
    for block in re.split(r"\n(?=@)", "\n" + m.group(3).strip()):
        block = block.strip()
        if not block:
            continue
        head, _, body = block.partition("\n")
        key, _, anchor = head[1:].partition("|")
        body = " ".join(body.split())
        if not body.startswith("("):
            sys.exit(f"note at @{key.strip()} must open with its (book.line): {body[:40]}")
        notes.append((key.strip(), anchor.strip(), body))
    return argument, commentary, notes


def main():
    n = int(sys.argv[1]); spec = Path(sys.argv[2])
    book = ROOT / "translation" / f"book_{n:02d}.txt"
    text = book.read_text(encoding="utf-8").replace("\r\n", "\n")
    parts = text.split(RULE)
    if len(parts) != 3:
        sys.exit("expected exactly two rule lines in the book file")
    if "Notes (DRAFT)" not in parts[2]:
        sys.exit("no 'Notes (DRAFT)' section: the notes look final already; edit the book file directly")
    argument, commentary, notes = parse_spec(spec.read_text(encoding="utf-8"))

    verse = parts[1].strip("\n").split("\n")
    pos = {}
    for i, raw in enumerate(verse):
        m = LINE.match(raw)
        if m:
            if m.group(2) in pos:
                sys.exit(f"duplicate key {m.group(2)} in verse")
            pos[m.group(2)] = i
    for key, _, _ in notes:
        if key not in pos:
            sys.exit(f"no verse line with key {key}")
    order = sorted(range(len(notes)), key=lambda i: pos[notes[i][0]])
    if order != list(range(len(notes))):
        sys.exit("notes are not in verse order: " + ", ".join(notes[i][0] for i in order))

    placeholders = {m.group(2) for raw in verse if (m := LINE.match(raw)) and "{{NOTE" in raw}
    marked = set()
    for num, (key, anchor, _) in enumerate(notes, 1):
        i = pos[key]; m = LINE.match(verse[i])
        body = NOTE.sub("", m.group(4)).rstrip()
        tag = f"[{num}]"
        if anchor:
            j = body.find(anchor)
            if j < 0:
                sys.exit(f"anchor {anchor!r} not found in line {key}: {body}")
            body = body[: j + len(anchor)] + tag + body[j + len(anchor):]
        else:
            body = body + tag
        verse[i] = m.group(1) + m.group(2) + m.group(3) + body
        marked.add(key)
    for i, raw in enumerate(verse):
        m = LINE.match(raw)
        if m and "{{NOTE" in raw:
            verse[i] = m.group(1) + m.group(2) + m.group(3) + NOTE.sub("", m.group(4)).rstrip()
    dropped = sorted(placeholders - marked, key=lambda k: pos[k])
    if dropped:
        print("placeholders resolved without a marker (merged or dropped):", ", ".join(dropped))

    head = [f"BOOK {n}", ""]
    head += textwrap.wrap(argument, WIDTH) + ["", "TRANSLATOR'S COMMENTARY", ""]
    for p in commentary:
        head += textwrap.wrap(p, WIDTH) + [""]
    out = head + [RULE, ""] + verse + ["", RULE, "", "Notes", ""]
    for num, (_, _, body) in enumerate(notes, 1):
        tag = f"[{num}] "
        out += textwrap.wrap(tag + body, WIDTH, subsequent_indent=" " * len(tag)) + [""]
    book.write_text("\n".join(out).rstrip("\n") + "\n", encoding="utf-8", newline="\n")
    print(f"wrote {book}: {len(notes)} notes, {len(commentary)} commentary paragraphs")


if __name__ == "__main__":
    main()
