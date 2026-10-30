# Handoff: state of the work and how to resume

Written 2026-10-30 at the end of the session that drafted Books 2-6 and
reviewed Book 1; updated the same day after the Book 2 review, the Book 1
audiobook build, the Book 3 review, and the Book 4 review. Read this, `README.md` and `translation/CONVENTIONS.md`
before touching anything. The manifest (`segments/manifest.json`) is the
source of truth for what has been done to each segment.

## Where things stand

| Stage | Done | Notes |
|---|---|---|
| translate (Opus) | 58/58 | every segment passes `check_segment` |
| fidelity (Sonnet) | 58/58 | findings tables in `segments/bNN/sKK.fidelity.txt` |
| annotate (Sonnet) | 58/58 | draft notes, all marked DRAFT |
| review (translator, Fable) | Books 1-4 (36/36) | `sKK.review.txt` + `sKK.patch.tsv`; Book 2: 78 lines, Book 3: 89, Book 4: 92 lines patched |
| assemble | all six books | `translation/book_0N.txt`; Books 1-4 from review text |
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

## Book 3 review (done 2026-10-30)

89 lines patched across the nine segments; reasons are `#` comments in the
patch files. Sonnet's eleven secondaries: five accepted (3.345, 3.513, 3.553,
3.803, 3.843), six rejected with the consensus of Bailey, Munro and Smith
(3.121 eadem = vita; 3.592 intra finis vitae; 3.662 the fore part seeks
itself; 3.969 ante adverbial; 3.1038 unus = alone, eadem with quiete; 3.1084
hiantis with the understood nos). One outright error found on the full read:
3.897, where praesidium governs factis florentibus tuisque (the dead man can
no longer guard his affairs and his own; Opus had him "flourishing"). Also
3.868 (nullo tempore = never born) and 3.1040 (memores motus = the
remembering motions). Register: exordia = origins enforced at 3.31 and
3.380; principia = beginnings was already right throughout; "particles"
removed at 3.708; the two em-dashes in the Opus draft removed. Refrains
3.87-90 and 3.519-520 made verbatim. b03s08 now passes the syllable-band
check (93%); only b06s03 still fails.

Source-text artifacts seen in `latin/` for Book 3, for the OCT collation:
the Perseus text prints doubled forms where the TEI marks a diaeresis
(3.233 "aeraaëra", 3.234, 3.236, 3.248, 3.269, 3.282, 3.287, 3.292, 3.302,
3.443, 3.456, 3.508, 3.571, 3.573, 3.591, 3.691 "aenamquenamque", 3.694
"asperaeasperë", 3.752, 3.980) and two garbled words (3.396
"coercenscoërcens", 3.433 "gerunturaegeruntur"). The English reads the
plain word in each case; the Latin files have not been touched.

## Book 4 review (done 2026-10-30)

Book 4 is ten segments, b04s00 to b04s09 (4.1-1287), not twelve as an
earlier version of this file said. 92 lines patched; reasons are `#`
comments in the patch files. Sonnet's five findings all accepted (4.127-128
cassa sensu = void of sense; 4.579 the hills repeated the sayings as they
returned; 4.1190 animus = mind; 4.1266 the seeds take their places; and the
4.35 register point). Secondaries: 4.219 (aestus = surge), 4.471 (the case,
not "my case") and 4.1088 (totum adverbial) accepted; 4.412 (many thousands
of lands, with Bailey, Munro and Rouse) and 4.591 (loca is the object of
tenere, the neighbors the subject of putentur) rejected. Errors found on the
full read: 4.1215-1216, where mutuus ardor is the subject and semina the
object of conflixit (Opus had the seeds dashing); 4.511 omnis with copia;
4.879 insuerit. Register: principia = beginnings enforced at 4.667, 4.699,
4.943; exordia = origins at 4.26 and 4.114; particulae = small part / tiny
parts at 4.261 and 4.776 ("particles" barred); nervi = sinews at 4.1043 and
4.1115; pari ratione = on a like principle at 4.395. Refrains: 4.1-23 taken
verbatim from the Book 1 review text, 4.26-28 from Book 3, 4.207 from Book
2; the eight repeats inside Book 4 are verbatim (list in CONVENTIONS under
"Refrains fixed in Book 4"). The two 20-syllable outliers (4.535, 4.1246)
and about thirty 17-19-syllable lines were brought into the band; every
Book 4 segment is now at 90% or better. Only b06s03 still fails the check.
The obscene passage (4.1030-1287) was read in full; the Opus draft already
kept the plain register and nothing there needed more than the fixes above.

Source-text artifacts seen in `latin/` for Book 4, for the OCT collation:
doubled diaeresis forms at 4.136, 4.187, 4.198, 4.247, 4.251, 4.274-275,
4.277, 4.281, 4.286, 4.291, 4.303, 4.327, 4.338, 4.340, 4.342, 4.345,
4.349, 4.358, 4.359, 4.366, 4.369, 4.558, 4.619, 4.647, 4.657, 4.693, 4.736,
4.846, 4.892, 4.933, 4.937, 4.954; "corum" for eorum at 4.116; "ainesse"
at 4.823 (the vehementer inesse crux). The English reads the plain word.

## Starting Book 5 (next session)

1. Open the repo, check `git log`, run `python tools/check_segment.py --all`
   (exit 1 is expected until the review reaches b06s03) and
   `python tools/refrains.py 5 --earlier`.
2. Book 5 is twelve segments, b05s00 to b05s11 (5.1-1457). Read the fidelity
   files first; weigh every finding and secondary.
3. Refrains to take from earlier review text: 5.196-197 = 2.178-179;
   5.224 and 5.781 "the shining shores of light"; 5.234 natura daedala rerum
   = "nature, artificer of things"; 5.351-363 = 3.806-818 (take the Book 3
   text where identical); 5.430-431 = 2.1062-1063; 5.441 = 2.726; 5.882 =
   4.53; 5.1385 = 4.585. Run the refrains tool for the rest.
4. Register points in Book 5: no scientific anachronism in the cosmogony
   and the history of civilization (no "evolution", no "atoms"); mundus =
   world; sweep principia = beginnings and exordia = origins (5.430) with the
   script as before; check "particles", "nerves", "soul", "superstition".
5. Patch, `python tools/review.py b05sKK segments/b05/sKK.patch.tsv`,
   `python tools/assemble.py 5`, commit with the usual identity (user.name
   spinchange, user.email spinchange@users.noreply.github.com,
   core.safecrlf=false), message ending with the Claude co-author line.
6. Update `translation/CONVENTIONS.md` with any new fixed terms and the table
   at the top of this file.

Uncommitted at the end of the Book 4 session, from the audiobook thread and
not part of the review: `audiobook/production-onyx.json`,
`tools/build_audiobook.py` (modified) and `audiobook-source/book_02.txt`
(new). Left for the user to commit with the Book 2 audiobook build.

## After the reviews

- Notes stage per book: resolve the `{{NOTE}}` placeholders and Sonnet's
  DRAFT notes into numbered notes `[1]`, `[2]` in the Iliad format; write the
  argument lines and commentary.
- Margin survey of Books 1 and 3-6; decide the published layout (verse with
  Machiavelli's notes keyed to lines, DigiVatLib folio links).
- OCT collation; then the web build on the Iliad and Odyssey pattern.
