# Handoff: state of the work and how to resume

Written 2026-10-30 at the end of the session that drafted Books 2-6 and
reviewed Book 1; updated the same day after the Book 2 review, the Book 1
audiobook build, the Book 3 review, the Book 4 review, the Book 5 review
and the Book 6 review. Read this, `README.md` and `translation/CONVENTIONS.md`
before touching anything. The manifest (`segments/manifest.json`) is the
source of truth for what has been done to each segment.

## Where things stand

| Stage | Done | Notes |
|---|---|---|
| translate (Opus) | 58/58 | drafts; the accepted text is the review file |
| fidelity (Sonnet) | 58/58 | findings tables in `segments/bNN/sKK.fidelity.txt` |
| annotate (Sonnet) | 58/58 | draft notes, all marked DRAFT |
| review (translator, Fable) | 58/58 (all six books) | `sKK.review.txt` + `sKK.patch.tsv`; Book 2: 78 lines, Book 3: 89, Book 4: 92, Book 5: 206, Book 6: 206 lines patched |
| gloss (Opus, second independent fidelity pass) | 58/58 on the review text and 58/58 on the Opus drafts | `sKK.gloss.txt`, `sKK.gloss-draft.txt`; the draft run calibrates the checker (it catches what the first pass caught) and its findings on lines the first review left unchanged were all adjudicated |
| review2 (translator, Fable; every line of every book read against the Latin) | 58/58 | `sKK.patch2.tsv` with a reason per change; 149 verse lines changed (12/23/26/36/28/24 by book) |
| assemble | all six books | `translation/book_0N.txt`, all from review text; `check_segment --all` now exits 0 |
| notes | all six books final (76, 89, 70, 55, 89, 86 notes) | no `{{NOTE: ...}}` placeholders or DRAFT notes remain; verse unchanged, `check_narration --all` matches |
| margin (Ross. 884) | all six books surveyed | 229 entries in `margin/marginalia.tsv` (27 each for Books 1 and 3, 39 for Book 4, 39 for Book 5, 46 for Book 6, 2026-10-31) |
| audiobook | all six books built | `audiobook-build-book0N/books/book-0N-full.wav` and `-review.m4a` (untracked); every chunk accepted on a strict QA pass except the four noted under "Audiobook" below |

Local repo only, no remote.

## Decisions made so far (binding unless revisited)

### Scope and form

- Complete line-for-line De Rerum Natura on the Iliad template: free verse,
  9-16 syllables (median about 13), one English line per Latin line, every
  key kept, lacunae printed as `[lacuna]` and never supplied, source order
  kept for transposed and lettered lines.
