"""Check that a book's verse still matches its pinned narration source.

Strips the [n] markers and {{NOTE}} placeholders from the numbered lines of
translation/book_NN.txt exactly as make_narration.py does, without writing
anything, and diffs the result against audiobook-source/book_NN.txt. Exit 0
when they are identical. Use this during the notes stage, while the audio is
rendering from the pinned sources.

Usage: python tools/check_narration.py 1 [2 ...] | --all
"""
import difflib, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NOTE = re.compile(r"\s*\{\{NOTE:.*?\}\}")
MARK = re.compile(r"\s*\[\d+\]")
LINE = re.compile(r"^\s*(\d+)([a-z]?)\s\s(.*)$")


def narration(n):
    text = (ROOT / "translation" / f"book_{n:02d}.txt").read_text(encoding="utf-8").replace("\r\n", "\n")
    parts = text.split("-" * 60)
    assert len(parts) >= 3, "expected two rule lines around the verse"
    lines = []
    for raw in parts[1].split("\n"):
        if raw.strip() == "[lacuna]":
            if lines and lines[-1] != "": lines.append("")
            continue
        m = LINE.match(raw)
        if not m:
            if raw.strip() == "" and lines and lines[-1] != "": lines.append("")
            continue
        key, letter, body = m.groups()
        body = re.sub(r"\s+", " ", MARK.sub("", NOTE.sub("", body)).strip())
        if letter or body in ("* * *", ""):
            continue
        lines.append(f"{key:>5}  {body}")
    return "\n".join(lines).strip("\n") + "\n"


def main():
    books = range(1, 7) if "--all" in sys.argv[1:] else [int(a) for a in sys.argv[1:]]
    bad = 0
    for n in books:
        src = (ROOT / "audiobook-source" / f"book_{n:02d}.txt").read_text(encoding="utf-8").replace("\r\n", "\n")
        now = narration(n)
        if now == src:
            print(f"book {n}: verse matches audiobook-source ({len(now.splitlines())} lines)")
        else:
            bad += 1
            print(f"book {n}: DIFFERS from audiobook-source")
            for d in difflib.unified_diff(src.splitlines(), now.splitlines(), "audiobook-source", "translation", lineterm="", n=0):
                print("  " + d)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
