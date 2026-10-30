# Handoff: state of the work and how to resume

Written 2026-10-30 at the end of the session that drafted Books 2-6 and
reviewed Book 1; updated the same day after the Book 2 review and the Book 1
audiobook build. Read this, `README.md` and `translation/CONVENTIONS.md`
before touching anything. The manifest (`segments/manifest.json`) is the
source of truth for what has been done to each segment.

## Where things stand

| Stage | Done | Notes |
|---|---|---|
| translate (Opus) | 58/58 | every segment passes `check_segment` |
| fidelity (Sonnet) | 58/58 | findings tables in `segments/bNN/sKK.fidelity.txt` |
| annotate (Sonnet) | 58/58 | draft notes, all marked DRAFT |
| review (translator, Fable) | Books 1-2 (17/17) | `sKK.review.txt` + `sKK.patch.tsv`; Book 2: 78 lines patched |
| assemble | all six books | `translation/book_0N.txt`; Books 1-2 from review text |
| notes | none final | 302 `{{NOTE: ...}}` placeholders across the books |
| margin (Ross. 884) | Book 2 surveyed | 51 entries in `margin/marginalia.tsv` |
| audiobook | Book 1 built | `audiobook-build-book01/books/book-01-full.wav` and `-review.m4a` (untracked) |

Local repo only, no remote.

## Decisions made so far (binding unless revisited)

### Scope and form

- Complete line-for-line De Rerum Natura on the Iliad template: free verse,
  9-16 syllables (median about 13), one English line per Latin line, every
  key kept, lacunae printed as `[lacuna]` and never supplied, source order
  kept for transposed and lettered lines.
- Latin is the Perseus TEI text (Bailey OCT orthography and numbering).
  Collate against a 1922 OCT scan before publication; not yet done.
- Credits: "From the Latin of Lucretius. Translated by Claude (Fable 5.1),
  with segment drafts by Claude Opus and checks by Claude Sonnet. Edited and
  produced by Chris Duffy." The translator's review is what makes the first
  credit true: the accepted text is the review file, not the Opus draft.

### Register

Full table in `translation/CONVENTIONS.md`. The fixed points: primordia =
first-beginnings; principia = beginnings (kept distinct); corpora prima =
first bodies; semina rerum = seeds of things; inane = void; religio =
religion (never superstition); animus = mind; anima = spirit (never soul);
mens = mind, "thought" when paired with animus; simulacra = images;
clinamen and declinare = swerve; ratio = reasoning, "by what principle"
where instrumental, "order" in summa caeli ratio; simplicitas = singleness;
concilium = union; coniuncta and eventa = conjoined properties and
accidents; daedala = artificer. Refrains recur verbatim (list in
CONVENTIONS under "Refrains fixed in Book 1"). No scientific anachronism in
the verse.

### Review method (agreed with the user 2026-10-30)

- Book 1: full read of every line against the Latin. Done; 29 lines patched.
- Books 2-6: one book per session. Act on every fidelity finding, then read
  the English of each segment straight through and check about one line in
  four against the Latin, plus every refrain and set piece.
- Fixes go in `segments/bNN/sKK.patch.tsv` (key, TAB, new text), applied with
  `python tools/review.py bNNsKK segments/bNN/sKK.patch.tsv`, which writes
  the review file and records the stage. Keep `{{NOTE}}` placeholders in
  patched lines; the notes stage consumes them later.
- Read with `python tools/sidebyside.py bNNsKK [first last]`. The fidelity
  file is `segments/bNN/sKK.fidelity.txt` (FINDINGS, then SECONDARY).
- Reassemble with `python tools/assemble.py N` after a book's review.

### Pipeline

- `tools/dispatch.py` runs headless `claude -p` with ANTHROPIC_API_KEY
  stripped (bills the subscription), no built-in tools and an empty MCP
  config (`--tools "" --strict-mcp-config --mcp-config tools/no_mcp.json`).
  Without that the model sometimes reached for a tool and the one-turn limit
  returned empty output. Safe to run several processes at once; manifest
  writes are locked and retried.
- Observed: Opus translate 60-120 s a segment, Sonnet fidelity 20-45 s,
  annotate about 25 s. Drafting all of Books 2-6 used a small fraction of
  the five-hour window.

### Machiavelli's margin

