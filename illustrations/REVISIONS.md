# Revision prompts for Gemini

Two of the illustrations need another pass, and the cover wants a larger version of a third. Each prompt is complete on
its own: paste the whole block, including the style block and exclusions
copied from `PROMPTS.md`. Keep the same 16:9 landscape format and the same
filename, so the build picks the new image up without any other change.

---

## 1. The cow searching for her calf (`book02_02_cow_searching_for_her_calf.jpg`) — must fix

**What is wrong:** the animal is a bull, not a cow. It has no udder and
there is a sheath under the belly. Lucretius's passage (2.352–366) is about
a *mother* searching for her lost calf, so the picture contradicts the
text. There is also a row of pseudo-letters on the frieze of the temple.

**Keep:** the composition, which is the best of the set: the small round
temple among trees, the altar with its thin smoke, the willows and the
river, the line of hoofprints, and the flat Pompeian fresco style.

> A quiet sacro-idyllic landscape, painted as an ancient Roman wall
> painting of the first century BC. In the middle distance, a small round
> temple among trees, with a thin column of incense smoke rising from an
> altar in front of it — the place where a calf has just been sacrificed
> (show only the altar and smoke, no blood, no carcass). In the
> foreground, a lone brown **cow — clearly a female, a mother, with a
> visible full udder between her hind legs, no male anatomy** — stands in
> a green glade beside a slow river lined with willows. She has turned her
> head back over her shoulder toward the temple, mouth open, lowing,
> searching. Behind her, a line of her cloven hoofprints crosses the soft
> ground. The willows, the fresh grass and the full river around her are
> peaceful and beautiful, and none of it comforts her. The mood is still
> and full of grief.
>
> *(+ style block + exclusions from PROMPTS.md)*
>
> Also: the temple's frieze and entablature must be plain, with no letters,
> numerals or inscription-like marks.

---

## 2. Epicurus defies Religio (`book01_00_epicurus_defies_religio.jpg`) — recommended

**What is wrong:** the monster in the sky came out as a hooded, bearded old
man, which reads as God the Father, and so looks like an attack on
Christianity, which is not Lucretius's target. (It is no longer on the home page, the cover or the
link card, which use Venus and Mars instead, but it still opens the
reading pages for Book 1.) In Latin *religio* is feminine, and the poem gives it
only a head showing from the regions of the sky and a "horrible aspect"
(1.64–65).

**Keep:** everything else — the crowd pressed flat to the ground, the one
upright philosopher in a plain himation looking up, the ring of fire at
the horizon with stars beyond it (the "flaming walls of the world", 1.73),
the painted Pompeian frame.

> A wide landscape at dusk, painted as an ancient Roman wall painting of
> the first century BC. Across the ground, crowds of people lie pressed
> flat, face down or cowering, hands over their heads, crushed by fear.
> Above them, filling the upper half of the sky, an immense monstrous head
> leans down out of dark storm clouds: **a vast, shapeless, inhuman
> storm-face, neither male nor female, like a Gorgon mask made of
> thundercloud — hollow glaring eyes, a gaping mouth, its edges dissolving
> into cloud. No beard, no hood, no robe, no crown, no halo, nothing that
> resembles a god of any religion or an old man.** In the middle of the
> crowd one man stands upright: a Greek philosopher in a plain undyed
> himation, bearded, calm, his head raised, looking straight up into the
> face of the monster without fear. At the far horizon behind the monster,
> a thin ring of fire marks the flaming walls of the world, and beyond it a
> glimpse of open, starry void.
>
> *(+ style block + exclusions from PROMPTS.md)*

---

## 3. Venus and Mars, square and large (`cover_medallion_source.jpg`) — for print

The cover, the link card, the home page and the print wrap use a circle cut
from `book01_01_venus_and_mars.jpg`. That image is only 1200 × 896, so the
circle is 560 pixels across and prints at about 225 pixels per inch on the
2.5 in medallion of the hardcover; a printer wants 300 or more. Ask Gemini
to repaint the same scene **as a square, at least 2048 × 2048**, saved as
`cover_medallion_source.jpg`. It will be shown in a circle, so keep both
faces in the upper-middle and nothing important near the corners.

> Venus and Mars, painted as an ancient Roman wall painting of the first
> century BC, framed tight on the two figures for a round medallion. Venus,
> crowned with myrtle, in a saffron chiton with a red mantle, sits on a
> grassy bank and looks down at Mars, who reclines against her knees,
> bare-chested, a grey cloak over his shoulder, gazing up at her, disarmed
> and at peace. Behind him his crested helmet, spear and round shield lie
> on the ground. Beyond them a calm blue sea, a meadow with goats, and
> spring flowers in the grass. Both faces in the upper half of the
> picture, the bodies filling the lower half; the corners can hold only
> grass and sky.
>
> *(+ style block + exclusions from PROMPTS.md)*

---

## After the new images arrive

- The cow and Epicurus need nothing else: rebuild the site
  (`python tools/build_web.py`).
- A square Venus and Mars feeds the cover medallion. Re-cut
  `cover_medallion.jpg` from `cover_medallion_source.jpg`, re-render
  `docs/cover.jpg` and `docs/social.jpg` from `cover.svg` and `social.svg`,
  and rebuild the print wrap (`python tools/build_wrap.py`). Ask Claude to
  do this; it is a few commands.
