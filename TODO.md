# TODO (EU-27)

Country-level workstreams live in `countries/NL/TODO.md` (the reference case) and apply to every country.
This file tracks the cross-country work.

## Model
- [x] Parameterized capacity model reproducing the Dutch xlsx (`model/capacity_model.py`)
- [x] EU-27 parameter dataset from Eurostat (`model/eu27_parameters.csv`)
- [x] Scaling rules from the NL baseline with small-state floors and frontline multiplier
- [ ] Replace population/GDP scaling with real per-country government IT inventories where published
      (FR DINUM, DE ITZBund, IT PSN migration data, PL RChO, EE RIT are the likeliest sources)
- [ ] Per-country PUE and facility CAPEX (climate and seismic design change both)
- [ ] Sensitivity: site size (12 MW unit), replication factor, headroom, utilization
- [ ] 5- and 10-year growth per country

## Geography
- [ ] Replace the first-pass regions in `generate_countries.py` with scored site selection per country
- [ ] Seismic and flood zoning as hard exclusions in the scoring
- [ ] Grid connection lead time as a scored criterion (IE, NL, DE, BE, ES are all constrained)

## Federation (deferred by decision, Sept 2026)
- [ ] Out-of-country reserve for frontline and micro states (EE data-embassy pattern)
- [ ] Pooled sovereign capacity for states under ~3 MW
- [ ] Mutual DR pairs and treaty basis

## Write-ups
- [ ] Hand-edit the five large states (DE, FR, IT, ES, PL) into full analyses like `countries/NL/GOAL.md`
- [ ] Verify the sovereign-cloud and digital-ID entries in `eu27_parameters.csv` against primary sources
