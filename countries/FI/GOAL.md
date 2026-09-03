# Finland - Sovereign Government Data Center Network

> Generated 2026-09-01 by `model/generate_countries.py` from the Dutch reference case
> (`countries/NL/GOAL.md`) and `model/eu27_parameters.csv`. Every number below is a **scaled working
> assumption**, not a sourced figure. Edit the CSVs in this directory and re-run
> `python3 model/capacity_model.py FI` to update the capacity numbers; edit
> `model/eu27_parameters.csv` or `model/scaling_rules.csv` and re-run the generator to update this file.

## 1. Working thesis

Finland does not need to become technologically autarkic. It needs enough independently controlled compute,
storage, networking, identity, cryptography and operational capability that the state can continue functioning
when foreign commercial infrastructure is unavailable, politically constrained, compromised, or no longer
trustworthy. The Dutch design rules (sovereignty is a stack, not a building; 3-5 separated regions; dual fibre
paths; no single hardware supplier; a first-class developer platform) are taken as the starting point and
adjusted below for what is structurally different about Finland.

## 2. Starting point

| | |
|---|---|
| Population | 5.64 m (Eurostat, 1 Jan 2025) |
| GDP | EUR 282 bn (2025, current prices) |
| Public administration employment (NACE O) | 116 k (Eurostat LFS 2025) |
| Non-household electricity price | 74.8 EUR/MWh (Eurostat, band IC, 2025-S2) |
| Renewables in electricity | 54.3% (2024) |
| Land area | 304,316 km2 |
| Live hyperscaler regions in-country | 1 |
| Existing government / sovereign cloud | Valtori (Government ICT Centre) state DCs + public-cloud brokerage; PiTuKri cloud security criteria; Digital Sovereignty Roadmap adopted Apr 2026; no branded sovereign cloud |
| National digital identity (anchor workload) | Suomi.fi e-Identification (DVV) |
| Internet exchange / cable landings | FICIX Helsinki/Espoo/Oulu; C-Lion1 Helsinki-Rostock (damaged Nov 2024) |

Relative to the Dutch baseline: population x0.31, public administration x0.16,
GDP x0.24. Resulting design load: x0.31 the Dutch figure.

## 3. What is structurally different from the Dutch case

- **Frontline exposure.** A land border with Russia or Belarus (or a Black Sea coast facing the war) changes the threat model from *geopolitical supply disruption* to *kinetic and sabotage risk against the facilities themselves*. Defense and security workloads are scaled up 1.5x/1.25x in the baseline, and at least one site should be hardened (EMP/blast, autonomous power for weeks, not hours). A purely national footprint cannot provide the out-of-country cold copy that Estonia's Data Embassy already demonstrates; this is the first item to revisit when the EU federation layer (Dutch GOAL.md section 16) is modelled.
- **Cheap, clean power (75 EUR/MWh, 54% renewables).** The economics favour building larger sites than the 12 MW planning unit and offering spare sovereign capacity to partners - a reason to revisit the site-size assumption.

## 4. Workload demand (scaled from the Dutch baseline)

Scaling weights per workload class are in `model/scaling_rules.csv`; the Dutch rows they scale are in
`countries/NL/workloads_inputs.csv`. Frontline multiplier applied: yes.

| Workload | Class | CPU cores | GPU eq. | Storage (PB) | Avail. factor |
|---|---|---:|---:|---:|---:|
| Digital identity / Suomi.fi e-Identification | Critical government | 5,600 | 0 | 1.2 | 1.5 |
| Core government applications | Government | 13,000 | 0 | 4.3 | 1.35 |
| Data platforms & analytics | Government data | 9,700 | 24 | 16.6 | 1.25 |
| AI / sovereign model serving | AI | 4,300 | 120 | 2.9 | 1.3 |
| Defense classified compute | Defense | 14,100 | 120 | 7.0 | 1.5 |
| Cybersecurity / SOC / telemetry | Security | 7,400 | 8 | 8.4 | 1.4 |
| Scientific / public research | Research | 6,300 | 32 | 4.8 | 1.15 |

## 5. Capacity model output

| Metric | Value |
|---|---:|
| Physical servers | 1,717 (CPU 1,175 / GPU 89 / storage 453) |
| Rack equivalents | ~54 |
| IT critical load | 2.9 MW |
| Facility load (PUE 1.25) | 3.6 MW |
| Facility design load (+20% headroom) | **4.3 MW** |
| Sites by capacity / recommended | 1 / **3** (minimum 3) |
| Average design MW per site | 1.4 MW |
| Total CAPEX | **EUR 104 m** (facility EUR 43 m, IT EUR 51 m, network EUR 9 m) |
| Annual energy | 31,580 MWh |
| Annual OPEX | **EUR 7 m / yr** (power EUR 2 m, non-power EUR 5 m) |

Full table: `facility_summary.csv`.

## 6. Proposed geography (first-pass hypothesis)

Site posture: hardened (frontline). Separation target: 50-100 km failure domains, dual fibre paths, distinct grid feeds.

| Region | Role | Share | Design MW | Racks | Facility CAPEX | Notes |
|---|---|---:|---:|---:|---:|---|
| Helsinki - Uusimaa | Primary civil cloud | 40% | 1.8 | 22 | EUR 18 m | Valtori estate, FICIX, C-Lion1 landing; 30 min from Tallinn. |
| Tampere - Pirkanmaa | Sovereign secondary | 27% | 1.2 | 14 | EUR 12 m | Inland, 180 km separation, strong grid. |
| Oulu / North | Government / continuity | 22% | 1.0 | 12 | EUR 10 m | Cheapest power, free cooling, far from the frontier; adds ~10 ms. |
| Kajaani - Kuopio | Strategic reserve | 10% | 0.4 | 5 | EUR 4 m | LUMI (Kajaani) proves power and cooling for large loads. |

These regions encode only the obvious constraints (capital estate, second metro, distance from the frontier,
fault or flood zone). They are to be replaced by the scored site selection in workstream A of the Dutch
`TODO.md` (grid capacity, flood risk, fibre, failure independence, physical security, land, cooling).

## 7. Geography and threat notes

Very low seismic/flood; abundant land, cold climate, cheapest EU power (nuclear+wind+hydro); 1,340 km Russian border (NATO since 2023); Baltic Sea subsea sabotage risk; continental grid link only via Sweden/Estonia

## 8. Recommendations specific to Finland

1. **Anchor on Suomi.fi e-Identification.** Digital identity is the workload that, if it fails, stops every other
   government service; it belongs in the sovereign core first, active-active across at least two regions.
2. **Build on the existing estate, do not replace it.** Valtori (Government ICT Centre) state DCs + public-cloud brokerage is the
   institutional starting point; the sovereign core should be its next generation, with one governance owner.
3. **Site posture: hardened (frontline).** Harden at least one region and plan an out-of-country cold copy.
4. **Power strategy.** Power is not the binding constraint; optimise for fibre diversity and failure-domain separation.
5. **Hybrid tier.** Use in-country commercial regions for the non-critical tier, but keep identity, defense, security telemetry and registries in the sovereign core.

## 9. Open questions

- Replace scaled workload rows with real ministry/agency demand (see `countries/NL/CAPACITY_PLAN.md` for the method).
- Which body owns the sovereign core, and how are agencies compelled or incentivised to migrate?
- Out-of-country reserve: which partner state, under what treaty?
- Site-size assumption: is the 12 MW planning unit right for Finland, or should sites be smaller?
