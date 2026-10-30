# Translation Conventions and Term Register

The authoritative register of fixed renderings and translation policy for
this De Rerum Natura. Decisions here are binding for every segment and
every book unless explicitly revisited. Modelled on the Iliad project's
`translation/CONVENTIONS.md`; started with the proem (1.1-145).

## Principles

1. **The committed text is the source of truth.** This file must agree with
   the translated books; when in doubt, grep `translation/book_*.txt` and
   `segments/`. Update this register whenever a rendering is fixed, with a
   first-use reference (book.line, the Latin's own numbering).
2. **A fixed term, once fixed, recurs identically.** Lucretius builds his
   argument on a small technical vocabulary and repeats it on purpose. The
   English repeats it on purpose. Do not vary a term away for elegance.
3. **Whole-passage repetition is verbatim.** Lucretius reuses blocks of his
   own lines (1.146-148 = 2.59-61 = 3.91-93 = 6.39-41; 1.926-950 = 4.1-25;
   many shorter refrains). When the Latin repeats, the English repeats its
   own earlier lines word for word.
4. **The argument stays visible.** This is a poem that argues. Its
   connectives (nam, quippe, etenim, praeterea, denique, quare, nunc,
   igitur, ergo) are structural, not filler. Render them: "for", "indeed",
   "further", "again", "finally", "therefore", "as it is", "and so". Do
   not drop them to save a beat.
5. **Distinct Latin gets distinct English by default.** Deliberate merges
   must be listed here (see the primordia cluster below).

## General stance (set in the proem)

- **Form**: plain, exact, dignified modern English free verse, line for
  line with the Latin (one English line per Latin line). Target a loose
  five-to-six-beat line, 9-16 syllables, median about 13. No meter, no
  rhyme, no archaism, no "thee". The Latin is hexameter; the English does
  not imitate it.
- **Line numbers**: every translated line carries its Latin line number.
  Notes cite (book.line). The source occasionally prints lines out of
  numerical order (editorial transpositions: 1.15 before 1.14; 1.156-158
  before 1.155; 1.1086 before 1.1085; 2.6 before 2.5; 2.680 after 2.659)
  and has lettered lines (1.860a, 2.164a, 2.465a, 2.528a, 2.903a). The
  translation follows the source order and keeps every key exactly.
- **Lacunae**: where the source marks a lost line it prints an unnumbered
  `[lacuna]` line. The translation prints the same, unnumbered, so the
  files stay aligned one to one. Never supply lost text.
- **Text followed**: the Perseus Digital Library's Latin text (orthography
  and numbering of Bailey's Oxford Classical Text), as given in `latin/`.
  See `latin/SOURCE.md`.
- **Footnote markers**: bracketed integers `[1]`, `[2]`... restarting at 1
  per book; each note opens with its (book.line). During drafting, agents
  leave `{{NOTE: reason}}` placeholders at the end of a line instead.
- **Names**: familiar Latinate spellings (Venus, Mars, Epicurus, Ennius,
  Memmius, Heraclitus, Empedocles). Mavors is rendered "Mars" (1.32) and
  noted once. Lucretius never names Epicurus in the proem ("Graius homo");
  the English keeps the periphrasis, "a man of Greece" (1.66).
- **Address**: Memmius is "you"; "Memmiadae nostro" (1.26) is "our son of
  the Memmii", "Memmi clara propago" (1.42) "the famous offspring of
  Memmius". The second person is kept wherever the Latin has it.

## Technical vocabulary (keep rigid)

| Latin | English | First | Notes |
|---|---|---|---|
| rerum natura | the nature of things | 1.21, 1.25 | the title; also where natura rerum recurs as a phrase |
| natura (alone) | nature | 1.44 | "the nature of the gods" (divum natura) |
| primordia (rerum) | first-beginnings (of things) | 1.55 | the technical name for atoms; hyphenated |
| corpora prima | first bodies | 1.61 | |
| semina rerum | seeds of things | 1.59 | |
| genitalia corpora | generative bodies | 1.58 | |
| materies | matter | 1.58 | |
| elementa | elements | 1.81 | also for letters of the alphabet in the analogy (1.197 etc.); keep "elements" and note the pun once |
| inane | void | | "the void"; never "vacuum" |
| locus ac spatium | place and space | | |
| corpus / corpora | body / bodies | | the physical sense; never "particles" |
| clinamen (2.292) / declinare | swerve | | noun and verb both "swerve" |
| ratio | reasoning | 1.51 | the doctrine or method (vera ratio = "true reasoning"); "by what principle" (qua ratione) where instrumental; "order" in summa caeli ratio (1.54), the system of heaven |
| religio | religion | 1.63 | never "superstition"; the proem's force depends on the plain word |
| animus | mind | 1.74 | |
| anima | spirit | 1.112 | the vital principle; never "soul" |
| mens | mind; "thought" when paired with animus | 1.144; 1.74 | merged with animus only where mens is non-technical ("mente animoque" 1.74 = "in thought and mind"); note at first technical contrast in Book 3 |
| simulacra | images | 1.123 | the Book 4 films; never "idols" |
| voluptas | pleasure | 1.1 | |
| foedera naturae | nature's covenants | | |
| leges naturae | nature's laws | | |
| species | face, appearance, likeness | 1.10 (face of the day), 1.125 (likeness) | context decides; "species ratioque" (1.148) = "the face and reasoning of nature" |
| daedala | artificer | 1.7 | daedala tellus = "the artificer earth"; natura daedala rerum (5.234) = "nature, artificer of things" |
| dias in luminis oras | the shining shores of light | 1.22 | whole-phrase refrain (1.170, 1.179 etc.); where the Latin has luminis oras without dias (2.577, 5.224, 5.781, 5.1389, 5.1455) the English is "the shores of light" |
| flammantia moenia mundi | the flaming walls of the world | 1.73 | |
| fera moenera militiai / belli | the savage works of war | 1.29, 1.32 | |
| quod superest | for the rest | 1.50 | transitional formula |
| nunc age | come now | | transitional formula |
| summa (rerum) | the sum of things | | |
| mundus | world | | the cosmos; "worlds" in plural |
| aevum | life, age | 1.45 | immortali aevo = "immortal life" |
| Acherusia templa | the precincts of Acheron | 1.120 | templa = regions/precincts, never "temples" |
| principia | beginnings | 1.484 | Lucretius's shorter synonym for primordia; "beginnings" keeps the two Latin words apart (also 1.740, 1.993, 1.1047) |
| simplicitas (solida / aeterna) | singleness | 1.548 | "of solid singleness", "strong in eternal singleness" (1.574, 1.609, 1.612) |
| concilium / conciliatus | union | 1.484 | the atomic combination; coetus = "meeting", "union" where it is the same idea |
| coniuncta / eventa | conjoined properties / accidents | 1.449 | Epicurus's symptomata; "conjoined" and "accidents" throughout |
| vera ratio | true reasoning | 1.498 | |
| vis | force | | validae vires = "sturdy strength" (1.576) |
| exordia (rerum) | origins (of things) | 2.333 | Lucretius's third name for the atoms (2.1062, 3.31, 4.26, 4.114, 5.430); "starting-point" only in the non-technical 1.149 |
| mobilitas | mobility | 2.65 | 2.142, 2.161; never "speed" |
| conciliatus | union | 2.100 | the noun of combination, same as concilium (2.134, 2.936 "a uniting") |
| species (of animals) | sight, form | 2.364 | "the sight of other calves"; never "shapes", which is figura |
| consimili ratione | on a like principle | 3.74 | 3.282; simili ratione 3.572 "by a like principle" |
| particulae | tiny parts, small pieces | 3.665 | 3.708; "particles" is barred along with corpora |
| sensifer | sense-bearing | 3.245 | sensiferos motus, 3.272, 3.570, 3.924 |
| memores motus (mentis) | the remembering motions | 3.1040 | memory as motion; not "mindful" |
| membranae | films | 4.32 | the skins the images are likened to (4.40, 4.59, 4.95); "films" is kept for this word only, never for simulacra |
| effigiae | effigies | 4.51 | 4.85, 4.105; a fourth name for the images, kept distinct |
| nervi | sinews | 4.536 | 4.1043, 4.1115; never "nerves" |
| pari / consimili ratione | on a like principle | 4.191, 4.395 | consimili causa (4.233) = "by a like cause"; adsimili ratione (4.425) "in the same way" |
| quod superest | for the rest | 4.195 | also where it opens a clause mid-argument (4.595, 4.768, 4.1283) |
| aetherius sol | the sun in the ether | 5.215 | 5.267, 5.281, 5.389; never "the sun of the upper air" |
| caeli rationes | the order of heaven | 2.178 | 5.196, 5.1183; ratio solis (5.614) = the order of the sun, the system of its motion |
| pari / simili ratione | on (by) a like principle | 5.643 | 5.910; ratione ulla in the non-technical 5.1052, 5.1054 = in any way |
| natura daedala rerum | nature, artificer of things | 5.234 | daedala signa (5.1451) = artful statues, the crafted work |
| rerum natura creatrix | the nature of things, the creator | 1.629 | 2.1117 "the creating nature of things"; 5.1362 "the nature of things herself, the creator" |
| anima (of wind, air) | air, breath | 6.130 | the non-technical sense in the meteorology (6.578, 6.586, 6.591, 6.693), noted at each place; anima = spirit wherever it is the vital principle (6.798, 6.1223, 6.1234, 6.1261) |
| lapis Magnes | the Magnes; this Magnesian stone | 6.908 | the Greek name kept as Lucretius keeps it (6.1046 "this Magnesian stone", 6.1064 "the Magnesian stones"); "magnet" only in the notes |
| ratio quae sit | what the principle is | 6.535 | 6.639, 6.861, 6.1090 (the explanation of a phenomenon); est ratio ut (6.132) = "there is a way"; ratio morborum (6.1138) = pattern; ratio remedii (6.1226) = method; rationem reddere (6.918, 6.1000) = give a reasoning |
| consimili / pari ratione | on a like principle | 6.506 | 6.881, 6.902, 6.1131, as in Books 3-5; naturali ratione (6.760) = by a natural principle |
| aether | the ether; the upper air | 6.65 | "the shores of the ether" (6.65, as 5.85), "the sign-bearing ether" (6.481), "the pores of the ether" (6.492); "the upper air" where it is the region (6.268, 6.291, as 3.21, 3.784) |

## Policy

- **Lucretius's own refrains** (e.g. 1.146-148 "this terror of the mind,
  then, and this darkness / must be scattered not by the sun's rays or the
  bright shafts of day / but by the face and reasoning of nature") are
  fixed at first occurrence and recur verbatim. Add each to the table
  above when first fixed.
- **Refrains fixed in Book 1** (recur verbatim wherever the Latin repeats):
  - 1.670-671 = 1.792-793 (= 2.753-754, 3.519-520): "for whatever is changed and
    passes out of its own bounds, / this at once is the death of what it was before."
  - 1.673 = 1.797: "so that all things do not return utterly to nothing for you,"
    and 1.674 = 1.757: "and the store of things, reborn from nothing, grow strong."
  - 1.429 = 1.531: "as I showed you above, a little while before."
  - 1.818-819 = 1.909-910: "with what and in what position they are held
    together, / and what motions they give and receive among themselves,"
  - 1.75-77 = 1.594-596 (second and third lines verbatim).
  - 1.926-950 = 4.1-25: Book 4 takes the Book 1 review text verbatim.
- **Refrains fixed in Book 2** (review of 2026-10-30; recur verbatim wherever
  the Latin repeats):
  - 2.55-58 (= 3.87-90, 6.35-38): "For just as children tremble and fear
    everything / in blind darkness, so we in the light are afraid / at times of
    things that are no more to be feared than / what children in the dark
    shudder at and imagine will come."
  - 2.336-337 = 2.723-724, and 2.337 = 2.694: "not that few are endowed with a
    like form, / but because, as a rule, not all are alike to all." (multa
    parum = few, with Bailey and Munro.)
  - 2.478-479 = 2.522-523: "Since I have taught this, I will go on to join to
    it a fact / which, fitted to this, draws its credit: that the
    first-beginnings of things"
  - 2.756 = 2.864 = 1.673 = 1.797 (ad nilum / ad nihilum): "so that all things
    do not return utterly to nothing for you."
  - 2.178-179 (= 5.196-197): "this, still, from the very order of heaven I
    would dare / to affirm, and to show from many other things,"
  - 2.726 = 2.1020 (= 5.441): "intervals, paths, connections, weights, blows,";
    2.1021 = 1.685: "collisions, motions, order, position, shapes" (concursus =
    collisions).
  - 2.1063 (= 5.431): "of earth and sea and sky and the race of living things."
  - 2.163 (= 4.207): "and run through many times the extent of space in the
    same"; 2.12 (= 3.62): "striving night and day with surpassing labor" (the
    Book 3 line is an infinitive; keep the rest).
  - Book 1 refrains confirmed verbatim in Book 2: 2.59-61 (1.146-148), 2.176
    (1.637), 2.237 (1.1080), 2.646-651 (1.44-49), 2.688-689 (1.823-824), 2.707
    (1.188), 2.750-754 (1.789-793), 2.761-762 and 2.1008-1009 (1.818-819).
  - `python tools/refrains.py N` lists every repeated line of Book N with the
    current English of each occurrence.
