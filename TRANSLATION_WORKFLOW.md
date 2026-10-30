# Translation Workflow (Lucretius)

Adapted from the Iliad project's `TRANSLATION_WORKFLOW.md` v2 for a
dispatched, segment-based production. Read with `translation/CONVENTIONS.md`
(binding) and `README.md` (the stage pipeline).

## Roles

- **Translator (Fable)**: owns the register, the proem sample, every review,
  the commentary and final notes, and the Machiavelli margin. Holds no whole
  book in context; works from findings and diffs.
- **Opus**: first-pass line-for-line translation of a segment.
- **Sonnet**: fidelity findings; draft notes.
- **Scripts**: everything mechanical (keys, lacunae, syllable band, assembly).

## Running a batch

```
python tools/segment.py                       # once, or after changing the Latin
python tools/dispatch.py --stage translate --book 1 --max 3
python tools/dispatch.py --stage fidelity  --book 1 --max 3
python tools/dispatch.py --stage annotate  --book 1 --max 3
python tools/check_segment.py --all
python tools/assemble.py 1
```
`dispatch.py` skips segments already done, so re-running continues where it
stopped. `--ids b01s03` targets one segment; `--limit 4` caps a batch;
`--dry-run` prints the first prompt. Errors are recorded in the manifest with
the last line of stderr; the full log is in `runs/`.

Billing: the dispatcher removes ANTHROPIC_API_KEY from the child environment
so the runs use the claude.ai login (subscription). `--billing api` keeps the
key and bills the API instead.

## Review (the translator's pass)

For each translated segment: read `sKK.fidelity.txt`; open the lines it
names and a random tenth of the rest against the Latin; fix; save the
accepted text as `sKK.review.txt` (same format). Resolve or delete every
`{{NOTE}}` placeholder, replacing accepted draft notes with `[n]` markers
only at assembly time. Update the register in the same session as any
rendering it fixes. A segment is "reviewed" when `sKK.review.txt` exists and
`check_segment.py` is clean on it.

## Finishing a book

After all segments are reviewed: `assemble.py`, then write the argument line
and the commentary, number the notes (`[1]`... restarting per book, each note
opening with its (book.line)), run `check_segment.py --all` and
`beatcheck.py`, commit the book with the register update.

## What triggers a footnote

As the Iliad: textual disputes; translator's judgment calls; realia;
Lucretius's own refrains at first occurrence; meaningful self-repetition.
Plus, for this poem: the first occurrence of a technical term whose Latin a
reader may know under another English name; and, sparingly, a genuinely
striking anticipation of later science, marked as the reader's association.
