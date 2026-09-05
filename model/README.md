# The model

Stdlib-only Python. `capacity_model.py` turns a workload table into servers, racks, megawatts, sites and
cost; `generate_countries.py` scales the Dutch baseline to the other 26 member states and writes their
briefs; `country_data.py` assembles every fact about a country into the one dict that the briefs, the JSON
bundle, the web app and the exported artefacts all render from.

## How to read the data files

**Not everything in here has the same standing.** Three different kinds of claim live in these CSVs, and
conflating them is the easiest way to misuse this project.

| Kind | Files and columns | Standing |
|---|---|---|
| **Sourced statistics** | `eu27_parameters.csv`: `population_m`, `gdp_eur_bn`, `gov_employment_k`, `elec_price_eur_mwh`, `renewables_pct`, `land_km2` | From Eurostat, with the dataset and vintage named in each country's brief. Checkable. |
| **Working assumptions** | `assumptions.csv`, and everything derived from it | Plausible planning figures, not sourced. Every row says so in its `Source / Status` column. |
| **Unverified research** | `eu27_parameters.csv`: `legal_instrument`, `certification_scheme`, `data_classification`, `procurement_vehicle`, `hyperscaler_gov_exposure`, `sovereign_cloud_initiative`, `digital_id`, `ixp`, `threat_notes` | Compiled September 2026 from public policy documents by one researcher. **Not checked against primary instruments.** |
| **Author's judgements** | `eu27_parameters.csv`: `gov_cloud_maturity`, `certification_strength`, `hyperscaler_dependency` | Ordinal ratings assigned by the author. **Not official ratings, and not measured.** Ireland and Denmark are rated `critical` because someone decided that, not because a body published it. |

Every row of `eu27_parameters.csv` carries a `data_status` column repeating this, because GitHub renders a
CSV as a clean table that looks more authoritative than it is.

## Why the ratings are not summed

The eight sovereignty-matrix dimensions are shown side by side and never combined into a score.
Certification strength and seismic risk are not commensurable, and a single number would imply a precision
this dataset does not have while being the first thing quoted out of context. See `DECISIONS.md` #10.

## Reproducibility

Generated files stamp their date from `SOURCE_DATE_EPOCH`, pinned in `.build-epoch`, so regenerating on a
different day does not rewrite 27 files with a new date and bury the real changes. `./test.sh` asserts that
running the generator twice is a byte-for-byte no-op.

## Files

```
capacity_model.py      workloads -> servers -> racks -> MW -> sites -> CAPEX/OPEX
country_data.py        assembles one country's facts into a dict; scores the matrix ordinals
generate_countries.py  scales NL to the other 26, writes briefs and SUMMARY.md
export_json.py         writes web/public/data/eu27.json from the same dict
export_artifacts.py    renders per-country PNG infographics and PDF briefings
assumptions.csv        shared engineering and economic defaults
eu27_parameters.csv    one row per member state; see the table above before using it
scaling_rules.csv      how each workload class scales from the Dutch baseline
migration_phases.csv   workload class -> migration phase
eu27_results.csv       one result row per country (generated; the golden file for tests)
```
