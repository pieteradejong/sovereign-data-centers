# Sweden - Sovereign Government Data Center Network

> Generated 2026-09-01 by `model/generate_countries.py` from the Dutch reference case
> (`countries/NL/GOAL.md`) and `model/eu27_parameters.csv`. Every number below is a **scaled working
> assumption**, not a sourced figure. Edit the CSVs in this directory and re-run
> `python3 model/capacity_model.py SE` to update the capacity numbers; edit
> `model/eu27_parameters.csv` or `model/scaling_rules.csv` and re-run the generator to update this file.

## 1. Working thesis

Sweden does not need to become technologically autarkic. It needs enough independently controlled compute,
storage, networking, identity, cryptography and operational capability that the state can continue functioning
when foreign commercial infrastructure is unavailable, politically constrained, compromised, or no longer
trustworthy. The Dutch design rules (sovereignty is a stack, not a building; 3-5 separated regions; dual fibre
paths; no single hardware supplier; a first-class developer platform) are taken as the starting point and
adjusted below for what is structurally different about Sweden.

## 2. Starting point

| | |
|---|---|
| Population | 10.59 m (Eurostat, 1 Jan 2025) |
| GDP | EUR 601 bn (2025, current prices) |
| Public administration employment (NACE O) | 420 k (Eurostat LFS 2025) |
| Non-household electricity price | 97.0 EUR/MWh (Eurostat, band IC, 2025-S2) |
| Renewables in electricity | 88.1% (2024) |
| Land area | 407,300 km2 |
| Live hyperscaler regions in-country | 3 |
| Existing government / sovereign cloud | Nationell molnpolicy (May 2026, guidance) + coordinated statlig it-drift via Forsakringskassan (SAFOS), Skatteverket, Lantmateriet, Trafikverket; no single state cloud; Kammarkollegiet procurement, DIGG coordination |
| National digital identity (anchor workload) | BankID / Freja eID+; state e-ID 2026 |
| Internet exchange / cable landings | Netnod Stockholm/Gothenburg/Malmo/Sundsvall; Baltic cables to FI/LV/LT/DK |

Relative to the Dutch baseline: population x0.59, public administration x0.59,
GDP x0.51. Resulting design load: x0.56 the Dutch figure.

## 3. What is structurally different from the Dutch case

- **Cheap, clean power (97 EUR/MWh, 88% renewables).** The economics favour building larger sites than the 12 MW planning unit and offering spare sovereign capacity to partners - a reason to revisit the site-size assumption.
- **Dense hyperscaler presence (3 live regions).** Commercial capacity, fibre and skills exist in-country; the sovereign core can stay lean and the hybrid model works as designed. The risk is the opposite one: political pressure to declare a hyperscaler region 'sovereign enough' (Dutch GOAL.md section 17: location is not sovereignty).

## 4. Workload demand (scaled from the Dutch baseline)

Scaling weights per workload class are in `model/scaling_rules.csv`; the Dutch rows they scale are in
`countries/NL/workloads_inputs.csv`. Frontline multiplier applied: no.

| Workload | Class | CPU cores | GPU eq. | Storage (PB) | Avail. factor |
|---|---|---:|---:|---:|---:|
| Digital identity / BankID | Critical government | 10,600 | 0 | 2.3 | 1.5 |
| Core government applications | Government | 32,300 | 0 | 10.6 | 1.35 |
| Data platforms & analytics | Government data | 19,300 | 48 | 33.0 | 1.25 |
| AI / sovereign model serving | AI | 9,200 | 264 | 6.2 | 1.3 |
| Defense classified compute | Defense | 17,600 | 152 | 8.8 | 1.5 |
| Cybersecurity / SOC / telemetry | Security | 12,900 | 16 | 14.7 | 1.4 |
| Scientific / public research | Research | 13,400 | 64 | 10.3 | 1.15 |

## 5. Capacity model output

| Metric | Value |
|---|---:|
| Physical servers | 3,212 (CPU 2,210 / GPU 154 / storage 848) |
| Rack equivalents | ~100 |
| IT critical load | 5.3 MW |
| Facility load (PUE 1.25) | 6.6 MW |
| Facility design load (+20% headroom) | **7.9 MW** |
| Sites by capacity / recommended | 1 / **3** (minimum 3) |
| Average design MW per site | 2.6 MW |
| Total CAPEX | **EUR 189 m** (facility EUR 79 m, IT EUR 93 m, network EUR 17 m) |
| Annual energy | 58,033 MWh |
| Annual OPEX | **EUR 14 m / yr** (power EUR 6 m, non-power EUR 9 m) |

Full table: `facility_summary.csv`.

## 6. Proposed geography (first-pass hypothesis)

Site posture: standard. Separation target: 50-100 km failure domains, dual fibre paths, distinct grid feeds.

| Region | Role | Share | Design MW | Racks | Facility CAPEX | Notes |
|---|---|---:|---:|---:|---:|---|
| Stockholm - Malardalen | Primary civil cloud | 40% | 3.2 | 41 | EUR 32 m | State IT providers, Netnod, all three hyperscaler regions; SE3 grid constraints. |
| Gavle - Sandviken | Sovereign secondary | 27% | 2.1 | 27 | EUR 22 m | Azure campus proves grid; SE2 surplus power. |
| Lulea - Boden / North | Government / continuity | 22% | 1.8 | 23 | EUR 18 m | SE1 cheapest power, free cooling, Meta campus; adds ~15 ms. |
| Gothenburg / West | Defense / industrial | 10% | 0.8 | 10 | EUR 8 m | Naval/defense cluster, North Sea routing away from the Baltic. |

These regions encode only the obvious constraints (capital estate, second metro, distance from the frontier,
fault or flood zone). They are to be replaced by the scored site selection in workstream A of the Dutch
`TODO.md` (grid capacity, flood risk, fibre, failure independence, physical security, land, cooling).

## 7. Geography and threat notes

No seismic/flood; cold climate favours free cooling; NATO (2024) with Baltic subsea sabotage and Gotland exposure; north-south grid bottlenecks (SE1/2 surplus vs SE3/4 constraints); 2nd-cheapest EU power, ~98% low-carbon

## 8. Recommendations specific to Sweden

1. **Anchor on BankID.** Digital identity is the workload that, if it fails, stops every other
   government service; it belongs in the sovereign core first, active-active across at least two regions.
2. **Build on the existing estate, do not replace it.** Nationell molnpolicy (May 2026, guidance) + coordinated statlig it-drift via Forsakringskassan (SAFOS), Skatteverket, Lantmateriet, Trafikverket is the
   institutional starting point; the sovereign core should be its next generation, with one governance owner.
3. **Site posture: standard.** Standard Tier III+ with 50-100 km separation is sufficient; spend the hardening budget on supply-chain assurance instead.
4. **Power strategy.** Power is not the binding constraint; optimise for fibre diversity and failure-domain separation.
5. **Hybrid tier.** Use in-country commercial regions for the non-critical tier, but keep identity, defense, security telemetry and registries in the sovereign core.

## 9. Open questions

- Replace scaled workload rows with real ministry/agency demand (see `countries/NL/CAPACITY_PLAN.md` for the method).
- Which body owns the sovereign core, and how are agencies compelled or incentivised to migrate?
- Which regions federate with EU partners for mutual disaster recovery, and which stay national-only?
- Site-size assumption: is the 12 MW planning unit right for Sweden, or should sites be smaller?
