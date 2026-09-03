# Denmark - Sovereign Government Data Center Network

> Generated 2026-09-01 by `model/generate_countries.py` from the Dutch reference case
> (`countries/NL/GOAL.md`) and `model/eu27_parameters.csv`. Every number below is a **scaled working
> assumption**, not a sourced figure. Edit the CSVs in this directory and re-run
> `python3 model/capacity_model.py DK` to update the capacity numbers; edit
> `model/eu27_parameters.csv` or `model/scaling_rules.csv` and re-run the generator to update this file.

## 1. Working thesis

Denmark does not need to become technologically autarkic. It needs enough independently controlled compute,
storage, networking, identity, cryptography and operational capability that the state can continue functioning
when foreign commercial infrastructure is unavailable, politically constrained, compromised, or no longer
trustworthy. The Dutch design rules (sovereignty is a stack, not a building; 3-5 separated regions; dual fibre
paths; no single hardware supplier; a first-class developer platform) are taken as the starting point and
adjusted below for what is structurally different about Denmark.

## 2. Starting point

| | |
|---|---|
| Population | 5.99 m (Eurostat, 1 Jan 2025) |
| GDP | EUR 418 bn (2025, current prices) |
| Public administration employment (NACE O) | 166 k (Eurostat LFS 2025) |
| Non-household electricity price | 121.6 EUR/MWh (Eurostat, band IC, 2025-S2) |
| Renewables in electricity | 79.7% (2024) |
| Land area | 41,987 km2 |
| Live hyperscaler regions in-country | 1 |
| Existing government / sovereign cloud | No sovereign cloud product; Statens It central hosting; Joint Government Digital Strategy 2026-29 + DKK 80m digital-sovereignty action plan; Ministry of Digitalisation Microsoft phase-out (2025) |
| National digital identity (anchor workload) | MitID |
| Internet exchange / cable landings | DIX Lyngby and Netnod Copenhagen; Blaabjerg/Esbjerg Atlantic landings (Havfrue/AEC-2) |

Relative to the Dutch baseline: population x0.33, public administration x0.23,
GDP x0.36. Resulting design load: x0.33 the Dutch figure.

## 3. What is structurally different from the Dutch case

- No structural flags differ from the Dutch reference case; the Dutch design rules transfer directly.

## 4. Workload demand (scaled from the Dutch baseline)

Scaling weights per workload class are in `model/scaling_rules.csv`; the Dutch rows they scale are in
`countries/NL/workloads_inputs.csv`. Frontline multiplier applied: no.

| Workload | Class | CPU cores | GPU eq. | Storage (PB) | Avail. factor |
|---|---|---:|---:|---:|---:|
| Digital identity / MitID | Critical government | 6,000 | 0 | 1.3 | 1.5 |
| Core government applications | Government | 15,500 | 0 | 5.1 | 1.35 |
| Data platforms & analytics | Government data | 12,100 | 24 | 20.7 | 1.25 |
| AI / sovereign model serving | AI | 6,400 | 184 | 4.3 | 1.3 |
| Defense classified compute | Defense | 10,000 | 88 | 5.0 | 1.5 |
| Cybersecurity / SOC / telemetry | Security | 6,600 | 8 | 7.6 | 1.4 |
| Scientific / public research | Research | 9,300 | 48 | 7.1 | 1.15 |

## 5. Capacity model output

| Metric | Value |
|---|---:|
| Physical servers | 1,861 (CPU 1,258 / GPU 100 / storage 503) |
| Rack equivalents | ~58 |
| IT critical load | 3.2 MW |
| Facility load (PUE 1.25) | 3.9 MW |
| Facility design load (+20% headroom) | **4.7 MW** |
| Sites by capacity / recommended | 1 / **3** (minimum 3) |
| Average design MW per site | 1.6 MW |
| Total CAPEX | **EUR 114 m** (facility EUR 47 m, IT EUR 57 m, network EUR 10 m) |
| Annual energy | 34,494 MWh |
| Annual OPEX | **EUR 9 m / yr** (power EUR 4 m, non-power EUR 5 m) |

Full table: `facility_summary.csv`.

## 6. Proposed geography (first-pass hypothesis)

Site posture: standard. Separation target: 50-100 km failure domains, dual fibre paths, distinct grid feeds.

| Region | Role | Share | Design MW | Racks | Facility CAPEX | Notes |
|---|---|---:|---:|---:|---:|---|
| Copenhagen / Zealand | Primary civil cloud | 40% | 1.9 | 24 | EUR 19 m | Statens It estate, DIX/Netnod; Zealand grid queue and storm-surge zoning. |
| Jutland / Fredericia - Aarhus | Sovereign secondary | 27% | 1.3 | 16 | EUR 13 m | Wind surplus, existing hyperscale campuses, Atlantic cable landings. |
| Funen / Odense | Government / continuity | 22% | 1.1 | 13 | EUR 11 m | Central, separated from both metros. |
| North Jutland | Strategic reserve | 10% | 0.5 | 6 | EUR 5 m | Cheapest power, reserve/expansion. |

These regions encode only the obvious constraints (capital estate, second metro, distance from the frontier,
fault or flood zone). They are to be replaced by the scored site selection in workstream A of the Dutch
`TODO.md` (grid capacity, flood risk, fibre, failure independence, physical security, land, cooling).

## 7. Geography and threat notes

Negligible seismic; low-lying storm-surge risk; land available in Jutland; wind surplus and strong interconnectors (Viking Link) but Zealand connection queues; energy net exporter; Baltic Sea cable/pipeline sabotage exposure; NATO

## 8. Recommendations specific to Denmark

1. **Anchor on MitID.** Digital identity is the workload that, if it fails, stops every other
   government service; it belongs in the sovereign core first, active-active across at least two regions.
2. **Build on the existing estate, do not replace it.** No sovereign cloud product is the
   institutional starting point; the sovereign core should be its next generation, with one governance owner.
3. **Site posture: standard.** Standard Tier III+ with 50-100 km separation is sufficient; spend the hardening budget on supply-chain assurance instead.
4. **Power strategy.** Power is not the binding constraint; optimise for fibre diversity and failure-domain separation.
5. **Hybrid tier.** Use in-country commercial regions for the non-critical tier, but keep identity, defense, security telemetry and registries in the sovereign core.

## 9. Open questions

- Replace scaled workload rows with real ministry/agency demand (see `countries/NL/CAPACITY_PLAN.md` for the method).
- Which body owns the sovereign core, and how are agencies compelled or incentivised to migrate?
- Which regions federate with EU partners for mutual disaster recovery, and which stay national-only?
- Site-size assumption: is the 12 MW planning unit right for Denmark, or should sites be smaller?
