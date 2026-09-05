# Design decisions

An ADR-style log of the decisions behind this project and the reasoning for each, so the "why" survives
independently of any chat transcript or anyone's memory.

**Conventions.** Newest section last. Each entry records what was decided, when, why, what was rejected,
and what would change it. Decisions that get overturned are marked **Superseded** and left in place — a
decision that changed is more informative than one quietly erased.

---

## Scope and structure

### 1. Scope is EU-27 only
**2026-09-03.** The 27 member states, no EFTA, UK, Western Balkans or candidate countries.

Every EU-27 state shares one legal baseline — GDPR, NIS2, the Data Act, and the (still unresolved) EU Cloud
Services Scheme — which is what makes them comparable on a single axis. Norway, Switzerland and the UK each
need their own adequacy and jurisdiction framing, so folding them in would mean four framings rather than
one. Rejected: geographic Europe (~44 states), where most have no meaningful national cloud programme and
the pages would be speculative.

*Would change if:* the EFTA states' sovereign-cloud programmes become substantial enough to warrant their
own comparable treatment.

### 2. One directory per country
**2026-09-03.** `countries/<ISO2>/` holds every artefact for that country: inputs, model outputs, the
brief, and eventually its PDF and poster.

Everything about a country is in one place, and there are no cross-country files that must be kept in sync
with the per-country ones. `countries/SUMMARY.md` and `model/eu27_results.csv` are the only aggregate
files, and both are generated.

### 3. Extend `GOAL.md` to 12 sections rather than add a second document
**2026-09-03.** The generated brief grew from 9 to 12 sections (adding legal posture, provider landscape,
migration path) instead of introducing a separate `STRATEGY.md`.

One brief per country is simpler to navigate and to publish. The known cost: `generate_countries.py`
rewrites `GOAL.md` unconditionally, so hand-edits are lost. `TODO.md` wants DE/FR/IT/ES/PL hand-deepened
eventually, which will collide with this. The documented escape is to rename a country's file out of the
generator's path.

*Would change if:* hand-authored country analysis becomes the main deliverable rather than the exception.

### 4. Research all 27 legal cells now, rather than scaffold and fill later
**2026-09-03.** The six legal/regulatory columns were populated for every state in one pass.

A structurally complete section full of `TODO` markers is worse than no section: it looks finished in a
table of contents and disappoints on arrival. The tradeoff is that these are one researcher's unverified
claims — addressed by decision 25 rather than by hedging the prose.

### 5. NL is excluded from generation
**2026-09-03.** `generate_countries.py` skips the Netherlands.

`countries/NL/GOAL.md` is the hand-written 20-section narrative that the entire model derives from — the
generator reads it as the baseline. Regenerating it would overwrite the source with a scaled copy of
itself. NL still receives CSVs, a bundle entry, an app page, a PDF and a poster.

---

## Architecture

### 6. Python is the source of truth; everything else renders one dict
**2026-09-03.** `model/country_data.py` assembles every fact about a country. The markdown brief, the JSON
bundle, the web app, the PDFs and the book are all renderings of that dict.

Four presentations of the same numbers will disagree eventually unless they share one origin. The app
therefore never recomputes canonical figures for display. The single deliberate exception is the scenario
sandbox, which recomputes under user-chosen assumptions and is visually marked as hypothetical.

### 7. Fact assembly split from rendering
**2026-09-03.** `write_goal()` was refactored from a 176-line function that interleaved fact-gathering with
markdown formatting into a pure dict → markdown renderer.

Without this, `export_json.py` would have had to re-derive the same flags and ratios, and the two would
have drifted. Verified behaviour-preserving: regenerating all 27 countries after the refactor produced a
byte-for-byte zero diff.

### 8. The migration phase map is keyed on `Class`, not `Workload`
**2026-09-03.** `model/migration_phases.csv` maps the seven workload *classes* to phases.

The generator rewrites workload *names* per country — the Dutch "Digital identity / DigiD" becomes
"Digital identity / Online-Ausweis eID + BundID" in Germany — so a name-keyed map would break for 26 of 27
countries. The seven class names are stable across all of them; a test now asserts this.

