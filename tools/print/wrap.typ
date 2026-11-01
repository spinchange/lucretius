// De Rerum Natura: the one-piece cover wrap (back, spine, front), 7 x 10 in.
// Inputs from tools/build_wrap.py: kind (hardcover | paperback), spine (in),
// medallion (path, from the project root).
//
// Hardcover casewrap, Lulu: each board panel is the trim plus 0.125 in
// overhang (7.125 x 10.25 in); 0.75 in of wrap on every side folds round the
// boards; the hinge is about 0.25 in from the spine on both boards; artwork
// may shift up to 0.25 in, so nothing that matters goes near an edge and
// type keeps 0.125 in clear of the spine folds.
// Paperback, Lulu: 7 x 10 in panels, 0.125 in bleed all round.

#let KIND = sys.inputs.at("kind", default: "hardcover")
#let SPINE = float(sys.inputs.at("spine")) * 1in
#let MEDALLION = sys.inputs.at("medallion")
#let BARCODE = sys.inputs.at("barcode", default: none)   // Lulu's ISBN barcode (SVG)

#let hard = KIND == "hardcover"
#let edge = if hard { 0.75in } else { 0.125in }      // wrap or bleed
#let pw = if hard { 7.125in } else { 7in }            // panel width
#let ph = if hard { 10.25in } else { 10in }           // panel height
#let W = 2 * edge + 2 * pw + SPINE
#let H = 2 * edge + ph
#let hinge = if hard { 0.25in } else { 0in }
// centre each panel's design on the board beside the hinge, half the hinge over
#let nudge = hinge / 2

#let chalk = rgb("#efe6d2")
#let ochre = rgb("#d6a64a")
#let iron = rgb("#e0a58f")      // his ink, lifted to read on red

#set page(width: W, height: H, margin: 0pt,
          fill: gradient.linear(rgb("#5a1a14"), rgb("#3d110d"), rgb("#24090a"), angle: 90deg))
#set text(font: "Palatino Linotype", fill: chalk, lang: "en", hyphenate: false,
          number-type: "lining")

// ------------------------------------------------------------ ornaments
#let meander-tile = tiling(size: (0.3in, 0.3in), {
  let u = 0.3in / 40
  let st = (paint: chalk, thickness: 3.4 * u)
  place(line(start: (0pt, 5 * u), end: (40 * u, 5 * u), stroke: st))
  place(line(start: (0pt, 34 * u), end: (40 * u, 34 * u), stroke: st))
  place(curve(stroke: st,
    curve.move((28 * u, 34 * u)), curve.line((28 * u, 11 * u)),
    curve.line((11 * u, 11 * u)), curve.line((11 * u, 26 * u)),
    curve.line((19 * u, 26 * u))))
})
#let meander(w) = rect(width: w, height: 0.3in, fill: meander-tile, stroke: none)
#let dots-tile = tiling(size: (0.11in, 0.09in),
  place(dx: 0.045in, dy: 0.045in - 0.019in, circle(radius: 0.019in, fill: chalk)))
#let dots-band(w) = {
  line(length: w, stroke: 1.1pt + chalk)
  v(0.04in)
  align(center, rect(width: w - 0.15in, height: 0.09in, fill: dots-tile, stroke: none))
  v(0.04in)
  line(length: w, stroke: 1.1pt + chalk)
}
#let frame(w, h) = {
  place(rect(width: w, height: h, stroke: 1.6pt + chalk.transparentize(10%)))
  place(dx: 0.09in, dy: 0.09in, rect(width: w - 0.18in, height: h - 0.18in,
        stroke: 0.6pt + chalk.transparentize(60%)))
}

// a panel's design area: inset 0.55 in from the board edges, the frame on it
#let inset = 0.55in
#let panel(x, body, dx: 0pt) = place(dx: x + inset + dx, dy: edge + inset, {
  let w = pw - 2 * inset
  let h = ph - 2 * inset
  frame(w, h)
  block(width: w, height: h, inset: (x: 0.28in, y: 0.3in), {
    set par(spacing: 0.08in)
    body
  })
})

// x of each panel's board edge
#let back-x = edge
#let spine-x = edge + pw
#let front-x = edge + pw + SPINE

