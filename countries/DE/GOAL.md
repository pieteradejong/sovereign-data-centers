# Germany - Sovereign Government Data Center Network

> Generated 2026-09-01 by `model/generate_countries.py` from the Dutch reference case
> (`countries/NL/GOAL.md`) and `model/eu27_parameters.csv`. Every number below is a **scaled working
> assumption**, not a sourced figure. Edit the CSVs in this directory and re-run
> `python3 model/capacity_model.py DE` to update the capacity numbers; edit
> `model/eu27_parameters.csv` or `model/scaling_rules.csv` and re-run the generator to update this file.

## 1. Working thesis

Germany does not need to become technologically autarkic. It needs enough independently controlled compute,
storage, networking, identity, cryptography and operational capability that the state can continue functioning
when foreign commercial infrastructure is unavailable, politically constrained, compromised, or no longer
trustworthy. The Dutch design rules (sovereignty is a stack, not a building; 3-5 separated regions; dual fibre
paths; no single hardware supplier; a first-class developer platform) are taken as the starting point and
adjusted below for what is structurally different about Germany.

## 2. Starting point

| | |
|---|---|
| Population | 83.58 m (Eurostat, 1 Jan 2025) |
| GDP | EUR 4,470 bn (2025, current prices) |
| Public administration employment (NACE O) | 3,041 k (Eurostat LFS 2025) |
| Non-household electricity price | 226.4 EUR/MWh (Eurostat, band IC, 2025-S2) |
| Renewables in electricity | 54.1% (2024) |
| Land area | 353,296 km2 |
| Live hyperscaler regions in-country | 6 |
| Existing government / sovereign cloud | Deutsche Verwaltungscloud (DVC) federated launched Mar 2025 (IT-Planungsrat/govdigital/FITKO); Bundescloud (ITZBund); Delos Cloud (SAP/Arvato on Azure, BSI-aligned); openDesk (ZenDiS); STACKIT/IONOS/T-Cloud; BSI C5 |
| National digital identity (anchor workload) | Online-Ausweis eID + BundID/DeutschlandID |
| Internet exchange / cable landings | DE-CIX Frankfurt (world's largest) Hamburg Munich; Norden/Sylt/Rostock landings |

Relative to the Dutch baseline: population x4.63, public administration x4.25,
GDP x3.82. Resulting design load: x4.26 the Dutch figure.

## 3. What is structurally different from the Dutch case

- **Expensive power (226 EUR/MWh vs. EU average ~184).** Power is the dominant OPEX line; free cooling, heat reuse, and siting near renewables or nuclear baseload move the economics more than server choice does. The model's power OPEX line is the number to attack first.
- **Dense hyperscaler presence (6 live regions).** Commercial capacity, fibre and skills exist in-country; the sovereign core can stay lean and the hybrid model works as designed. The risk is the opposite one: political pressure to declare a hyperscaler region 'sovereign enough' (Dutch GOAL.md section 17: location is not sovereignty).

## 4. Workload demand (scaled from the Dutch baseline)

Scaling weights per workload class are in `model/scaling_rules.csv`; the Dutch rows they scale are in
`countries/NL/workloads_inputs.csv`. Frontline multiplier applied: no.

| Workload | Class | CPU cores | GPU eq. | Storage (PB) | Avail. factor |
|---|---|---:|---:|---:|---:|
| Digital identity / Online-Ausweis eID + BundID | Critical government | 83,400 | 0 | 18.5 | 1.5 |
| Core government applications | Government | 244,100 | 0 | 79.9 | 1.35 |
| Data platforms & analytics | Government data | 147,900 | 336 | 253.5 | 1.25 |
| AI / sovereign model serving | AI | 68,700 | 1952 | 45.8 | 1.3 |
| Defense classified compute | Defense | 139,000 | 1184 | 69.5 | 1.5 |
| Cybersecurity / SOC / telemetry | Security | 99,400 | 144 | 112.9 | 1.4 |
| Scientific / public research | Research | 99,300 | 488 | 76.4 | 1.15 |

## 5. Capacity model output

| Metric | Value |
|---|---:|
| Physical servers | 24,531 (CPU 16,916 / GPU 1,146 / storage 6,469) |
| Rack equivalents | ~767 |
| IT critical load | 40.2 MW |
| Facility load (PUE 1.25) | 50.3 MW |
| Facility design load (+20% headroom) | **60.4 MW** |
| Sites by capacity / recommended | 6 / **6** (minimum 4) |
| Average design MW per site | 10.1 MW |
| Total CAPEX | **EUR 1,435 m** (facility EUR 604 m, IT EUR 704 m, network EUR 127 m) |
| Annual energy | 440,722 MWh |
| Annual OPEX | **EUR 164 m / yr** (power EUR 100 m, non-power EUR 65 m) |

Full table: `facility_summary.csv`.

## 6. Proposed geography (first-pass hypothesis)

Site posture: standard. Separation target: 50-100 km failure domains, dual fibre paths, distinct grid feeds.

| Region | Role | Share | Design MW | Racks | Facility CAPEX | Notes |
|---|---|---:|---:|---:|---:|---|
| Frankfurt - Rhine-Main | Primary civil cloud | 36% | 21.7 | 276 | EUR 217 m | DE-CIX, ITZBund estate; grid saturated - expect multi-year connection lead time. |
| Berlin - Brandenburg | Sovereign secondary | 18% | 10.9 | 138 | EUR 109 m | Federal ministries, AWS ESC and STACKIT prove grid headroom in the east. |
| Munich / Bavaria | Defense / industrial | 18% | 10.9 | 138 | EUR 109 m | Defense-industrial cluster, Bundeswehr IT; southern separation. |
| Hamburg / North | Government / continuity | 18% | 10.9 | 138 | EUR 109 m | Wind surplus, North Sea cable landings (Norden/Sylt). |
| Leipzig - Saxony | Strategic reserve | 10% | 6.0 | 77 | EUR 60 m | Post-coal land and grid; reserve/expansion. |

These regions encode only the obvious constraints (capital estate, second metro, distance from the frontier,
fault or flood zone). They are to be replaced by the scored site selection in workstream A of the Dutch
`TODO.md` (grid capacity, flood risk, fibre, failure independence, physical security, land, cooling).

## 7. Geography and threat notes

Low seismic; Ahr/Rhine/Elbe floods (2021); Frankfurt grid saturated (multi-year waits) with headroom in Brandenburg/east; 3rd-highest EU power price; north-south grid bottlenecks; LNG gas import; NATO; sabotage/drone incidents at DCs 2024-25

## 8. Recommendations specific to Germany

1. **Anchor on Online-Ausweis eID + BundID.** Digital identity is the workload that, if it fails, stops every other
   government service; it belongs in the sovereign core first, active-active across at least two regions.
2. **Build on the existing estate, do not replace it.** Deutsche Verwaltungscloud (DVC) federated launched Mar 2025 (IT-Planungsrat/govdigital/FITKO) is the
   institutional starting point; the sovereign core should be its next generation, with one governance owner.
3. **Site posture: standard.** Standard Tier III+ with 50-100 km separation is sufficient; spend the hardening budget on supply-chain assurance instead.
4. **Power strategy.** Power is the binding constraint; treat grid connection lead time and on-site generation as first-order site criteria.
5. **Hybrid tier.** Use in-country commercial regions for the non-critical tier, but keep identity, defense, security telemetry and registries in the sovereign core.

## 9. Open questions

- Replace scaled workload rows with real ministry/agency demand (see `countries/NL/CAPACITY_PLAN.md` for the method).
- Which body owns the sovereign core, and how are agencies compelled or incentivised to migrate?
- Which regions federate with EU partners for mutual disaster recovery, and which stay national-only?
- Site-size assumption: is the 12 MW planning unit right for Germany, or should sites be larger?
