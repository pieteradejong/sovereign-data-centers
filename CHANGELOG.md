# Changelog

What changed and when. Reasoning for the choices behind these changes lives in
[`DECISIONS.md`](DECISIONS.md); this file records the work itself.

---

## 2026-09-07

### Changed — the contacts repo now lives at `contacts/`

`sovereign-data-centers-contacts` moved from a sibling directory under `~/dev/projects/` to `contacts/`
inside this working tree. It is still a separate private repo with its own `.git` and its own remote —
nothing was merged and no file crossed between repos. Reasoning in [`DECISIONS.md`](DECISIONS.md) #46.

Verified rather than assumed, because #40 and #45 both record this exact class of assumption going wrong:

| Check | Result |
|---|---|
| `git -C contacts remote -v`, `status -sb` | private remote intact, `main` in sync, one commit `9e0270f` |
| `git status --porcelain`, `git ls-files contacts` | both empty — the outer repo sees nothing |
| `git check-ignore -v contacts/NL/list.md` | `.gitignore:38:**/contacts/` |
| `git add -f contacts/` on a scratch clone with the real files | one mode-160000 gitlink, 180 bytes; 473 distinctive tokens from `NL/list.md`, zero in the staged diff |
| `git clean -nxfd` | does **not** list `contacts/` — one `-f` refuses to remove a nested repo |
| `git clean -nxffd` | **does** list it. The one new hazard; keep the private repo pushed |
| 18 name strings from the private files vs. all 21 public commits | only `European Parliament` and `Tweede Kamer` — institutions, same result as #45's audit |
| `./test.sh --no-e2e` | passes; the generators walk `countries/` only |

The `.gitignore` rules (`**/contacts/`, `*-contacts.md`) stay, demoted to a second layer behind the
nested `.git`, and the comment block above them now says so.

### Removed — the empty `book/contacts/`

