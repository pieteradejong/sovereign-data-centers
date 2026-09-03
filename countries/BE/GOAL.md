# Belgium - Sovereign Government Data Center Network

> Generated 2026-09-01 by `model/generate_countries.py` from the Dutch reference case
> (`countries/NL/GOAL.md`) and `model/eu27_parameters.csv`. Every number below is a **scaled working
> assumption**, not a sourced figure. Edit the CSVs in this directory and re-run
> `python3 model/capacity_model.py BE` to update the capacity numbers; edit
> `model/eu27_parameters.csv` or `model/scaling_rules.csv` and re-run the generator to update this file.

## 1. Working thesis

Belgium does not need to become technologically autarkic. It needs enough independently controlled compute,
storage, networking, identity, cryptography and operational capability that the state can continue functioning
when foreign commercial infrastructure is unavailable, politically constrained, compromised, or no longer
trustworthy. The Dutch design rules (sovereignty is a stack, not a building; 3-5 separated regions; dual fibre
paths; no single hardware supplier; a first-class developer platform) are taken as the starting point and
adjusted below for what is structurally different about Belgium.

## 2. Starting point

| | |
|---|---|
| Population | 11.90 m (Eurostat, 1 Jan 2025) |
| GDP | EUR 642 bn (2025, current prices) |
| Public administration employment (NACE O) | 447 k (Eurostat LFS 2025) |
| Non-household electricity price | 186.6 EUR/MWh (Eurostat, band IC, 2025-S2) |
| Renewables in electricity | 31.3% (2024) |
| Land area | 30,452 km2 |
| Live hyperscaler regions in-country | 2 |
| Existing government / sovereign cloud | Federal G-Cloud (BOSA/Smals community cloud); Smals selected Google Cloud as public-cloud pillar (Jun 2026) under federal sovereignty/portability rules |
| National digital identity (anchor workload) | Belgian eID card + itsme (CSAM) |
| Internet exchange / cable landings | BNIX Brussels; transit via Amsterdam/London |

Relative to the Dutch baseline: population x0.66, public administration x0.62,
GDP x0.55. Resulting design load: x0.61 the Dutch figure.

## 3. What is structurally different from the Dutch case

- No structural flags differ from the Dutch reference case; the Dutch design rules transfer directly.

## 4. Workload demand (scaled from the Dutch baseline)

Scaling weights per workload class are in `model/scaling_rules.csv`; the Dutch rows they scale are in
`countries/NL/workloads_inputs.csv`. Frontline multiplier applied: no.

| Workload | Class | CPU cores | GPU eq. | Storage (PB) | Avail. factor |
|---|---|---:|---:|---:|---:|
| Digital identity / Belgian eID card + itsme | Critical government | 11,900 | 0 | 2.6 | 1.5 |
| Core government applications | Government | 35,300 | 0 | 11.6 | 1.35 |
| Data platforms & analytics | Government data | 21,100 | 48 | 36.2 | 1.25 |
| AI / sovereign model serving | AI | 9,900 | 280 | 6.6 | 1.3 |
| Defense classified compute | Defense | 19,800 | 168 | 9.9 | 1.5 |
| Cybersecurity / SOC / telemetry | Security | 14,300 | 24 | 16.2 | 1.4 |
| Scientific / public research | Research | 14,300 | 72 | 11.0 | 1.15 |

## 5. Capacity model output

| Metric | Value |
|---|---:|
| Physical servers | 3,528 (CPU 2,430 / GPU 167 / storage 931) |
| Rack equivalents | ~110 |
| IT critical load | 5.8 MW |
| Facility load (PUE 1.25) | 7.3 MW |
| Facility design load (+20% headroom) | **8.7 MW** |
| Sites by capacity / recommended | 1 / **3** (minimum 3) |
| Average design MW per site | 2.9 MW |
| Total CAPEX | **EUR 207 m** (facility EUR 87 m, IT EUR 102 m, network EUR 18 m) |
| Annual energy | 63,564 MWh |
| Annual OPEX | **EUR 21 m / yr** (power EUR 12 m, non-power EUR 9 m) |

Full table: `facility_summary.csv`.

## 6. Proposed geography (first-pass hypothesis)

Site posture: standard. Separation target: 50-100 km failure domains, dual fibre paths, distinct grid feeds.

| Region | Role | Share | Design MW | Racks | Facility CAPEX | Notes |
|---|---|---:|---:|---:|---:|---|
| Brussels - Flemish Brabant | Primary civil cloud | 40% | 3.5 | 45 | EUR 35 m | Federal institutions, BNIX, Smals/G-Cloud estate; Elia connection queue is the constraint. |
| Wallonia / Mons - Charleroi | Sovereign secondary | 27% | 2.4 | 30 | EUR 24 m | Existing hyperscale cluster (St. Ghislain) proves power and fibre; south of Meuse flood zone. |
| Antwerp - Limburg | Government / continuity | 22% | 2.0 | 25 | EUR 20 m | Northern separation, port/industrial grid. |
| Liege - Ardennes | Strategic reserve | 10% | 0.9 | 11 | EUR 9 m | Eastern reserve; avoid 2021 Vesdre/Ourthe flood plains. |

These regions encode only the obvious constraints (capital estate, second metro, distance from the frontier,
fault or flood zone). They are to be replaced by the scored site selection in workstream A of the Dutch
`TODO.md` (grid capacity, flood risk, fibre, failure independence, physical security, land, cooling).

## 7. Geography and threat notes

No seismic; dense and land-constrained; Meuse flood risk (2021); Elia grid connection queues around Brussels/Antwerp; nuclear extension to 2035; gas/electricity import dependent; NATO/EU HQ host (hybrid/cyber target)

## 8. Recommendations specific to Belgium

1. **Anchor on Belgian eID card + itsme.** Digital identity is the workload that, if it fails, stops every other
   government service; it belongs in the sovereign core first, active-active across at least two regions.
2. **Build on the existing estate, do not replace it.** Federal G-Cloud (BOSA/Smals community cloud) is the
   institutional starting point; the sovereign core should be its next generation, with one governance owner.
3. **Site posture: standard.** Standard Tier III+ with 50-100 km separation is sufficient; spend the hardening budget on supply-chain assurance instead.
4. **Power strategy.** Power is not the binding constraint; optimise for fibre diversity and failure-domain separation.
5. **Hybrid tier.** Use in-country commercial regions for the non-critical tier, but keep identity, defense, security telemetry and registries in the sovereign core.

## 9. Open questions

- Replace scaled workload rows with real ministry/agency demand (see `countries/NL/CAPACITY_PLAN.md` for the method).
- Which body owns the sovereign core, and how are agencies compelled or incentivised to migrate?
- Which regions federate with EU partners for mutual disaster recovery, and which stay national-only?
- Site-size assumption: is the 12 MW planning unit right for Belgium, or should sites be smaller?
