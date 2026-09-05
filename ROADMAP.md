# Roadmap

Where this project stands, what is next, and what gates what. Reasoning behind individual choices lives in
[`DECISIONS.md`](DECISIONS.md); the record of what changed is in [`CHANGELOG.md`](CHANGELOG.md).

**Status as of 2026-09-05.** The model, the data, the documents, the web app and the test suite are built
and pushed. The blocker for anything public-facing is not code — it is that roughly 200 researched legal
cells across 27 jurisdictions have not been verified against primary sources.

---

## The goal

A national data-sovereignty strategy for every EU member state, covering four things per country:

1. **Capacity and siting** — how much compute, storage and power a sovereign core needs, and where it goes
2. **Legal and regulatory posture** — the governing instrument, certification regime, classification ladder
   and procurement route, plus foreign-jurisdiction exposure
3. **Current state and provider landscape** — what the state runs today and what it depends on
4. **Migration path and cost** — a phased, costed sequence from today's estate to the sovereign target

Delivered three ways: a markdown brief and artefacts in each country's directory, an interactive web
application, and a printed book aimed at European policymakers.

---

## Done

### The model
- Stdlib-only Python capacity model: workloads → servers → racks → MW → sites → CAPEX/OPEX
- Reproduces the original Dutch spreadsheet exactly (5,691 servers, 14.2 MW, EUR 339 m), asserted in tests
- Scales the Dutch baseline to 26 other states by population, public-administration employment and GDP
- Four-phase migration model, keyed on workload class, with CAPEX conserving to the total
- Byte-reproducible generation via `SOURCE_DATE_EPOCH`, pinned in `.build-epoch`

### The data
- `eu27_parameters.csv`: 25 columns × 27 states, including six researched legal/regulatory columns and two
  ordinal columns that the sovereignty matrix scores from
- One directory per country holding inputs, model outputs, and a 12-section brief

### The web app (`web/`)
React 19, Vite 8, TypeScript 6, Tailwind 4, D3 7. Seven working routes:

| Route | Content |
|---|---|
| `/` | EU-27 totals, the small-state cliff, the binding-constraint finding |
| `/matrix` | Sovereignty readiness matrix — 27 × 8 diverging heatmap, sortable, cells reveal source text |
| `/workloads` | Country × workload heatmap with absolute / row-normalized toggle |
| `/scenario` | Live sandbox — six sliders recompute all 27 countries in the browser |
| `/countries` | Index of all member states |
| `/country/:iso` | The full briefing |
| `/methodology` | What the model is, what it is not, and the assumption table |

### Tooling and testing
- `init.sh`, `run.sh`, `test.sh` following the workspace template convention
- 15 Python tests, 30 Vitest (including TS/Python parity), 15 Playwright (E2E, accessibility, responsive)
- CI on GitHub, including a check that committed generated files match the model
- Chart palette validated for colour-vision deficiency on both light and dark surfaces

### Per-country artefacts
- A one-page infographic (`<ISO>-infographic.png`) and a PDF briefing (`<ISO>-briefing.pdf`) in every
  country directory, produced by `model/export_artifacts.py` via `run.sh export`
- Data-driven, not AI-generated; no state emblems or official-looking wordmarks; the provenance caveat is
  printed on the poster itself, because images get shared without the page that explains them

### Deployment configuration
`vercel.json` (strict CSP, `nosniff`, `DENY` framing, restrictive `Permissions-Policy`) and a `robots.txt`
that blocks indexing until the verification gate passes.

### Documentation
`DECISIONS.md` (41 entries), `ROADMAP.md`, `CHANGELOG.md`, `README.md` with the institutional outreach map,
and a data-correction issue template.

---

## In progress

### Security-audit remediation
A full security and privacy audit was completed 2026-09-04. The repository came back largely clean: no
secrets in the full history, no personal data, zero dependency vulnerabilities, no XSS surface, no data
egress beyond the app fetching its own bundle. Critical-infrastructure sensitivity was assessed and
cleared as ordinary published policy analysis — the facts are public, the resolution is metro-level, and
the sites are explicitly hypothetical.

Four findings remain open:

