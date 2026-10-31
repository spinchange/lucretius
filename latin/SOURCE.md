# Source text

`book_01.txt` to `book_06.txt` are extracted from the Perseus Digital Library's
TEI edition of Lucretius, *De Rerum Natura* (PerseusDL canonical-latinLit,
`phi0550.phi001.perseus-lat1.xml`, CC BY-SA 4.0 markup; the copy used is at
`source/drn_perseus_lat1.xml`). The TEI header records its printed source as
"Lost information". The line numbering is the standard numbering shared by
Munro and by Cyril Bailey's Oxford Classical Text (1900; 2nd ed. 1922). The
text itself is not Bailey's: a full collation against an OCR of the 1922 OCT
(2026-10-30) shows the archaizing orthography Munro used (divom, volgo,
inritat, haut, quicque, nihil for Bailey's divum, vulgo, irritat, haud,
quidque, nil) and readings that agree now with Munro against Bailey (6.956
singular tempestas), now with the manuscripts against both (1.721 Aeoliae,
1.520 vocaret), and at 4.547 (Dauliades natae hortis) with neither. Notes in
the translation that cite an editor's reading were checked against Bailey's
1922 apparatus in the second-round review.

Format: each line is its number right-aligned in width 5, two spaces, the
Latin. Lines are in the edition's printed order, which departs from numerical
order where the editor transposed lines; the translation follows the printed
order and keeps every key.

| Book | Numbered lines | Lacuna markers | Highest number |
|---|---|---|---|
| 1 | 1110 | 8 (after 1.1093: lines 1094-1101 are lost) | 1117 |
| 2 | 1178 | 0 | 1174 |
| 3 | 1094 | 2 (after 3.97, 3.823) | 1094 |
| 4 | 1287 | 3 (after 4.126, 4.144, 4.289) | 1287 |
| 5 | 1457 | 1 (after 5.1012) | 1457 |
| 6 | 1286 | 6 (after 6.47, 6.51, 6.52, 6.607, 6.697, 6.839) | 1286 |

Total: 7412 numbered lines plus 20 lacuna markers.

Transpositions in printed order: 1.15 before 1.14; 1.156-158 before 1.155;
1.1086 before 1.1085; 2.6 before 2.5; 2.680 after 2.659 (then 2.660-679,
2.681). Lettered lines: 1.860a, 2.164a, 2.465a, 2.528a, 2.903a. Book 2's
count exceeds its highest number by four for this reason.

Extraction script: `tools/extract_latin.py` (reads the XML, writes the six
files, prints this anomaly report).
