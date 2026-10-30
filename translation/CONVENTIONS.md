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
| ratio | reasoning | 1.51 | the doctrine or method (vera ratio = "true reasoning"); "by what principle" (qua ratione) where instrumental |
| religio | religion | 1.63 | never "superstition"; the proem's force depends on the plain word |
| animus | mind | 1.74 | |
| anima | spirit | 1.112 | the vital principle; never "soul" |
| mens | mind | 1.144 | merged with animus only where mens is non-technical; note at first technical contrast in Book 3 |
| simulacra | images | 1.123 | the Book 4 films; never "idols" |
| voluptas | pleasure | 1.1 | |
| foedera naturae | nature's covenants | | |
| leges naturae | nature's laws | | |
| species | face, appearance, likeness | 1.10 (face of the day), 1.125 (likeness) | context decides; "species ratioque" (1.148) = "the face and reasoning of nature" |
| daedala | artificer | 1.7 | daedala tellus = "the artificer earth"; natura daedala rerum (5.234) = "nature, artificer of things" |
| dias in luminis oras | the shining shores of light | 1.22 | whole-phrase refrain (1.170, 1.179, 2.577, 5.224, 5.781 etc.) |
| flammantia moenia mundi | the flaming walls of the world | 1.73 | |
| fera moenera militiai / belli | the savage works of war | 1.29, 1.32 | |
| quod superest | for the rest | 1.50 | transitional formula |
| nunc age | come now | | transitional formula |
| summa (rerum) | the sum of things | | |
| mundus | world | | the cosmos; "worlds" in plural |
| aevum | life, age | 1.45 | immortali aevo = "immortal life" |
| Acherusia templa | the precincts of Acheron | 1.120 | templa = regions/precincts, never "temples" |

## Policy

- **Lucretius's own refrains** (e.g. 1.146-148 "this terror of the mind,
  then, and this darkness / must be scattered not by the sun's rays or the
  bright shafts of day / but by the face and reasoning of nature") are
  fixed at first occurrence and recur verbatim. Add each to the table
  above when first fixed.
- **Scientific anachronism**: never import a modern term the Latin does not
  have (no "atom" for primordia, no "molecule", no "evolution"). The notes
  may say where a modern reader will hear an anticipation; the verse may
  not.
- **Proper nouns in the myths** (Iphianassa, Trivia, Danaans, Orcus,
  Helicon) stay as Lucretius has them, with a note at first use. Trivia
  (1.84) = "the Virgin of the Crossways" with a note that it is Diana.
- **Obscenity and plainness** (Book 4): plain English, neither coy nor
  coarse beyond the Latin.