// ------------------------------------------------------------ front
#panel(front-x, dx: nudge, {
  set align(center)
  meander(100%)
  v(0.3in)
  text(size: 14.5pt, style: "italic", fill: chalk.transparentize(15%))[Aeneadum genetrix, hominum divomque voluptas]
  v(0.04in)
  text(size: 10.5pt, fill: chalk.transparentize(40%))[Mother of Aeneas’ race, pleasure of men and gods]
  v(0.28in)
  text(size: 21pt, tracking: 0.12em)[LUCRETIUS’]
  v(0.1in)
  text(size: 39pt, tracking: 0.05em)[DE RERUM]
  v(0.02in)
  text(size: 39pt, tracking: 0.05em)[NATURA]
  v(0.12in)
  line(length: 2.1in, stroke: 0.9pt + ochre)
  v(0.1in)
  text(size: 12pt, fill: ochre, tracking: 0.16em)[ON THE NATURE OF THINGS]
  v(0.08in)
  text(size: 8.6pt, tracking: 0.13em, fill: chalk.transparentize(20%))[WITH THE MARGINALIA OF NICCOLÒ MACHIAVELLI]
  v(0.24in)
  dots-band(100%)
  v(0.16in)
  box(width: 2.5in, height: 2.5in, radius: 50%, clip: true, stroke: 2.4pt + chalk,
      image(MEDALLION, width: 2.5in, height: 2.5in, fit: "cover"))
  v(0.14in)
  dots-band(100%)
  v(1fr)
  v(0.18in)
  text(size: 8.5pt, tracking: 0.32em, fill: chalk.transparentize(25%))[TRANSLATED BY]
  v(0.03in)
  text(size: 19pt, tracking: 0.1em)[CLAUDE]
  v(0.22in)
  meander(100%)
})

// ------------------------------------------------------------ spine
#place(dx: spine-x, dy: edge, block(width: SPINE, height: ph, {
  set align(center + horizon)
  rotate(90deg, reflow: true, block(width: ph - 1.6in, {
    set align(horizon)
    grid(columns: (auto, 1fr, auto), align: horizon,
      text(size: 12pt, tracking: 0.18em)[LUCRETIUS],
      align(center, text(size: 15.5pt, tracking: 0.08em)[DE RERUM NATURA]),
      text(size: 10pt, tracking: 0.18em, fill: chalk.transparentize(20%))[CLAUDE])
  }))
}))

// ------------------------------------------------------------ back
#panel(back-x, dx: -nudge, {
  set align(center)
  meander(100%)
  v(0.55in)
  set par(leading: 0.6em)
  text(size: 15pt, style: "italic", fill: iron)[motum varium esse et ex eo \ nos liberam habere mentem]
  v(0.14in)
  text(size: 10.5pt, fill: chalk.transparentize(15%))[That motion is various, and from this we have a free mind.]
  v(0.06in)
  text(size: 8.4pt, tracking: 0.08em, fill: chalk.transparentize(40%))[MACHIAVELLI, IN THE MARGIN OF HIS LUCRETIUS, BESIDE 2.251–256]
  v(0.5in)
  block(width: 4.55in, {
    set align(left)
    set par(justify: true, leading: 0.62em, spacing: 0.95em, first-line-indent: 0em)
    set text(size: 10.6pt, hyphenate: true)
    [Lucretius’ poem _On the Nature of Things_ sets out, in six books of
    Latin verse, the Epicurean account of the world: everything is made of
    atoms moving through the void, the gods do not govern it, and death is
    nothing to us. This edition renders it line for line into English, all
    7,412 lines, with the translator’s notes and a commentary on every book.

    Around 1497 the young Niccolò Machiavelli copied the whole poem out by
    hand. His copy survives in the Vatican Library, and in its margins are
    the notes he made as he read, thickest where Lucretius argues that the
    first-beginnings swerve and that the mind is therefore free. Here each
    of his reading marks stands in the margin beside the line it marks, as
    it stands in his copy.]
  })
  v(0.4in)
  text(size: 9pt, tracking: 0.14em, fill: chalk.transparentize(25%))[DERERUMNATURA.ORG]
  v(1fr)
  // Lulu wants the ISBN barcode in the bottom-right corner of the back cover
  align(right, box(width: 2in, height: 1.35in, align(right + bottom,
    if BARCODE != none { image(BARCODE, width: 1.9in) })))
})