- Latin is the Perseus TEI text (standard Munro/Bailey numbering; its orthography and some readings follow Munro rather than Bailey's OCT, see latin/SOURCE.md).
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
- Second round (done 2026-10-30 for all six books): `python tools/dispatch.py
  --stage gloss` runs the Opus clause-by-clause check (`prompts/gloss.md`)
  on the review text, `--stage gloss-draft` on the Opus drafts. The
  translator then read every line of Books 2-6 against the Latin with the
  gloss findings in hand (Book 1 had been read in full already). Fixes go in
  `sKK.patch2.tsv` (comment lines give the reason), applied with
  `python tools/review.py bNNsKK segments/bNN/sKK.patch2.tsv --round 2`,
  which takes the review file as its base and records `review2`. A patch
  line replaces the whole line, so a note-bearing line must carry its
  `{{NOTE: ...}}` in the patch. After a book: `python tools/reassemble_verse.py N`
  (verse lines only; the book file keeps its final notes), `make_narration.py N`,
  `check_narration.py --all`, `check_segment.py --all`, then
  `python tools/refresh_chunks.py N --apply` for the audio (below).

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
- Book 1 survey complete (2026-10-31, canvases 12-32): 27 entries. Two
  verbal notes only (the Greek ὁμοιομέρειαν at 1.830 in the lighter ink,
  and "Comp̄" = Comparatio against the wormwood simile 1.936-942); the
  rest are marks (1.7, 1.774, 1.780, 1.1055, the crosses at 1.1092 and
  1.1102 flanking the great lacuna, order marks at 1.1060-1061, a variant
  at 1.1093), the omission of 1.305, the eye-skip of 1.585-588 repaired in
  the margin with two manicules as tie-marks, and fourteen scribal
  corrections. Brown lists nothing for Book 1. Details in margin/README.md.
- Book 3 survey complete (2026-10-31, canvases 53-73, fols. 41v-61v): 27
  entries. No verbal note; three marginal words in the lighter ink (diu
  supplied at 3.419, torrari at 3.661, "( particip/or" at 3.692); the
  book's mark is the right-margin dash, fourteen of them, thickest over
  the mortality proofs (566-614) and the consolation (866-898, 1026-1044,
  two flanking the death of Epicurus at 1042-1044); eleven scribal
  corrections; Book 3 ends on 61v with the rubric for Book 4. Details in
  margin/README.md.
- Book 4 survey complete (2026-10-31, canvases 73-96, fols. 61v-84v): 39
  entries. One verbal note, "( ÿ de gallo" at 4.710 (74r); the marginal
  word "( ordia" at 4.35 (62r, not 4.28); two whole lines supplied in the
  margin in the lighter ink (174-175 beside 128 on 64r, 1034 on 80r) and
  three words (protelo 190, hostem 1051, stinguere possit 1098); sixteen
  right-margin dashes, five of them on 65r (180-199), one at 1233 on the
  gods and fertility; a cross at 672; omissions at 568-570 and 1249-1250
  (eye-skips); the copy keeps the manuscripts' line order at 32-39,
  302-323 and 542-543; an unexplained extra line after 102. Book 4 ends on
  84v with the rubric for Book 5. Details in margin/README.md.
- Book 5 survey complete (2026-10-31, canvases 96-122, fols. 84v-110v): 39
  entries. No verbal note; one marginal word, "( metutum" at 5.1140 (105r);
  five right-margin dashes (102, 321, 909, 938, 1296) and four dotted lines
  at 1096-1100 (fire from rubbing branches); an "H" in the margin at 499;
  the exemplar's two-line form of 5.26 placed after 31, and the 571/574
  doublet placed before and after 570; twenty-six scribal corrections, the
  copy's "puer adhuc" at 884 among them; no line missing. Book 5 ends on
  110v with a small colophon and the rubric for Book 6. Details in
  margin/README.md.
- Book 6 (done 2026-10-31, fols. 110v-133v): 46 entries. Thirteen marginal
  words in the lighter ink (frit 364, rehalat 523, geli duramen 530, derupta
  539, subcudit 551, gleba 553, minant 563, pelagu 619, ningues 736,
  permanater 916, inanitur vacefit 1005-1006, cibatus 1127, expers somno
  1181); two Greek glosses (πρηστηρ 424, ετησιαι 716); 625-628 supplied
  vertically in the margin of 121v; dashes at 105, 534, 1075-1077; a dot at
  1194; the exemplar's order at 48-51, 1174, 1282-1286; twenty scribal
  corrections. The subscription "Nicolaus Maclavellus scripsit foeliciter" on
  133v is struck through by one stroke; "Finis Τελος" above it is not.
  Terence follows on 134r. Images on disk through canvas 146. Details in
  margin/README.md.

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

## Book 5 review (done 2026-10-30)

Book 5 is twelve segments, b05s00 to b05s11 (5.1-1457). 206 lines patched;
reasons are `#` comments in the patch files. About two thirds of the patches
are band work: the Opus draft of Book 5 ran long (roughly ninety lines of
17-22 syllables, and a few of 6-8), and every segment is now at 97% or
better. Sonnet's two findings both accepted: 5.53, where the draft had
translated an emendation (immortalibus) instead of the printed "iam
mortalibus e divis" (the English now follows the printed text, with a note
on the other reading); 5.1409, genus is the subject of didicere. Secondaries:
5.72 (vesci = make use of), 5.349 (inter nos = among ourselves), 5.372
(parallel to exspargi), 5.709 and 5.754 (eius, ei = the sun, named), 5.1095
(caeli plaga = a quarter of the sky), 5.1209 (fear clause), 5.1239
(relinquunt = consign), 5.1386 (reperta passive), 5.1408 (vigiles = the
wakeful) accepted; 5.58 rejected (aevum has no single fixed rendering and
"time" is the sense of aevi leges). Found on the full read: 5.31 Thracia
locative; 5.186 species creandi = a likeness of creation; 5.1031 infantia
linguae = the tongue's own infancy; 5.1302-1304 rebalanced so Poeni stays in
its line; 5.1344-1346 recast (ante ... quam = before it happened). Register:
aetherius sol = the sun in the ether (5.215, 5.267, 5.281, 5.389); caeli
rationes = the order of heaven (5.196, 5.1183) and ratio solis = the order of
the sun (5.614); pari / simili ratione = on a like principle (5.643, 5.910);
mobilitas = mobility (5.858); "the shores of light" where the Latin lacks
dias (5.224, 5.781, 5.1389, 5.1455). No scientific anachronism was found in
the cosmogony or the history of civilization; no "particles", "nerves",
"soul", "superstition" or dashes. Refrains: the full list is in
`translation/CONVENTIONS.md` under "Refrains fixed in Book 5"; the main
borrowings are 5.111-112 from Book 1, 5.128-140 and 5.351-363 from Book 3,
5.196-199 from Book 2, 5.419-421 from Book 1, 5.882 and 5.1385 from Book 4.
Only b06s03 still fails the syllable-band check.

