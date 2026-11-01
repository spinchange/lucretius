// De Rerum Natura: the print interior, 7 x 10 in.
// Data comes from tools/build_print.py (--input data=/print-build/work/...json).
// See that script's docstring for the design.

#let D = json(sys.inputs.at("data"))
#let COLOUR = D.colour

// ---------------------------------------------------------------- geometry
#let trim-w = 7in
#let trim-h = 10in
#let m-inside = 0.875in
#let m-outside = 2.05in        // the text's outer margin: Machiavelli's column lives here
#let col-w = 1.4in             // his column
#let col-gap = 0.17in          // between the verse and his column
#let text-w = trim-w - m-inside - m-outside
#let wide-outside = 0.875in    // back matter: a plain, wide measure

// ---------------------------------------------------------------- colour
#let ink = rgb("#1a1714")
#let iron = if COLOUR { rgb("#8a2b17") } else { luma(72) }   // his ink
#let quiet-ink = luma(105)

#set document(title: "De Rerum Natura — On the Nature of Things",
              author: ("Lucretius",))
#set text(font: "Palatino Linotype", size: 10pt, fill: ink, lang: "en",
          hyphenate: false, number-type: "old-style")
#set par(leading: 0.74em, spacing: 0.74em)

// ---------------------------------------------------------------- page furniture
// <quiet>: no running head on this page (openers, title pages)
// <blank>: nothing at all (versos left empty to open a recto)
// <rh>: the running head from here on
// <geom>: which measure is in force from here on (see is-wide)
#let on-page(lbl, p) = query(lbl).any(m => m.location().page() == p)
#let latest(lbl, p) = {
  let xs = query(lbl).filter(m => m.location().page() <= p)
  if xs.len() > 0 { xs.last().value } else { none }
}
// <geom>: "verse" from the first book to the end of the last; elsewhere
// the plain measure (front and back matter)
#let is-wide(p) = latest(<geom>, p) != "verse"
#let is-blank(p) = {
  // a page left empty by recto(): the page before it ends a section and
  // the page after it opens one
  let ends = query(<end>).any(m => m.location().page() == p - 1)
  let opens = query(<quiet>).any(m => m.location().page() == p + 1)
  ends and opens and not on-page(<end>, p) and not on-page(<quiet>, p)
}

// the type area of the verse pages runs into the margin column
#let full-band(recto, body) = {
  let w = text-w + col-gap + col-w
  if recto { block(width: w, body) } else { move(dx: -(col-gap + col-w), block(width: w, body)) }
}

#let header-fn = context {
  let p = here().page()
  if on-page(<quiet>, p) or on-page(<nofolio>, p) or is-blank(p) { return }
  let recto = calc.odd(p)
  let head = latest(<rh>, p)
  set text(size: 7.4pt, tracking: 0.16em, fill: quiet-ink, number-type: "lining")
  let body = if recto { align(right, upper(head)) } else { align(left, upper[De Rerum Natura]) }
  if is-wide(p) { body } else { full-band(recto, body) }
}

#let footer-fn = context {
  let p = here().page()
  if is-blank(p) or on-page(<nofolio>, p) { return }
  let recto = calc.odd(p)
  let num = counter(page).display()
  set text(size: 8.5pt, fill: quiet-ink)
  if on-page(<quiet>, p) { align(center, num) }
  else if is-wide(p) { align(if recto { right } else { left }, num) }
  else { full-band(recto, align(if recto { right } else { left }, num)) }
}

#set page(width: trim-w, height: trim-h, binding: left,
          margin: (inside: m-inside, outside: wide-outside, top: 0.95in, bottom: 0.9in),
          header-ascent: 38%, footer-descent: 40%,
          header: header-fn, footer: footer-fn, numbering: "i")

// open the next section on a right-hand page; mark the end of this one so
// that a verso left empty is recognised as blank
#let recto() = {
  [#metadata(none) <end>]
  pagebreak(to: "odd", weak: true)
}

// headings are invisible markers for the contents and the PDF outline;
// every visible title is set by hand
#show heading: none

// ---------------------------------------------------------------- the margin
#let mg-state = state("mg-bottom", (0, 0pt))