| # | Finding | Remediation | Severity |
|---|---|---|---|
| 1 | `countries/NL/Rijkscloud-...png` is AI-generated (OpenAI `gpt-image`, per embedded C2PA credentials) and wears Dutch state iconography, with no disclosure anywhere | `ASSETS.md` recording provenance; captions at every reference; sibling README beside the file | High |
| 2 | Unverified legal claims lose their caveat where a reader meets them — brief §10 is prose, and the header caveat covers only "every number"; the CSVs render on GitHub as authoritative tables | Caveat inside §10; disclose the ordinal columns as author judgements; caveat in the CSVs; record the public repo as a publication channel in `DECISIONS.md` #25 | Medium-high |
| 3 | MIT covers software, not the dataset, and does not address the EU sui generis database right | Split licence: MIT for code, CC BY 4.0 for data, following the `projects/newsletter` pattern | Medium |
| 4 | Housekeeping: committed Playwright output, a byte-duplicate of the NL brief, dangling `~/dev/...` references | Remove, confirm, annotate | Low |

---

## Planned

### Next — provenance and verification (gates everything public-facing)
This is the most valuable remaining work, and the only thing standing between the project and a custom
domain or a printed book.

- `model/sources.csv`: one row per `(country, column)` → URL, publisher, retrieval date, confidence, quote
- Tiered verification: primary source for any cell asserting a legal obligation; official government page
  for the rest
- A **sampling audit** producing a measured error rate per column — confidence as a number, not a feeling
- Eurostat figures re-pulled from the public API and diffed against the CSV

### Then — deployment
`vercel.json` and `robots.txt` are in place: static build from `web/dist`, strict CSP, PR previews, and
`noindex` until verification passes. Staged as `*.vercel.app` (noindex) → `*.vercel.app` (indexed, after
Tier-1 verification) → **`eu27.cloud`** (after the sampling audit). The domain is deliberately
unofficial-sounding; see `DECISIONS.md` #41.

### Then — the choropleth
`/map` is in the navigation but unbuilt. Needs `d3-geo` with a conic projection — Cyprus and Malta are
~3,000 km from Ireland, so an unprojected EU map wastes most of its area on ocean.

### Later — the paper book
`paper_book/`, 7 × 10 in, ~280–320 pp, grayscale-safe interior, typeset with Typst (installed).

Structured as **an authored argument plus a country gazetteer**, because measurement forced it: pairwise
prose similarity across the generated briefs is 73.5% on average, with Lithuania and Latvia at 90.2%. A
book that is 91% generated text would be unreadable front to back. Parts I, II and V (~20–30k words) have
to be written; the 27 briefings become an explicitly labelled reference section.

`run.sh book` dispatches to `paper_book/build.py`, which **does not exist yet.**

### Later — outreach
The institutional map is in the README. Named individuals stay in `paper_book/contacts/`, gitignored, in
official capacity only. Outreach itself waits on verification: the first thing any of these bodies would
check is the entry about their own country.

---

## Deliberately deferred

Recorded so that "we knew and chose not to" stays distinguishable from "we missed it". Full reasoning in
`DECISIONS.md` #32.

- **`scaleQuantile` instead of `scaleQuantize`** in the workload heatmap. With Germany at 24,531 servers
  against Malta's 502, even-domain bucketing pushes most countries into the lightest shade. A genuine
  legibility bug, not a preference.
- **Sub-package D3 imports** (`d3-scale` rather than `d3`), which would cut a 47 KB chunk to about 15 KB.
- **Discriminating dimensions for the matrix leaders.** France scores 1.00 on all eight dimensions and
  Germany on seven. The distribution is healthy overall, and France genuinely does lead EU sovereign-cloud
  doctrine, so this is a finding rather than a defect — but better data (eIDAS wallet status, operator
  ownership structure) would separate the leaders.

## Out of scope

- Federation and out-of-country reserve for frontline and micro states — deferred by decision
- Scored site selection replacing the first-pass regions
- Hand-deepening the five largest states into full NL-style analyses, which collides with unconditional
  brief regeneration
- Publishing a min-cut analysis naming specific infrastructure nodes. `countries/NL/TODO.md` workstream C
  proposes this; the security audit flagged that a published min-cut over real fibre and power topology
  would be a materially different artefact from anything here today, and needs a deliberate decision first
- Rewriting git history to remove the artwork or the author email. Both are already in public, pushed
  history; a force-push would not undo caching or forks, and neither warrants it

---

## The one thing that gates the rest

Everything above is buildable. The project's real constraint is epistemic: the capacity figures are openly
scaled placeholders and the framing covers them honestly, but the legal and regulatory entries are
**assertions about what real jurisdictions require**, made from public policy documents by one researcher,
and not yet checked against primary sources.

That is fine for a public research repository with prominent caveats and a corrections channel — which is
what exists today, and arguably the fastest route to getting them verified. It is not fine for a custom
domain, a printed book, or anything handed to an official. The verification work is the gate, and it does
not get cheaper by being deferred.
