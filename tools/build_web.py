#!/usr/bin/env python3
"""Build the web reading edition: one HTML page per book, into docs/.

Ported from the Iliad project's tools/build_web.py (wrath-sing-goddess.com),
which was itself ported from the Odyssey's. The book-file format is the
same (argument, TRANSLATOR'S COMMENTARY, verse, Notes), so the parser is
the Iliad's with two additions for Lucretius: lettered lines (860a) and the
unnumbered `[lacuna]` lines the printed text leaves open. New here is the
margin layer: Machiavelli's reading marks from margin/marginalia.tsv set in
the actual right margin of the English beside the line they key to, and the
state of his copy on a page of its own (HANDOFF.md, "Margin layout").

Reads translation/book_0N.txt, latin/book_0N.txt, margin/marginalia.tsv
and illustrations/INDEX.md (all untouched) and emits:

    docs/index.html                  landing page
    docs/read/read.css               shared stylesheet
    docs/read/index.html             contents: the six books with their
                                     arguments, plus site search
    docs/read/book-0N.html           one page per book: the argument, the
                                     translator's note (collapsed), the two
                                     illustrations at their passages, the
                                     verse with line anchors and Machiavelli's
                                     margin, and the endnotes
    docs/read/margin.html            Machiavelli's margin: the introduction,
                                     every reading mark keyed to its line, and
                                     the state of the copy, one table per book
    docs/art/*.jpg                   the illustrations, resized for the web
    docs/social.jpg                  the 1200x630 link-preview image
    docs/api/                        machine-readable mirror: aligned-0N.jsonl
                                     (Latin and English paired line by line),
                                     book-0N.txt, marginalia.json, manifest.json
    docs/robots.txt, sitemap.xml, llms.txt

Each verse line gets an anchor (#L123, #L860a); every fifth line shows its
number in the gutter and every line's number is a copyable permalink. The
bracketed [7] note markers become superscript links to endnotes at the foot
of the page, keeping the source's own per-book numbering.

After building, refresh the search bundle with:

    npx -y pagefind --site docs

Usage:
    python tools/build_web.py
"""
from __future__ import annotations
import csv
import hashlib
import html
import json
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "translation"
LATIN = ROOT / "latin"
MARGIN = ROOT / "margin" / "marginalia.tsv"
ART = ROOT / "illustrations"
ART_INDEX = ART / "INDEX.md"
DOCS = ROOT / "docs"
AUDIO_PUBLISHED = ROOT / "audiobook" / "published.json"
OUT = DOCS / "read"
OUT_API = DOCS / "api"
OUT_ART = DOCS / "art"

# Every illustration carries this credit, so that no one takes an image for
# a photograph of a real Roman wall painting.
ART_CREDIT = "AI-generated illustration (Gemini), after Pompeian wall painting"
MARGIN_ART = "machiavelli_copying_lucretius.jpg"
MARGIN_ART_CREDIT = (
    "AI-generated illustration (Gemini), after late-fifteenth-century "
    "Florentine panel painting")

# The site has no domain yet: set SITE when it does. Everything that must
# be absolute (canonical links, Open Graph, the sitemap, llms.txt) hangs
# off this one constant.
SITE = os.environ.get("DRN_SITE", "https://de-rerum-natura.example")
REPO = os.environ.get("DRN_REPO", "https://github.com/spinchange/lucretius")
SITE_NAME = "De Rerum Natura — On the Nature of Things"
TAGLINE = "on the nature of things"
VATLIB = "https://digi.vatlib.it/view/MSS_Ross.884"

# --- the book-file format (shared with the Iliad's build_epub.py) ----------
# BOOK N / argument / TRANSLATOR'S COMMENTARY / prose / ---- / verse / ---- /
# Notes / "[7] (1.123-125) note text" with indented continuations.
RULE_RE = re.compile(r"^-{20,}\s*$")
VERSE_RE = re.compile(r"^\s*(\d+[a-z]?)\s\s+(\S.*)$")
LACUNA_RE = re.compile(r"^\s*\[lacuna\]\s*$")
REF_RE = re.compile(r"\[(\d+)\]")                        # inline marker: men[1]
DEF_RE = re.compile(r"^\[(\d+)\]\s+(?:\((\d+)\.(\d+[a-z]?)([^)]*)\)\s*)?(.*)$")

# a book.line citation in prose, book bounded to 1-6. Group 1 catches a
# preceding author/work name so citations of other texts ("Thucydides
# 2.47", "Aeneid 6.842", "Art of Love 2.657") are left unlinked.
CITE_RE = re.compile(
    r"((?:\b(?:Od|Odyssey|Il|Iliad|Aen|Aeneid|Georg|Georgics|Ecl|Eclogues|"
    r"Met|Metamorphoses|Fasti|Love|Amores|Heroides|Tristia|Hor|Horace|Odes|"
    r"Satires|Epistles|Ars|Ov|Ovid|Verg|Virgil|Vergil|Cic|Cicero|ND|Fin|Tusc|"
    r"Tusculans|Div|Sen|Seneca|NQ|Ep|Plin|Pliny|NH|HN|Hdt|Herodotus|History|"
    r"Histories|Thuc|Thucydides|Plut|Plutarch|Moralia|Lives|Diod|Diodorus|"
    r"Strabo|Paus|Pausanias|Athen|Athenaeus|Gell|Gellius|Macr|Macrobius|"
    r"Serv|Servius|Lact|Lactantius|Aug|Augustine|Isid|Isidore|Varro|LL|RR|"
    r"Liv|Livy|Tac|Tacitus|Ann|Hist|Suet|Suetonius|Quint|Quintilian|Inst|"
    r"Vitr|Vitruvius|Colum|Columella|Cato|Agr|Enn|Ennius|Emp|Empedocles|"
    r"Epic|Epicurus|Men|Pyth|KD|SV|DL|Diog|Diogenes|Laert|Laertius|Oen|"
    r"Oenoanda|Philod|Philodemus|PHerc|Lucr|DRN|Catull|Catullus|Prop|"
    r"Propertius|Tib|Tibullus|Juv|Juvenal|Pers|Persius|Mart|Martial|Stat|"
    r"Statius|Luc|Lucan|Sil|Val|Manil|Manilius|Arat|Aratus|Phaen|Nic|"
    r"Nicander|Theoc|Theocritus|Call|Callimachus|Ap|Apollonius|Arg|Aesch|"
    r"Aeschylus|Soph|Sophocles|Eur|Euripides|Ar|Aristophanes|Xen|Xenophon|"
    r"Mem|Arist|Aristotle|Phys|Metaph|Cael|Mete|Thphr|Theophrastus|HP|CP|"
    r"Simpl|Simplicius|Sext|Sextus|Galen|Hipp|Hippocrates|Epid|Hom|Homer|"
    r"Hes|Hesiod|Theog|Theogony|WD|Works|Pind|Pindar|Plato|Tim|Timaeus|Rep|"
    r"Republic|Laws|Phd|Phaedo|Boeth|Boethius|Apul|Apuleius|Petr|Petronius|"
    r"Nep|Nepos|Sall|Sallust|Caes|Caesar|BG|Bailey|Munro|Smith|Rouse|Brown|"
    r"Kenney|Fowler|Sedley|Leonard|Giussani|Ernout|Lachmann|Marullus|"
    r"Marullo|Lambinus|DK|Us|Usener|Arr|Arrighetti|Bertelli|p|pp|n|nn|c|ca|"
    r"ch|chs|fol|fols|vol|vols|no|nos|fr|frr|bk|bks|Book|Books|book|books|"
    r"lines?|ll|l|cf|canvas|Canvas)\.?\s+)?)"
    r"\b([1-6])\.([1-9]\d{0,3}[a-z]?)\b")

ROMAN = ["I", "II", "III", "IV", "V", "VI"]
TOTAL_LINES = 7412  # six books, Munro/Bailey numbering, lettered lines counted
LACUNAE = 20        # the unnumbered gaps the printed text leaves open

# Which kinds of marginalia go beside the verse, and which record the state
# of the copy (HANDOFF.md, "Margin layout").
READING_KINDS = {"note", "gloss", "marginal word", "manicule", "mark"}
COPY_KINDS = {"correction", "variant", "omission", "order marks",
              "supplied lines", "catchword", "colophon", "heading",
              "guide letter"}
# the two manicules at 1.589 are tie-marks for the supplied lines 585-588,
# not reading marks: they go with that repair in the copy table
TIE_MARK_KEYS = {"1.589"}
GLYPH = {"[manicule]": "☞", "-": "–", "*": "∗", "+": "+",
         "=": "=", "x": "×"}


# ---------------------------------------------------------------------------
# Parsing


def published_audio() -> dict[int, dict]:
    """Books whose narration is live on an audio host (the Iliad's
    tools/build_audio_web.py writes this file; nothing is published yet).
    Set AUDIO_PREVIEW=1 to include books encoded but not uploaded."""
    if not AUDIO_PUBLISHED.exists():
        return {}
    data = json.loads(AUDIO_PUBLISHED.read_text(encoding="utf-8"))
    preview = os.environ.get("AUDIO_PREVIEW") == "1"
    return {int(k): e for k, e in data["books"].items()
            if preview or e.get("uploaded_sha256") == e.get("sha256")}


def minutes(seconds: float) -> str:
    return f"{int(round(seconds / 60))} min"


def listen_block(n: int, audio: dict[int, dict]) -> str:
    e = audio.get(n)
    if not e:
        return ""
    return (f'<figure class="listen" data-pagefind-ignore>'
            f'<audio controls preload="none" src="{esc(e["url"])}"></audio>'
            f'<figcaption>Listen &middot; {minutes(e["duration_seconds"])} &middot; '
            f'<a href="{esc(e["url"])}" download="de-rerum-natura-book-{n:02d}.m4a">download</a> &middot; '
            f'<a href="../podcast.xml">podcast feed</a></figcaption></figure>')


def esc(text: str) -> str:
    return html.escape(text, quote=False)


