# Changelog

What changed and when. Reasoning for the choices behind these changes lives in
[`DECISIONS.md`](DECISIONS.md); this file records the work itself.

---

## 2026-09-04

### Added — web application (`web/`)

An interactive visualization of the EU-27 dataset. React 19, Vite 8, TypeScript 6, Vitest 5, Tailwind 4,
D3 7, all exactly pinned.

| Route | What it shows |
|---|---|
| `/` | EU-27 totals, the small-state cliff, the binding-constraint finding |
| `/matrix` | Sovereignty readiness matrix — 27 × 8 diverging heatmap, sortable, cells link to source text |
| `/workloads` | Country × workload class heatmap, absolute / row-normalized toggle |
| `/scenario` | Live sandbox — six assumption sliders recompute all 27 countries in the browser |
| `/countries` | Index of all member states |
| `/country/:iso` | Full briefing: capacity, geography, legal posture, landscape, migration path |
| `/methodology` | What the model is, what it is not, and the shared assumption table |

The whole dataset is ~40 KB gzipped, so it ships client-side in one request. No API, no server.

### Added — tooling scripts

- **`init.sh`** — version-checked prerequisites, dependency install, data bundle generation. Idempotent,
  verified from a deleted `node_modules`.
- **`run.sh`** — `dev` (default), `build`, `preview`, `test`, `lint`, `format`, `type-check`, `data`,
  `export`, `book`, `clean`, `health`, `help`.
- **`test.sh`** — the full gate, eight stages, cheapest first, failing on the first problem.
- **`.build-epoch`** — the pinned generation date, read by all three scripts.

### Added — testing

- **TS/Python parity suite.** Asserts `web/src/model/capacity.ts` reproduces `model/eu27_results.csv` for
  all 27 countries. Gates the scenario sandbox. 30 assertions.
- **Playwright suite.** 15 tests: rendered-data assertions, axe accessibility on all seven routes, and a
  375 px responsive check. Drives the installed Chrome rather than downloading Chromium.
- Earlier the same week: 15 stdlib Python tests covering model invariants, CSV integrity, referential
  integrity and generator determinism.

### Added — documentation

- **`DECISIONS.md`** — 37 dated ADR-style entries.
- **`CHANGELOG.md`** — this file.

### Fixed — accessibility

- `aria-sort` moved from the sort button to the `<th>` that owns it.
- `--color-fg-muted` darkened from `#898781` to `#6f6d66`. The design-system value measures 3.21:1 against
  the page — correct for axis ticks at the 3:1 graphical threshold, failing AA as body text.
- Toggle button text changed from white on terracotta (3.12:1) to slate (4.85:1).

### Fixed — legibility

- Matrix column headers were clipped to `w-6`, rendering every dimension name as "Sov…", "Cert…", "Hyp…".
  Found by screenshotting the built page; every automated check passed while the chart was unreadable.

### Fixed — tooling

- `SOURCE_DATE_EPOCH` was a duplicated literal in two scripts and missing from `init.sh`, so initialising a
  fresh clone made the committed bundle look stale. Centralised in `.build-epoch`.
- The E2E preview server moved to port 4823 with `strictPort`. Another workspace project was serving 4173;
  Playwright silently reused it and tested a different application.
- Playwright's `channel: 'chrome'` hardcodes `/Applications/Google Chrome.app`; this machine has Chrome at
  `/Applications/Chrome.app`. The binary is now resolved explicitly, with Brave and Edge as fallbacks.

### Corrected — figures that were wrong

Both found by asserting them in tests rather than repeating them:

- **"`min_sites` binds for 26 of 27 countries"** → the real figure is **24** strictly floor-bound. Germany
  alone exceeds its floor (6 sites against 4); France and Italy tie theirs exactly at 4. The "26" came
  from an early survey that counted ties as floor-bound.
- **"Nine states fall below 1 MW per site"** → the real figure is **8**. This conflated two different
  metrics; `README.md` separately claimed nine states under 3 MW total design load, also wrong, also 8.
  The same eight countries satisfy both: SI, EE, LV, CY, MT, LU, LT, HR.

---

## 2026-09-03

### Added — legal and regulatory dataset

`model/eu27_parameters.csv` extended from 17 to 25 columns, researched for all 27 member states:
`legal_instrument`, `certification_scheme`, `data_classification`, `procurement_vehicle`,
`hyperscaler_gov_exposure`, `gov_cloud_maturity`, plus the ordinals `certification_strength` and
`hyperscaler_dependency` that the sovereignty matrix scores from.

These are **unverified research**, not sourced fact — see `DECISIONS.md` #25 for the gate that must pass
before publication.

### Added — migration phasing

`model/migration_phases.csv` maps the seven workload classes to four phases (sovereign core, security and
defense, state record, elective). `capacity_model.py` emits `countries/<ISO>/migration_phases.csv` with
servers, MW, CAPEX and cumulative share per phase. No new sizing math: it groups results the model already
computed, and phase CAPEX sums to the model's total.

### Added — country briefs extended from 9 to 12 sections

Sections 10–12 cover legal and regulatory posture, current state and provider landscape, and a costed
migration path. Prose varies on certification strength, hyperscaler dependency and government-cloud
maturity rather than reading identically 27 times.

### Added — the fact layer

- `model/country_data.py` assembles every fact about a country into one dict.
- `model/export_json.py` writes `web/public/data/eu27.json` from that same dict.
- `write_goal()` refactored into a pure dict → markdown renderer, 70 lines shorter. Verified
  behaviour-preserving: regenerating all 27 countries produced a byte-for-byte zero diff.

### Added — reproducibility

Generated files stamp their date from `SOURCE_DATE_EPOCH` when set. Previously every run rewrote 27 files
with a new date, burying real changes and making "regenerating changes nothing" untestable.

### Fixed — CSV corruption in the published output

The `IT` and `ES` rows had unquoted commas in the `ixp` field, shifting every later field. Italy's
published brief printed " Sicily" as its entire threat-notes section, and Spain's printed " Grace Hopper)
and Barcelona (2Africa". A field-count test now catches this class of defect.

### Fixed — writers disagreeing on row order

`model/eu27_results.csv` was written by both `generate_countries.py` (NL first) and
`capacity_model.py --all` (alphabetical). Any golden-file comparison would have been pure noise. Both now
sort by ISO.

### Fixed — an incorrect claim about Ireland

The exposure entry stated that all three hyperscalers anchor their principal EU regions in Dublin. AWS and
Azure do; Google's `europe-west1` is in Belgium. The existing `hyperscaler_regions_live=2` was right and
the prose was wrong.

### Added — CI

`.github/workflows/ci.yml` runs the Python suite and fails if committed generated files are stale.

---

## 2026-09-01 and earlier

The repository existed as three commits with the entire EU-27 generalization untracked: both Python
scripts, the parameter dataset, all 26 generated country directories and `SUMMARY.md`. Committing that
baseline was the prerequisite for everything above, since regenerating 27 files against an uncommitted
tree produces an unreviewable diff.

Prior history: a single-country Dutch capacity model (`GOAL.md`, an xlsx, three input CSVs, an
infographic), generalized to all 27 member states by a stdlib-only Python model.
