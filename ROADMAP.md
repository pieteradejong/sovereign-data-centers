# Roadmap

Where this project stands, what is next, and what gates what. Reasoning behind individual choices lives in
[`DECISIONS.md`](DECISIONS.md); the record of what changed is in [`CHANGELOG.md`](CHANGELOG.md).

**Status as of 2026-09-08.** The model, the data, the documents, the web app and the test suite are built
and pushed, and the web app is deployed at
[sovereign-data-centers.vercel.app](https://sovereign-data-centers.vercel.app) with indexing disabled. Every
finding from both security audits is now closed. The blocker for anything further public-facing is not code
— it is that 189 researched legal cells across 27 jurisdictions have not been verified against primary
sources. The ledger and the tooling for that work now exist and are empty:
[`VERIFICATION.md`](VERIFICATION.md), `model/sources.csv`, `./run.sh sources`.

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
- 29 Python tests, 30 Vitest (including TS/Python parity), 15 Playwright (E2E, accessibility, responsive)
- CI on GitHub, including a check that committed generated files match the model
- Chart palette validated for colour-vision deficiency on both light and dark surfaces

### Per-country artefacts
- A one-page infographic (`<ISO>-infographic.png`) and a PDF briefing (`<ISO>-briefing.pdf`) in every
  country directory, produced by `model/export_artifacts.py` via `run.sh artefacts` (not `run.sh export`,
  which typesets something else entirely — corrected 2026-09-08)
- Data-driven, not AI-generated; no state emblems or official-looking wordmarks; the provenance caveat is
  printed on the poster itself, because images get shared without the page that explains them

### Deployment configuration
`vercel.json` (strict CSP, `nosniff`, `DENY` framing, restrictive `Permissions-Policy`) and a `robots.txt`
that blocks indexing until the verification gate passes.

### Deployment — stage 1 (2026-09-07)
Live at **https://sovereign-data-centers.vercel.app**, `noindex`, on the Vercel project
`pieteradejongs-projects/sovereign-data-centers`.

- **Deploys are manual.** The Vercel GitHub App is not installed on the account, so the project could not
  be linked to the repository and does not build on push. Until it is, shipping a change means running
  `vercel deploy --prod` from a clean checkout — a stale site is the failure mode to watch for.
- `.vercelignore` exists because the Vercel CLI reads it **instead of** `.gitignore`, not in addition to
  it. It therefore repeats every rule that matters, `**/contacts/` first among them: without it the
  private contacts working tree (#46) would be uploaded with the source. Any new `.gitignore` rule that
  protects something has to be mirrored there.
- `vercel.json` sets `github.silent`, so there is no deploy status on the commit; check the Vercel
  dashboard.

### Artefact integrity (2026-09-08)
- The tracked per-country posters and PDFs are a deliberate deliverable, not an accident (#51); #41 is
  scoped to the typst build directories it always meant
- PDFs are byte-reproducible: Chrome's wall-clock `/CreationDate` and `/ModDate` are rewritten to
  `.build-epoch` (#53), verified by exporting all 27 twice and comparing hashes
- `countries/ARTEFACTS.csv` records each artefact's hash and the hash of the bundle it was rendered from;
  `tests/test_artifacts.py` fails when the data has moved past the binaries (#52)
- `tests/test_docs.py` asserts decision numbers are unique and every `#N` reference resolves (#55)

### Documentation
`DECISIONS.md` (55 entries), `ROADMAP.md`, `CHANGELOG.md`, `VERIFICATION.md`, `README.md` with the
institutional outreach map, and a data-correction issue template.

---

## In progress

### Security-audit remediation
A full security and privacy audit was completed 2026-09-04. The repository came back largely clean: no
secrets in the full history, no personal data, zero dependency vulnerabilities, no XSS surface, no data
egress beyond the app fetching its own bundle. Critical-infrastructure sensitivity was assessed and
cleared as ordinary published policy analysis — the facts are public, the resolution is metro-level, and
the sites are explicitly hypothetical.

All four were remediated in `f03fde7` (2026-09-05) and are closed. Recorded here for the trail:

| # | Finding | Remediation | Severity |
|---|---|---|---|
| 1 | `countries/NL/Rijkscloud-...png` is AI-generated (OpenAI `gpt-image`, per embedded C2PA credentials) and wears Dutch state iconography, with no disclosure anywhere | `ASSETS.md` recording provenance; captions at every reference; sibling README beside the file | High |
| 2 | Unverified legal claims lose their caveat where a reader meets them — brief §10 is prose, and the header caveat covers only "every number"; the CSVs render on GitHub as authoritative tables | Caveat inside §10; disclose the ordinal columns as author judgements; caveat in the CSVs; record the public repo as a publication channel in `DECISIONS.md` #25 | Medium-high |
| 3 | MIT covers software, not the dataset, and does not address the EU sui generis database right | Split licence: MIT for code, CC BY 4.0 for data, following the `projects/newsletter` pattern | Medium |
| 4 | Housekeeping: committed Playwright output, a byte-duplicate of the NL brief, dangling `~/dev/...` references | Remove, confirm, annotate | Low |

### Security-audit remediation — round two

**A second audit was run 2026-09-06**, covering the working tree and all 21 commits of history rather
than the current state alone. The repository came back clean on every question that matters for a public
repo: no secrets in the tree or in any commit; no emails, phone numbers or local home paths in tracked
files; zero npm vulnerabilities across five exact-pinned runtime dependencies; no XSS sink and a single
same-origin `fetch`; strict CSP; CI on `pull_request` rather than `pull_request_target`, so fork PRs
cannot reach secrets; and no author name or local path embedded in the generated PDF metadata.

**The contacts split (#45) was verified end to end**, since it landed the same day. (The private repo
moved to `contacts/` inside this tree on 2026-09-07 under #46; it is the same repo with the same remote,
and the checks below were re-run after the move with the same results.) The private repo is
in fact private, and is pushed and in sync with its origin — which is the part that matters, because
#45's stated rationale is backup, and an unpushed private repo would have satisfied the privacy half of
that argument while quietly failing the other half. Every distinctive token in the private files was then
cross-checked against the public repo's full history: zero emails, zero phone numbers and zero personal
names appear anywhere in it. The only overlaps are `European Parliament` and `Tweede Kamer`, which are
institutions and belong in the public outreach map.

Four findings, none of them a disclosure. **All four were closed on 2026-09-08:**

| # | Finding | Remediation | Severity |
|---|---|---|---|
| 1 | 56 generated binaries (27 briefing PDFs, 27 infographic PNGs, 12.7 MB of a 17 MB `.git`) are committed, directly contradicting `README.md` ("Nothing they produce is committed") and #41 ("No generated PDF is ever committed"). `model/export_artifacts.py` writes them into `countries/<ISO>/`, a path #41's safeguard never covered | **Closed 2026-09-08.** They ship deliberately: #51 records why, #24 already said so, and #41 was scoped to the typst build directories it actually governed. `README.md` and `ASSETS.md` corrected; `./run.sh artefacts` added, since `./run.sh export` was never the command that produced them | Medium |
| 1a | Those PDFs embed a real wall-clock `CreationDate` rather than the pinned `.build-epoch`, so they are not byte-reproducible and every rebuild produces a spurious diff. Their `Creator` is `HeadlessChrome`/`Skia`, not the typst path `README.md` implies | **Closed 2026-09-08.** Both date fields are rewritten to `.build-epoch` after printing, length-preserving so the xref table survives (#53). Also found: the PDFs were themselves stale. `f03fde7` changed the bundle and re-rendered the 27 posters but not the 27 PDFs, which kept a provenance banner reading "Generated 2026-09-03" for three days. Re-rendered from the current bundle, and `countries/ARTEFACTS.csv` now makes the next occurrence a test failure (#52) | Medium |
| 2 | `.github/workflows/ci.yml` declares no `permissions:` block and inherits the default `GITHUB_TOKEN` scope, though the job runs stdlib Python and needs read only | **Closed 2026-09-08.** Added, with a comment saying why the job needs nothing more | Low-medium |
| 3 | `ROADMAP.md` still described the four 2026-09-04 findings as open after `f03fde7` closed them, and still pointed named individuals at `paper_book/contacts/` after #45 moved them to a private repo | Fixed in this pass | Low |

**Informational.** `pieter.a.dejong@gmail.com` appears as committer on all 21 commits and is permanently
public. This matches `chokepoints-globe` and is presumably deliberate; it is noted only because
`~/dev/CLAUDE.md` calls it out, and because it cannot be scrubbed without rewriting history.

**The pattern worth naming.** Findings 1 and 3 are the same failure as the two near misses already
recorded in #49 and #45: a document asserts a rule, the tree quietly stops matching it, and nothing
complains. Three of the four findings above are drift between what the docs claim and what the repository
does — none of them dangerous on its own, all of them the shape that hides something that is. The
countermeasure is a check that fails the build, not a more carefully written sentence.

**Acted on, 2026-09-08.** Closing them turned up two more instances of exactly this pattern, which is the
argument for the checks rather than against them:

- `DECISIONS.md` #24 ("per-country PDFs and posters are tracked") and #41 ("no generated PDF is ever
  committed") were both written on 2026-09-04 and contradict each other. The binaries were not committed by
  accident; they were committed under one rule while another rule said they were not. Resolved in #51.
- The register had **two entries numbered 38, 39, 40 and 41**. `README.md` cited #41 meaning the PDF rule
  and this file cited #41 meaning the domain choice, and both were correct. Renumbered to #47-#50 (#55).
- `ASSETS.md` and this file both credited `./run.sh export` with producing the per-country artefacts. That
  command typesets something else entirely; the artefacts had no `run.sh` entry point at all until one was
  added.

Fourteen new Python tests cover them: artefact presence and hash drift, artefact staleness against the
data bundle, wall-clock dates in a PDF, ledger validity and the coverage ratchet, and duplicate or
dangling decision numbers.

---

## Planned

### Next — provenance and verification (gates everything public-facing)
This is the most valuable remaining work, and the only thing standing between the project and an indexed
site, a custom domain, or a printed book. The working document is [`VERIFICATION.md`](VERIFICATION.md);
this is the state of the five steps.

1. **Build `model/sources.csv`.** ✅ *Scaffolded 2026-09-08, and empty.* Schema as planned —
   `country,column,url,publisher,retrieved,confidence,quote` — with `model/sources.py` validating it and
   `tests/test_sources.py` guarding it. A row whose quote is under 20 characters fails, because a URL alone
   does not show the cited page says what the cell claims.
2. **Apply the tiered rule.** ✅ *Encoded, not yet applied.* Three tier-1 columns require `confidence:
   primary`; four tier-2 columns take an official government page; the three ordinal columns are author
   judgements and a source row for one is a validation error. **189 cells. 0 done.** This is the work.
3. **Add a CI check** that fails when a legal cell has no `sources.csv` row. ✅ *Exists as
   `python3 model/sources.py --strict`, deliberately not yet wired into CI* — it would fail on day one and
   be disabled on day two. What CI enforces today is the ratchet: `COVERAGE_FLOOR` in
   `tests/test_sources.py` may only be raised, so verified cells cannot silently become unverified. Switch
   to `--strict` when coverage reaches 189.
4. **Re-pull Eurostat from the public API** and diff against the CSV, so the figures carry a retrieval
   date rather than an assumption.
5. **Run the sampling audit.** A random sample per column, independently re-checked, producing a
   **measured error rate per column** — confidence as a number, not a feeling. This is the artefact that
   opens stages 2 and 3; the earlier steps only make it possible.

### Then — deployment stage 2: indexing
**Gated on:** Tier-1 verification (steps 1–4 above).

Delete the two `Disallow` lines from `web/public/robots.txt` — the file's own comment says exactly this —
redeploy, and confirm the live `/robots.txt` no longer disallows. Nothing else changes: same URL, same
headers.

### Then — deployment stage 3: `eu27.cloud`
**Gated on:** the sampling audit (step 5 above).

Register `eu27.cloud`, add it to the Vercel project, point DNS, and let the apex redirect settle. The
domain is deliberately unofficial-sounding so the site is not mistaken for an EU institution's; see
`DECISIONS.md` #50. A custom domain is also what makes the SSO-protection setting irrelevant, since
protection applies to `*.vercel.app` only.

### Then — the choropleth
`/map` is in the navigation but unbuilt, so the nav currently points at nothing.

1. Add `d3-geo` and pick a **conic projection**. Cyprus and Malta are ~3,000 km from Ireland, so an
   unprojected EU map wastes most of its area on ocean.
2. Feed it the existing `web/public/data/eu27.json`; `topojson-client` and `world-atlas` are already
   dependencies, so no new ones are needed.
3. Use **`scaleQuantile`, not `scaleQuantize`**, for the fill — this is the already-recorded decision
   under *Deliberately deferred*: Germany at 24,531 servers against Malta's 502 pushes even-domain
   bucketing into a single shade.
4. Keep the provenance caveat on the map itself, as on the infographics — a map gets screenshotted away
   from the page that qualifies it.

### Later — the paper book
`paper_book/`, 7 × 10 in, ~280–320 pp, grayscale-safe interior, typeset with Typst (installed).

Structured as **an authored argument plus a country gazetteer**, because measurement forced it: pairwise
prose similarity across the generated briefs is 73.5% on average, with Lithuania and Latvia at 90.2%. A
book that is 91% generated text would be unreadable front to back. Parts I, II and V (~20–30k words) have
to be written; the 27 briefings become an explicitly labelled reference section.

`run.sh book` dispatches to `paper_book/build.py`, which **does not exist yet.**

### Later — outreach
The institutional map is in the README. Named individuals live in the private repo
`sovereign-data-centers-contacts` (#45), checked out at `contacts/` since 2026-09-07 but
still a separate private repo with its own remote (#46), in
official capacity only. Outreach itself waits on verification: the first thing any of these bodies would
check is the entry about their own country.

---

## Open questions

### Two per-country PDFs, from two renderers
Raised 2026-09-08 while resolving the #24/#41 contradiction, and left open deliberately.

- `countries/<ISO>/<ISO>-briefing.pdf` — headless Chrome printing `/country/:iso`. Tracked (#51).
- `/briefs/<ISO>.pdf` on the site — typst, from `book/build.py --briefs`. Not tracked (#41).

Both render from the same dict, so they cannot disagree about a figure, and #6 is satisfied. But
#39 chose typst precisely because printing web CSS gives no facing-page margins, no widow control
and viewport-driven page breaks — "acceptable for a screenshot, weak for a document handed to a
ministry" — and then the Chrome path came back the next day for the tracked artefacts without that
being weighed.

If only one should exist, it is the typst brief, and the tracked artefact becomes poster-only. That
is a product decision about what a country directory is *for*, not housekeeping, so it is not being
made as a side effect of an audit fix.

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