#let mark-body(items, recto) = {
  set par(leading: 0.42em, spacing: 0.5em, justify: false)
  set align(if recto { left } else { right })
  set text(number-type: "lining")
  for it in items {
    if "glyph" in it {
      block(below: 0.45em)[
        #text(fill: iron, size: 12pt, it.glyph)#h(0.35em)#text(size: 5.8pt, fill: quiet-ink, tracking: 0.04em)[fol.~#it.fol]
      ]
    } else {
      block(below: 0.6em)[
        #text(fill: iron, size: 7.6pt, style: if it.greek { "normal" } else { "italic" },
              lang: if it.greek { "el" } else { "la" }, it.lat)
        #if it.en != "" [ \ #text(size: 6.6pt, it.en)]
        #h(0.25em)#text(size: 5.8pt, fill: quiet-ink, tracking: 0.04em)[fol.~#it.fol]
      ]
    }
  }
}

// set at the start of a verse line: places his marks level with it, in the
// outer column, pushed down below the previous mark on the page if they
// would collide
#let margin-marks(items) = box(context {
  let pos = here().position()
  let recto = calc.odd(pos.page)
  let (pp, py) = mg-state.get()
  let y0 = pos.y - 7.2pt
  let shift = if pp == pos.page and py > y0 { py - y0 } else { 0pt }
  let body = block(width: col-w, mark-body(items, recto))
  let h = measure(body).height
  mg-state.update((pos.page, y0 + shift + h + 3.5pt))
  place(top + left, dx: if recto { text-w + col-gap } else { -(col-gap + col-w) },
        dy: shift - 7.2pt, body)
})

// line numbers in the inner margin
#let line-no(k) = box(context {
  let recto = calc.odd(here().page())
  let n = text(size: 7.2pt, fill: quiet-ink, number-type: "lining", k)
  if recto { place(top + left, dx: -0.42in, dy: -0.66em, box(width: 0.3in, align(right, n))) }
  else { place(top + left, dx: text-w + 0.12in, dy: -0.66em, n) }
})

#let verse-line(l) = {
  par(hanging-indent: 1.4em, justify: false)[
    #if l.show { line-no(l.k) }#if l.mg.len() > 0 { margin-marks(l.mg) }#for p in l.p {
      if p.at(0) == "t" { p.at(1) } else { super(size: 6.6pt, typographic: false, str(p.at(1))) }
    }
  ]
}

// ---------------------------------------------------------------- pieces of prose
#let prose(paras, size: 10pt, indent: 1.2em) = {
  set par(justify: true, first-line-indent: (amount: indent, all: false),
          leading: 0.62em, spacing: 0.62em)
  set text(size: size, hyphenate: true)
  for p in paras [#p #parbreak()]
}

#let section-title(t, sub: none) = {
  v(0.9in)
  align(center)[
    #text(size: 15pt, tracking: 0.14em, upper(t))
    #if sub != none [ \ #v(0.3em) #text(size: 9.5pt, style: "italic", fill: quiet-ink, sub)]
  ]
  v(0.45in)
}

// ---------------------------------------------------------------- front matter
// half title
#[#metadata(none) <nofolio>]
#v(2.6in)
#align(center)[#text(size: 20pt, tracking: 0.12em)[DE RERUM NATURA]]
#pagebreak()
#[#metadata(none) <nofolio>]
#pagebreak()

// title page
#[#metadata(none) <nofolio>]
#v(1.3in)
#align(center)[
  #text(size: 12pt, tracking: 0.3em)[LUCRETIUS]
  #v(0.25in)
  #text(size: 30pt, tracking: 0.06em)[DE RERUM NATURA]
  #v(0.08in)
  #text(size: 12.5pt, style: "italic")[On the Nature of Things]
  #v(0.45in)
  #line(length: 1.2in, stroke: 0.6pt + iron)
  #v(0.35in)
  #text(size: 10pt)[A line-for-line translation from the Latin]
  #v(0.12in)
  #text(size: 10pt)[with the marginalia of #text(fill: iron)[Niccolò Machiavelli] \ from his own copy of the poem, Vatican MS Ross. 884]
  #v(1.1in)
  #text(size: 9pt, tracking: 0.25em)[TRANSLATED BY] \
  #v(0.04in)
  #text(size: 15pt, tracking: 0.1em)[CLAUDE] \
  #v(0.04in)
  #text(size: 9pt, fill: quiet-ink)[(Fable 5.1)]
  #v(0.3in)
  #text(size: 9pt, tracking: 0.25em)[EDITED BY] \
  #v(0.04in)
  #text(size: 11.5pt, tracking: 0.08em)[CHRISTOPHER DUFFY, SR.]
  #v(1fr)
  #text(size: 8.5pt, fill: quiet-ink, tracking: 0.08em)[dererumnatura.org]
]
#pagebreak()

