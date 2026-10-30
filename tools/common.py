"""Shared helpers: paths, line parsing, manifest IO."""
import json, re, threading
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LATIN = ROOT / "latin"
SEG = ROOT / "segments"
MANIFEST = SEG / "manifest.json"
PROMPTS = ROOT / "prompts"
_lock = threading.Lock()

# A text line is: key right-aligned in width 5, two spaces, text.
# Lacuna lines have an empty key and the text "[lacuna]".
LINE = re.compile(r"^\s*(\S*)\s\s(.*)$")


def parse_lines(text):
    """Return [(key, text)] for every non-blank line in numbered-line format."""
    rows = []
    for raw in text.splitlines():
        if not raw.strip():
            continue
        m = LINE.match(raw)
        if not m:
            rows.append((None, raw.strip()))  # malformed; checker reports it
            continue
        rows.append((m.group(1), m.group(2).strip()))
    return rows


def fmt_line(key, text):
    return f"{key:>5}  {text}"


def read_book(n):
    return parse_lines((LATIN / f"book_{n:02d}.txt").read_text(encoding="utf-8"))


def load_manifest():
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def save_manifest(m):
    with _lock:
        tmp = MANIFEST.with_suffix(".tmp")
        tmp.write_text(json.dumps(m, indent=1, ensure_ascii=False), encoding="utf-8")
        tmp.replace(MANIFEST)


def seg_dir(entry):
    d = SEG / f"b{entry['book']:02d}"
    d.mkdir(parents=True, exist_ok=True)
    return d


def seg_path(entry, stage):
    return seg_dir(entry) / f"s{entry['seg']:02d}.{stage}.txt"
