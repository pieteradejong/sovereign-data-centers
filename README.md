# Sovereign Data Centers for European States

Planning models and write-ups for national sovereign government data center networks, one per EU member state.
The Netherlands (`RijksCloud`) is the worked reference case; the other 26 are generated from it by a
parameterized model and are meant to be refined country by country.

## Layout

```
model/
  assumptions.csv            shared engineering/economic defaults (the Dutch "working assumptions")
  eu27_parameters.csv        one row per country: population, GDP, public-admin employment, power price,
                             renewables, land, frontline/grid/seismic flags, existing gov cloud, digital ID, IXPs
  scaling_rules.csv          how each workload class scales from the NL baseline (weights, floors, frontline multiplier)
  capacity_model.py          workloads -> servers -> racks -> MW -> sites -> CAPEX/OPEX, for any country dir
  generate_countries.py      builds countries/<ISO>/ inputs + GOAL.md for all 27, runs the model, writes SUMMARY.md
  eu27_results.csv           one result row per country (generated)
countries/
  SUMMARY.md                 cross-country table (generated)
  NL/                        the reference case: hand-written GOAL.md, xlsx model, inputs, infographic, TODO, plan
  DE/ FR/ ... (x26)          params.csv, workloads_inputs.csv, region_allocation_inputs.csv (generated inputs, edit freely)
                             GOAL.md (generated write-up), facility_summary.csv, region_allocation_output.csv (outputs)
```

## Running

```
python3 model/capacity_model.py NL          # one country
python3 model/capacity_model.py --all       # all, refreshes model/eu27_results.csv
python3 model/generate_countries.py         # regenerate the 26 derived countries from NL + parameters
```

Standard library only. `capacity_model.py` reproduces the Dutch xlsx exactly (5,691 servers, 14.2 MW design,
EUR 339 m CAPEX) when run on `countries/NL/`.

## Method

Every country inherits the Dutch assumption set (`model/assumptions.csv`) and overrides only what is
observably different: the Eurostat non-household electricity price and the minimum number of in-country sites
(2 for LU/MT/CY, 4 for DE/FR/IT/ES/PL/RO, 3 otherwise). Workload demand is the Dutch workload table scaled
per class by a blend of population, public-administration employment and GDP (`model/scaling_rules.csv`),
with a floor for small states (an identity platform or a SOC does not shrink linearly with population) and a
multiplier on defense/security for frontline states. Regions are first-pass geographic hypotheses that
encode only the obvious constraints; they are placeholders for the scored site selection described in
`countries/NL/TODO.md` workstream A.

The write-ups are generated, and say so at the top. To keep hand edits to a country's `GOAL.md`, rename it
(e.g. `GOAL.md` -> `ANALYSIS.md`) or stop running the generator for that country; the generator only ever
rewrites `GOAL.md`, `params.csv`, `workloads_inputs.csv` and `region_allocation_inputs.csv`, never `NL/`.

## What the first pass shows

- The EU-27 "sovereign core" tier is small: ~306 MW design load, ~125k servers, ~EUR 7.2 bn CAPEX,
  ~EUR 0.7 bn/yr OPEX across 86 sites. Germany alone is ~60 MW; nine states are under 3 MW.
- For states under ~3 MW, three in-country sites means sub-1 MW rooms, which is a closet, not a data center.
  The Dutch 3-region rule does not survive contact with Estonia, Slovenia or Luxembourg; those cases push
  toward fewer, hardened in-country sites plus an out-of-country reserve, i.e. the EU federation layer that
  is deliberately out of scope for now (Dutch `GOAL.md` section 16).
- Power price, not hardware, separates the OPEX outcomes: Ireland and Cyprus pay 3x Finland per MWh.
- Seven states have frontline exposure (EE, LV, LT, PL, FI, RO, BG); five have no live hyperscaler region and
  therefore no in-jurisdiction commercial tier for the hybrid model.

## Caveats

Same as the Dutch case, only more so: every input is a working assumption or a scaled placeholder, the
electricity prices are 2025-S2 band-IC averages rather than negotiated tariffs, and public-administration
employment is Eurostat NACE section O (excludes public health and education). The per-country sovereign-cloud
and digital-ID entries were researched in September 2026 and will date.

## Reference case

`countries/NL/GOAL.md` is the full write-up of the design philosophy, physical/logical architecture,
sovereignty stack, threat model and open questions. Read it first; the generated country files assume it.
