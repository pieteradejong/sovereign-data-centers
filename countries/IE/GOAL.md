# Ireland - Sovereign Government Data Center Network

> Generated 2026-09-01 by `model/generate_countries.py` from the Dutch reference case
> (`countries/NL/GOAL.md`) and `model/eu27_parameters.csv`. Every number below is a **scaled working
> assumption**, not a sourced figure. Edit the CSVs in this directory and re-run
> `python3 model/capacity_model.py IE` to update the capacity numbers; edit
> `model/eu27_parameters.csv` or `model/scaling_rules.csv` and re-run the generator to update this file.

## 1. Working thesis

Ireland does not need to become technologically autarkic. It needs enough independently controlled compute,
storage, networking, identity, cryptography and operational capability that the state can continue functioning
when foreign commercial infrastructure is unavailable, politically constrained, compromised, or no longer
trustworthy. The Dutch design rules (sovereignty is a stack, not a building; 3-5 separated regions; dual fibre
paths; no single hardware supplier; a first-class developer platform) are taken as the starting point and
adjusted below for what is structurally different about Ireland.

## 2. Starting point

| | |
|---|---|
| Population | 5.42 m (Eurostat, 1 Jan 2025) |
| GDP | EUR 602 bn (2025, current prices) |
| Public administration employment (NACE O) | 144 k (Eurostat LFS 2025) |
| Non-household electricity price | 255.2 EUR/MWh (Eurostat, band IC, 2025-S2) |
| Renewables in electricity | 41.3% (2024) |
| Land area | 68,655 km2 |
| Live hyperscaler regions in-country | 2 |
| Existing government / sovereign cloud | No sovereign cloud; OGCIO Build to Share + Government Cloud Network + Backweston government DCs; cloud-first Advice Note; Digital Decade 2025 report flags DC grid limits |
| National digital identity (anchor workload) | MyGovID (Public Services Card) |
| Internet exchange / cable landings | INEX Dublin/Cork; Atlantic landings Killala Kinsale Cork |

Relative to the Dutch baseline: population x0.30, public administration x0.20,
GDP x0.51. Resulting design load: x0.38 the Dutch figure.

## 3. What is structurally different from the Dutch case

- **Grid isolation.** The national grid is an electrical island or nearly so (weak or single interconnection). The April 2025 Iberian blackout and Cyprus/Malta interconnector outages show the failure mode. Every site needs on-site generation and storage sized for multi-day ride-through, and the PUE and facility CAPEX assumptions should be revisited upward once site studies exist.
- **Expensive power (255 EUR/MWh vs. EU average ~184).** Power is the dominant OPEX line; free cooling, heat reuse, and siting near renewables or nuclear baseload move the economics more than server choice does. The model's power OPEX line is the number to attack first.

## 4. Workload demand (scaled from the Dutch baseline)

Scaling weights per workload class are in `model/scaling_rules.csv`; the Dutch rows they scale are in
`countries/NL/workloads_inputs.csv`. Frontline multiplier applied: no.

| Workload | Class | CPU cores | GPU eq. | Storage (PB) | Avail. factor |
|---|---|---:|---:|---:|---:|
| Digital identity / MyGovID | Critical government | 5,400 | 0 | 1.2 | 1.5 |
| Core government applications | Government | 13,800 | 0 | 4.5 | 1.35 |
| Data platforms & analytics | Government data | 14,300 | 32 | 24.5 | 1.25 |
| AI / sovereign model serving | AI | 9,300 | 264 | 6.2 | 1.3 |
| Defense classified compute | Defense | 9,000 | 80 | 4.5 | 1.5 |
| Cybersecurity / SOC / telemetry | Security | 5,900 | 8 | 6.8 | 1.4 |
| Scientific / public research | Research | 13,400 | 64 | 10.3 | 1.15 |

## 5. Capacity model output

| Metric | Value |
|---|---:|
| Physical servers | 2,024 (CPU 1,336 / GPU 125 / storage 563) |
| Rack equivalents | ~63 |
| IT critical load | 3.5 MW |
| Facility load (PUE 1.25) | 4.4 MW |
| Facility design load (+20% headroom) | **5.3 MW** |
| Sites by capacity / recommended | 1 / **3** (minimum 3) |
| Average design MW per site | 1.8 MW |
| Total CAPEX | **EUR 131 m** (facility EUR 53 m, IT EUR 66 m, network EUR 12 m) |
| Annual energy | 38,830 MWh |
| Annual OPEX | **EUR 16 m / yr** (power EUR 10 m, non-power EUR 6 m) |

Full table: `facility_summary.csv`.

## 6. Proposed geography (first-pass hypothesis)

Site posture: standard. Separation target: 50-100 km failure domains, dual fibre paths, distinct grid feeds.

| Region | Role | Share | Design MW | Racks | Facility CAPEX | Notes |
|---|---|---:|---:|---:|---:|---|
| Dublin | Primary civil cloud | 40% | 2.1 | 26 | EUR 22 m | OGCIO/Backweston estate, INEX; EirGrid connection moratorium to ~2028 is binding. |
| Cork | Sovereign secondary | 27% | 1.4 | 17 | EUR 14 m | Atlantic cable landings (Kinsale, Amitie), Celtic Interconnector. |
| Galway - Limerick / West | Government / continuity | 22% | 1.2 | 14 | EUR 12 m | Wind surplus, AEC-1 landing (Killala). |
| Midlands / Athlone | Strategic reserve | 10% | 0.5 | 6 | EUR 5 m | Post-peat land and grid; reserve/expansion. |

These regions encode only the obvious constraints (capital estate, second metro, distance from the frontier,
fault or flood zone). They are to be replaced by the scored site selection in workstream A of the Dutch
`TODO.md` (grid capacity, flood risk, fibre, failure independence, physical security, land, cooling).

## 7. Geography and threat notes

Negligible seismic; Atlantic storm/coastal and river floods; GRID IS BINDING: EirGrid Dublin DC connection moratorium to ~2028, DCs ~21% of national electricity; most expensive EU power; single UK gas pipeline until Celtic Interconnector (~2027); neutral non-NATO; subsea cable vulnerability

## 8. Recommendations specific to Ireland

1. **Anchor on MyGovID.** Digital identity is the workload that, if it fails, stops every other
   government service; it belongs in the sovereign core first, active-active across at least two regions.
2. **Build on the existing estate, do not replace it.** No sovereign cloud is the
   institutional starting point; the sovereign core should be its next generation, with one governance owner.
3. **Site posture: standard.** Standard Tier III+ with 50-100 km separation is sufficient; spend the hardening budget on supply-chain assurance instead.
4. **Power strategy.** Power is the binding constraint; treat grid connection lead time and on-site generation as first-order site criteria.
5. **Hybrid tier.** Use in-country commercial regions for the non-critical tier, but keep identity, defense, security telemetry and registries in the sovereign core.

## 9. Open questions

- Replace scaled workload rows with real ministry/agency demand (see `countries/NL/CAPACITY_PLAN.md` for the method).
- Which body owns the sovereign core, and how are agencies compelled or incentivised to migrate?
- Which regions federate with EU partners for mutual disaster recovery, and which stay national-only?
- Site-size assumption: is the 12 MW planning unit right for Ireland, or should sites be smaller?
