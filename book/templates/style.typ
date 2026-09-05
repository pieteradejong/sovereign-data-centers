// Shared interior style for the book and the standalone country briefs.
//
// Mono by decision (DECISIONS.md #28): briefing documents get photocopied, so the
// interior uses luma() only — no hue anywhere. Layout reference is Editorial
// Data-Report (DECISIONS.md #21).
//
// Two wrappers, deliberately not abstracted into one: the book is A5 with recto part
// openers and a chapter break per country, the brief is A4 with no breaks and a title
// block. They share the colours, the type scale and the table helpers below; the page
// geometry and heading behaviour genuinely differ.

#let ink    = luma(15)
#let mid    = luma(95)
#let quiet  = luma(140)
#let rule   = luma(200)
#let wash   = luma(244)

#let _footer(provenance) = context {
  set text(size: 6.5pt, fill: quiet)
  line(length: 100%, stroke: 0.3pt + rule)
  v(2pt)
  grid(
    columns: (1fr, auto),
    align: (left, right),
    text(provenance),
    text(str(counter(page).get().first())),
  )
}

#let _type(size: 9.5pt) = {
  set text(font: ("Libertinus Serif", "Georgia", "Times New Roman"), size: size, fill: ink, lang: "en")
  set par(justify: true, leading: 0.62em, spacing: 0.9em)
  set heading(numbering: none)
}

// ---------------------------------------------------------------------------
// The book — A5, part openers on recto, one country per chapter.
// ---------------------------------------------------------------------------

#let book(title: "", subtitle: "", generated: "", provenance: "", body) = {
  set document(title: title, author: "Pieter de Jong")
  set page(
    paper: "a5",
    margin: (inside: 20mm, outside: 16mm, top: 18mm, bottom: 20mm),
    // Decision #25: provenance on every page, not only in the front matter.
    footer: _footer(provenance),
  )
  set text(font: ("Libertinus Serif", "Georgia", "Times New Roman"), size: 9.5pt, fill: ink, lang: "en")
  set par(justify: true, leading: 0.62em, spacing: 0.9em)
  set heading(numbering: none)

  show link: set text(fill: mid)
  show raw: set text(font: ("Menlo", "DejaVu Sans Mono"), size: 8pt)

  show heading.where(level: 1): it => {
    pagebreak(weak: true, to: "odd")
    v(28mm)
    set text(size: 20pt, weight: "regular", tracking: 0.4pt)
    block(it.body)
    v(3mm)
    line(length: 34mm, stroke: 0.8pt + ink)
    v(12mm)
  }
  show heading.where(level: 2): it => {
    pagebreak(weak: true)
    v(4mm)
    set text(size: 14pt, weight: "regular")
    block(it.body)
    v(2mm)
  }
  show heading.where(level: 3): it => {
    v(3mm)
    set text(size: 9.5pt, weight: "bold", tracking: 0.6pt)
    block(upper(it.body))
    v(0.5mm)
  }

  set table(stroke: none, inset: (x: 4pt, y: 3.2pt))
  show table.cell.where(y: 0): set text(weight: "bold", size: 7.5pt)

  v(40mm)
  align(center)[
    #set text(size: 17pt, tracking: 0.5pt)
    #title
    #v(4mm)
    #set text(size: 9.5pt, fill: mid, tracking: 0.2pt)
    #subtitle
  ]
  pagebreak()
  body
}

// ---------------------------------------------------------------------------
// A standalone country brief — A4, title block, no forced breaks.
// ---------------------------------------------------------------------------

#let brief(country: "", iso: "", standfirst: "", generated: "", provenance: "", body) = {
  set document(title: country + " — sovereign data centre capacity", author: "Pieter de Jong")
  set page(
    paper: "a4",
    margin: (x: 24mm, top: 22mm, bottom: 22mm),
    footer: _footer(provenance),
  )
  set text(font: ("Libertinus Serif", "Georgia", "Times New Roman"), size: 10pt, fill: ink, lang: "en")
  set par(justify: true, leading: 0.62em, spacing: 0.95em)
  set heading(numbering: none)

  show link: set text(fill: mid)
  show raw: set text(font: ("Menlo", "DejaVu Sans Mono"), size: 8.5pt)

  // No page breaks: a brief is meant to be read straight through.
  show heading.where(level: 2): it => {
    v(5mm)
    set text(size: 10pt, weight: "bold", tracking: 0.6pt)
    block(upper(it.body))
    v(1mm)
    line(length: 100%, stroke: 0.3pt + rule)
    v(1mm)
  }
  show heading.where(level: 3): it => {
    v(3mm)
    set text(size: 10pt, weight: "bold")
    block(it.body)
  }

  set table(stroke: none, inset: (x: 5pt, y: 3.6pt))
  show table.cell.where(y: 0): set text(weight: "bold", size: 8pt)

  // Title block
  block[
    #set text(size: 7.5pt, fill: quiet, tracking: 1.2pt)
    #upper("Sovereign government data centre capacity") #h(1fr) #upper(iso)
  ]
  v(1mm)
  line(length: 100%, stroke: 0.8pt + ink)
  v(3mm)
  block[
    #set text(size: 22pt, weight: "regular", tracking: 0.3pt)
    #country
  ]
  v(2mm)
  block[
    #set text(size: 8.5pt, fill: mid)
    #standfirst
  ]
  v(3mm)
  block(
    fill: wash,
    inset: (x: 7pt, y: 6pt),
    width: 100%,
  )[
    #set text(size: 7.5pt, fill: mid)
    *What this is.* A capacity planning model, not a forecast and not a proposal. Every
    figure is a working assumption scaled from a hand-built Dutch reference case. The
    legal and regulatory entries were researched in September 2026 and will date.
    Corrections are welcome and wanted. Generated #generated.
  ]
  v(5mm)

  body
}

// ---------------------------------------------------------------------------
// Shared helpers
// ---------------------------------------------------------------------------

#let datatable(caption: none, ..args) = {
  block(breakable: false)[
    #table(..args)
    #if caption != none {
      v(1mm)
      text(size: 6.5pt, fill: quiet, caption)
    }
  ]
}

#let standfirst(body) = {
  block(
    fill: wash,
    inset: (x: 6pt, y: 5pt),
    width: 100%,
    text(size: 8pt, fill: mid, body),
  )
  v(2mm)
}