Source-text artifacts seen in `latin/` for Book 5, for the OCT collation:
doubled diaeresis forms at 5.254, 5.273, 5.276, 5.278, 5.434, 5.490, 5.498,
5.501-502, 5.511, 5.522, 5.538, 5.553, 5.562, 5.580, 5.605-606, 5.637,
5.645, 5.653, 5.696, 5.825; "poetaepoëtae" at 5.327, 5.405, 5.1444;
"suessesuësse" at 5.912; "coegitcoëgit" at 5.1354; "tutaTA" at 5.859;
"patebant" for petebant at 5.1319. The English reads the plain word.

## Book 6 review (done 2026-10-30)

Book 6 is ten segments, b06s00 to b06s09 (6.1-1286). 206 lines patched;
reasons are `#` comments in the patch files. Sonnet found nothing at the
FINDINGS level in any segment; of the eight secondaries, seven accepted
(6.90 caeli divisis partibus, an ablative absolute, the augurs' division of
the sky; 6.130 anima = air, noted; 6.296 maturo culmine = ripe at its crest;
6.377 ancipiti bello = a two-fronted war; 6.598 natura is the subject of
dissoluat and dispandat; 6.973 amaracinum unguentum = marjoram oil; 6.1012
quod dicitur esse alienum, a relative clause) and one rejected (6.30-31:
naturali is ablative and agrees with both casu and vi, so "natural chance or
force" keeps it, with Bailey). Found on the full read: 6.1121-1122, where
repit, conturbat and coactat are singular, the hostile air creeping like
mist and cloud (Opus had the mist and cloud as subject); 6.16 plural (the
men of 6.12 are the subject of cogi); 6.292 revocare ad diluviem = bring
back the flood; 6.753-754 non iras Palladis pervigili causa, the crows do
not flee Pallas's anger at their watching; 6.762-764 reordered as the Latin
runs; 6.794 the woman is the subject of recumbit; 6.1225 certabant = vied.
Register: mobilitas = mobility enforced at 6.486 (Opus had "speed"), mobilis
= mobile at 6.204; consimili / pari ratione = on a like principle at 6.506,
6.881, 6.902, 6.1131; ratio quae sit = what the principle is (6.535, 6.639,
6.861, 6.1090), est ratio ut = there is a way (6.132); lapis Magnes kept as
the Greek name at 6.908 (the English "magnet" only in the notes), with "this
Magnesian stone" at 6.1046; anima = air or breath in the meteorology,
noted at 6.130, 6.578, 6.693, and spirit in the plague. No scientific
anachronism in the meteorology, the magnet or the plague: no "electricity",
"magnetism", "bacteria", "infection", "particles", "nerves", "soul",
"superstition" or dashes in the verse (the DRAFT notes mention some of these
words to rule them out). Refrains: the full list is in
`translation/CONVENTIONS.md` under "Refrains fixed in Book 6"; the main
borrowings are 6.35-41 from Books 2 and 1, 6.60-61 and 6.94-95 from Book 1,
6.62-70 from Book 5, 6.635-638 from Book 5, 6.924-935 from Book 4, and
6.91-93 = 6.383-385 inside the book. Band: Book 6 was the loosest draft
(b06s03 at 80%, b06s06 at 84%, fifteen 20-21-syllable lines); every segment
is now at 97% or better and `python tools/check_segment.py --all` exits 0
for the first time. Two Book 4 refrain lines that run to 17-19 syllables
(6.928, 6.932) and three 17-18-syllable lines in b06s07-s08 (6.881, 6.1000,
6.1131) were left.

Source-text artifacts seen in `latin/` for Book 6, for the OCT collation:
doubled diaeresis forms of aer at 6.250, 6.304, 6.346, 6.367, 6.444, 6.684,
6.685, 6.831, 6.1003, 6.1024, 6.1027, 6.1028, 6.1035, 6.1037, 6.1097,
6.1118, 6.1120, 6.1128, 6.1142, 6.1227; "poetaepoetae" at 6.754;
"suevitsuevit" at 6.953; "coercetcoercet" at 6.954 (the second form carries
the diaeresis). The English reads the plain word; the notes at 6.250 and
6.684 say so and the notes stage can drop them.

## Notes stage (started 2026-10-30)

All six books are done (2026-10-30, one commit per book): each
`translation/book_0N.txt` now has the argument, the translator's
commentary, `[n]` markers in the verse and numbered notes in the Iliad
format (each opening with its (book.line)); 76, 89, 70, 55, 89 and 86 notes
for Books 1 to 6. Method: the
`{{NOTE}}` placeholders and Sonnet's DRAFT notes were read against the verse
and the Latin, merged where they duplicated each other, dropped where they
only restated the register or paraphrased the argument, and rewritten; a
spec file (ARGUMENT / COMMENTARY / NOTES with `@key | anchor` heads) was
applied with the new one-shot `python tools/apply_notes.py N spec.txt`, which
strips every placeholder, inserts the markers and refuses to run on a book
whose notes are already final. `python tools/check_narration.py N` (or
`--all`) strips markers and placeholders the way make_narration.py does and
diffs the verse against `audiobook-source/book_0N.txt` without writing
anything; it must report a match after every notes commit while the audio is
rendering. The verse wording was not touched.

### Lines to fix after the audio builds

Done in the second round (2026-10-30): every item below was fixed in the
review files (1.170, 1.179, 2.833, 4.771/4.800 now agree, 4.1034, 5.1436
"the wakeful", 5.1401 "out of measure", 5.1453), or confirmed as a decision
(6.750). The list is kept as the record of what was found during the audio
builds.

- 1.170 and 1.179: the English has "the shining shores of light" where the
  Latin (oras in luminis exit; in luminis oras) lacks dias. The register's
  rule, applied in Books 2 and 5 (2.577, 5.224, 5.781, 5.1389, 5.1455), is
  "the shores of light" without "shining" where dias is absent; note [4] at
  1.22 states that rule. Proposed fix: drop "shining" in both lines (13 and
  14 syllables after the change). The user decides; the alternative is to
  amend the register to treat 1.170 and 1.179 as the full refrain.
- 2.833 "by the particles before they part into the seeds of things":
  "particles" was barred by the register in the Book 3 review (particulae =
  tiny parts, small pieces; 3.665, 3.708, 4.261, 4.776), but the Book 2
  review predates that rule and left it. Proposed fix: "by the small pieces
  before they part into the seeds of things" (13 syllables). Note [69] at
  2.833 is written so that it stays true either way.
- 4.771-772 "born after / in another posture" against 4.800-801 "born after
  it / in another posture": the Latin of the two pairs is identical except
  for the first word, so the English should match (drop or add "it").
- 4.1034 "parts swollen with much seed" against 4.1047 "places swollen with
  much seed": loca both times; make the two lines agree.
- 5.1436 "the watchmen" (vigiles mundi) against 5.1405 and 5.1408 "the
  wakeful" (vigiles, vigilantibus): Lucretius uses one word for the
  shepherds and for the sun and moon, and the echo is lost; note [84] at
  5.1436 points it out. Proposed fix: "But the wakeful of the world,
  traversing its great revolving precinct" or similar.
- 5.1401 "to step out of time" against 5.1409 "to keep the measure": numerum
  both times, a deliberate pair in the Latin; consider "out of measure" at
  1401.
- 5.1452-1453 "the experience of the unflagging mind, / taught little by
  little as men advanced step by step": progredientis agrees with mentis,
  so it is the mind that advances step by step, not men. Minor.
- 6.750 "the temple of kindly Pallas Tritonis": templum here is the
  building on the Acropolis, and "temple" was kept as the one exception
  to the "precincts" rule; the Book 6 commentary says so. No change
  proposed; listed so the exception is a decision and not an oversight.

## Next session

The second-round review is complete and committed. Before anything else, run
`git log`, `python tools/check_segment.py --all` (expect 58 segment lines and
exit 0) and `python tools/check_narration.py --all` (expect every book to
match). Then:

1. Audio: done. The second-round re-render finished 2026-10-31 (86 chunks
   re-rendered across the six books, every chunk accepted, all six masters
   and review mixes rebuilt; see "Audiobook"). Nothing pending.
2. Margin survey: done for all six books 2026-10-31. Decide the published layout.
3. Web build on the Iliad and Odyssey pattern.

## Audiobook (built 2026-10-30, re-rendered for the second round 2026-10-31)

Second-round re-render: `python tools/refresh_chunks.py N --apply` re-chunked
every changed line in place (old takes marked superseded, chunk reopened),
then `bash tools/resume_rerender.sh N` synthesized, QA'd and auto-accepted
(a copy lives in runs/; the script loads `runs/openai.env` if present, else
the user-level OPENAI_API_KEY from the registry, so a key changed mid-session
is picked up without restarting). Re-rendered chunks: Book 1, 9; Book 2, 11;
Book 3, 15; Book 4, 17; Book 5, 18; Book 6, 16. Chunks hand-accepted on a
strict review because every difference was a transcriber slip (homophones,
plurals, spellings, proper names, and the known bleating/Cecrops priming):
1.025, 2.012, 3.005, 3.006, 3.020, 4.026, 6.026. Lengths now 62.2, 64.8,
62.3, 73.4, 81.4, 74.1 minutes.

Pitfall found and fixed by hand: `qa` overwrites a candidate's status, so a
take marked superseded by refresh_chunks that is QA'd again comes back as
pass or fail and could be auto-accepted although its audio reads the old
text. Audit after any re-render: every accepted candidate's
`tts_text_sha256` must equal its chunk's `tts_sha256` (Book 1 chunk 003 is
the one legitimate exception: its accepted take 004 was made with a
pronunciation respelling in the first build). The audit found two such
takes in Book 2 and two in Book 3 and re-marked them; none had been accepted.


