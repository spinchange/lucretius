# Handoff: state of the work and how to resume

Written 2026-10-30 at the end of the session that drafted Books 2-6 and
reviewed Book 1. Read this, `README.md` and `translation/CONVENTIONS.md`
before touching anything. The manifest (`segments/manifest.json`) is the
source of truth for what has been done to each segment.

## Where things stand

| Stage | Done | Notes |
|---|---|---|
| translate (Opus) | 58/58 | every segment passes `check_segment` |
| fidelity (Sonnet) | 58/58 | findings tables in `segments/bNN/sKK.fidelity.txt` |
| annotate (Sonnet) | 58/58 | draft notes, all marked DRAFT |
| review (translator, Fable) | Book 1 only (8/8) | `sKK.review.txt` + `sKK.patch.tsv` |
| assemble | all six books | `translation/book_0N.txt`, header says DRAFT |
| notes | none final | 302 `{{NOTE: ...}}` placeholders across the books |
| margin (Ross. 884) | Book 2 surveyed | 51 entries in `margin/marginalia.tsv` |

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
  lemma for "variam esse figuram principiorum" corrected to 2.347-348; four
  verbal notes she does not list (2.62, 2.184-185, 2.217-219, 2.333);
  variants, order marks, supplied line ends and the catchword recorded.
  Brown's PDF is in the user's Downloads folder (copyrighted; consult it,
  never copy it into the repo).
- Books 1 and 3-6 not yet surveyed.

## Starting Book 2 (next session)

1. Open the repo at `H:\My Drive\agent-journal\lucretius`, check `git log`,
   and run `python tools/check_segment.py --all` (should be clean).
2. Book 2 is segments b02s00 to b02s08 (2.1-1174). Firm fidelity findings
   to act on: 2.714 in b02s04 ("caecis corporibus ... percita plagis": the
   unseen bodies strike, they do not flee) and 2.1104 in b02s07. The 2.1104
   finding is WRONG: "indignos inque merentes" is tmesis for "immerentes",
   both words mean undeserving, so Opus's "the unworthy and the undeserving"
   stands. Ten secondaries across the book; weigh each.
3. Refrains to make verbatim against Book 1's accepted text: 2.59-61 =
   1.146-148 (the proem sample); 2.753-754 = 1.670-671; "dias in luminis
   oras" at 2.577 is the variant "visentis luminis oras", so "the shores of
   light" without "shining", as the draft has it. The Book 2 proem ("suave
   mari magno") is a set piece; read it in full.
4. Register points in Book 2: the swerve passage 2.216-293 (swerve for both
   noun and verb). Lines carrying Machiavelli's notes should read well on
   their own, since they will be quoted beside his words: 2.62, 2.184-185,
   2.217-219, 2.333 and the 16 Brown items (exact lines in
   `margin/marginalia.tsv`).
5. Patch, review, `python tools/assemble.py 2`, commit with the usual
   identity (user.name spinchange, user.email
   spinchange@users.noreply.github.com, core.safecrlf=false), message ending
   with the Claude co-author line.
6. Update `translation/CONVENTIONS.md` with any new fixed terms, and the
   table at the top of this file.

## After the reviews

- Notes stage per book: resolve the `{{NOTE}}` placeholders and Sonnet's
  DRAFT notes into numbered notes `[1]`, `[2]` in the Iliad format; write the
  argument lines and commentary.
- Margin survey of Books 1 and 3-6; decide the published layout (verse with
  Machiavelli's notes keyed to lines, DigiVatLib folio links).
- OCT collation; then the web build on the Iliad and Odyssey pattern.
