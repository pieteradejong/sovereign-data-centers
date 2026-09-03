# Austria - Sovereign Government Data Center Network

> Generated 2026-09-01 by `model/generate_countries.py` from the Dutch reference case
> (`countries/NL/GOAL.md`) and `model/eu27_parameters.csv`. Every number below is a **scaled working
> assumption**, not a sourced figure. Edit the CSVs in this directory and re-run
> `python3 model/capacity_model.py AT` to update the capacity numbers; edit
> `model/eu27_parameters.csv` or `model/scaling_rules.csv` and re-run the generator to update this file.

## 1. Working thesis

Austria does not need to become technologically autarkic. It needs enough independently controlled compute,
storage, networking, identity, cryptography and operational capability that the state can continue functioning
when foreign commercial infrastructure is unavailable, politically constrained, compromised, or no longer
trustworthy. The Dutch design rules (sovereignty is a stack, not a building; 3-5 separated regions; dual fibre
paths; no single hardware supplier; a first-class developer platform) are taken as the starting point and
adjusted below for what is structurally different about Austria.

## 2. Starting point

| | |
|---|---|
| Population | 9.20 m (Eurostat, 1 Jan 2025) |
| GDP | EUR 514 bn (2025, current prices) |
| Public administration employment (NACE O) | 333 k (Eurostat LFS 2025) |
| Non-household electricity price | 198.6 EUR/MWh (Eurostat, band IC, 2025-S2) |
| Renewables in electricity | 90.1% (2024) |
| Land area | 82,519 km2 |
| Live hyperscaler regions in-country | 1 |
| Existing government / sovereign cloud | BRZ (Bundesrechenzentrum) federal computing centre / BRZ Cloud; 2026 Digital Administration Guideline names digital sovereignty as core principle; no branded sovereign cloud |
| National digital identity (anchor workload) | ID Austria |
| Internet exchange / cable landings | VIX Vienna; landlocked (no subsea) |

Relative to the Dutch baseline: population x0.51, public administration x0.46,
GDP x0.44. Resulting design load: x0.48 the Dutch figure.

## 3. What is structurally different from the Dutch case

- **Expensive power (199 EUR/MWh vs. EU average ~184).** Power is the dominant OPEX line; free cooling, heat reuse, and siting near renewables or nuclear baseload move the economics more than server choice does. The model's power OPEX line is the number to attack first.

## 4. Workload demand (scaled from the Dutch baseline)

Scaling weights per workload class are in `model/scaling_rules.csv`; the Dutch rows they scale are in
`countries/NL/workloads_inputs.csv`. Frontline multiplier applied: no.

| Workload | Class | CPU cores | GPU eq. | Storage (PB) | Avail. factor |
|---|---|---:|---:|---:|---:|
| Digital identity / ID Austria | Critical government | 9,200 | 0 | 2.0 | 1.5 |
| Core government applications | Government | 26,800 | 0 | 8.8 | 1.35 |
| Data platforms & analytics | Government data | 16,600 | 40 | 28.5 | 1.25 |
| AI / sovereign model serving | AI | 7,900 | 224 | 5.3 | 1.3 |
| Defense classified compute | Defense | 15,300 | 128 | 7.6 | 1.5 |
| Cybersecurity / SOC / telemetry | Security | 10,900 | 16 | 12.4 | 1.4 |
| Scientific / public research | Research | 11,400 | 56 | 8.8 | 1.15 |

## 5. Capacity model output

| Metric | Value |
|---|---:|
| Physical servers | 2,739 (CPU 1,882 / GPU 131 / storage 726) |
| Rack equivalents | ~86 |
| IT critical load | 4.5 MW |
| Facility load (PUE 1.25) | 5.6 MW |
| Facility design load (+20% headroom) | **6.8 MW** |
| Sites by capacity / recommended | 1 / **3** (minimum 3) |
| Average design MW per site | 2.3 MW |
| Total CAPEX | **EUR 161 m** (facility EUR 68 m, IT EUR 79 m, network EUR 14 m) |
| Annual energy | 49,453 MWh |
| Annual OPEX | **EUR 17 m / yr** (power EUR 10 m, non-power EUR 7 m) |

Full table: `facility_summary.csv`.

## 6. Proposed geography (first-pass hypothesis)

Site posture: standard. Separation target: 50-100 km failure domains, dual fibre paths, distinct grid feeds.

| Region | Role | Share | Design MW | Racks | Facility CAPEX | Notes |
|---|---|---:|---:|---:|---:|---|
| East / Vienna - Lower Austria | Primary civil cloud | 40% | 2.7 | 35 | EUR 27 m | VIX connectivity, federal ministries, BRZ estate; Danube flood zoning applies. |
| Upper Austria / Linz | Sovereign secondary | 27% | 1.8 | 23 | EUR 18 m | Industrial grid, hydro power, 180 km from Vienna. |
| Styria / Graz | Government / continuity | 22% | 1.5 | 19 | EUR 15 m | Southern separation, research campus (TU Graz). |
| Tyrol - Salzburg / West | Strategic reserve | 10% | 0.7 | 9 | EUR 7 m | Alpine hydro; expansion or hardened reserve. |

These regions encode only the obvious constraints (capital estate, second metro, distance from the frontier,
fault or flood zone). They are to be replaced by the scored site selection in workstream A of the Dutch
`TODO.md` (grid capacity, flood risk, fibre, failure independence, physical security, land, cooling).

## 7. Geography and threat notes

Low seismic (Vienna Basin moderate); Danube/Alpine flood risk (2024); flat land concentrated in the east; winter power importer; gas-import dependent; neutral non-NATO; ~500 km from Ukraine

## 8. Recommendations specific to Austria

1. **Anchor on ID Austria.** Digital identity is the workload that, if it fails, stops every other
   government service; it belongs in the sovereign core first, active-active across at least two regions.
2. **Build on the existing estate, do not replace it.** BRZ (Bundesrechenzentrum) federal computing centre / BRZ Cloud is the
   institutional starting point; the sovereign core should be its next generation, with one governance owner.
3. **Site posture: standard.** Standard Tier III+ with 50-100 km separation is sufficient; spend the hardening budget on supply-chain assurance instead.
4. **Power strategy.** Power is the binding constraint; treat grid connection lead time and on-site generation as first-order site criteria.
5. **Hybrid tier.** Use in-country commercial regions for the non-critical tier, but keep identity, defense, security telemetry and registries in the sovereign core.

## 9. Open questions

- Replace scaled workload rows with real ministry/agency demand (see `countries/NL/CAPACITY_PLAN.md` for the method).
- Which body owns the sovereign core, and how are agencies compelled or incentivised to migrate?
- Which regions federate with EU partners for mutual disaster recovery, and which stay national-only?
- Site-size assumption: is the 12 MW planning unit right for Austria, or should sites be smaller?