def paragraphs(lines: list[str]) -> list[str]:
    """Blank-line-separated runs of lines, each joined into one string."""
    out: list[str] = []
    cur: list[str] = []
    for ln in lines:
        if ln.strip():
            cur.append(ln.strip())
        elif cur:
            out.append(" ".join(cur))
            cur = []
    if cur:
        out.append(" ".join(cur))
    return out


def key_sort(key: str) -> tuple[int, str]:
    m = re.match(r"(\d+)([a-z]?)$", key)
    return (int(m.group(1)), m.group(2))


def parse_book(path: Path) -> dict:
    """Return {n, argument, commentary, stanzas, notes, alias}.

    stanzas: list of stanzas, each a list of ("v", key, text) or ("lacuna",)
    items; key is the line number as printed ("860a" for lettered lines).
    notes: list of {num, book, line, span, body} in file order, num being
    the source's own bracketed number."""
    lines = path.read_text(encoding="utf-8").splitlines()
    rules = [i for i, ln in enumerate(lines) if RULE_RE.match(ln)]
    if len(rules) != 2:
        raise SystemExit(f"{path.name}: expected two rules, found {len(rules)}")
    head, verse, tail = (lines[:rules[0]], lines[rules[0] + 1:rules[1]],
                         lines[rules[1] + 1:])

    m = re.match(r"BOOK (\d+)", head[0].strip())
    if not m:
        raise SystemExit(f"{path.name}: unexpected first line {head[0]!r}")
    n = int(m.group(1))
    try:
        ci = next(i for i, ln in enumerate(head)
                  if ln.strip() == "TRANSLATOR'S COMMENTARY")
    except StopIteration:
        raise SystemExit(f"{path.name}: no TRANSLATOR'S COMMENTARY header")
    argument = " ".join(ln.strip() for ln in head[1:ci] if ln.strip())
    commentary = paragraphs(head[ci + 1:])

    stanzas: list[list[tuple]] = []
    cur: list[tuple] = []
    for ln in verse:
        if not ln.strip():
            if cur:
                stanzas.append(cur)
                cur = []
            continue
        if LACUNA_RE.match(ln):
            cur.append(("lacuna",))
            continue
        vm = VERSE_RE.match(ln)
        if not vm:
            raise SystemExit(f"{path.name}: unparsed verse line {ln!r}")
        cur.append(("v", vm.group(1), vm.group(2)))
    if cur:
        stanzas.append(cur)

    notes: list[dict] = []
    for ln in tail:
        if not ln.strip() or ln.strip().lower() == "notes":
            continue
        dm = DEF_RE.match(ln)
        if dm:
            num, book, line, span, body = dm.groups()
            notes.append({"num": int(num), "book": int(book) if book else n,
                          "line": line, "span": (span or "").strip(),
                          "body": body.strip()})
        elif notes and ln.startswith(" "):
            notes[-1]["body"] += " " + ln.strip()
        else:
            raise SystemExit(f"{path.name}: unparsed note line {ln!r}")

    cited = {int(x) for st in stanzas for it in st if it[0] == "v"
             for x in REF_RE.findall(it[2])}
    defined = {nt["num"] for nt in notes}
    if cited - defined:
        raise SystemExit(f"{path.name}: markers without notes "
                         f"{sorted(cited - defined)}")
    for orphan in sorted(defined - cited):
        print(f"  (book {n}: note [{orphan}] is never cited; omitted)")
    alias: dict[int, int] = {}
    for nt in notes:
        am = re.match(r"^[—-]+\s*merged into \[(\d+)\]\.?$", nt["body"])
        if am:
            alias[nt["num"]] = int(am.group(1))
    if any(t not in defined or t in alias for t in alias.values()):
        raise SystemExit(f"{path.name}: bad merged-note alias {alias}")
    notes = [nt for nt in notes if nt["num"] in cited and nt["num"] not in alias]
    return {"n": n, "argument": argument, "commentary": commentary,
            "stanzas": stanzas, "notes": notes, "alias": alias}


def read_latin(n: int) -> list[tuple[str, str]]:
    """(key, text) in the printed order; the lacuna markers are skipped."""
    rows = []
    for raw in (LATIN / f"book_{n:02d}.txt").read_text(
            encoding="utf-8").splitlines():
        m = VERSE_RE.match(raw)
        if m:
            rows.append((m.group(1), m.group(2).strip()))
        elif raw.strip() and not LACUNA_RE.match(raw):
            raise SystemExit(f"latin/book_{n:02d}.txt: unparsed line {raw!r}")
    return rows


# ---------------------------------------------------------------------------
# Machiavelli's margin


KEY_RE = re.compile(r"^(\d)\.(\d+[a-z]?)")


def parse_margin() -> list[dict]:
    """The marginalia table, one dict per row, with the rows numbered (the
    id used by the anchors on margin.html) and each row's anchor lines
    worked out from its book.line column.

    anchors: the (book, key) pairs a reading mark is set beside. A range
    ("2.251-256") sits beside its first line; a list ("1.774, 1.780") beside
    each; "2.425+" and "4.911 (below)" beside the line named; "2.1 (before)"
    beside line 1; the catchwords have no line and no anchor."""
    rows = []
    with MARGIN.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE)
        for i, r in enumerate(reader, 1):
            r = {k: (v or "").strip() for k, v in r.items()}
            r["id"] = i
            r["canvas"] = int(r["canvas"])
            anchors = []
            book = None
            for part in r["book.line"].split(","):
                part = part.strip()
                m = KEY_RE.match(part)
                if not m:
                    continue
                book = int(m.group(1))
                anchors.append((book, m.group(2)))
            if book is None:
                # a catchword at the foot of a quire: place it by its folio
                book = None
            r["book"] = book
            r["anchors"] = anchors
            r["reading"] = (r["kind"] in READING_KINDS
                            and r["book.line"] not in TIE_MARK_KEYS)
            if r["kind"] not in READING_KINDS | COPY_KINDS:
                raise SystemExit(f"marginalia row {i}: unknown kind {r['kind']!r}")
            rows.append(r)
    # the catchwords belong to the book whose folio they close: find it from
    # the nearest preceding row with a book
    last = None
    for r in rows:
        if r["book"] is None:
            r["book"] = last
        last = r["book"]
    return rows


def folio_link(r: dict, cls: str = "fol") -> str:
    return (f'<a class="{cls}" href="{VATLIB}/{r["canvas"]:04d}" '
            f'title="DigiVatLib, canvas {r["canvas"]}">fol. {esc(r["folio"])}</a>')


def lang_attr(text: str) -> str:
    return ' lang="grc"' if re.search(r"[Ͱ-Ͽἀ-῿]", text) else ' lang="la"'


def margin_span(r: dict) -> str:
    """One reading mark, set beside its line."""
    title = html.escape(r["diplomatic"], quote=True)
    out = [f'<span class="mg mg-{r["kind"].replace(" ", "-")}" title="{title}">']
    exp = r["expanded"]
    if r["kind"] in ("mark", "manicule"):
        glyph = GLYPH.get(exp, exp)
        out.append(f'<a class="mg-glyph" href="margin.html#m{r["id"]}">{esc(glyph)}</a>')
    else:
        out.append(f'<a class="mg-lat"{lang_attr(exp)} href="margin.html#m{r["id"]}">{esc(exp)}</a>')
        if r["english"]:
            out.append(f'<span class="mg-en">{esc(r["english"])}</span>')
    out.append(folio_link(r, "mg-fol"))
    out.append("</span>")
    return "".join(out)


# ---------------------------------------------------------------------------
# Illustrations


ART_HEAD_RE = re.compile(r"^###\s+(\d+)\.\s+(.*?)\s*\(`([1-6])\.(\d+)[^`]*`.*\)\s*$")
ART_FILE_RE = re.compile(r"\*\*File:\*\*\s*\[`([^`]+)`\]")


def parse_art() -> dict[int, list[dict]]:
    """The illustrations by book: [{file, title, line}] from INDEX.md, where
    each ### heading names the passage and the next **File:** line the
    image. line is the first line of the passage, where the figure is
    placed (before the stanza that contains it)."""
    by_book: dict[int, list[dict]] = {}
    if not ART_INDEX.exists():
        return by_book
    cur = None
    for ln in ART_INDEX.read_text(encoding="utf-8").splitlines():
        hm = ART_HEAD_RE.match(ln)
        if hm:
            cur = {"title": hm.group(2), "book": int(hm.group(3)),
                   "line": int(hm.group(4)), "ref": None}
            cur["ref"] = re.search(r"\(`([^`]+)`", ln).group(1)
            continue
        fm = ART_FILE_RE.search(ln)
        if fm and cur:
            cur["file"] = fm.group(1)
            if not (ART / cur["file"]).exists():
                raise SystemExit(f"illustration missing: {cur['file']}")
            by_book.setdefault(cur["book"], []).append(cur)
            cur = None
    return by_book