// copyright
#[#metadata(none) <nofolio>]
#v(1fr)
#block(width: 100%)[
  #set text(size: 8pt, hyphenate: true)
  #set par(justify: false, leading: 0.55em, spacing: 0.9em)
  #block(spacing: 1.6em)[
    #set par(spacing: 1.1em)
    // the copyright information Lulu asks for, as the user gave it
    De Rerum Natura \
    On the Nature of Things, with the Marginalia of Niccolò Machiavelli \
    Lucretius \
    Notes by Niccolò Machiavelli \
    Translated by Claude Fable, V.I \
    Edited by Christopher Duffy, Sr. \
    Illustrated by Gemini Argon, IV

    Copyright © 2026 Christopher Duffy, Sr. \
    This work is licensed under Creative Commons Attribution 4.0 International
    (CC BY 4.0). You are free to share and adapt this material for any purpose,
    even commercially, as long as you give appropriate credit to the original
    author.

    ISBN 978-0-557-67921-8 \
    Imprint: Lulu.com
  ]

  Lucretius, _De Rerum Natura_ (_On the Nature of Things_), in a line-for-line
  English translation from the Latin, with notes, the translator’s commentary
  on each book, and the marginalia of Niccolò Machiavelli.

  The English translation is dedicated to the public domain under Creative
  Commons CC0 1.0: copy it, print it, teach it, remix it, no permission
  needed. The notes, the translator’s commentary, and the transcription and
  English of the margin are © 2026 Christopher Duffy, Sr., licensed under Creative
  Commons Attribution 4.0 (CC BY 4.0). Machiavelli’s words are his own and in
  the public domain. The Latin followed is the Perseus Digital Library’s text,
  in the public domain.

  The translation was produced by a language model (Claude) from the Latin,
  line by line, checked twice against it, and edited by a human. The method
  and the full revision history are public at
  github.com/spinchange/lucretius. The whole text, with Machiavelli’s margin,
  a narration of every book, and a machine-readable edition, is free to read
  at dererumnatura.org.

  Machiavelli’s marginalia are transcribed from Vatican Library, MS Ross. 884,
  which can be seen at digi.vatlib.it/view/MSS_Ross.884. The images of the
  manuscript are the Library’s and are not reproduced here.

  Set in Palatino Linotype. #if not COLOUR [Machiavelli’s marks are printed in grey.] else [Machiavelli’s marks are printed in a red-brown, after the iron-gall ink of his copy.]
]
#pagebreak()

// contents
#recto()
#[#metadata(none) <quiet>]
#heading(outlined: false, bookmarked: true)[Contents]
#section-title("Contents")
#context {
  set text(size: 10pt)
  let hs = query(heading.where(level: 1)).filter(h => h.outlined)
  for h in hs {
    let loc = h.location()
    let num = numbering(loc.page-numbering(), ..counter(page).at(loc))
    let indent = if h.supplement == [book] { 1.4em } else { 0pt }
    block(above: if h.supplement == [book] { 0.62em } else { 1.1em }, below: 0pt,
      grid(columns: (1fr, auto), column-gutter: 0.5em,
        pad(left: indent, box(width: 100%)[#h.body #box(width: 1fr, repeat(gap: 0.35em, text(fill: quiet-ink)[.]))]),
        text(number-type: "old-style", num)))
  }
}

// the note on the margin
#recto()
#[#metadata(none) <quiet>]
#[#metadata("Machiavelli’s Margin") <rh>]
#heading[Machiavelli’s Margin]
#section-title("Machiavelli’s Margin")
#prose(D.intro)
#v(0.3in)
#block(width: 100%)[
  #set text(size: 8.6pt)
  #set par(justify: false, leading: 0.55em, spacing: 0.75em)
  #align(center)[#text(size: 8pt, tracking: 0.2em)[THE MARKS IN THE MARGIN]]
  #v(0.4em)
  #grid(columns: (0.6in, 1fr), row-gutter: 0.7em, column-gutter: 0.6em,
    align(right, text(fill: iron, style: "italic")[nil fieri]), [his words, in his Latin or Greek, with an English rendering beneath],
    align(right, text(fill: iron, size: 12pt)[☞]), [a pointing hand: the only one in the poem stands at 2.82],
    align(right, text(fill: iron, size: 12pt)[– #h(0.2em) ∗ #h(0.2em) ×]), [a dash, a star, a cross: marks where the reader stopped],
    align(right, text(size: 6.4pt, fill: quiet-ink, tracking: 0.04em)[fol.~23v]), [the leaf of the manuscript the mark is on],
  )
]

// ---------------------------------------------------------------- the books
#recto()
#set page(margin: (inside: m-inside, outside: m-outside, top: 0.95in, bottom: 0.9in),
          numbering: "1")