Left behind by the `paper_book/` → `book/` rename (#38) and the near miss in #40. An empty directory
called `contacts` in this repo is a trap for precisely the mistake the ignore rules exist to prevent.

---

## 2026-09-06

### Repository lineage — where the frontier note came from

The note was first published as a standalone public repo, `pieteradejong/dutch_frontier_model`, before it
was clear it belonged here. That repo is now **archived** and read-only, with its description pointing at
`countries/NL/FRONTIER-MODEL.md` so the old URL still leads somewhere useful. Nothing was deleted: the
single commit remains readable, and the local working copy was removed once the content landed here.

Archiving locks a repo immediately, so setting that forwarding description required unarchiving it for
one call and re-archiving straight after. Worth knowing before archiving anything else.

### Audited — security and privacy, round two

Second full audit, 2026-09-06, covering the working tree **and** all 21 commits rather than the current
state alone. Findings and the verification detail are in [`ROADMAP.md`](ROADMAP.md); the summary is that
nothing is disclosed and three of the four findings are documentation drift.

The audit also closed out bookkeeping the repo had been carrying: the four 2026-09-04 findings were
remediated in `f03fde7` but `ROADMAP.md` still listed them as open, and it still sent readers to
`paper_book/contacts/` for named individuals after #45 moved them into a private repo. Both corrected.

The contacts split (#45) landed the same day and was verified rather than taken on trust — the private
repo is private, is pushed and in sync with origin, and no token from it appears anywhere in this
repository's history. See ROADMAP for why the "pushed" half of that check is the one that matters.

**Open, and deliberately not fixed here:** 56 generated binaries (27 briefing PDFs, 27 infographic PNGs,
12.7 MB) are committed even though `README.md` and #41 both say they never are. That needs a decision
about intent, not a patch — see ROADMAP finding 1.

### Added — the frontier-model note (`countries/NL/FRONTIER-MODEL.md`)

An authored companion to the RijksCloud capacity plan answering "what would it take for the Netherlands
to develop its own frontier model, or at least something suitable?" — the question that comes up every
time the sovereign cloud plan is discussed. Drafted as a standalone repo, merged here because it only
makes sense next to the NL reference case. Reasoning in DECISIONS.md #44.

Three tiers, costed: sovereign *deployment* capability (€50-150M, 18 months, fits inside RijksCloud's
existing GPU envelope), sovereign mid-scale pretraining (€1.5-3B, 5 years, Eemshaven), and frontier
parity (€15-30B+, only as lead partner in an EU gigafactory consortium). Conclusion: frontier parity is
not unilaterally feasible and is the wrong goal; the binding constraints are grid capacity, a
Dutch-language corpus ~1% the size of a frontier training corpus, and training talent.

The note is deliberately framed as a **separate** ask from RijksCloud — ~150 MW against 14.2 MW, $4-6B
against €339M — because the two compete for the same Dutch grid connections and bundling them would sink
the government-cloud case.

Unlike everything else under `countries/`, this file is authored, not generated. `run.sh data` does not
write it; the name is one `generate_countries.py` never touches, like `CAPACITY_PLAN.md` and `TODO.md`.
Its cost figures are reconstructed order-of-magnitude estimates, labelled as such, and held to a lower
evidentiary standard than the model's parameters.

## 2026-09-04 (later)

### Added — the book (`book/`)

`./run.sh book` typesets an A5 print edition with typst. Structure follows DECISIONS.md #27: Parts I, II
and V are authored prose in `manuscript/`, Parts III (the 27-country gazetteer) and IV (reference tables)
are generated by `book/build.py` from `web/public/data/eu27.json` — the same dict the briefs and the web
app render from, so the book cannot drift from the model.

| Path | What it is |
|---|---|
| `book/build.py` | Renderer and CLI. Standard library only, like the rest of the model |
| `book/templates/style.typ` | Mono interior (#28), two page geometries (#40), shared table helpers |
| `book/manuscript/` | Parts I, II and V — **scaffolds**, spine only, ~24k words still to write |
| `book/build/` | Output. Gitignored (#41) |

Current output: 81 pages, 703 KB. Parts III and IV are complete; the authored parts are chapter headings
and opening paragraphs.

### Added — per-country PDF briefs

`./run.sh export` builds 27 standalone A4 briefs into `book/build/briefs/<ISO>.pdf` (1.05 MB total, about
40 KB each, ~2.5 s for all 27). Same renderer as the book's gazetteer chapter — `country_entry(c,
standalone=True)` promotes the headings and swaps the wrapper (#39).

`./run.sh build` now also writes them into `web/dist/briefs/`, served from the app at `/briefs/<ISO>.pdf`
(#42). Skipped with a warning rather than failing when typst is absent.

### Added — `OUTREACH.md`

Institutional distribution map: policy owner, operator, certification authority, procurement vehicle,
parliamentary scrutiny and press desks for all 27 member states, plus an EU-level tier and a send order.
Built on the institutional columns already in `eu27_parameters.csv`, with a provenance table marking which
rows are repo-sourced and which need verification before send (#43).

### Fixed — two bugs surfaced by rendering the briefs

1. **`seismic` is not a boolean.** It holds `"low"` / `"moderate"` / `"high"`, so a truthiness test on it
   was true for all 27 countries and every brief printed a seismic flag — including Germany, which
   `SUMMARY.md` correctly shows with none. The flag rule now matches the model's own
   (`country_data.py:125`): only `"high"` counts. Affects 6 countries, not 27.
2. **`~` is a non-breaking space in typst.** It was missing from the escape set, so "EU average ~184"
   printed as "EU average 184" — silently dropping the approximation marker from a figure. Added to
   `_SPECIAL`.

Both were invisible in the model, the JSON bundle and the web app; only typesetting the value exposed
them. Consistent with #36 — rendering it and looking at it is load-bearing.

### Changed

- **`paper_book/` → `book/`** (#38). `run.sh`, `.gitignore` and DECISIONS.md #26 updated. Both commands
  that referenced the old path had been broken since they were written.
- **`run.sh export`** now points at `book/build.py --briefs` instead of the never-written
  `model/export_artifacts.py`. Help text corrected: it builds briefs, not "reports and posters".
- **`init.sh`** no longer claims Chrome is needed for PDF export. It is needed for the Playwright E2E
  suite only; the typst warning now covers `export` as well as `book`.

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