- Source: Vatican MS Ross. 884 on DigiVatLib. Page images are for personal
  study only; `margin/images/` is gitignored and never published. The
  published layer will carry transcriptions plus folio links only.
- Folio to canvas: recto NNr = canvas NN+11, verso NNv = canvas NN+12.
  Lucretius fols. 1r-133v; Terence, Eunuchus, 134r-153v; subscription
  "Finis. Nicolaus Maclavellus scripsit foeliciter" on 133v.
- Book 2 survey complete: all 16 items in Brown's list (The Return of
  Lucretius to Renaissance Florence, 2010, ch. 4 nn. 15-20) confirmed; her
  lemma for "variam esse figuram principiorum" corrected to 2.340-341 (the
  bracketed Latin is "Debent nimirum non omnibus omnia prorsum / esse pari
  filo similique affecta figura"; an earlier entry said 2.347-348); four
  verbal notes she does not list (2.62, 2.184-185, 2.217-219, 2.333);
  variants, order marks, supplied line ends and the catchword recorded.
  Brown's PDF is in the user's Downloads folder (copyrighted; consult it,
  never copy it into the repo).
- Books 1 and 3-6 not yet surveyed.

## Book 2 review (done 2026-10-30)

78 lines patched across the nine segments; the patch files carry the
reasons as `#` comments, including the three Sonnet findings rejected
(2.714, the consensus reading of Bailey, Munro and Rouse; 2.1093; 2.1104,
tmesis). Register points settled: principia = beginnings was enforced in
fourteen lines where Opus had "first-beginnings"; exordia = origins (2.333);
mobilitas = mobility; conciliatus = union. Refrains made verbatim with Book 1
and inside Book 2 are listed in `translation/CONVENTIONS.md` under "Refrains
fixed in Book 2". A new tool, `python tools/refrains.py N [--earlier]`, lists
every repeated Latin line of Book N with the current English of each
occurrence; run it before each review.

## Starting Book 3 (next session)

1. Open the repo, check `git log`, run `python tools/check_segment.py --all`
   (exit 1 is expected until the reviews reach b03s08 and b06s03, whose Opus
   drafts fall under the 80% syllable-band floor) and
   `python tools/refrains.py 3 --earlier`.
2. Book 3 is segments b03s00 to b03s08 (3.1-1094; bounds 1-135, 136-261,
   262-380, 381-547, 548-669, 670-818, 819-930, 931-1052, 1053-1094). Sonnet
   found no firm FINDINGS in Book 3; eleven secondaries across the book (s00
   1, s02 1, s03 1, s04 3, s05 1, s06 1, s07 2, s08 1). Weigh each.
3. Refrains to make verbatim against the accepted text: 3.87-90 = 2.55-58
   (3.87 "fear everything", 3.90 "what children in the dark shudder at and
   imagine will come."); 3.91-93 = 1.146-148 (already matches); 3.519-520 =
   1.670-671 ("for whatever is changed and passes out of its own bounds, /
   this at once is the death of what it was before."); 3.62 keeps "night and
   day with surpassing labor" (2.12) in its infinitive.
4. Register points in Book 3: animus = mind and anima = spirit is the book's
   whole subject; the first technical contrast (3.94 ff., 3.136 ff.) gets the
   note promised in CONVENTIONS; mens = "mind", "thought" only when paired
   with animus. Sweep principia = beginnings (not "first-beginnings") with a
   script as was done for Book 2, since Opus slips on it. The proem (3.1-30)
   and the diatribe against the fear of death (3.830-1094) are set pieces;
   read them in full.
5. Patch, `python tools/review.py b03sKK segments/b03/sKK.patch.tsv`,
   `python tools/assemble.py 3`, commit with the usual identity (user.name
   spinchange, user.email spinchange@users.noreply.github.com,
   core.safecrlf=false), message ending with the Claude co-author line.
6. Update `translation/CONVENTIONS.md` with any new fixed terms and the table
   at the top of this file.

## After the reviews

- Notes stage per book: resolve the `{{NOTE}}` placeholders and Sonnet's
  DRAFT notes into numbered notes `[1]`, `[2]` in the Iliad format; write the
  argument lines and commentary.
- Margin survey of Books 1 and 3-6; decide the published layout (verse with
  Machiavelli's notes keyed to lines, DigiVatLib folio links).
- OCT collation; then the web build on the Iliad and Odyssey pattern.
