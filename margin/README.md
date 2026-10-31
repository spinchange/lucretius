# Machiavelli's margin: MS Vat. Ross. 884

Niccolò Machiavelli's autograph copy of De Rerum Natura (with Terence's
Eunuchus), made about 1497 from a printed edition carrying Marullo's
emendations. The hand was identified by Sergio Bertelli (1961). His own
marginal notes, about twenty, cluster in Book 2 on the swerve and on the
lines that argue from it to free will, with others on the gods' indifference.

## Method

- Images: DigiVatLib, https://digi.vatlib.it/view/MSS_Ross.884, IIIF
  manifest `images/manifest.json`, canvas list `images/canvases.tsv`
  (canvas number, folio label, image service). Openings are downloaded to
  `images/` for personal study only; that folder is gitignored and nothing
  from it is ever published. Terms: free use of the images is for personal
  study; publication of images needs the Library's authorisation.
- Layout of the copy: about 28 lines a page, 56 a folio, Lucretius first.
  Folio 8v-9r (canvas 20) carries 1.429-484; Book 1 ends and Book 2 begins
  on fol. 20v (canvas 32, confirmed), so Book 2 runs to about fol. 41, Book 3 to about fol. 61, and so on. Each book
  opens with a "LIBER" heading.
- Transcription: the translator reads each opening, records every mark in
  Machiavelli's hand (verbal notes, nota signs, manicules, underlinings,
  corrections) in `marginalia.tsv`, expands abbreviations in the
  transcription column and keeps the diplomatic form in the next, then
  checks each reading against Alison Brown, The Return of Lucretius to
  Renaissance Florence (2010), appendix, recording agreement or difference.