### 9. `capacity_model.py` stays ignorant of `eu27_parameters.csv`
**2026-09-03.** The capacity model reads only a country directory plus shared assumptions. The
country-level hybrid-eligibility gate (does an in-jurisdiction commercial region exist?) is applied
downstream in `country_data.py`.

Keeps the model runnable against any country directory without a parameter file, which is what makes it
portable and easy to test.

---

## Method and honesty

### 10. No composite sovereignty score
**2026-09-03.** The sovereignty matrix shows eight ordinal dimensions side by side and never sums them.

The dimensions are not commensurable — certification strength and seismic risk do not add. A single number
would imply a precision this dataset does not have and would be the first thing quoted out of context. Each
column's normalization is stated on the page, and every cell links to its source text.

### 11. The matrix test guards column variance, not leader saturation
**2026-09-03.** France scores 1.00 on all eight dimensions and Germany on seven.

The first version of the test failed on any fully-saturated country. On inspection the distribution is
healthy — every column has at least two distinct values, column means range 0.19–0.81, and total scores
spread 2.2–8.0 with stdev 1.50 — and France genuinely does lead EU sovereign-cloud doctrine. Saturation by
a real leader is a finding; a dimension that scores everyone identically is the actual defect, so that is
what the test now checks.

*Would change if:* discriminating data becomes available for the leading states — eIDAS wallet notification
status, share of government workloads under national certification, or operator ownership structure (who
operates the sovereign cloud, and on whose technology).

### 12. Storage is not the sizing driver — confirmed, not assumed
**2026-09-03.** `TIER0-TIER1-SIZING.md` asked whether site count was being derived from storage volume,
which would invert the model. It is not.

`capacity_model.py` computes `sites = max(sites_by_mw, min_sites)`, and the hand-set `min_sites` floor
strictly binds for **24 of 27 countries**. Germany alone genuinely needs more sites than its floor (6
against a floor of 4); France and Italy sit exactly at the tie, where `sites_by_mw == min_sites == 4`, so
their floor coincides with the engineering answer rather than overriding it. NL's storage would have to
grow roughly 10× to change its site count.

The finding that matters more: site count is mostly a *political* parameter, not an engineering result,
and the app should show that rather than hide it.

**Corrected 2026-09-04.** This entry first read "26 of 27, Germany alone" — inherited from an early survey
that counted the France and Italy ties as floor-bound and repeated without checking. The TS/Python parity
test caught it by asserting the count. Recomputed from the model: 24 strictly floor-bound, 3 at or above
their floor (DE, FR, IT), of which only DE exceeds it.

### 13. Stdlib-only Python, no pytest
**2026-09-03.** The model and its tests use only the standard library.

The project already had this property and it is worth keeping: the Python half needs no install step at
all, which makes CI trivial and the model portable.

---

## Verification

### 14. Vet, don't assert
**2026-09-03.** Every claim gets a measurement before it is reported.

This is not a slogan; it has caught four real defects that would otherwise have shipped:

1. **`IT` and `ES` had unquoted commas** in `eu27_parameters.csv`, shifting every later field. Italy's
   published brief printed " Sicily" as its entire threat-notes section.
2. **Two writers disagreed on row order** in `eu27_results.csv` — the generator put NL first, `--all`
   sorted alphabetically — which would have made any golden-file test pure noise.
3. **An incorrect claim of my own**: that all three hyperscalers anchor their principal EU regions in
   Dublin. AWS and Azure do; Google's `europe-west1` is in Belgium. The existing
   `hyperscaler_regions_live=2` was right and the prose was wrong.
4. **73.5% mean prose similarity** across the 26 generated briefs (47 of 325 pairs above 80%, LT–LV at
   90.2%), which is why the book is structured as argument-plus-gazetteer rather than a read-through.