All six books rendered with `audiobook/production-onyx.json` (gpt-4o-mini-tts,
onyx, 0.95) through the gated pipeline: prepare, synthesize, qa, accept,
concat, review. Narration sources are `audiobook-source/book_0N.txt` from
`python tools/make_narration.py N`. Build output is untracked under
`audiobook-build-book0N/`; the manifest there records every take, its
transcript metrics and the acceptance reason.

| Book | Chunks | Length | Retaken chunks | Accepted without a strict pass |
|---|---|---|---|---|
| 1 | 25 | 62.1 min | 3, 12, 19, 21 | 012 (`take in` heard as taken) |
| 2 | 26 | 64.9 min | 10, 12, 16, 21, 22, 23 | none |
| 3 | 24 | 62.0 min | 5, 8, 17, 18, 19, 20 | 020 (`laid asleep` heard as lay to sleep) |
| 4 | 29 | 72.5 min | 4, 6, 10, 11, 12, 15, 16 | 012 (`already` heard as all ready) |
| 5 | 32 | 82.1 min | 3, 25 | none |
| 6 | 29 | 73.4 min | 1, 10, 11, 15, 26, 27 | none |

Flagged for listening on the review masters: 1.534 and 1.117-124 (Book 1,
see its manifest); 3.876-918 (`laid asleep`); 4.507-552 (`already`,
Daulian); 6.1131-1177 (`bleating flocks`, Cecrops: all five takes transcribe
them as bleeding and sea crops, which looks like the transcriber primed by
the plague context; the accepted take is a strict pass). Book 6 chunk 001
ends at the lacuna after 6.47; the first take invented nine words to finish
the broken sentence, the accepted retake stops at "the glorious chariot".

