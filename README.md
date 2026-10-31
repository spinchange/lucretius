# De Rerum Natura — a line-for-line translation

A complete line-for-line English translation of Lucretius, *On the Nature of
Things*, with a layer recording the marginal notes Niccolò Machiavelli wrote
in his own manuscript copy of the poem (Vatican Library, MS Ross. 884).
Companion to the same project's Iliad ([wrath-sing-goddess.com](https://wrath-sing-goddess.com/)),
Odyssey ([theclaudyssey.com](https://theclaudyssey.com/)) and Apology.

- **From the Latin of** Lucretius
- **Translated by** Claude (Fable 5.1), with segment drafts by Claude Opus
  and checks by Claude Sonnet, as recorded in `segments/manifest.json`
- **Edited and produced by** Chris Duffy

## Source text

The Latin is the Perseus Digital Library's text, whose orthography and line
numbering follow Cyril Bailey's Oxford Classical Text (public domain). See
`latin/SOURCE.md` for the extraction, the lacunae, and the transposed and
lettered lines. 7,412 numbered lines in six books.

## How the translation is made

The work is cut into segments of about 110 lines at Lucretius's own paragraph
breaks (`tools/segment.py`). Each segment passes through:

1. **translate** (Opus): one English line per Latin line, under the binding
   register `translation/CONVENTIONS.md` and the translator's own sample of
   the proem (`translation/proem_sample.txt`).
2. **check** (script): keys match the Latin one to one, lacunae preserved,
   no Latin left, syllable band 9-16 (`tools/check_segment.py`).
3. **fidelity** (Sonnet): Latin and English side by side, findings table
   under the rubric in `prompts/fidelity.md`.
4. **annotate** (Sonnet): draft footnotes, marked DRAFT.
5. **review** (the translator): reads the findings and the lines against
   the Latin, fixes, and writes `sKK.review.txt`, the accepted text.
6. **gloss** (Opus): a second, independent fidelity check of the accepted
   text, clause by clause (`prompts/gloss.md`, `sKK.gloss.txt`); the same
   check run on the draft (`gloss-draft`) calibrates it against the errors
   the review found.
7. **review, second round** (the translator): a full read of every line
   against the Latin with the gloss findings in hand; patches applied with
   `review.py --round 2`.

`tools/dispatch.py` runs stages 1, 3, 4 and 6 as headless `claude -p` jobs and
records every run (model, time, result) in `segments/manifest.json`, so the
work can stop and resume at any point. `tools/assemble.py` builds
`translation/book_NN.txt` from the accepted segments; the translator then
writes the argument, the commentary and the final numbered notes in the
Iliad project's format.

## Machiavelli's margin

`margin/` holds the transcription of Machiavelli's marginalia in Ross. 884,
keyed to book and line, with an English rendering and a link to the folio on
DigiVatLib. The notes are his text and public domain; the page images are
the Vatican Library's and are not reproduced here. Reference: Alison Brown,
*The Return of Lucretius to Renaissance Florence* (2010), appendix.

## Layout

```
latin/            the Latin, one numbered file per book; SOURCE.md; source/ (TEI)
translation/      CONVENTIONS.md (register), proem_sample.txt, book_NN.txt
segments/         manifest.json and per-segment files bNN/sKK.{latin,translate,fidelity,annotate,review}.txt
prompts/          the three stage prompts
tools/            segment, dispatch, check_segment, sidebyside, refrains, review,
                  assemble, apply_notes, check_narration, make_narration,
                  build_audiobook, beatcheck, extract_latin
audit/            rubric and findings
margin/           Machiavelli's marginalia
runs/             headless run logs (not committed)
```
