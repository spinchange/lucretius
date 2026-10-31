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

The Latin is the Perseus Digital Library's text, which keeps the standard
Munro/Bailey line numbering; its orthography and some of its readings follow
Munro rather than Bailey's Oxford Classical Text (both public domain). See
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

## Web edition

`python tools/build_web.py` builds the reading edition into `docs/` on the
Iliad and Odyssey pattern: a landing page, one page per book (argument,
translator's note, the two illustrations at their passages, the verse with
line anchors `#L216` and Machiavelli's reading marks in the right margin,
the notes), `read/margin.html` (the introduction to the margin, every
reading mark, and the state of the copy as one table per book), the
machine-readable layer under `api/` (Latin-English `aligned-0N.jsonl`,
`book-0N.txt`, `marginalia.json`, `manifest.json`), and `robots.txt`,
`sitemap.xml`, `llms.txt`. Then `npx -y pagefind` refreshes the site search
bundle (`pagefind.yml`). The site's domain is not yet chosen: the build
reads it from `DRN_SITE` (and the repository URL from `DRN_REPO`), with
placeholders otherwise.

## Layout

```
latin/            the Latin, one numbered file per book; SOURCE.md; source/ (TEI)
translation/      CONVENTIONS.md (register), proem_sample.txt, book_NN.txt
segments/         manifest.json and per-segment files bNN/sKK.{latin,translate,fidelity,annotate,review,gloss,gloss-draft}.txt
                  and the review patches sKK.patch.tsv (round 1) and sKK.patch2.tsv (round 2, with reasons)
prompts/          the stage prompts (translate, fidelity, annotate, gloss)
tools/            segment, dispatch, check_segment, sidebyside, refrains, review,
                  assemble, reassemble_verse, apply_notes, check_narration,
                  make_narration, build_audiobook, refresh_chunks, beatcheck,
                  extract_latin, build_web
audit/            rubric and findings
margin/           Machiavelli's marginalia
illustrations/    twelve fresco-style pictures, two to a book, with INDEX.md
docs/             the built web edition (GitHub Pages root): read/, api/, art/, pagefind/
runs/             headless run logs (not committed)
```
