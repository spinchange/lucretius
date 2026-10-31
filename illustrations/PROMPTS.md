# Prompts for the next illustrations

Four prompts: one replacement and three new images. Every prompt ends with
the same **style block** and **exclusions**, so the new images match the
best of the existing set (the Venus and Mars, Iphigenia and Acheron
frescoes) and move away from the glowing digital look of the motes and
the concept-art look of the echo.

All of them are landscape **16:9**, with the main subject centred, so that
the 1200×630 social-card crop and the 300 px hero thumbnail both work.

## Style block (append to every Pompeian prompt)

> Painted as an ancient Roman wall painting of the first century BC, in the
> Second Style of Pompeii and Boscoreale (Villa of the Mysteries, Villa of
> P. Fannius Synistor, the sacro-idyllic landscapes of Boscotrecase). True
> fresco on lime plaster: flat, matte mineral pigments only — cinnabar red,
> yellow ochre, Egyptian blue, green earth, carbon black, lime white. Loose,
> quick, visible brushwork; figures modelled with a few strokes of light
> and shadow, not smooth academic shading. The scene is framed as a panel
> on a painted wall, with faux-marble dado panels and painted columns or
> pilasters at the sides. Even, flat daylight with no single light source.
> Only light, natural wear: a few hairline cracks, slight fading.

## Exclusions (append to every prompt)

> No text, letters, inscriptions or signatures anywhere. No glowing light,
> sparkles, lens flare, light rays, god-rays or volumetric light. No
> photographic depth of field. No faces on the sun or moon. No fantasy or
> video-game styling. No Christian iconography. No modern objects.

---

## 1. Replacement for Book 3, image 1 — the quiet seats of the gods (`3.14–30`)

The current `book03_01` mixes in the honey-rimmed cup, which comes from
1.936ff and 4.11ff, not Book 3. This prompt keeps the Book 3 scene on its
own. Keep the filename `book03_01_…` (rename it to
`book03_01_quiet_seats_of_the_gods.jpg` and update INDEX.md) and the passage
reference `3.14–30`.

> A painted wall that seems to open in the middle: the central panel of
> the wall parts like a curtain of plaster, and through the opening the
> viewer sees into the infinite void. Far off, on a calm island of light
> in a clear, cloudless pale-blue sky, the Epicurean gods recline on simple
> couches in an open colonnade, at perfect ease, paying no attention to
> the world — no wind moves their robes, no cloud, rain or snow comes near
> them. Around them, scattered through the dark void, tiny fragments of
> matter drift: small stones, specks, distant worlds. In the lower part of
> the picture the ground is shown as if transparent, and beneath it there
> is nothing at all — no underworld, no temples of Acheron, only more
> void. The mood is serene and slightly uncanny, the "divine pleasure and
> shudder" of 3.28–30.
>
> *(+ style block + exclusions)*

The old image can be retired, or kept for a later spot near 4.11 if Book 4
ever gets a third illustration.

---

## 2. New: Epicurus defies Religio (`1.62–79`) — the home page and social card

The poem's founding image, and the obvious picture for the landing page.
Lucretius describes Religion as a head looming down from the regions of
the sky over human life, which lies crushed on the ground; a Greek man is
the first to lift his eyes against it, and goes beyond the "flaming walls
of the world" (1.73).

> A wide landscape at dusk. Across the ground, crowds of people lie
> pressed flat, face down or cowering, hands over their heads, crushed by
> fear. Above them, filling the upper half of the sky, an immense,
> monstrous veiled head leans down out of dark clouds: grey and shrouded
> like a storm, with a heavy, menacing, inhuman face, half-hidden, glaring
> down at the people. It is a personification of superstitious fear, not a
> god of any religion. In the middle of the crowd one man stands upright:
> a Greek philosopher in a plain undyed himation, bearded, calm, his head
> raised, looking straight up into the face of the monster without fear.
> At the far horizon behind the monster, a thin ring of fire marks the
> flaming walls of the world, and beyond it a glimpse of open, starry void
> — where the man's mind is going.
>
> *(+ style block + exclusions)*

INDEX.md entry, placed **first** under Book 1 so that the build uses it as
the landing-page hero:

```
### 1. Epicurus Defies Religio (`1.62–79`)
- **File:** [`book01_00_epicurus_defies_religio.jpg`](file:///H:/My%20Drive/agent-journal/lucretius/illustrations/book01_00_epicurus_defies_religio.jpg)
```

Then delete `docs/social.jpg` and rebuild, so the social card is cut from
the new image.

---

## 3. New: Machiavelli copying Lucretius (c. 1497) — for the margin page

This is deliberately **not** in the Pompeian style. The poem's pictures are
Roman, and Machiavelli's picture is Florentine, so the style tells the
reader which layer of the edition they are in.

The book must not show legible writing. Anything that looks like a page
of handwriting will be mistaken for Ross. 884 itself.

> An imagined scene, painted as a Florentine panel painting of about
> 1480–1500, in the manner of Domenico Ghirlandaio's *Saint Jerome in his
> Study* (Ognissanti) — tempera and oil on panel, clear even light, crisp
> outlines, a carefully described scholar's study. A young Florentine man
> of about twenty-eight, clean-shaven, thin face, short dark hair, in a
> plain dark red *lucco* (gown), sits at a wooden writing desk at night,
> copying a book by hand. In front of him, a small paper manuscript is
> open, seen at a low angle so that its pages show only as faint grey
> lines; beside it, propped on a stand, the printed book he is copying
> from. A quill, an inkwell, a pen knife, a candle in a brass holder, a
> few other books on a shelf, an hourglass. Through a small window, the
> dome of Florence cathedral against a dark blue sky. The mood is quiet
> and absorbed.
>
> No text, letters, or legible writing anywhere, especially not on the
> pages. No signatures. No glowing light, sparkles or lens flare. No
> photographic depth of field. No modern objects.

The margin page has no image slot yet. Once the image exists, the build
needs a small change to put it at the head of `margin.html`, with a
caption that says it is an imagined scene.

---

## 4. Optional: the cow searching for her calf (`2.352–366`)

One of the most moving passages in the poem, and a natural fit for the
Second Style's sacro-idyllic landscapes. It could replace the motes image
(`book02_02`), or be a third Book 2 image.

> A quiet sacro-idyllic landscape. In the middle distance, a small
> round temple among trees, with a thin column of incense smoke rising
> from an altar in front of it — the place where a calf has just been
> sacrificed (show only the altar and smoke, no blood, no carcass). In the
> foreground, a lone brown cow stands in a green glade beside a slow river
> lined with willows. She has turned her head back toward the temple,
> lowing, searching. Behind her, a line of her cloven hoofprints crosses
> the soft ground. The willows, the fresh grass and the full river around
> her are peaceful and beautiful, and none of it comforts her. The mood
> is still and full of grief.
>
> *(+ style block + exclusions)*

INDEX.md entry if it replaces the motes:

```
### 4. The Cow Searching for Her Calf (`2.352–366`)
- **File:** [`book02_02_cow_searching_for_her_calf.jpg`](file:///H:/My%20Drive/agent-journal/lucretius/illustrations/book02_02_cow_searching_for_her_calf.jpg)
```