#counter(page).update(1)
#[#metadata("verse") <geom>]
#for (i, b) in D.books.enumerate() {
  if i > 0 { recto() }
  [#metadata(none) <quiet>]
  [#metadata("Book " + b.roman) <rh>]
  heading(supplement: [book])[Book #b.roman]
  v(1.15in)
  align(center)[
    #text(size: 9pt, tracking: 0.42em)[BOOK] \
    #v(0.12in)
    #text(size: 34pt, tracking: 0.04em, number-type: "lining", b.roman)
  ]
  v(0.35in)
  align(center, block(width: 88%)[
    #set par(justify: false, leading: 0.6em)
    #text(size: 9.6pt, style: "italic", b.argument)
  ])
  v(0.45in)
  set par(justify: false)
  for st in b.stanzas {
    block(below: 0.74em * 2, spacing: 0pt, {
      for l in st {
        if "lacuna" in l {
          par(text(size: 8.5pt, style: "italic", fill: quiet-ink, tracking: 0.1em)[#h(1.4em)\[lacuna\]])
        } else {
          verse-line(l)
        }
      }
    })
  }
  if b.notes.len() > 0 {
    v(0.35in)
    align(center, text(size: 8pt, tracking: 0.2em)[NOTES TO BOOK #b.roman])
    v(0.2in)
    set text(size: 8.4pt, hyphenate: true)
    set par(justify: true, leading: 0.5em, spacing: 0.62em, hanging-indent: 1.3em)
    for nt in b.notes {
      par[#text(number-type: "lining")[*#nt.num*]#h(0.5em)#if nt.where != "" [#text(fill: quiet-ink, number-type: "lining")[#nt.where] —] #nt.body]
    }
  }
}

// ---------------------------------------------------------------- back matter
#recto()
#set page(margin: (inside: m-inside, outside: wide-outside, top: 0.95in, bottom: 0.9in))
#[#metadata("plain") <geom>]
#[#metadata(none) <quiet>]
#[#metadata("The Translator’s Commentary") <rh>]
#heading[The Translator’s Commentary]
#section-title("The Translator’s Commentary", sub: "on the text and translation of each book")
#for b in D.books {
  v(0.25in)
  align(center, text(size: 9pt, tracking: 0.3em)[BOOK #b.roman])
  v(0.12in)
  prose(b.commentary, size: 9.4pt)
}

#recto()
#[#metadata(none) <quiet>]
#[#metadata("The State of the Copy") <rh>]
#heading[The State of the Copy]
#section-title("The State of the Copy", sub: "corrections, variants, omissions and the other entries that record the copy rather than a reading")
#{
  set text(size: 7.4pt, hyphenate: true, number-type: "lining")
  set par(justify: false, leading: 0.45em, spacing: 0.5em)
  for b in D.books {
    if b.copy.len() == 0 { continue }
    v(0.2in)
    align(center, text(size: 8.5pt, tracking: 0.3em)[BOOK #b.roman])
    v(0.1in)
    table(
      columns: (0.55in, 0.38in, 0.62in, 1.45fr, 1fr, 1.7fr),
      stroke: (x, y) => if y == 0 { (bottom: 0.5pt + quiet-ink) } else { (bottom: 0.25pt + luma(200)) },
      inset: (x: 3pt, y: 3.5pt),
      table.header(..([line], [fol.], [kind], [the copy], [reading], [note]).map(t => text(size: 6.8pt, tracking: 0.1em, upper(t)))),
      ..b.copy.map(r => (
        r.line, r.fol, text(style: "italic", r.kind), r.dipl,
        text(fill: iron, style: if r.greek { "normal" } else { "italic" }, r.exp),
        r.note,
      )).flatten()
    )
  }
}
#[#metadata(none) <end>]