- **Refrains fixed in Book 3** (review of 2026-10-30):
  - 3.87-90 = 2.55-58 and 3.519-520 = 1.670-671 confirmed verbatim; 3.62 keeps
    2.12 in its infinitive ("to strive night and day with surpassing labor");
    3.91-93 = 1.146-148 verbatim.
  - 3.806-818 recur almost word for word at 5.351-363: when Book 5 is
    reviewed, take the Book 3 review text for the lines that are identical.
  - Dashes: the accepted verse uses none (commas, semicolons, colons for the
    Latin's breaks; 3.428 and 3.481 were changed).
  - mens beside animus = "thought" (3.94, 3.139, 3.142, 3.398, 3.402, 3.615);
    mens alone, including instrumental mente, = "mind" (3.240).
- **Refrains fixed in Book 4** (review of 2026-10-30):
  - 4.1-23 = 1.926-948 verbatim (4.11 "for just as physicians" for nam; 4.24-25
    differ in the Latin and keep their own English); 4.26-28 = 3.31-33 ("But
    since" for Sed quoniam); 4.207 = 2.163 verbatim, 4.208 parallel to 2.164
    ("the sun's lights" for lumina, where 2.164 has fulgura).
  - Inside Book 4: 4.30-31 = 4.36-37; 4.65 = 4.102; 4.165 = 4.725; 4.180-182 =
    4.909-911; 4.772 = 4.801; 4.774 = 4.799; 4.804 = 4.808; 4.992-995 =
    4.1000-1003. All verbatim.
  - For Books 5 and 6: 4.53 recurs at 5.882, 4.171 at 6.252, 4.217-229 at
    6.923-935, 4.585 at 5.1385. Take the Book 4 review text where the Latin
    is identical.
  - principia = beginnings enforced at 4.667, 4.699, 4.943; exordia = origins
    at 4.26 and 4.114; "ordia prima" (4.35, tmesis) = first-beginnings.
  - particulae (4.261, 4.776) = small part, tiny parts; "particles" barred.
  - The lovers' Greek pet names (4.1160-1169) are rendered in English inside
    quotation marks, with one note.
- **Refrains fixed in Book 5** (review of 2026-10-30):
  - Taken verbatim from earlier review text where the Latin is identical:
    5.111-112 = 1.738-739; 5.128-140 = 3.784-796 ("Just as" for sicut, and
    the sentence runs on with semicolon and colon); 5.196 = 2.178; 5.198-199
    parallel to 2.180-181 (paratam = prepared, rerum = things); 5.210-212
    parallel to 1.211-212 ("rouse them to birth"); 5.351-363 = 3.806-818;
    5.419-421 = 1.1021-1023; 5.431 = 2.1063; 5.441 = 2.726 (the verb
    turbabat moves up to 5.440 so the list stands verbatim); 5.622 = 3.371;
    5.882 = 4.53; 5.1216 keeps the words of 1.1004 ("an everlasting tract of
    age"); 5.1385 = 4.585; 5.1393 = 2.30, and 5.1394-1396 parallel 2.31-33 in
    the past tense.
  - Inside Book 5: 5.188-191 = 5.423-426; 5.267 = 5.389; 5.528 = 5.1348;
    5.571 = 5.574 and 5.584 = 5.596 (the repeated lines editors bracket);
    5.764 = 5.771 ("while monthly the moon glides through the cone's rigid
    shadows"); 5.1217 = 5.379 ("the strong forces of immeasurable age");
    5.1388-1389 and 5.1454-1455 differ only in the verb (digs up / raises).
  - For Book 6: 5.82-90 recur at 6.58-66 (5.88-90 already = 1.75-77);
    5.269-272 at 6.635-638. Take the Book 5 review text where the Latin is
    identical.
  - 5.224, 5.781, 5.1389, 5.1455 "the shores of light": the Latin has no
    dias, as at 2.577.
  - principia = beginnings was already right throughout Book 5 (5.184,
    5.440); exordia = origins at 5.430 and 5.471; the non-technical exordia
    cepit (5.331) = "took its beginnings" and causarum exordia prima (5.677)
    = "the first starting-points of causes". mobilitas = mobility enforced
    at 5.858.
- **Refrains fixed in Book 6** (review of 2026-10-30):
  - Taken verbatim from earlier review text where the Latin is identical:
    6.35-38 = 2.55-58 (and 3.87-90); 6.39-41 = 1.146-148; 6.60-61 and
    6.94-95 = 1.153-154 ("The causes of whose workings they can in no way
    see, / and they suppose them to be done by divine power."); 6.62-70 =
    5.82-90 (6.70 keeps the Latin's semicolon); 6.252 = 4.171; 6.635-638 =
    5.269-272 (6.637 "returns" for redit, where 5.271 has fluit); 6.924-926
    and 6.928-935 = 4.218-220 and 4.222-229 (6.927 differs in the Latin:
    varii sonitus manare; 6.923 = 4.217 verbatim, 6.922 recast so that
    mitti falls in 6.923 as it does in the Book 4 English).
  - Inside Book 6: 6.91-93 = 6.383-385 ("from what quarter the flying fire
    has come, or into which half / it has turned from here, in what way
    through walled-in places / it has slipped in, and how, having held
    sway, it has carried itself out"); 6.988-989 = 6.995-996.
  - Book 6 has no technical principia or exordia; the four principio
    (6.740, 6.942, 6.962, 6.1145) are the adverb, "First" or "At first".
  - "To begin with" and "First" both stand for Principio at a paragraph
    head (6.96 "First", 6.608 "First"); either is accepted.
- **Scientific anachronism**: never import a modern term the Latin does not
  have (no "atom" for primordia, no "molecule", no "evolution"). The notes
  may say where a modern reader will hear an anticipation; the verse may
  not.
- **Proper nouns in the myths** (Iphianassa, Trivia, Danaans, Orcus,
  Helicon) stay as Lucretius has them, with a note at first use. Trivia
  (1.84) = "the Virgin of the Crossways" with a note that it is Diana.
- **Obscenity and plainness** (Book 4): plain English, neither coy nor
  coarse beyond the Latin.