Pipeline notes: `parse_translation` keeps a single transposed line in
sequence (2.680 after 2.659) instead of cutting it into its own chunk.
Pronunciation notes for Books 2-6 names are in the config; `verify` on the
Book 1-2 builds now reports a config-hash change for that reason alone.
Transcription QA calls can drop on a transient TLS error and leave a take
`unreviewed`; rerun `qa --chunks NNN`.

## After the reviews

- Notes stage per book: done for all six books (2026-10-30); see "Notes
  stage" above.
- Margin survey done for all six books; decide the published layout (verse with
  Machiavelli's notes keyed to lines, DigiVatLib folio links).
- OCT collation: done 2026-10-30 against an OCR of Bailey's 1922 text
  (scratch alignment script, monotone fuzzy match, reports kept out of the
  repo). Result: the Perseus text is not Bailey's. Orthography is Munro's
  (divom, volgo, inritat, haut, quicque, nihil), and after orthographic
  variants are filtered about 650 word-level differences remain across the
  six books, nearly all editorial readings (1.263 alit/alid, 1.276
  pontus/ventus, 1.404 ferai/ferarum, 1.492 cum/tum, 1.721 Aeoliae/Italiae,
  1.777, 1.843, 4.547, 6.956 and so on), not transcription errors. The
  source-edition claims were corrected (latin/SOURCE.md, README, Book 1
  commentary, this file), and the two notes that misstated Bailey's reading
  (4.547, 6.956) were fixed from his apparatus. The Munro 1886 OCR was
  downloaded but the alignment produced nothing usable against it; not
  pursued.
- Then the web build on the Iliad and Odyssey pattern.
