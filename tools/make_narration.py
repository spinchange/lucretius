"""Write the narration source for a book's audiobook: the verse only.

Reads translation/book_NN.txt, keeps the numbered lines between the two
rule lines (no header, commentary or notes), strips {{NOTE: ...}}
placeholders and [n] note markers, drops lettered lines that carry no text
(860a "* * *"), and turns [lacuna] lines into blank lines so the narration
pauses there. Source order is kept, including transposed lines.

Usage: python tools/make_narration.py 1   -> audiobook-source/book_01.txt
"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NOTE = re.compile(r"\s*\{\{NOTE:.*?\}\}")
MARK = re.compile(r"\s*\[\d+\]")
LINE = re.compile(r"^\s*(\d+)([a-z]?)\s\s(.*)$")


def main():
    n = int(sys.argv[1])
    src = ROOT / "translation" / f"book_{n:02d}.txt"
    out_dir = ROOT / "audiobook-source"; out_dir.mkdir(exist_ok=True)
    out = out_dir / f"book_{n:02d}.txt"
    text = src.read_text(encoding="utf-8").replace("\r\n", "\n")
    parts = text.split("-" * 60)
    assert len(parts) >= 3, "expected two rule lines around the verse"
    verse = parts[1]
    lines, kept, dropped = [], 0, []
    for raw in verse.split("\n"):
        if raw.strip() == "[lacuna]":
            if lines and lines[-1] != "": lines.append("")
            continue
        m = LINE.match(raw)
        if not m:
            if raw.strip() == "" and lines and lines[-1] != "": lines.append("")
            continue
        key, letter, body = m.groups()
        body = MARK.sub("", NOTE.sub("", body)).strip()
        body = re.sub(r"\s+", " ", body)
        if letter or body in ("* * *", ""):
            dropped.append(key + letter); continue
        lines.append(f"{key:>5}  {body}")
        kept += 1
    out.write_text("\n".join(lines).strip("\n") + "\n", encoding="utf-8", newline="\n")
    print(f"wrote {out}: {kept} lines; dropped {dropped}")


if __name__ == "__main__":
    main()