5. **Two miscounted headline figures**, both caught by asserting them in tests rather than repeating them.
   The `min_sites` floor binds for 24 countries, not 26 (see #12). And eight states fall below 1 MW per
   site, not nine — the "nine" came from `README.md`, which was itself wrong about a different metric
   (states under 3 MW total design load, also eight). The same eight countries happen to satisfy both:
   SI, EE, LV, CY, MT, LU, LT, HR.

The pattern in every one of these: a number quoted from an earlier summary rather than recomputed. The
app now derives these counts from the data at render time, so the page cannot drift from the model.

### 15. The generator is byte-reproducible
**2026-09-03.** Generated files stamp their date from `SOURCE_DATE_EPOCH` when set, following the
reproducible-builds convention.

Previously every run rewrote 27 files with a new date, so real changes were buried in date churn and
"regenerating changes nothing" could not be tested. Now it can be, and it is — the refactor in decision 7
was proven safe this way.

### 16. Both writers sort `eu27_results.csv` by ISO
**2026-09-03.** See defect 2 above. Committed generated files must be identical regardless of which code
path produced them, or golden-file comparison is worthless.

### 17. `test.sh` fails fast
**2026-09-04.** The full gate runs everything in cheap-to-expensive order and stops at the first failure.

Chosen deliberately. The alternative — `templates/general/general-template/scripts/test.sh` omits `set -e`
and accumulates an exit code so every check runs and a summary prints — is better when you want one full
report per run, and is the fallback if fail-fast becomes annoying.

---

## Tooling and stack

### 18. React 19 / Vite 6 / TypeScript 5.7 / Vitest 3 / ESLint 9 flat config
**2026-09-04.** Rather than the pins in `templates/ts-web/production-ready`.

`templates/DEPENDENCY_MATRIX.md` carries a 2026-09-01 audit note stating its Dec-2024 pins are ~20 months
stale and that recent workspace projects have moved to React 19 / Vite 6–8 / TS 6. This is a greenfield app
with no legacy constraint, so it follows current practice rather than a self-declared-stale baseline. Exact
version pinning, no `^` or `~`, per the workspace rule.

Consequence: the template's `.eslintrc.cjs` is a rule-list reference rather than a copyable file, since
ESLint 9 uses flat config.

### 19. Template bugs deliberately not copied
**2026-09-04.** Four defects confirmed in `templates/ts-web/production-ready`:

- `"test": "vitest"` is **watch mode**, so `./run.sh test`, `run.sh health` and the `pre-push` hook all
  hang in non-interactive use. Here: `"test": "vitest run"` with `test:watch` separate.
- `test:` config is duplicated in `vite.config.ts` and `vitest.config.ts`; the standalone file wins at
  runtime, so the vite block is dead config. Here: only `vitest.config.ts`.
- `@vitest/coverage-v8` is not installed, so the 80% thresholds in `vitest.config.ts` silently cannot run.
- `dist/` is committed by accident.

Worth reporting back to the template so they get fixed at source.

### 20. Tailwind, matching the template
**2026-09-04.** Despite the app being SVG-chart-heavy, where Tailwind does comparatively little.

Consistency with the workspace's other web projects won over dropping three build dependencies.

### 21. Warm Neutral + Terracotta design system
**2026-09-04.** From `~/dev/design/DESIGN_SYSTEMS.md`, with Editorial Data-Report as the layout reference.

Of the five systems in that library, two are dark single-theme (Nocturnal Cartography, Quant Terminal) and
unusable in print. Warm Neutral + Terracotta is authored paper-first, is mostly neutral so it survives
grayscale conversion for the book, and its single accent collapses to one distinguishable gray. Its
institutional restraint also suits a ministerial audience better than a dashboard palette.

### 22. Playwright drives the installed Chrome
**2026-09-04.** `channel: 'chrome'` with `PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1`.

Full Playwright API for E2E, axe and visual regression without the ~400 MB Chromium download, which
`~/dev/CLAUDE.md` asks be confirmed before pulling. Note the local binary is at
`/Applications/Chrome.app/Contents/MacOS/Google Chrome` — not the conventional `Google Chrome.app` path —
with Brave and Edge as fallbacks.

### 23. Typst over Pandoc + LaTeX
**2026-09-04.** Typst 0.15.1, installed via Homebrew: a single 44.9 MB bottle with zero dependencies,
Apache-2.0.

`pandoc` was already installed but no TeX engine was. MacTeX is multi-GB; BasicTeX ~100 MB plus package
installs; Tectonic was the closest alternative. Typst needs no LaTeX distribution at all and its templates
are readable, which fits the workspace's dependency-light rule.

---

## Publication

### 24. Deliverables are committed; build output is not
**2026-09-04.** Per-country PDFs, posters and the JSON bundle are tracked. `web/dist/` and
`web/node_modules/` are gitignored.

**Supersedes** an earlier decision to "commit everything", which was taken when the site was hand-written
static HTML with no build step. With Vite, `dist/` is regenerated by Vercel on every push, so committing it
adds permanent binary churn and buys nothing.

### 25. Publication is gated on verification
**2026-09-04.** The site stays on `*.vercel.app` and nothing goes to print until: Tier-1 legal cells are
verified against primary sources, a sampling audit has produced a measured error rate per column,
provenance is visible on every page and in every PDF, the corrections channel is live, and three briefs
have been read end to end.

The six legal columns are **factual claims about real jurisdictions** — a different epistemic category from
the scaled capacity placeholders. The repo's "working assumption" banner honestly covers a scaled MW
figure; it does not cover asserting what Spain's certification regime requires. Publishing unverified legal
claims under an authoritative-sounding domain is this project's one real reputational risk, and a printed
book cannot be corrected after the fact.

### 26. Named individuals never go in the public repo
**2026-09-04.** The outreach contact list holds institutional roles and published official contact points —
committee, directorate, agency. Named individuals with contact details live in `book/contacts/`,
which is gitignored.

A list of named officials in a public GitHub repo is a scrape target, ages badly, and a public official's
work contact is still personal data under GDPR requiring a documented lawful basis. The institutional map
carries essentially all the useful information at none of the risk.

### 27. The book is an authored argument plus a country gazetteer
**2026-09-04.** Parts I, II and V are newly written (~20–30k words); the 27 country briefings are an
explicitly labelled reference section.

Driven by measurement, not taste: at 73.5% mean pairwise prose similarity, the generated briefs would make
an unreadable read-through book. Reference works are allowed to be formulaic — an almanac entry is supposed
to resemble every other entry — but only if the book is honest about which part is reference and puts the
argument somewhere else.

### 28. Grayscale-safe book interior
**2026-09-04.** Mono interior, colour cover, every heatmap re-encoded by value and texture rather than hue.

Briefing documents get photocopied, so a chart that dies in black and white dies in exactly the setting
this book is for. Mono print-on-demand is also roughly a third the unit cost at ~300 pages. The web and PDF
editions keep full colour.

---

## The web app

### 29. Heatmaps are HTML tables, not SVG
**2026-09-04.** The sovereignty matrix and workload heatmap render as `<table>` elements with a `<button>`
per cell, rather than as SVG `<rect>` grids.

Every cell has to be individually focusable and screen-reader addressable. With real DOM elements that is
free — a button gets keyboard focus and an `aria-label` naming its row, column and value. With SVG it
means hand-plumbing roles, tabindex and labels onto shapes that have none of it by default. The axe
accessibility tests passed on the first run as a direct result.

The cost is that SVG's expressiveness is unavailable for these two charts. That is a fair trade for the
two views the whole site is built around.

*Would change if:* a chart needs geometry a table cannot express — which is exactly why the choropleth,
when built, will be SVG.

### 30. D3 is used as a maths library, not a charting library
**2026-09-04.** Only `scaleLinear` and `scaleQuantize` are imported. No `d3.select`, no data joins.

D3's DOM-manipulation half fights React, which owns the DOM. Its scales, projections and statistics are
genuinely worth having. Using only the second half is deliberate.

Known inefficiency: importing the `d3` meta-package pulls a 47 KB chunk to use two functions. Importing
`d3-scale` directly would cut that to roughly 15 KB. Left as-is for now under decision 32.

### 31. No Three.js, and no 3D
**2026-09-04.** Considered and rejected.

There is no third dimension in this data. A 3D rendering of a 27 × 8 ordinal matrix would occlude cells
behind other cells and read worse than the flat grid, at roughly 600 KB. The one arguable case — a globe
showing subsea cable landings — is decoration: the sovereignty argument in this project is jurisdictional,
not geographic.

### 32. Known improvements deliberately deferred
**2026-09-04.** Three changes were identified as genuine improvements and consciously not made, to keep
the codebase simple while the data is still unverified:

- **`scaleQuantile` instead of `scaleQuantize`** in the workload heatmap. `scaleQuantize` splits the
  domain evenly, and with Germany at 24,531 servers against Malta's 502 most countries fall into the
  lightest bucket. `scaleQuantile` splits by rank, which is what a 27-row comparison wants. This is a real
  legibility bug, not a preference.
- **Sub-package imports** (`d3-scale` rather than `d3`), for the chunk-size reason in decision 30.
- **The choropleth** (`/map`), which needs `d3-geo` with a conic projection. Cyprus and Malta are ~3,000 km
  from Ireland, so an unprojected EU map wastes most of its area on ocean.

Recorded here rather than lost, because "we knew and chose not to" is different from "we missed it".

### 33. Scripts at the repo root, following the workspace template convention
**2026-09-04.** `init.sh`, `run.sh` and `test.sh` sit flat at the root, matching
`templates/rn-supabase` rather than the `scripts/` subdirectory used by the older general template.

Conventions copied from `templates/ts-web/production-ready`: `set -e`, the `RED/GREEN/YELLOW/BLUE/NC`
colour block, `print_info`/`print_success`/`print_error`, `case "${1:-...}"` dispatch, unknown command →
error then help then exit 1.

Four bugs in that template were deliberately **not** copied, and are worth fixing at source:

| Template bug | Consequence |
|---|---|
| `"test": "vitest"` | Watch mode. `./run.sh test`, `run.sh health` and the pre-push hook all hang non-interactively |
| `test:` config in both `vite.config.ts` and `vitest.config.ts` | The vite block is dead config; the standalone file wins |
| `@vitest/coverage-v8` not installed | The 80% thresholds in `vitest.config.ts` silently cannot run |
| `dist/` committed | Build output in git |

### 34. The build date lives in `.build-epoch`
**2026-09-04.** One file, read by all three scripts.

It was first written as a literal in `run.sh` and `test.sh` and omitted from `init.sh` — so initialising a
fresh clone regenerated the bundle with today's date and immediately made the committed file look stale.
`test.sh` caught this on its first full run. A constant duplicated across three files is a constant that
will disagree with itself.

### 35. Accessibility defects found by testing, not by review
**2026-09-04.** The axe suite found three real problems on first run:

- `aria-sort` was on the sort `<button>` rather than the `<th>` that owns it — invalid ARIA.
- `--color-fg-muted` (`#898781`) measures **3.21:1** against the page. That value comes from the design
  system, where it is correct for axis ticks at the 3:1 graphical threshold, but it fails AA as body text.
  Darkened to `#6f6d66` (4.63:1) so one token is safe everywhere it is used. Worth feeding back to
  `~/dev/design/DESIGN_SYSTEMS.md`.
- White on the terracotta accent measures **3.12:1**. Replaced with slate (4.85:1).

None of these were visible to the palette validator, which checks chart colours against a surface, not
arbitrary text-on-background pairs in a finished layout.

### 36. Screenshots are part of testing, not a nicety
**2026-09-04.** The rotated column headers in the matrix were clipped to `w-6`, rendering every dimension
name as "Sov...", "Cert...", "Hyp...". Types passed, lint passed, axe passed, 15 E2E assertions passed —
and the chart was unreadable.

Nothing except looking at the rendered page catches that class of defect. The plan's "render it and look
at it" step is load-bearing.

### 37. The E2E suite binds a dedicated port
**2026-09-04.** Playwright's preview server uses 4823 with `strictPort`, not Vite's default 4173.

Another project in this workspace was already serving 4173. The preview server failed to bind, Playwright
happily reused the existing one, and the tests ran green against a completely different application before
this was noticed. `strictPort` turns that silent pass into a hard failure.

---

## Print and distribution

### 38. The book directory is `book/`, not `paper_book/`
**2026-09-04.** Renamed; `run.sh`, `.gitignore` and #26 above updated to match.

`run.sh` called `paper_book/build.py` and `.gitignore` excluded `paper_book/contacts/`, but neither the
directory nor the script had ever been written — so `./run.sh book` and `./run.sh export` both failed with
a Python "no such file" error while `CHANGELOG.md` listed them as delivered commands. Given the folder had
to be created anyway, it takes the shorter name, and there is exactly one name for it rather than two.

### 39. One typst renderer for the book and the per-country briefs
**2026-09-04.** `book/build.py --briefs` emits 27 standalone A4 PDFs from the same `country_entry()` that
renders the book's gazetteer chapter. `run.sh export` points at it. The Chrome-headless export path implied
by `init.sh`'s browser check is abandoned.

The alternative was printing the React app's `/country/:iso` route to PDF with headless Chrome. That gives
web CSS in a print context: no facing-page margins, no widow and orphan control, and page breaks that fall
where the viewport says rather than where the document should break. Acceptable for a screenshot, weak for
a document handed to a ministry.

The deeper objection is #6. Two renderers means two places the same country's figures can diverge, which is
the failure mode the single-dict rule exists to prevent. A brief is the gazetteer entry plus a title block —
about forty lines of shared code, not a second pipeline. `country_entry(c, standalone=True)` promotes the
section headings by one level and drops the chapter title; everything else is identical by construction.

Chrome is still required for the Playwright E2E suite (#22), so `init.sh` keeps the check — but its stated
justification was corrected, since it claimed Chrome was needed for an export that no longer uses it.

*Would change if:* a brief needs a chart the model cannot emit as typst or SVG.

### 40. A5 book, A4 briefs
**2026-09-04.** Two page geometries in `templates/style.typ`, sharing colours, type scale and table helpers.

A book that is read through and a brief that is handed across a desk are different objects. The A5 interior
takes recto part openers and a page break per country; the A4 brief takes a title block and no forced breaks
at all, because it is meant to be read straight through in two pages. The two wrappers are deliberately not
factored into one parameterised function — the page geometry and the heading behaviour genuinely differ, and
the shared part is small enough that duplicating fifteen lines is clearer than the abstraction that would
avoid it.

### 41. No generated PDF is ever committed
**2026-09-04.** `book/build/` and `web/dist/` are gitignored. The briefs and the book are built on demand.

Twenty-eight PDFs at roughly 40 KB each for the briefs and 700 KB for the book is about 1.8 MB per build —
and CI already regenerates model outputs on every push, so any change to `model/` would rewrite all
twenty-eight binaries. Git history never shrinks, and `~/dev/CLAUDE.md` is explicit that regenerable build
artifacts stay out of it. The build is deterministic given `.build-epoch` (#34), which is what makes not
committing them safe: the PDF is always reproducible from source at any commit.

This is also why the briefs are written to `web/dist/briefs/` and never to `web/public/`. `public/` is
tracked — `eu27.json` lives there and CI asserts it is fresh — so a PDF placed there would be committed by
the same rule that keeps the bundle honest.

### 42. The PDFs ship from the existing web app, not a separate one
**2026-09-04.** `./run.sh build` writes the briefs into `web/dist/briefs/<ISO>.pdf`, served from the same
origin as the app at `/briefs/<ISO>.pdf`.

A separate PDF site would need its own deployment, its own domain, and its own copy of the provenance
banner that #25 requires everywhere — three new things to keep in sync, for content derived from the data
the main app already serves. It would also put the PDF a navigation hop away from `/country/:iso`, which is
the page where a reader actually wants it.

The reason to split would be a different audience or different access control. There is one audience here,
and it is the same one for both.

*Open:* Vercel's build image has no typst, so a deploy built there produces the app without the briefs.
Either the build installs typst, or CI builds the briefs and attaches them to a GitHub Release with the app
linking out. Unresolved; the local build is correct either way.

### 43. The outreach map is institutional; individuals are gitignored
**2026-09-04.** `OUTREACH.md` carries offices, agencies, committees and press desks for all 27 states plus
the EU layer. Named individuals go in `book/contacts/`, which is gitignored under #26.

Two-thirds of the map was already in `model/eu27_parameters.csv` — `sovereign_cloud_initiative`,
`certification_scheme` and `procurement_vehicle` name the operator, the certifying authority and the buying
channel for every member state, researched against primary sources when those columns were built. Rebuilding
that from memory would have produced a second, less reliable copy of a dataset the repo already has.

The file therefore carries an explicit provenance table separating what it inherits from the CSV from what
was added from general knowledge. Ministry names, parliamentary committees and press desks are in the second
category and are marked check-before-send: digital portfolios are merged, split and renamed at nearly every
reshuffle, and three of the twenty-seven moved within the last two years.

Send order is operator, then scrutiny, then trade press, then ministry — not the reverse. The operator holds
the workload inventory the model is guessing at and is the only party who can falsify it, and a ministerial
send that arrives before the operator has seen it tends to be routed back to that operator as a threat.

---

## Artefacts, outreach and deployment

### 38. Per-country infographics are generated from the model, never illustrated
**2026-09-05.** Each country gets a one-page PNG infographic and a PDF briefing, rendered
by headless Chrome from a `/poster/:iso` route in the app.

Every figure comes from `country_data.build()` via the JSON bundle, so a poster cannot
disagree with its brief. This is the deliberate opposite of the existing Dutch artwork
(decision 39), whose grid routing, cable landings and growth curves were drawn by an image
model and derive from nothing in this repository — and which still shows PUE 1.70 against
the model's 1.25.

Two rules the layout follows, both from the security audit:

- **No state emblems, flags, crowns or official-looking wordmarks.** These are concept
  posters for a programme that exists in no member state, and they say so.
- **The caveat is printed on the poster.** An image gets shared without the page that
  explains it, so the disclaimer has to travel with the pixels.

Poster height is measured per country from the rendered DOM rather than fixed: region
counts vary from two to five, so a fixed height would clip Romania or leave Malta
two-thirds blank.

### 39. AI-generated assets must be labelled at every reference
**2026-09-05.** Arising from the security audit.

`countries/NL/Rijkscloud-...png` carries C2PA Content Credentials naming OpenAI `gpt-image`
v2.0 and the IPTC code `trainedAlgorithmicMedia`, plus an invisible watermark. None of this
was documented anywhere, which is the worst case: the provenance is embedded, so a
C2PA-aware viewer reveals it before the repository does.

Any AI-generated asset must be labelled wherever it is referenced, with its tool, date and
what in it is model-derived versus illustrative. Future artwork avoids state iconography
entirely.

Remediation is tracked in `ROADMAP.md` and not yet complete.

### 40. Outreach lists: institutions in public, individuals never
**2026-09-05.** Extends decision 26 after a request to put named politicians and
journalists in the README.

The public README carries the institutional map — ITRE, LIBE, IMCO, DG CONNECT, DG DIGIT,
the Telecom Working Party, ENISA, and each state's procurement body and cloud operator,
which are already columns in the dataset. Named individuals live in
`paper_book/contacts/`, gitignored, in official capacity only and with no personal contact
details.

Roles outlast people: "Chair, ITRE" survives an election and a name does not, so the
institutional map is also the more durable artefact.

**A near miss worth recording.** `.gitignore` contained `book/contacts/` rather than
`paper_book/contacts/` — the prefix was lost when the line was written, so the directory
intended to hold named individuals was never actually ignored. The security audit reported
it clean only because the directory did not yet exist. Found and fixed 2026-09-05 before
any file was created; the rule is now widened to `**/contacts/` and `*-contacts.md` so a
differently-named file cannot slip through. Verified with `git check-ignore`.

### 41. Deployment is staged, and the domain is deliberately unofficial-sounding
**2026-09-05.** Vercel, static build from `web/dist`, Git-integrated: `main` ships
production, every PR gets a preview URL.

Three stages, gated on verification rather than on readiness of the code:

| Stage | Where | Gate |
|---|---|---|
| Now | `*.vercel.app`, `noindex` via `robots.txt` | none — it is a working draft |
| Next | `*.vercel.app`, indexable | Tier-1 legal cells verified against primary sources |
| Then | `eu27.cloud` | sampling audit error rate measured |

**The domain choice follows from decision 25.** Unverified claims about what 27
jurisdictions require must not sit under a name that reads as a register.
`eusovereigncloud.eu`, `sovereigncloud.eu` and anything on `.eu` imply an EU institution;
`.org` implies an established NGO. `eu27.cloud` is short and topical, and `.cloud`
unmistakably signals a project. It pairs with a masthead line stating the work is
independent and unaffiliated.

`vercel.json` sets a strict CSP (`default-src 'self'`, no inline scripts, `frame-ancestors
'none'`), `nosniff`, `DENY` framing and a restrictive `Permissions-Policy`. The app makes
one network call — fetching its own data bundle — so nothing looser is needed. No
analytics.
