# Verification

The one thing gating everything public-facing: whether the legal and regulatory claims in
`model/eu27_parameters.csv` have been checked against primary sources. `ROADMAP.md` states the
gate; this file is how the work is done and where it currently stands.

**Status: 0 of 189 cells sourced.** Run `./run.sh sources` for the live figure.

---

## What is and is not at issue

The capacity figures are openly scaled placeholders. The model says so, the briefs say so, the
posters print it on their face, and nobody is misled by a number that announces its own basis.

The legal and regulatory columns are a different kind of claim. They assert what 27 real
jurisdictions **require** — the governing instrument, the certification regime, the
classification ladder, the procurement route. They were researched from public policy documents
by one person and have not been checked against the instruments themselves. That is fine for a
research repository that says so and offers a corrections channel, which is what exists today.
It is not fine for an indexed site, a custom domain, a printed book, or anything handed to an
official (`DECISIONS.md` #25).

The three ordinal columns — `gov_cloud_maturity`, `certification_strength`,
`hyperscaler_dependency` — are author judgements derived from the columns above (#10). They are
**disclosed as judgements, never cited**. Attaching a source row to one is a validation error,
because a sourced-looking judgement is precisely the dishonesty this workstream exists to
prevent.

## The ledger

`model/sources.csv`, one row per sourced claim:

| Field | Meaning |
|---|---|
| `country` | ISO-2 code, must exist in `eu27_parameters.csv` |
| `column` | one of the seven sourceable columns below |
| `url` | absolute `http(s)` URL of the page or document consulted |
| `publisher` | the body that published it, as it names itself |
| `retrieved` | `YYYY-MM-DD`, the date the page was read |
| `confidence` | `primary`, `official`, or `secondary` |
| `quote` | **the words on the page that support the cell** |

```csv
country,column,url,publisher,retrieved,confidence,quote
EE,legal_instrument,https://www.riigiteataja.ee/en/eli/...,Riigi Teataja,2026-09-08,primary,"Public information holders shall ..."
```

**The quote is the requirement.** A URL shows that a page exists, not that it says what the cell
claims. It also survives the page being rewritten: a quote that no longer appears at its URL is a
finding, whereas a bare link that now says something else looks exactly like a verified cell.
Rows with a quote under 20 characters fail validation.

Rows are sorted by `(country, column)` so a diff shows what was added rather than where it
landed.

## The tiered rule

| Tier | Columns | What counts |
|---|---|---|
| **1** — asserts a legal obligation | `legal_instrument`, `data_classification`, `certification_scheme` | the instrument itself: the statute, decree or scheme document. `confidence` must be `primary`. |
| **2** — describes what the state does | `sovereign_cloud_initiative`, `procurement_vehicle`, `digital_id`, `hyperscaler_gov_exposure` | an official government page. `primary` or `official`. |
| — **not sourceable** | `gov_cloud_maturity`, `certification_strength`, `hyperscaler_dependency` | author judgements; disclosed in the briefs and the CSVs, never cited |

`secondary` (press, vendor material, an aggregator) never satisfies tier 1. It is allowed to be
recorded for tier 2 while a better source is found, and it is visible as such in the ledger.

7 sourceable columns x 27 member states = **189 cells**.

## Working through it

```bash
./run.sh sources            # coverage report; fails on an unusable row
python3 model/sources.py --strict   # the end state: fails while any cell is unsourced
```

One country at a time, tier 1 first:

1. Read the cell in `model/eu27_parameters.csv`.
2. Find the instrument. National legal gazette first (Riigi Teataja, Legifrance,
   Gesetze-im-Internet, and so on), the ministry's own page second.
3. Add the row, with the sentence that carries the claim as the `quote`.
4. If the source contradicts the cell, **fix the cell**, and note it in `CHANGELOG.md`. The point
   of the exercise is to find these, so finding one is the process working.
5. Raise `COVERAGE_FLOOR` in `tests/test_sources.py` in the same commit.

`COVERAGE_FLOOR` is a ratchet and may only be raised. `--strict` is the end state `ROADMAP.md`
step 3 asks for and already works; it is not wired into CI yet, because a gate that fails on the
day it lands is a gate that gets disabled on the day after (`DECISIONS.md` #54).

## Then: the sampling audit

Coverage is not accuracy. Once a column is fully sourced, a random sample of its cells is
re-checked independently, and the disagreement rate is published per column. That measured error
rate — confidence as a number rather than a feeling — is what opens deployment stage 3 and the
book. Sourcing every cell only makes it possible to measure.

## Separately: the Eurostat figures

`population_m`, `gdp_eur_bn`, `gov_employment_k`, `elec_price_eur_mwh`, `renewables_pct` and
`land_km2` are Eurostat values, already described as sourced. They need a **retrieval date and a
re-pull against the public API** (`ROADMAP.md` step 4), not the tiered treatment above — a figure
carrying a dataset code and a date is verifiable by anyone in a way a paraphrased legal
requirement is not.

## What this gates

| Stage | Gate |
|---|---|
| Indexing — delete the two `Disallow` lines from `web/public/robots.txt` | tier-1 cells sourced, Eurostat re-pulled |
| `eu27.cloud` | sampling audit error rate measured |
| The printed book | sampling audit error rate measured |
| Institutional outreach | the entry for that body's own country, verified |

The last row is the practical one. The first thing any of these bodies checks is what the
repository says about them.