def export_art(art: dict[int, list[dict]]) -> None:
    """Resize the illustrations to 1200 px wide for the web, and cut the
    social card from the first of them."""
    try:
        from PIL import Image
    except ImportError:
        print("  (Pillow not installed: illustrations not exported)")
        return
    OUT_ART.mkdir(parents=True, exist_ok=True)
    files = [it["file"] for items in art.values() for it in items]
    if (ART / MARGIN_ART).exists():
        files.append(MARGIN_ART)
    for fname in files:
        src = ART / fname
        dst = OUT_ART / fname
        if dst.exists() and dst.stat().st_mtime >= src.stat().st_mtime:
            continue
        im = Image.open(src).convert("RGB")
        if im.width > 1200:
            im = im.resize((1200, round(im.height * 1200 / im.width)),
                           Image.LANCZOS)
        im.save(dst, "JPEG", quality=82, optimize=True, progressive=True)
    first = art.get(1, [None])[0]
    if first and not (DOCS / "social.jpg").exists():
        im = Image.open(ART / first["file"]).convert("RGB")
        w, h = im.size
        th = round(w * 630 / 1200)
        top = max(0, (h - th) // 2)
        im = im.crop((0, top, w, top + th)).resize((1200, 630), Image.LANCZOS)
        im.save(DOCS / "social.jpg", "JPEG", quality=85, optimize=True)


def figure(it: dict, n: int) -> str:
    plain = it["title"].replace("*", "")
    title = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", esc(it["title"]))
    return (f'<figure class="art" data-pagefind-ignore>'
            f'<a href="../art/{it["file"]}"><img src="../art/{it["file"]}" '
            f'alt="{html.escape(plain, quote=True)}" loading="lazy"></a>'
            f'<figcaption>{title} '
            f'<a class="cite" href="#L{it["line"]}">{esc(it["ref"])}</a>'
            f'<span class="credit">{esc(ART_CREDIT)}</span></figcaption>'
            f'</figure>')


# ---------------------------------------------------------------------------
# Page furniture


def css_version() -> str:
    return hashlib.md5(CSS.encode("utf-8")).hexdigest()[:8]


def social_meta(title: str, desc: str, path: str) -> str:
    url = f"{SITE}/{path}"
    t, d = html.escape(title), html.escape(desc)
    return f"""<link rel="canonical" href="{url}">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="{html.escape(SITE_NAME)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/social.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
"""


def page(title: str, desc: str, body: str, path: str, depth_home: str = "../",
         indexed: bool = False, head_extra: str = "", wrap_cls: str = "") -> str:
    body_attr = " data-pagefind-body" if indexed else ""
    cls = f' class="wrap{(" " + wrap_cls) if wrap_cls else ""}"'
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
{social_meta(title, desc, path)}<link rel="stylesheet" href="read.css?v={css_version()}">
{head_extra}</head>
<body>
<div class="band"></div>
<div{cls}{body_attr}>
<p class="site" data-pagefind-ignore><a href="{depth_home}">De Rerum Natura · {TAGLINE}</a></p>
{body}
</div>
<div class="band"></div>
<footer>
  <a href="index.html">Contents</a> · <a href="margin.html">Machiavelli’s margin</a> · <a href="{depth_home}">About</a><br>
  translation <a href="https://creativecommons.org/publicdomain/zero/1.0/">CC0</a> (public domain) ·
  notes, commentary &amp; the margin transcription © 2026 Chris Duffy, <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a> ·
  Latin source public domain
</footer>
</body>
</html>
"""


def booknav(n: int, bottom: bool = False) -> str:
    prev_a = (f'<a href="book-{n-1:02d}.html">&lsaquo; Book {n-1}</a>'
              if n > 1 else "<span></span>")
    next_a = (f'<a href="book-{n+1:02d}.html">Book {n+1} &rsaquo;</a>'
              if n < 6 else "<span></span>")
    cls = "booknav bottom" if bottom else "booknav"
    return (f'<nav class="{cls}" data-pagefind-ignore>{prev_a}'
            f'<span class="mid"><a href="index.html">Contents</a> · '
            f'<a href="margin.html">Margin</a></span>{next_a}</nav>')


def cite_links(escaped: str, here: int | None = None) -> str:
    """Turn book.line citations in already-escaped text into deep links.
    A citation preceded by another work's name ("Aeneid 6.842") is left
    alone. `here` is the current book: citations into it link within the
    page."""
    def link(m: re.Match) -> str:
        if m.group(1):
            return m.group(0)
        b, l = int(m.group(2)), m.group(3)
        target = f"#L{l}" if b == here else f"book-{b:02d}.html#L{l}"
        return f'<a class="cite" href="{target}">{b}.{l}</a>'
    return CITE_RE.sub(link, escaped)


def prose(text: str, here: int | None = None) -> str:
    return cite_links(esc(text), here)


# ---------------------------------------------------------------------------
# Book pages


def build_book(bk: dict, margin: list[dict], art: list[dict],
               audio: dict[int, dict] | None = None) -> str:
    n = bk["n"]
    # reading marks by anchor key, in table order
    beside: dict[str, list[dict]] = {}
    for r in margin:
        if r["reading"]:
            for b, key in r["anchors"]:
                if b == n:
                    beside.setdefault(key, []).append(r)
    # the illustrations stand immediately before the first line of the
    # passage they show
    art_at: dict[str, list[dict]] = {}
    for it in art:
        art_at.setdefault(str(it["line"]), []).append(it)

    out = [booknav(n)]
    out.append('<header class="bookhead">')
    out.append(f'<h1 data-pagefind-meta="title">Book {ROMAN[n-1]}</h1>')
    if bk["argument"]:
        out.append(f'<p class="argument">{esc(bk["argument"])}</p>')
    out.append("</header>")
    out.append(listen_block(n, audio or {}))

    if bk["commentary"]:
        out.append('<details class="tnote">')
        out.append(f'<summary>Translator’s note on Book {n}</summary>')
        for para in bk["commentary"]:
            text = re.sub(r"\bnote \[?(\d+)\]?(?!\d)",
                          r'<a href="#n\1">note \1</a>', prose(para, n))
            out.append(f"<p>{text}</p>")
        out.append("</details>")
    if beside:
        out.append('<p class="mg-key" data-pagefind-ignore>In the right margin: '
                   'what Machiavelli wrote beside these lines in his own copy, '
                   'Vatican MS Ross. 884, each linked to its folio. '
                   '<a href="margin.html">About the margin</a>.</p>')

    out.append('<div class="verse">')
    seen: set[int] = set()
    used: set[str] = set()
    for stanza in bk["stanzas"]:
        out.append('<div class="stanza">')
        for item in stanza:
            if item[0] == "lacuna":
                out.append('<p class="lacuna" title="a gap in the printed text; '
                           'nothing is supplied">[lacuna]</p>')
                continue
            _, key, text = item
            for it in art_at.pop(key, []):
                out.append(figure(it, n))

            def ref(m: re.Match) -> str:
                i = bk["alias"].get(int(m.group(1)), int(m.group(1)))
                anchor = "" if i in seen else f' id="r{i}"'
                seen.add(i)
                return (f'<a class="fnref"{anchor} href="#n{i}">'
                        f'<sup>{i}</sup></a>')
            body = REF_RE.sub(ref, esc(text))
            num_i, suffix = key_sort(key)
            shown = (num_i % 5 == 0 and not suffix) or key == "1"
            cls = "ln" if shown else "ln ghost"
            extra = "" if shown else ' aria-hidden="true" tabindex="-1"'
            num = (f'<a class="{cls}" href="#L{key}" data-pagefind-ignore'
                   f' title="copy link to line {key}"{extra}>{key}</a>')
            mg = "".join(margin_span(r) for r in beside.get(key, []))
            if mg:
                used.add(key)
                mg = f'<span class="mgs" data-pagefind-ignore>{mg}</span>'
            vcls = "v hasmg" if mg else "v"
            out.append(f'<p class="{vcls}" id="L{key}">{num}{body}{mg}</p>')
        out.append("</div>")
    out.append("</div>")
    if art_at:
        raise SystemExit(f"book {n}: illustration keyed to a line that is "
                         f"not in the verse: {sorted(art_at)}")
    for key in beside:
        if key not in used:
            raise SystemExit(f"book {n}: margin entry keyed to {key}, "
                             f"which is not a verse line")

    if bk["notes"]:
        out.append('<section class="notes">')
        out.append("<h2>Notes</h2>")
        for nt in bk["notes"]:
            i = nt["num"]
            if nt["line"] is not None:
                span = esc(nt["span"]).replace("-", "–")
                where = f'line{"s" if span else ""} {nt["line"]}{span}'
                line_a = f'<a class="nline" href="#L{nt["line"]}">{where}</a> — '
            else:
                line_a = ""
            out.append(
                f'<p class="note" id="n{i}">'
                f'<span class="nnum">{i}</span> '
                f'{line_a}{prose(nt["body"], n)} '
                f'<a class="back" href="#r{i}" title="back to the text">&#8617;</a></p>')
        out.append("</section>")

    out.append(booknav(n, bottom=True))
    out.append(COPY_JS)

    arg = bk["argument"].rstrip(".")
    desc = (f"Book {n} of Lucretius, De Rerum Natura, in a line-for-line "
            f"English translation" + (f": {arg}." if arg else "."))
    return page(f"De Rerum Natura, Book {n} — On the Nature of Things", desc,
                "\n".join(out), f"read/book-{n:02d}.html", indexed=True,
                wrap_cls="margined" if beside else "")


COPY_JS = """\
<script>
(function () {
  if (!navigator.clipboard) return;
  document.addEventListener('click', function (ev) {
    var a = ev.target.closest && ev.target.closest('a.ln');
    if (!a) return;
    var url = new URL(a.getAttribute('href'), location.href).href;
    navigator.clipboard.writeText(url).then(function () {
      var t = document.createElement('span');
      t.className = 'copied';
      t.textContent = 'link copied';
      var r = a.getBoundingClientRect();
      t.style.left = (r.left + window.scrollX) + 'px';
      t.style.top = (r.top + window.scrollY) + 'px';
      document.body.appendChild(t);
      setTimeout(function () { t.remove(); }, 1200);
    }).catch(function () {});
  });
})();
</script>"""

SEARCH_HEAD = '<link rel="stylesheet" href="../pagefind/pagefind-ui.css">\n'

SEARCH_BLOCK = """\
<div id="search"></div>
<script src="../pagefind/pagefind-ui.js"></script>
<script>
window.addEventListener('DOMContentLoaded', function () {
  if (window.PagefindUI) new PagefindUI({
    element: '#search', showSubResults: true, showImages: false,
    translations: { placeholder: 'Search the poem, the notes, and the margin\\u2026' }
  });
});
</script>"""


def build_contents(books: dict[int, dict], margin: list[dict],
                   audio: dict[int, dict] | None = None) -> str:
    audio = audio or {}
    out = ['<header class="bookhead"><h1>De Rerum Natura</h1>',
           '<p class="argument">a line-for-line translation '
           '&middot; six books</p></header>',
           SEARCH_BLOCK,
           '<ol class="toc">']
    for n in range(1, 7):
        arg = esc(books[n]["argument"])
        mins = (f' <em class="mins">&#9654; {minutes(audio[n]["duration_seconds"])}</em>'
                if n in audio else "")
        out.append(
            f'<li><a href="book-{n:02d}.html"><b>Book {ROMAN[n-1]}</b>'
            f'<span>{arg}{mins}</span></a></li>')
    out.append("</ol>")
    if audio:
        hours = sum(e["duration_seconds"] for e in audio.values()) / 3600
        scope = ("every book" if len(audio) == 6
                 else f"{len(audio)} of the six books so far")
        out.append(
            '<p class="apparatus"><a href="../podcast.xml">Listen</a>'
            f' — the poem read aloud, {scope}, about {hours:.0f} hours: a player'
            ' at the head of each book, or subscribe to the podcast feed.</p>')
    reading = sum(1 for r in margin if r["reading"])
    out.append(
        '<p class="apparatus"><a href="margin.html">Machiavelli’s margin</a>'
        f' — what Niccolò Machiavelli wrote beside the poem in the copy he made '
        f'with his own hand, about 1497: {reading} marks and notes, set in the '
        f'margin of this translation and keyed to their folios in the Vatican '
        f'Library’s manuscript.</p>')
    return page("Read De Rerum Natura — On the Nature of Things",
                "Lucretius, On the Nature of Things, complete in a "
                "line-for-line English translation with notes: all six "
                "books, free to read online, with Machiavelli's marginalia.",
                "\n".join(out), "read/index.html", head_extra=SEARCH_HEAD)


# ---------------------------------------------------------------------------
# Machiavelli's margin: the introduction, the reading marks, the copy


MARGIN_INTRO = [
    "Vatican Library, MS Ross. 884 is a copy of De Rerum Natura in the hand "
    "of Niccolò Machiavelli. He made it himself, in his late twenties, in "
    "the years around 1497, from a printed edition that carried the "
    "emendations of Michele Marullo, and bound it with Terence’s Eunuchus; "
    "the subscription on the last leaf of the poem reads Nicolaus "
    "Maclavellus scripsit foeliciter, struck through by a single stroke, "
    "while the Finis Τέλος above it stands. The hand was identified by "
    "Sergio Bertelli in 1961. Alison Brown’s The Return of Lucretius to "
    "Renaissance Florence (2010) prints his notes on Book 2 and is the "
    "checklist against which every reading here was made.",
    "This layer records everything written in the margins and between the "
    "lines of the 133 folios of the poem: the verbal notes, nearly all of "
    "them beside Book 2 on the motion of the first-beginnings, the swerve, "
    "the free mind that follows from it, and the gods’ indifference; the "
    "Greek glosses; the single words in a lighter ink that gloss a hard "
    "Latin word; the pointing hand at 2.82; and the dashes, crosses and "
    "other marks that show where the reader stopped. Those are the reading "
    "marks, and on the book pages each is set in the right margin beside "
    "the English of the line it stands against, in the Latin as Machiavelli "
    "wrote it (abbreviations expanded) with an English rendering beneath "
    "and a link to the folio on DigiVatLib, where the page itself can be "
    "seen. Everything else, the copyist’s own corrections, the variants "
    "written in the margin, the lines he dropped and the lines he supplied, "
    "the order marks, catchwords and colophons, is the state of the copy "
    "rather than a record of reading, and is tabulated here, book by book, "
    "beneath the reading marks.",
    "The images of the manuscript belong to the Vatican Library and are "
    "not reproduced; every entry links to its opening on DigiVatLib "
    "instead (a recto NNr is canvas NN+11, a verso NNv is canvas NN+12). "
    "The transcription keeps the diplomatic form of each note, expands its "
    "abbreviations, keys it to the line of the poem by the words it stands "
    "against rather than by counting, and records whether Brown’s list "
    "prints it. Where the copy’s line order or wording differs from the "
    "Latin printed here, the entry says so. The copy was written at "
    "twenty-eight lines a page.",
]


def entry_order(r: dict) -> tuple:
    """Line order on the margin page: by first anchor, the catchwords and
    colophons (no anchor, or a + key) after everything else of their book;
    ties keep the table's order."""
    if not r["anchors"]:
        return (10**6, r["id"])
    b, key = r["anchors"][0]
    num, suffix = key_sort(key)
    return (num, suffix, r["id"])


def brown_label(r: dict) -> str:
    """How Brown's list stands to the entry; nothing for the entries she
    does not print or that were not checked against her."""
    if r["brown"] in ("", "not listed", "unchecked"):
        return ""
    if r["brown"] == "agrees":
        return "in Brown’s list"
    return f"Brown: {esc(r['brown'])}"


def book_href(b: int, key: str, here_margin: bool = True) -> str:
    return f"book-{b:02d}.html#L{key}"


def line_label(r: dict) -> str:
    """The book.line column as it stands, with its first anchor linked."""
    text = esc(r["book.line"])
    if r["anchors"]:
        b, key = r["anchors"][0]
        return f'<a class="cite" href="{book_href(b, key)}">{text}</a>'
    return text


def render_margin_entry(r: dict) -> str:
    out = [f'<p class="mentry" id="m{r["id"]}">']
    out.append(f'<span class="mline">{line_label(r)}</span> · {folio_link(r)} · '
               f'<span class="mkind">{esc(r["kind"])}</span><br>')
    exp = r["expanded"]
    if r["kind"] in ("mark", "manicule"):
        out.append(f'<span class="mglyph">{esc(GLYPH.get(exp, exp))}</span> ')
    else:
        out.append(f'<span class="mlat"{lang_attr(exp)}>{esc(exp)}</span> ')
    if r["english"]:
        out.append(f'<span class="men">{cite_links(esc(r["english"]))}</span>')
    out.append(f'<br><span class="mdipl">{cite_links(esc(r["diplomatic"]))}</span>')
    extra = []
    if brown_label(r):
        extra.append(brown_label(r))
    if r["remarks"]:
        extra.append(cite_links(esc(r["remarks"])))
    if extra:
        out.append(f'<br><span class="mrem">{" · ".join(extra)}</span>')
    out.append("</p>")
    return "".join(out)


def render_copy_table(rows: list[dict]) -> str:
    out = ['<table class="copy"><thead><tr><th>line</th><th>fol.</th>'
           '<th>kind</th><th>the copy</th><th>reading</th><th>note</th>'
           '</tr></thead><tbody>']
    for r in rows:
        note = cite_links(esc(r["english"]))
        if r["remarks"]:
            note += f' <span class="mrem">{cite_links(esc(r["remarks"]))}</span>'
        if brown_label(r):
            note += f' <span class="mrem">{brown_label(r)}</span>'
        out.append(
            f'<tr id="m{r["id"]}"><td class="mline">{line_label(r)}</td>'
            f'<td>{folio_link(r)}</td><td class="mkind">{esc(r["kind"])}</td>'
            f'<td class="mdipl">{esc(r["diplomatic"])}</td>'
            f'<td class="mlat"{lang_attr(r["expanded"])}>{esc(r["expanded"])}</td>'
            f'<td class="men">{note}</td></tr>')
    out.append("</tbody></table>")
    return "\n".join(out)


def build_margin(margin: list[dict]) -> str:
    reading = [r for r in margin if r["reading"]]
    copy = [r for r in margin if not r["reading"]]
    out = ['<nav class="booknav" data-pagefind-ignore>'
           '<a href="index.html">&lsaquo; Contents</a><span></span>'
           '<a href="book-01.html">Book 1 &rsaquo;</a></nav>',
           '<header class="bookhead">',
           '<h1 data-pagefind-meta="title">Machiavelli’s Margin</h1>',
           '<p class="argument">what he wrote beside the poem in his own '
           'copy, Vatican MS Ross. 884</p>',
           '</header>']
    if (ART / MARGIN_ART).exists():
        out.append(
            f'<figure class="art" data-pagefind-ignore>'
            f'<a href="../art/{MARGIN_ART}"><img src="../art/{MARGIN_ART}" '
            f'alt="Machiavelli copying De Rerum Natura in his study, Florence, c. 1497 (an imagined scene)" '
            f'loading="lazy"></a>'
            f'<figcaption>Niccolò Machiavelli copying <em>De Rerum Natura</em>, '
            f'Florence, c. 1497 — an imagined scene'
            f'<span class="credit">{esc(MARGIN_ART_CREDIT)}</span>'
            f'</figcaption></figure>')
    out.append('<div class="prose">')
    for para in MARGIN_INTRO:
        out.append(f"<p>{prose(para)}</p>")
    out.append(
        f'<p class="apparatus">{len(margin)} entries: {len(reading)} reading '
        f'marks, set in the margin of the book pages and listed here, and '
        f'{len(copy)} entries on the state of the copy. '
        f'Jump to a book: ' + " · ".join(
            f'<a href="#book-{n}">{ROMAN[n-1]}</a>' for n in range(1, 7))
        + '. The whole table is also served as '
        '<a href="../api/marginalia.json">marginalia.json</a>.</p>')
    out.append("</div>")
    for n in range(1, 7):
        out.append(f'<section class="mbook" id="book-{n}">')
        out.append(f'<h2>Book {ROMAN[n-1]}</h2>')
        rd = sorted((r for r in reading if r["book"] == n), key=entry_order)
        cp = sorted((r for r in copy if r["book"] == n), key=entry_order)
        out.append(f'<h3>In the margin <span class="count">{len(rd)}</span></h3>')
        if rd:
            for r in rd:
                out.append(render_margin_entry(r))
        else:
            out.append('<p class="mrem">No reading mark in this book.</p>')
        out.append(f'<h3>The copy <span class="count">{len(cp)}</span></h3>')
        if cp:
            out.append(render_copy_table(cp))
        out.append("</section>")
    out.append('<nav class="booknav bottom" data-pagefind-ignore>'
               '<a href="index.html">&lsaquo; Contents</a><span></span>'
               '<a href="book-01.html">Book 1 &rsaquo;</a></nav>')
    return page("Machiavelli’s Margin — De Rerum Natura",
                "Every mark and note Niccolò Machiavelli wrote in his own "
                "manuscript copy of Lucretius (Vatican MS Ross. 884), "
                "transcribed, translated, keyed to the line of the poem and "
                "linked to its folio.", "\n".join(out), "read/margin.html",
                indexed=True)


# ---------------------------------------------------------------------------
# Machine-readable mirror (docs/api/)


API_NOTE = (
    "Machine-readable mirror of a line-for-line English translation of "
    "Lucretius, De Rerum Natura, with Machiavelli's marginalia. "
    "aligned-0N.jsonl is the parallel corpus for one book: one JSON object "
    "per verse line, {book, line, key, latin, en}, in the printed order of "
    "the text (line is the integer, key the printed number including the "
    "letter of a lettered line such as 860a), English verse only (no note "
    "markers); the printed text's lacunae are not rows. book-0N.txt is the "
    "full translation source for one book: a one-line argument, the "
    "translator's commentary, numbered verse lines ('  123  text', one "
    "English line per Latin line, same numbering) with bracketed [7] "
    "markers pointing into a notes section of endnotes, each opening with "
    "its (book.line) reference. marginalia.json is every mark and note in "
    "Machiavelli's copy (Vatican MS Ross. 884): canvas, folio, book.line, "
    "kind, diplomatic transcription, expanded reading, English, agreement "
    "with Brown 2010, remarks. Cite passages as book.line, e.g. 2.216. "
    "Human-readable edition with line anchors: /read/book-0N.html#L216.")


def aligned_book(bk: dict) -> list[dict]:
    n = bk["n"]
    latin = read_latin(n)
    en = {it[1]: REF_RE.sub("", it[2]).rstrip()
          for st in bk["stanzas"] for it in st if it[0] == "v"}
    if len(latin) != len(en) or sorted(k for k, _ in latin) != sorted(en):
        raise SystemExit(f"book {n}: Latin/English line keys disagree")
    rows = []
    for key, text in latin:
        num, _ = key_sort(key)
        rows.append({"book": n, "line": num, "key": key, "latin": text,
                     "en": en[key]})
    return rows


def build_api(books: dict[int, dict], margin: list[dict]) -> tuple[int, int]:
    OUT_API.mkdir(parents=True, exist_ok=True)
    manifest_books = []
    total = 0
    total_notes = 0
    sample = None
    for n in range(1, 7):
        bk = books[n]
        src = SRC / f"book_{n:02d}.txt"
        (OUT_API / f"book-{n:02d}.txt").write_text(
            src.read_text(encoding="utf-8"), encoding="utf-8")
        rows = aligned_book(bk)
        total += len(rows)
        total_notes += len(bk["notes"])
        if n == 2:
            sample = next(r for r in rows if r["key"] == "216")
        (OUT_API / f"aligned-{n:02d}.jsonl").write_text(
            "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows),
            encoding="utf-8")
        last = max(key_sort(it[1])[0] for st in bk["stanzas"]
                   for it in st if it[0] == "v")
        manifest_books.append({
            "book": n,
            "argument": bk["argument"],
            "lines": len(rows),
            "last_line": last,
            "notes": len(bk["notes"]),
            "marginalia": sum(1 for r in margin if r["book"] == n),
            "aligned": f"{SITE}/api/aligned-{n:02d}.jsonl",
            "text": f"{SITE}/api/book-{n:02d}.txt",
            "html": f"{SITE}/read/book-{n:02d}.html",
        })
    if total != TOTAL_LINES:
        raise SystemExit(f"aligned corpus has {total} lines, "
                         f"expected {TOTAL_LINES}")
    marg = [{"id": r["id"], "book": r["book"], "book_line": r["book.line"],
             "canvas": r["canvas"], "folio": r["folio"],
             "url": f"{VATLIB}/{r['canvas']:04d}", "kind": r["kind"],
             "layer": "reading" if r["reading"] else "copy",
             "diplomatic": r["diplomatic"], "expanded": r["expanded"],
             "english": r["english"], "brown": r["brown"],
             "remarks": r["remarks"]} for r in margin]
    (OUT_API / "marginalia.json").write_text(
        json.dumps(marg, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    manifest = {
        "title": SITE_NAME,
        "description": API_NOTE,
        "site": SITE,
        "repository": REPO,
        "license": ("English translation (the 'en' fields and the verse in "
                    "book-0N.txt): CC0 1.0 (public domain dedication). "
                    "Notes, commentary, and the margin transcription and "
                    "English: CC BY 4.0, (c) 2026 Chris Duffy. Latin: the "
                    "Perseus Digital Library text (public domain; markup "
                    "CC BY-SA 4.0), Munro/Bailey numbering. Machiavelli's "
                    "notes themselves: public domain."),
        "lines": total,
        "lacunae": LACUNAE,
        "notes": total_notes,
        "marginalia": len(margin),
        "marginalia_file": f"{SITE}/api/marginalia.json",
        "books": manifest_books,
    }
    (OUT_API / "manifest.json").write_text(
        json.dumps(manifest, indent=1, ensure_ascii=False) + "\n",
        encoding="utf-8")
    landing = (API_LANDING
               .replace("{CSSV}", css_version())
               .replace("{SITE}", SITE)
               .replace("{REPO}", REPO)
               .replace("{TOTAL}", f"{total:,}")
               .replace("{NOTES}", f"{total_notes:,}")
               .replace("{MARG}", str(len(margin)))
               .replace("{SAMPLE}", esc(json.dumps(sample, ensure_ascii=False))))
    (OUT_API / "index.html").write_text(landing, encoding="utf-8")
    build_crawler_files(total, total_notes, len(margin))
    print(f"  {total:,} aligned lines, {total_notes:,} notes, "
          f"{len(margin)} marginalia entries")
    return total, total_notes


def build_crawler_files(total: int, total_notes: int, marg: int) -> None:
    (DOCS / "robots.txt").write_text(
        "# Everything here is meant to be read, by people and by machines.\n"
        "# Machine-readable layer (JSONL parallel corpus, the marginalia as JSON):\n"
        f"#   {SITE}/api/manifest.json\n"
        "User-agent: *\n"
        "Allow: /\n"
        f"Sitemap: {SITE}/sitemap.xml\n",
        encoding="utf-8")
    urls = ([f"{SITE}/", f"{SITE}/read/index.html", f"{SITE}/read/margin.html"]
            + [f"{SITE}/read/book-{n:02d}.html" for n in range(1, 7)]
            + [f"{SITE}/api/"])
    (DOCS / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"<url><loc>{u}</loc></url>\n" for u in urls)
        + "</urlset>\n",
        encoding="utf-8")
    (DOCS / "llms.txt").write_text(f"""\
# {SITE_NAME}

> A complete line-for-line English translation of Lucretius, De Rerum
> Natura: all {total:,} lines, one English line per Latin line on the
> standard Munro/Bailey numbering, translated by a language model (Claude)
> from the Latin and human-edited, with {total_notes:,} notes and a layer
> recording the {marg} marks and notes Niccolò Machiavelli wrote in his
> own manuscript copy of the poem (Vatican MS Ross. 884). The English
> translation is public domain (CC0 1.0); the notes, the translator's
> commentary and the margin transcription are CC BY 4.0; the Latin is the
> Perseus Digital Library's text (public domain).

Cite passages as book.line (e.g. 2.216). Every verse of the reading
edition has a stable anchor: /read/book-02.html#L216.

## Machine-readable layer

- [manifest.json]({SITE}/api/manifest.json): describes every file below,
  with per-book URLs, line counts, and licensing
- [aligned-01.jsonl … aligned-06.jsonl]({SITE}/api/aligned-02.jsonl): the
  Latin-English parallel corpus, one JSON object per verse line
  ({{book, line, key, latin, en}})
- [book-01.txt … book-06.txt]({SITE}/api/book-02.txt): full translation
  source per book: argument, translator's commentary, verse, and the
  line-keyed notes
- [marginalia.json]({SITE}/api/marginalia.json): Machiavelli's marginalia,
  every entry with its folio link
- [About the API]({SITE}/api/): formats, examples, licensing detail

## Reading edition

- [Contents]({SITE}/read/index.html): all six books, one page each
- [Machiavelli's margin]({SITE}/read/margin.html): the introduction, the
  reading marks, and the state of the copy
- [About]({SITE}/)

## Companions

- [The Iliad](https://wrath-sing-goddess.com/) and
  [The Odyssey](https://theclaudyssey.com/): the same project's
  line-for-line Homer, each with its own machine-readable layer

## Source

- [Repository]({REPO}): full revision history, Latin source, build tools
""", encoding="utf-8")


API_LANDING = """\
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>The text as data — De Rerum Natura</title>
<meta name="description" content="The full translation, CC0, structured for machines: a Latin-English parallel corpus of Lucretius in JSONL, all {TOTAL} lines aligned to the standard numbering, plus Machiavelli's marginalia as JSON.">
<link rel="canonical" href="{SITE}/api/">
<meta property="og:title" content="The text as data — De Rerum Natura">
<meta property="og:description" content="A Latin-English parallel corpus of Lucretius in JSONL, all {TOTAL} lines aligned to the standard numbering, CC0, plus Machiavelli's marginalia as JSON. No key, no auth: static files.">
<meta property="og:type" content="article">
<meta property="og:site_name" content="De Rerum Natura — On the Nature of Things">
<meta property="og:url" content="{SITE}/api/">
<meta property="og:image" content="{SITE}/social.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="../read/read.css?v={CSSV}">
<style>
  pre{background:rgba(0,0,0,.35); border:1px solid rgba(214,166,74,.3);
      border-radius:6px; padding:12px 14px; overflow-x:auto;
      font-size:.82rem; line-height:1.5}
  code{font-size:.9em}
  h2{font-weight:normal; font-variant:small-caps; letter-spacing:.06em;
     margin:34px 0 10px; color:var(--ochre)}
  dl.files dt{font-family:ui-monospace,Consolas,monospace; margin-top:14px}
  dl.files dd{margin:2px 0 0 0; opacity:.9; font-size:.95rem}
  .lede{font-size:1.05rem}
</style>
</head>
<body>
<div class="band"></div>
<div class="wrap">
<p class="site"><a href="../">De Rerum Natura · on the nature of things</a></p>
<header class="bookhead"><h1>The text as data</h1>
<p class="argument">the full translation, CC0, structured for machines</p></header>

<p class="lede">Everything on this page is a stable, fetchable URL: a complete
Latin-English parallel corpus of De Rerum Natura ({TOTAL} verse lines,
aligned one-to-one on the standard Munro/Bailey numbering), the full
translation source with its {NOTES} notes and the translator's commentary on
each book, and the {MARG} entries of Machiavelli's margin. The English is
public domain (CC0). No key, no tracking, no limits of ours: it is a
directory of static files.</p>

<h2>The files</h2>
<dl class="files">
<dt><a href="manifest.json">manifest.json</a></dt>
<dd>describes everything below: per-book URLs, line counts, note counts,
book arguments, licensing. Start here if you are a script.</dd>
<dt><a href="aligned-02.jsonl">aligned-01.jsonl … aligned-06.jsonl</a></dt>
<dd>the parallel corpus, one book per file: one JSON object per verse line,
Latin and English paired.</dd>
<dt><a href="book-02.txt">book-01.txt … book-06.txt</a></dt>
<dd>the full translation source, one book per file: the argument, the
translator's commentary, the numbered verse, and the endnotes keyed to
line numbers.</dd>
<dt><a href="marginalia.json">marginalia.json</a></dt>
<dd>Machiavelli's marginalia in Vatican MS Ross. 884: {MARG} entries, each
with canvas and folio, the line of the poem, kind, diplomatic
transcription, expanded reading, English, and a link to the page on
DigiVatLib.</dd>
</dl>

<h2>The aligned corpus</h2>
<p>One JSON object per line, in the printed order. From
<a href="aligned-02.jsonl">aligned-02.jsonl</a>, the first line of the
swerve:</p>
<pre>{SAMPLE}</pre>
<p>The alignment is exact and complete: every English line was translated
from, and checked twice against, the Latin line it sits beside. The
numbering is the standard one. <code>line</code> is the integer and
<code>key</code> the printed number, which carries a letter for the five
lettered lines (1.860a, 2.164a, 2.465a, 2.528a, 2.903a); where the printed
text transposes lines (1.15 before 1.14, 2.680 after 2.659) both files keep
the printed order. The twenty places where the text is lost are marked
<code>[lacuna]</code> in the reading edition and are not rows here.</p>

<h2>The margin</h2>
<p>Every entry of the marginalia table. From
<a href="marginalia.json">marginalia.json</a>:</p>
<pre>{"id": 36, "book": 2, "book_line": "2.217-219", "canvas": 36, "folio": "24v",
 "url": "https://digi.vatlib.it/view/MSS_Ross.884/0036", "kind": "note",
 "layer": "reading", "expanded": "quom declinent principia",
 "english": "When the first-beginnings swerve.", ...}</pre>

<h2>Citing and linking</h2>
<p>Cite passages as <code>book.line</code> (e.g. <code>2.216</code>). Every
line of the reading edition has a stable anchor, so any citation can become
a link: <a href="../read/book-02.html#L216">/read/book-02.html#L216</a>.</p>

<h2>Examples</h2>
<p>Fetch one book's alignment and pull out one line:</p>
<pre>curl -s {SITE}/api/aligned-02.jsonl | grep '"key": "216"'</pre>
<p>Load the whole poem as a dataset:</p>
<pre>import json, urllib.request
rows = []
for n in range(1, 7):
    url = f"{SITE}/api/aligned-{n:02d}.jsonl"
    with urllib.request.urlopen(url) as f:
        rows += [json.loads(line) for line in f]
assert len(rows) == 7412</pre>

<h2>Licensing</h2>
<p>Three layers, cleanly separated. The <strong>English translation</strong>
(every <code>en</code> field, and the verse in <code>book-0N.txt</code>) is
dedicated to the public domain under
<a href="https://creativecommons.org/publicdomain/zero/1.0/">CC0 1.0</a>.
The <strong>Latin</strong> is the Perseus Digital Library's text, in the
public domain (its TEI markup is CC BY-SA 4.0). The <strong>notes, the
translator's commentary, and the transcription and English of the
margin</strong> are © 2026 Chris Duffy,
<a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>;
Machiavelli's words are his own and public domain. The illustrations are
AI-generated (Google Gemini) and are not reproductions of ancient
paintings.</p>

<h2>Provenance</h2>
<p>The translation was produced by a language model (Claude) from the Latin,
line by line, checked twice against it, and edited by a human; the method
and the full revision history are public in <a href="{REPO}">the
repository</a>. The same project's Iliad and Odyssey, with the same
machine-readable layer, are at
<a href="https://wrath-sing-goddess.com/api/">wrath-sing-goddess.com/api/</a>
and <a href="https://theclaudyssey.com/api/">theclaudyssey.com/api/</a>.</p>

</div>
<div class="band"></div>
<footer><a href="../read/index.html">Contents</a> · <a href="../">About</a></footer>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# The landing page


def build_landing(books: dict[int, dict], margin: list[dict], total: int,
                  total_notes: int, art: dict[int, list[dict]]) -> str:
    reading = sum(1 for r in margin if r["reading"])
    hero = art.get(1, [None])[0]
    hero_html = (f'<a href="read/book-01.html#L{hero["line"]}"><img src="art/{hero["file"]}" '
                 f'alt="{html.escape(hero["title"], quote=True)}" '
                 f'title="{html.escape(ART_CREDIT, quote=True)}"></a>'
                 if hero else "")
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(SITE_NAME)}</title>
<meta name="description" content="A complete line-for-line English translation of Lucretius, De Rerum Natura, from the Latin, with notes, a translator's commentary on every book, and the marginalia Machiavelli wrote in his own copy of the poem. Free to read online.">
<link rel="canonical" href="{SITE}/">
<meta property="og:title" content="{html.escape(SITE_NAME)}">
<meta property="og:description" content="Lucretius, On the Nature of Things, complete in a line-for-line English translation with notes, and Machiavelli's margin. Free to read online.">
<meta property="og:site_name" content="{html.escape(SITE_NAME)}">
<meta property="og:url" content="{SITE}/">
<meta property="og:image" content="{SITE}/social.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:type" content="book">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Book",
  "name": "{html.escape(SITE_NAME)}",
  "author": {{"@type": "Person", "name": "Lucretius"}},
  "translator": {{"@type": "Person", "name": "Claude (Fable 5.1)"}},
  "editor": {{"@type": "Person", "name": "Chris Duffy"}},
  "inLanguage": "en",
  "url": "{SITE}/",
  "license": "https://creativecommons.org/publicdomain/zero/1.0/",
  "isAccessibleForFree": true,
  "bookFormat": "https://schema.org/EBook",
  "isBasedOn": {{
    "@type": "Book",
    "name": "T. Lucreti Cari De Rerum Natura (Perseus Digital Library text, Munro/Bailey numbering)",
    "inLanguage": "la"
  }}
}}
</script>
<link rel="stylesheet" href="read/read.css?v={css_version()}">
<style>
  .wrap{{max-width:820px}}
  header.land{{text-align:center; padding:26px 0 8px}}
  .epigraph{{font-style:italic; opacity:.85; margin:6px 0 2px; font-size:1.05rem}}
  .epigraph .la{{display:block; font-size:1.2rem; opacity:.95; margin-bottom:.25rem; font-style:normal}}
  header.land h1{{font-size:clamp(2.4rem,8vw,4rem); letter-spacing:.04em; margin:.15em 0 .05em; font-weight:normal}}
  .sub{{color:var(--ochre); font-size:1.25rem; letter-spacing:.2em; margin:.1em 0 .3em; font-variant:small-caps}}
  .rule{{width:120px; height:0; border-top:1px solid var(--ochre); opacity:.8; margin:.6em auto}}
  .byline{{font-size:.82rem; letter-spacing:.14em; text-transform:uppercase; opacity:.85}}
  .byline .role{{color:var(--ochre)}}
  .hero{{display:flex; gap:34px; align-items:center; margin:34px 0 8px; flex-wrap:wrap; justify-content:center}}
  .hero img{{width:300px; max-width:80vw; border-radius:3px; box-shadow:0 14px 44px rgba(0,0,0,.5); border:1px solid rgba(214,166,74,.35)}}
  .hero .blurb{{flex:1; min-width:260px}}
  .stat{{display:flex; gap:26px; flex-wrap:wrap; margin-top:12px; font-size:.95rem}}
  .stat b{{color:var(--ochre); font-size:1.15rem; display:block; font-weight:normal}}
  .downloads{{margin:30px 0; text-align:center}}
  .downloads h2{{font-weight:normal; letter-spacing:.08em; font-variant:small-caps;
    color:var(--ochre); font-size:1.35rem; margin:.2em 0 .1em; border:0}}
  .btns{{display:flex; gap:14px; justify-content:center; flex-wrap:wrap; margin-top:16px}}
  .btn{{display:inline-block; padding:13px 22px; border:1px solid var(--ochre);
    border-radius:5px; color:var(--chalk); text-decoration:none; background:rgba(214,166,74,.08);
    transition:background .15s, transform .1s; min-width:150px}}
  .btn:hover{{background:rgba(214,166,74,.2); transform:translateY(-1px)}}
  .btn b{{display:block; font-size:1.05rem; color:var(--ochre)}}
  .btn span{{font-size:.8rem; opacity:.8}}
  section{{margin:34px 0}}
  section h2{{font-weight:normal; font-variant:small-caps; letter-spacing:.06em;
    color:var(--ochre); border-bottom:1px solid rgba(214,166,74,.3); padding-bottom:6px}}
  .feat{{display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:18px}}
  .feat div{{background:rgba(0,0,0,.18); border:1px solid rgba(239,230,210,.12);
    border-radius:6px; padding:16px 18px}}
  .feat h3{{margin:.1em 0 .3em; color:var(--chalk); font-weight:normal; font-size:1.05rem}}
  .feat p{{margin:0; font-size:.92rem; opacity:.85}}
</style>
</head>
<body>
<div class="band"></div>
<div class="wrap">
<header class="land">
  <p class="epigraph"><span class="la" lang="la">Aeneadum genetrix, hominum divomque voluptas</span>
     Mother of Aeneas’ race, pleasure of men and gods</p>
  <h1>De Rerum Natura</h1>
  <div class="sub">On the Nature of Things</div>
  <div class="rule"></div>
  <p class="byline">
    <span class="role">from the Latin of</span> Lucretius &nbsp;·&nbsp;
    <span class="role">translated by</span> Claude (Fable 5.1) &nbsp;·&nbsp;
    <span class="role">edited &amp; produced by</span> Chris Duffy
  </p>
</header>
<div class="hero">
  {hero_html}
  <div class="blurb">
    <p>A complete <strong>line-for-line</strong> English translation of
    Lucretius’ poem on the Epicurean universe: every one of its {total:,}
    English lines keyed one-to-one to its Latin line, in plain, exact free
    verse that keeps his terms rigid and his repetitions verbatim.</p>
    <p>Each book opens with a translator’s commentary and closes with its
    notes. In the margin of the English stands what Niccolò Machiavelli
    wrote in the margin of the copy he made of the poem with his own hand,
    about 1497, now Vatican MS Ross. 884: his notes on the swerve and the
    free mind, his Greek, his marks, each linked to its folio.</p>
    <div class="stat">
      <div><b>6</b> books</div>
      <div><b>{total:,}</b> lines</div>
      <div><b>{total_notes}</b> notes</div>
      <div><b>{reading}</b> marginal notes &amp; marks</div>
    </div>
  </div>
</div>
<div class="downloads">
  <h2>Read it</h2>
  <div class="btns">
    <a class="btn" href="read/">
      <b>Read online</b><span>all six books, searchable</span></a>
    <a class="btn" href="read/margin.html">
      <b>Machiavelli’s margin</b><span>his notes, keyed to the poem</span></a>
    <a class="btn" href="api/">
      <b>The text as data</b><span>Latin and English, line by line</span></a>
  </div>
</div>
<section>
  <h2>Start anywhere</h2>
  <p>The poem argues from its first line to its last, but it can be entered
  at any of its set pieces.
  <a href="read/book-01.html#L1">Book 1</a> opens with the hymn to Venus and
  the sacrifice of Iphigenia, and proves that nothing comes from nothing;
  <a href="read/book-02.html#L216">Book 2</a> is the swerve, and the motes
  in the sunbeam; <a href="read/book-03.html#L830">Book 3</a> argues that
  death is nothing to us; <a href="read/book-04.html#L1058">Book 4</a> is
  the images, the senses, and the diatribe against love;
  <a href="read/book-05.html#L925">Book 5</a> is the birth of the world and
  the history of mankind from the first fire to the first song;
  <a href="read/book-06.html#L1138">Book 6</a> is thunder, the magnet, and
  the plague at Athens, on which the poem breaks off.</p>
</section>
<section>
  <h2>What’s inside</h2>
  <div class="feat">
    <div><h3>Line for line</h3><p>One English line per Latin line, same
      numbering, so the two can be read side by side; the lacunae are left
      open, never supplied.</p></div>
    <div><h3>The terms kept rigid</h3><p>Primordia is first-beginnings every
      time, inane is void, religio is religion, anima is spirit and never
      soul; the word atom never appears, because Lucretius never uses it.</p></div>
    <div><h3>The refrains kept</h3><p>Where the Latin repeats a line, the
      English repeats its own earlier line word for word.</p></div>
    <div><h3>Annotated</h3><p>{total_notes} notes on the Latin, the doctrine,
      the text and the translation choices, as endnotes to each book, and a
      translator’s commentary on every book.</p></div>
    <div><h3>Machiavelli’s margin</h3><p>Every mark and note in his autograph
      copy, read from the Vatican Library’s images, transcribed, translated
      and set beside the line it stands against.</p></div>
    <div><h3>Illustrated</h3><p>Thirteen pictures in the manner of the wall
      paintings of Lucretius’ own century, at the passages they show, and a
      Florentine panel on the margin page.</p></div>
  </div>
</section>
<section>
  <h2>About the text</h2>
  <p>The Latin is the Perseus Digital Library’s text, which keeps the
  standard numbering of Munro and Bailey and follows Munro in its spelling
  and some of its readings; the translation follows the printed text
  throughout, keeps the printed order where lines are transposed, and
  marks the twenty places where the text is lost rather than supplying
  them. The English translation is original to this project. The source,
  the build pipeline, and the full record of how each segment was drafted,
  checked and reviewed live in <a href="{REPO}">the repository</a>.</p>
  <p>The translation itself is dedicated to the public domain under
  <a href="https://creativecommons.org/publicdomain/zero/1.0/">CC0</a>:
  copy it, print it, teach it, remix it, no permission needed. The notes,
  commentary, and the transcription and English of the margin are © 2026
  Chris Duffy under
  <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>.
  The images of Ross. 884 are the Vatican Library’s and are not reproduced
  here; every entry links to its page on DigiVatLib.</p>
  <p>The illustrations are AI-generated (Google Gemini) in the manner of
  Pompeian wall painting. They are modern pictures of the poem’s scenes,
  not reproductions of ancient paintings, and the cracks and wear in them
  are invented.</p>
  <p>This is the third of the project’s line-for-line translations. The
  Iliad is at <a href="https://wrath-sing-goddess.com/">wrath-sing-goddess.com</a>
  and the Odyssey at <a href="https://theclaudyssey.com/">theclaudyssey.com</a>.</p>
</section>
</div>
<div class="band"></div>
<footer>
  On the nature of things · translation <a href="https://creativecommons.org/publicdomain/zero/1.0/">CC0</a> (public domain) ·
  notes, commentary &amp; the margin © 2026 Chris Duffy, <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a> ·
  Latin source public domain
</footer>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# Stylesheet: Pompeian red ground, ochre rule and links, chalk text, the
# margin in a lighter ink, as in the manuscript.


CSS = """\
:root{
  --red:#5a1a14; --red-deep:#24090a; --chalk:#efe6d2; --ochre:#d6a64a;
  --ink:#f3dfb0;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
html,body{margin:0}
body{
  background:
    radial-gradient(ellipse at 50% 38%, rgba(0,0,0,0) 55%, rgba(10,3,3,.55) 100%),
    linear-gradient(#5a1a14, #3e1210 55%, #24090a);
  background-attachment:fixed;
  color:var(--chalk);
  font-family:"Palatino Linotype","Book Antiqua",Palatino,Georgia,serif;
  line-height:1.55; min-height:100vh;
}
a{color:var(--ochre)}
.wrap{max-width:680px; margin:0 auto; padding:0 22px}

/* the running scroll of a Second-Style frieze */
.band{height:26px; background-repeat:repeat-x; background-size:auto 26px;
  background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='40' height='26'><g fill='none' stroke='%23efe6d2' stroke-width='2.2'><path d='M0 3 H40'/><path d='M0 23 H40'/><path d='M0 18 C8 18 10 8 20 8 S32 18 40 18'/><path d='M20 8 c-4 0 -6 3 -6 5 s3 4 5 3'/></g></svg>");
  opacity:.8; margin:14px 0 0}

.site{text-align:center; margin:18px 0 0; font-size:.8rem;
  letter-spacing:.14em; text-transform:uppercase}
.site a{color:var(--chalk); opacity:.75; text-decoration:none}
.site a:hover{opacity:1; color:var(--ochre)}

.booknav{display:flex; justify-content:space-between; gap:12px;
  margin:20px 0 0; font-size:.92rem}
.booknav.bottom{margin:34px 0 8px; border-top:1px solid rgba(214,166,74,.3);
  padding-top:16px}
.booknav a{text-decoration:none}
.booknav a:hover{text-decoration:underline}
.booknav span{min-width:70px}
.booknav .mid{min-width:0}

.bookhead{text-align:center; margin:26px 0 30px}
.bookhead h1{font-weight:normal; letter-spacing:.12em; font-size:2.1rem;
  margin:0 0 .15em}
.argument{font-style:italic; opacity:.85; margin:0}

.listen{margin:-14px 0 24px; padding:10px 14px 8px; text-align:center;
  background:rgba(0,0,0,.18); border:1px solid rgba(239,230,210,.12);
  border-radius:6px}
.listen audio{width:100%; max-width:520px; display:block; margin:0 auto;
  color-scheme:dark}
.listen figcaption{font-size:.8rem; opacity:.75; margin-top:6px;
  letter-spacing:.04em}
.listen figcaption a{text-decoration:none}
.listen + .tnote{margin-top:0}
.toc .mins{font-style:normal; font-size:.78em; color:var(--ochre);
  opacity:.8; white-space:nowrap; margin-left:.4em}

.tnote{margin:-10px 0 28px; padding:0 14px; font-size:.92rem;
  background:rgba(214,166,74,.06); border:1px solid rgba(214,166,74,.25);
  border-radius:6px}
.tnote summary{cursor:pointer; padding:9px 0; color:var(--ochre);
  font-variant:small-caps; letter-spacing:.06em; list-style-position:inside}
.tnote summary:hover{text-decoration:underline}
.tnote[open] summary{border-bottom:1px solid rgba(214,166,74,.2);
  margin-bottom:6px}
.tnote p{margin:0 0 .8em; opacity:.92}
.tnote p:last-child{padding-bottom:6px}
.mg-key{font-size:.82rem; opacity:.75; margin:-14px 0 22px; font-style:italic}

/* the illustrations, at their passages */
.art{margin:14px 0 26px; text-align:center}
.verse .art{margin-left:-2.6rem}
.art img{width:100%; height:auto; border-radius:3px;
  box-shadow:0 10px 34px rgba(0,0,0,.45); border:1px solid rgba(214,166,74,.3)}
.art figcaption{font-size:.82rem; opacity:.8; margin-top:8px; font-style:italic}
.art figcaption .cite{font-style:normal; margin-left:.4em}
.art figcaption .credit{display:block; font-style:normal; font-size:.72rem;
  opacity:.65; margin-top:3px; letter-spacing:.02em}

.verse{padding-left:2.6rem}
.stanza{margin:0 0 1.15em}
.v{margin:0; position:relative; padding-left:1.4em; text-indent:-1.4em}
.lacuna{margin:.3em 0; padding-left:1.4em; font-style:italic; opacity:.5;
  font-size:.9em; letter-spacing:.1em}
.ln{position:absolute; left:-3.4rem; top:.32em; width:2.6rem;
  text-align:right; font-size:.72em; color:var(--ochre); opacity:.55;
  text-decoration:none; text-indent:0}
.ln:hover{opacity:1}
.ln.ghost{opacity:0}
.v:hover .ln.ghost{opacity:.55}
.v:hover .ln.ghost:hover{opacity:1}
@media (hover:none){.ln.ghost{display:none}}
.copied{position:absolute; z-index:9; transform:translateY(-130%);
  font-size:.7rem; font-variant:small-caps; letter-spacing:.08em;
  color:var(--ochre); background:rgba(36,9,10,.95);
  border:1px solid rgba(214,166,74,.5); border-radius:10px;
  padding:2px 9px; pointer-events:none; white-space:nowrap}
.v:target, .note:target, .mentry:target, tr:target{background:rgba(214,166,74,.14);
  border-radius:3px}
.fnref{text-decoration:none; padding:0 .08em}
.fnref sup{font-size:.68em}

/* ---- Machiavelli's margin, beside the line ----
   Folded under the line as an aside by default; set out in the right
   margin where the window is wide enough to hold a 15em column there. */
.mgs{display:block; text-indent:0; margin:.15em 0 .5em 0; font-size:.8rem;
  line-height:1.3; color:var(--ink); opacity:.9}
.mg{display:block; margin:0 0 .3em; padding-left:.9em;
  border-left:2px solid rgba(214,166,74,.45)}
.mg-lat{font-style:italic; text-decoration:none; color:var(--ink)}
.mg-lat:hover{text-decoration:underline}
.mg-lat[lang=grc]{font-style:normal}
.mg-glyph{text-decoration:none; color:var(--ochre); font-size:1.1em;
  margin-right:.5em}
.mg-en{display:block; opacity:.8; font-size:.95em}
.mg-fol{display:inline-block; font-size:.85em; letter-spacing:.04em;
  text-decoration:none; opacity:.75; font-variant:small-caps}
.mg-fol:hover{opacity:1; text-decoration:underline}
.mg-mark .mg-fol, .mg-manicule .mg-fol{display:inline}
@media (min-width:1200px){
  .wrap.margined{margin-left:max(22px, calc(50% - 460px))}
  .mgs{position:absolute; left:calc(100% + 1.4rem); top:.1em; width:15em;
    margin:0}
  .mg{border-left:0; padding-left:0; margin:0 0 .45em}
  .mg-glyph{font-size:1.25em}
}

.notes{margin-top:40px; border-top:1px solid rgba(214,166,74,.3);
  padding-top:6px}
.notes h2{font-weight:normal; font-variant:small-caps; letter-spacing:.06em;
  color:var(--ochre); font-size:1.25rem}
.note{font-size:.92rem; opacity:.92; margin:0 0 .85em;
  padding-left:1.6em; text-indent:-1.6em}
.nnum{color:var(--ochre); font-size:.8em; vertical-align:.25em}
.nline{font-variant:small-caps; text-decoration:none; white-space:nowrap}
.nline:hover{text-decoration:underline}
.back{text-decoration:none}
.cite{text-decoration:none; white-space:nowrap}
.cite:hover{text-decoration:underline}

.prose p{margin:0 0 1em}
.prose h2, .mbook h2{font-weight:normal; font-variant:small-caps;
  letter-spacing:.06em; color:var(--ochre); font-size:1.3rem;
  margin:36px 0 12px; border-bottom:1px solid rgba(214,166,74,.3);
  padding-bottom:4px}

.toc{list-style:none; margin:0; padding:0}
.toc li{margin:0 0 2px}
.toc a{display:flex; gap:14px; align-items:baseline; padding:9px 12px;
  text-decoration:none; color:var(--chalk); border-radius:5px;
  border:1px solid transparent}
.toc a:hover{background:rgba(214,166,74,.1); border-color:rgba(214,166,74,.35)}
.toc b{color:var(--ochre); font-weight:normal; letter-spacing:.06em;
  white-space:nowrap; min-width:5.4em}
.toc span{font-style:italic; opacity:.85; font-size:.95rem}

.apparatus{margin:14px 0 8px; padding:12px 14px; font-size:.95rem;
  background:rgba(214,166,74,.07); border:1px solid rgba(214,166,74,.3);
  border-radius:6px}
.toc + .apparatus{margin-top:26px}

/* ---- the margin page ---- */
.mbook h3{font-weight:normal; font-size:1.05rem; color:var(--ochre);
  margin:22px 0 10px; letter-spacing:.04em}
.mbook h3 .count{opacity:.6; font-size:.85em; margin-left:.4em}
.mentry{font-size:.92rem; margin:0 0 14px; padding:6px 10px;
  border-left:2px solid rgba(214,166,74,.35); scroll-margin-top:20px}
.mline{font-variant:small-caps; letter-spacing:.03em}
.mkind{opacity:.7; font-size:.85em; text-transform:uppercase;
  letter-spacing:.08em}
.mlat{font-style:italic; color:var(--ink)}
.mlat[lang=grc]{font-style:normal}
.mglyph{color:var(--ochre); font-size:1.15em; margin-right:.3em}
.men{opacity:.92}
.mdipl{font-size:.85em; opacity:.7}
.mrem{font-size:.85em; opacity:.7}
.fol{text-decoration:none; font-variant:small-caps; letter-spacing:.03em}
.fol:hover{text-decoration:underline}
table.copy{border-collapse:collapse; width:100%; font-size:.82rem;
  margin:0 0 14px}
table.copy th{font-weight:normal; text-align:left; color:var(--ochre);
  font-variant:small-caps; letter-spacing:.05em; padding:4px 6px;
  border-bottom:1px solid rgba(214,166,74,.35)}
table.copy td{vertical-align:top; padding:5px 6px;
  border-bottom:1px solid rgba(239,230,210,.1); scroll-margin-top:20px}
table.copy td.mline{white-space:nowrap}
table.copy td.mkind{white-space:nowrap; font-size:.8em}
@media (min-width:1200px){
  .wrap.margined .mbook{margin-right:-18em}
}

footer{text-align:center; font-size:.8rem; opacity:.7; padding:20px 0 40px}

/* ---- site search (Pagefind default UI, re-themed) ---- */
#search{margin:6px 0 22px;
  --pagefind-ui-scale:.9;
  --pagefind-ui-primary:var(--ochre);
  --pagefind-ui-text:var(--chalk);
  --pagefind-ui-background:rgba(0,0,0,.25);
  --pagefind-ui-border:rgba(214,166,74,.45);
  --pagefind-ui-tag:rgba(214,166,74,.18);
  --pagefind-ui-border-width:1px;
  --pagefind-ui-border-radius:5px;
  --pagefind-ui-font:inherit}
#search .pagefind-ui__search-input{color:var(--chalk)}
#search .pagefind-ui__search-input::placeholder{color:var(--chalk); opacity:.55}
#search .pagefind-ui__result{border-color:rgba(214,166,74,.25)}
#search .pagefind-ui__result-link{color:var(--ochre)}
#search .pagefind-ui__result-excerpt{color:var(--chalk); opacity:.9}
#search mark{background:rgba(214,166,74,.4); color:inherit; border-radius:2px}
#search .pagefind-ui__button{background:rgba(214,166,74,.1); color:var(--ochre);
  border:1px solid rgba(214,166,74,.45)}
#search .pagefind-ui__message{color:var(--chalk); opacity:.8}

@media (max-width:560px){
  .wrap{padding:0 14px}
  .verse{padding-left:2.1rem}
  .verse .art{margin-left:-2.1rem}
  .ln{left:-2.6rem; width:2rem}
  .toc b{min-width:4.6em}
  table.copy{font-size:.76rem}
}
"""


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "read.css").write_text(CSS, encoding="utf-8")
    margin = parse_margin()
    art = parse_art()
    export_art(art)
    audio = published_audio()
    print(f"margin: {len(margin)} entries, "
          f"{sum(1 for r in margin if r['reading'])} beside the verse; "
          f"art: {sum(len(v) for v in art.values())} illustrations; "
          f"audio: {len(audio)} book(s) live")
    books: dict[int, dict] = {}
    for n in range(1, 7):
        bk = parse_book(SRC / f"book_{n:02d}.txt")
        if bk["n"] != n:
            raise SystemExit(f"book_{n:02d}.txt says BOOK {bk['n']}")
        books[n] = bk
        (OUT / f"book-{n:02d}.html").write_text(
            build_book(bk, margin, art.get(n, []), audio), encoding="utf-8")
        print(f"book-{n:02d}.html")
    (OUT / "index.html").write_text(build_contents(books, margin, audio),
                                    encoding="utf-8")
    (OUT / "margin.html").write_text(build_margin(margin), encoding="utf-8")
    total, total_notes = build_api(books, margin)
    (DOCS / "index.html").write_text(
        build_landing(books, margin, total, total_notes, art), encoding="utf-8")
    print("index.html + margin.html + read.css + api/ + landing page")
    print("now refresh the search bundle:  npx -y pagefind --site docs")


if __name__ == "__main__":
    main()