- Publication: text only. Each note is keyed to book.line of the poem,
  given in Latin and English, and linked to its folio on DigiVatLib
  (https://digi.vatlib.it/view/MSS_Ross.884/NNNN, NNNN = canvas number).

## Files

- `marginalia.tsv`: canvas, folio, book.line, kind, diplomatic, expanded,
  English, Brown (agree / differs / not listed), remarks.
- `images/`: study copies (gitignored).

## Brown's list (Return of Lucretius, 2010, ch. 4 nn. 15-20) as the checklist

Folio -> canvas: canvas 32 is fol. 20v-21r, so a recto NNr sits on canvas
NN+11 and a verso NNv on canvas NN+12.

| fol. | canvas | at | Brown's reading |
|---|---|---|---|
| 22r | 33 | 2.82 | manicule (pointing hand) at "Avius a vera longe ratione vagaris" |
| 22v | 34 | 2.112 | simulachrum principiorum |
| 23r | 34 | 2.142 | de celeritate motus |
| 23v | 35 | 2.164a | nil fieri consilio (on "Nam neque consilio debent tardata morari") |
| 25r | 36 | 2.250-55 | motum varium esse et ex eo nos liberam habere mentem |
| 25v | 37 | 2.284-87 | in seminibus esse pondus plagas et clinamen |
| 26r | 37 | 2.294-96 | nil esse suo densius aut rarius principio |
| 26v | 38 | (2.333ff?) | variam esse figuram principiorum (Brown prints "at 2.294-96") |
| 28r | 39 | after 2.425 | semina quae titillant sensum (after two inserted lines) |
| 29r | 40 | 2.471-72, 479-82 | mare ex quibus constet principiis; in uno principio non posse esse plures formas, idest, infinitas |
| 30r | 41 | 2.516-18, 523-25 | in eodem principio frigus, tepor & calor esse possunt; principia cuiuslibet formae esse infinita |
| 31r | 42 | 2.585-88 | unum quoque ex vario principiorum genere constare |
| 31v | 43 | after 2.598-99 | de genitrice deorum |
| 32r | 43 | 2.646-48 | deos non curare mortalia |

Brown also records the text change at 2.262 (motus ... rigantur -> homines
reguntur, Pomponio Leto's alternative) and the omission of 2.258. Her
appendix (pp. 113-122) is about the exemplar, not a list of marginalia; the
list above is the whole of what she prints for Book 2. The copy's Lucretius
runs fols. 1r-133v; Terence's Eunuchus follows (134r-153v); the subscription
"Finis. Nicolaus Maclavellus scripsit foeliciter" is on fol. 133v.

## Survey of Book 2 (done 2026-10-29, canvases 32-53, fols. 20v-42r)

Every opening of Book 2 was read. Results in `marginalia.tsv` (51 entries):

- All sixteen items on Brown's list were found and read; every verbal note
  agrees with her transcription letter for letter. One correction to her
  lemma: "variam esse figuram principiorum" stands at 2.340-341, not
  2.294-296 (her n. 20 repeats the lemma of n. 19).
- Four verbal notes in the same lighter ink are not on her list:
  "De motu principiorum" (fol. 21v, at 2.62), "nil sursum ferri propria
  natura" (24r, 2.184-185), "quom declinent principia" (24v, 2.217-219),
  and "De figura atomorum" (26v, 2.333). The last uses the word atomi,
  which Lucretius never does. The 24v note is the first of the swerve
  notes, two folios before the one she prints.
- The Epicurean gloss on 20v ("sarcos eustates catastema" = σαρκὸς εὐσταθὲς
  κατάστημα, with the Latin "carnis ... constitutio") heads the pleasure
  proem and is not in her list either.
- The rest are variants in the margin (ortus, confecta, pavit, sedentes,
  vel), order marks (2.5-6, 2.44-53, 2.622-623), supplied line ends
  (2.618, 2.655, 2.1143, 3.3), interlinear corrections, a struck
  dittography, dashes, and the catchword.
- Verbal notes are concentrated in fols. 21v-32r (2.62-2.648): the swerve,
  motion, atomic shape, and the gods' indifference. Nothing verbal from
  2.660 to the end of the book.

The folios of Books 1 and 3-6 have not been surveyed. Brown reports "brief
marginalia in later chapters" that replicate other witnesses; a survey
would settle what they are.

## Survey of Book 1 (done 2026-10-31, canvases 12-32, fols. 1r-20v)

Every page of Book 1 was read (fol. 1r is canvas 12, the opening with the
flyleaf; thereafter verso NNv and recto NN+1r share canvas NN+12). Results in
`marginalia.tsv` (27 entries, placed before the canvas-32 rows of the Book 2
survey, which already carried the Book 1 colophon on fol. 20v).

- Brown prints nothing for Book 1 and says only that "brief marginalia in
  later chapters" replicate other witnesses; every Book 1 entry is therefore
  "not listed".
- Verbal notes: two. The Greek ὁμοιομέρειαν in the right margin at 1.830,
  in the lighter ink and the cursive Greek hand of the gloss on fol. 20v;
  and "Comp̄" (Comparatio) with a bracket against the wormwood simile,
  1.936-942, in the brown ink of the text. Nothing in Book 1 resembles the
  doctrinal headings of Book 2 (De motu principiorum, De figura atomorum).
- Marks: an asterisk at 1.7; dashes at 1.774 and 1.780 (as at 2.735,
  2.741); an "x" over the copy's eternis at 1.1055; two crosses at 1.1092 and
  1.1102 flanking the great lacuna, which the copy passes over without a gap
  (1093 runs straight into 1102); order marks b/a at 1.1060-1061 in the
  red-brown ink of the marks at 2.5-6; a marginal "(at cibetur" (al. cibetur?)
  at 1.1093.
- Omissions: 1.305 is absent (compare 2.258). The two manicules of Book 1
  (fol. 11r, at 1.589 and at the head of the marginal block) are tie-marks
  for 1.585-588, which the scribe dropped by eye-skip (584 "reddita constant"
  struck to "finis") and then wrote vertically in the right margin. They are
  not reading marks like the hand at 2.82.
- Scribal corrections in the line or interlinear: 1.237, 344, 506+ (513-514
  copied early and struck), 523, 631, 663, 709, 760 (ipsa supplied in the
  margin), 805, 830 (scrutemur supplied in the margin), 934, 935, 976, 991
  (false start at the head of 18v).
- Not entered: the guide letter "a" and the later ink initial A on 1r are
  entered once for the state of the copy; the running heads ("Liber" /
  "Primus" across 1v-2r, "Liber" / ".I." across 8v-9r, "Liber" at the head of
  20v); the quire signatures (a with a flourish at the foot of 5r; b, bii,
  biii, biiii, bv at the feet of 11r-15r: quires of ten leaves, a = fols.
  1-10, b = 11-20); the modern pencil foliation on each recto and pencil
  line-counts at every hundredth line (100 on 2v, 200 on 4r, and so on to
  1000 on 18v), plus a pencil "38" at 1.1038 on 19r, the line to which
  Bertelli traced the copy's agreement with the corrections of Laur. 35.32
  (Brown, appendix, p. 114): someone has marked the place.
- Layout confirmed: 28 lines a page throughout Book 1; Book 1 ends on 20v
  after five lines, followed by the rubric and the Greek gloss.

## Survey of Book 3 (done 2026-10-31, canvases 53-73, fols. 41v-61v)

Every page of Book 3 was read. Results in `marginalia.tsv` (27 entries,
appended after the Book 2 rows). Book 3 runs from the rubric on 41v to the
rubric "Lucretii liber quartus incipit Feliciter" on 61v, twelve lines down,
where Book 4 begins with a drawn initial A; the running head "Liber" /
"Tertius" stands across 41v-42r and "Liber" / ".iii." across 50v-51r.

- Brown prints nothing for Book 3; every entry is "not listed".
- No verbal note of the Book 2 kind. Three marginal words in the lighter
  ink: "diu" supplied at 3.419 (a correction); "torrari" at 3.661, the copy's
  own reading picked out in the margin; and "( particip / or" at 3.692, with
  the bracket prefix of the Book 1 and 2 marginal words, reading uncertain.
- The characteristic mark of this book is the short right-margin dash, as at
  2.735 and 2.741 and 1.774 and 1.780: at 3.131, 169, 518 (double), 566,
  583, 591, 614, 866, 876, 898, 1026, 1044, with a left-margin dash at 1042
  and a tick at 747. They thicken over the proofs that the spirit dies with
  the body (566-614) and over the consolation (866-898, 1026-1044), where
  the two at 1042 and 1044 flank the death of Epicurus. A D-shaped sign with
  three dots stands at 3.436.
- No omission of a whole line was found; the repeated line 763 is present.
  Scribal corrections in the line or interlinear: 3.30, 131 (h added to
  armoniai), 155, 335, 513, 590, 725 and 995 (line ends supplied), 897-898
  and 931 (anticipations struck), 1068.
- Not entered: the scribe's own paragraph capitals set out in the margin
  (3.41, 94, 228, 241, 289, 350, 417, 624, 978); the quire signatures e ii -
  e v (42r-45r), f - f v (51r-55r), g (61r); the modern pencil foliation;
  green crayon marks (modern) at 3.419, 433 and 1018.
- Show-through: the note at 3.692 on 54r appears reversed on 54v and is not
  a second note.
- Seen in passing for Book 4: "( ordia" in the right margin of 62r at 4.35
  (in ordia prima), the lighter ink.

## Survey of Book 4 (done 2026-10-31, canvases 73-96, fols. 61v-84v)

Every page of Book 4 was read (canvases 76-97 downloaded for it). Results in
`marginalia.tsv` (39 entries, appended after the Book 3 rows). Book 4 runs
from the rubric on 61v, where the drawn initial A begins 4.1 after twelve
lines of Book 3, to the rubric "Lucretii liber quintus incipit" on 84v, six
lines down, where Book 5 begins with an initial Q in grey. Running heads:
"Liber" / "Quartus" across 61v-62r, "Liber" / ".iiii." across 73v-74r,
"Liber" / "Quintus" across 84v-85r.

- Brown prints nothing for Book 4; every entry is "not listed".
- One verbal note: "( ÿ de gallo" in the right margin of 74r at 4.710, the
  lighter ink and the bracket prefix of the marginal words, heading the
  example of the cock and the lion. The sign between the bracket and the
  words looks like "ij" or "ÿ". One marginal word: "( ordia" at 4.35 on
  62r (in ordia prima); the earlier note of it as 4.28 was a miscount.
- Two whole lines supplied in the margin in the lighter ink, both with the
  bracket prefix: 4.174-175 written vertically in the left margin of 64r
  with a tie-mark after 128 (the copy also has them in place on 64v;
  "quanta" in the margin, "quantula" in the text), and 4.1034 in the right
  margin of 80r, omitted in the text by eye-skip to the near-identical 1047.
  Words supplied in the margin: protelo at 190 (65r), hostem at 1051 (80r),
  stinguere possit at 1098 (81r); the line end "tantum semota videtur" at
  288 (66v) in the lighter ink.
- Marks: the right-margin dash again, sixteen of them (4.73, 133, 153, 180,
  188, 189, 196, 199, 292, 305, 547, 566, 656, 735, 905, 1172, 1233), five
  on one page over the speed of the images (65r, 180-199); a cross at 672;
  four dots at 399; three dots under the last line of 77v (911); a small
  sign at 176 and a wavy stroke at 364, probably the scribe's own paragraph
  signs. The dash at 1233 stands at the denial that the gods govern
  fertility.
- Omissions: 4.568-570 absent (eye-skip from sonorem 567 to sonorem 570);
  1249-1250 run into one line (magis ... magis); 1034 omitted and supplied
  in the margin. The copy's line order follows the manuscripts where the
  editions transpose: 32, 38, 39 stand after 52 (62v), and 30-31 are not
  repeated; 67r carries 291-301 then 324-340, 67v 341-352 then 302-317, 68r
  353-363, 318-323, 364-374; 542-543 stand after 552 (71v). 910-911 repeat
  181-182 as in the editions. An extra line "corpora res multae quae mittunt
  corpore aperto" stands between 102 and 103 on 63v, not visibly struck,
  beside a struck anticipation of 104; it needs checking against the
  exemplar's text. Readings noted: ostendi est (103), dissimilesque (104),
  et gelida cygni nece torti (547).
- Scribal corrections in the line or interlinear: 4.302-303 (309
  anticipated and struck), 372, 522, 546, 592, 800, 983, 1033, 1125, 1152.
- Not entered: the scribe's paragraph capitals set out in the margin (4.269,
  337, 353, 387, 476, 513, 524, 526, 570, 598, 615, 673, 722, 779, 836, 877,
  907, 962); the quire signatures g ii - g v (62r-65r), h - h v (71r-75r),
  I - I iiii (81r-84r), with the boxed catchword "blandaq;" at the foot of
  80v (quires of ten leaves: g = 61-70, h = 71-80, I = 81-90); the modern
  pencil foliation and a pencil "29" at the head of 76v; a green crayon mark
  at 4.449 (modern); show-through of the marginal block of 64r on 64v and
  grey show-through in the margins of 75r and 84r.

## Survey of Book 5 (done 2026-10-31, canvases 96-122, fols. 84v-110v)

Every page of Book 5 was read (canvases 98-124 downloaded for it). Results in
`marginalia.tsv` (39 entries, appended after the Book 4 rows). Book 5 runs
from the rubric on 84v, where the grey initial Q begins 5.1 after six lines
of Book 4, to 110v, where after fifteen lines a small colophon in the lighter
ink ("quintus explicit feliciter") and the rubric "Lucretii liber sextus
incipit foeliciter" precede Book 6. Running heads: "Liber" / "Quintus"
across 84v-85r, "Liber" / ".V." across 85v-86r, "Liber" / "Sextus" across
110v-111r.

- Brown prints nothing for Book 5; every entry is "not listed".
- No verbal note. One marginal word in the lighter ink with the bracket
  prefix: "( metutum" at 5.1140 on 105r, the rare participle in "nimis ante
  metutum". Nothing else in the lighter ink beyond the colophon on 110v and
  the line end "Stimphala colotes" run out into the margin of 85r.
- Marks: right-margin dashes at 5.102, 321, 909, 938, 1296 (five, against
  sixteen in Book 4); four dotted lines at 1096-1100, the discovery of fire
  from rubbing branches; a capital "H" in the right margin at 499, purpose
  unclear; two left-margin strokes at 1115 and 1181 in the text ink, probably
  the scribe's own ticks.
- The line order of the exemplar shows at 5.26, given as two lines after 31
  ("tanto opere officerent nobis uncisque timendis / unguibus Arcadiae
  volucres Stymphala colentes", the Italian expansion of the Stymphalian
  birds), and at 570-574, where the repeated line stands before and after
  570 and not after 573. No whole line was found missing.
- Scribal corrections in the line or interlinear, twenty-six of them: 5.26
  (dittography), 183, 210, 264-266, 294, 491, 522, 609, 640 (a letter
  supplied over a hole in the leaf), 669, 778, 803, 806, 884 (the copy's
  "puer adhuc" struck back to the received text), 925, 977, 993, 1039,
  1126, 1169, 1173, 1174, 1187, 1278, 1399, 1421. Most are false starts
  anticipating the next word.
- Not entered: the scribe's paragraph capitals and flourishes (5.76, 92,
  146, 200, 240, 251, 261, 273, 281, 306, 324, 396, 419, 471, 510, 564,
  590, 629, 663, 673, 680, 705, 722, 727, 737, 752, 780, 836, 877, 889, 901,
  907, 916, 962, 1241, 1281); the catchword "Preterea" boxed at the foot of
  90v (entered once) with the quire signatures k - k v (91r-95r), L - L v
  (101r-105r) and M (111r): quires of ten leaves, k = fols. 91-100, L =
  101-110; a brown-ink "iij" with a bracket at the head of 108v; the modern
  pencil foliation and a pencil "700" at 5.700 on 97r; a green crayon mark
  at 5.449 (modern); grey show-through in the margins of 89v, 91v, 92r,
  98r and 100r, none of it a mark.

The folios of Book 6 have not been surveyed. Seen in passing for Book 6:
nothing in the margins of 110v-111r (6.1-35).
