# Bulgaria - Sovereign Government Data Center Network

> Generated 2026-09-01 by `model/generate_countries.py` from the Dutch reference case
> (`countries/NL/GOAL.md`) and `model/eu27_parameters.csv`. Every number below is a **scaled working
> assumption**, not a sourced figure. Edit the CSVs in this directory and re-run
> `python3 model/capacity_model.py BG` to update the capacity numbers; edit
> `model/eu27_parameters.csv` or `model/scaling_rules.csv` and re-run the generator to update this file.

## 1. Working thesis

Bulgaria does not need to become technologically autarkic. It needs enough independently controlled compute,
storage, networking, identity, cryptography and operational capability that the state can continue functioning
when foreign commercial infrastructure is unavailable, politically constrained, compromised, or no longer
trustworthy. The Dutch design rules (sovereignty is a stack, not a building; 3-5 separated regions; dual fibre
paths; no single hardware supplier; a first-class developer platform) are taken as the starting point and
adjusted below for what is structurally different about Bulgaria.

## 2. Starting point

| | |
|---|---|
| Population | 6.44 m (Eurostat, 1 Jan 2025) |
| GDP | EUR 116 bn (2025, current prices) |
| Public administration employment (NACE O) | 220 k (Eurostat LFS 2025) |
| Non-household electricity price | 141.3 EUR/MWh (Eurostat, band IC, 2025-S2) |
| Renewables in electricity | 33.8% (2024) |
| Land area | 110,001 km2 |
| Live hyperscaler regions in-country | 0 |
| Existing government / sovereign cloud | State Hybrid Private Cloud (SHPC) for e-Governance - Ministry of e-Government / Information Services JSC (upgraded 2024) |
| National digital identity (anchor workload) | Bulgarian eID (biometric ID card + Evrotrust); EUDI wallet law in draft |
| Internet exchange / cable landings | BIX.BG and NetIX Sofia; Varna Black Sea landings |

Relative to the Dutch baseline: population x0.36, public administration x0.31,
GDP x0.10. Resulting design load: x0.30 the Dutch figure.

## 3. What is structurally different from the Dutch case

- **Frontline exposure.** A land border with Russia or Belarus (or a Black Sea coast facing the war) changes the threat model from *geopolitical supply disruption* to *kinetic and sabotage risk against the facilities themselves*. Defense and security workloads are scaled up 1.5x/1.25x in the baseline, and at least one site should be hardened (EMP/blast, autonomous power for weeks, not hours). A purely national footprint cannot provide the out-of-country cold copy that Estonia's Data Embassy already demonstrates; this is the first item to revisit when the EU federation layer (Dutch GOAL.md section 16) is modelled.
- **High seismic risk.** Base isolation or seismic-rated structures are mandatory, not optional, at the primary site; the second and third regions should be chosen in a different seismic domain so a single event cannot take out two regions. Expect facility CAPEX above the EUR 10 m/MW planning figure.
- **No hyperscaler region in-country.** Unlike the Netherlands, there is no commercial hyperscale tier to fall back on for non-critical workloads without leaving the jurisdiction. The sovereign core therefore has to be sized for a larger share of total government demand, and the hybrid model (Dutch GOAL.md section 7) needs a cross-border commercial tier.

## 4. Workload demand (scaled from the Dutch baseline)

Scaling weights per workload class are in `model/scaling_rules.csv`; the Dutch rows they scale are in
`countries/NL/workloads_inputs.csv`. Frontline multiplier applied: yes.

| Workload | Class | CPU cores | GPU eq. | Storage (PB) | Avail. factor |
|---|---|---:|---:|---:|---:|
| Digital identity / Bulgarian eID | Critical government | 6,400 | 0 | 1.4 | 1.5 |
| Core government applications | Government | 18,300 | 0 | 6.0 | 1.35 |
| Data platforms & analytics | Government data | 8,000 | 16 | 13.7 | 1.25 |
| AI / sovereign model serving | AI | 1,800 | 48 | 1.2 | 1.3 |
| Defense classified compute | Defense | 16,100 | 136 | 8.0 | 1.5 |
| Cybersecurity / SOC / telemetry | Security | 9,400 | 16 | 10.7 | 1.4 |
| Scientific / public research | Research | 2,600 | 16 | 2.0 | 1.15 |

## 5. Capacity model output

| Metric | Value |
|---|---:|
| Physical servers | 1,749 (CPU 1,239 / GPU 71 / storage 439) |
| Rack equivalents | ~55 |
| IT critical load | 2.8 MW |
| Facility load (PUE 1.25) | 3.5 MW |
| Facility design load (+20% headroom) | **4.2 MW** |
| Sites by capacity / recommended | 1 / **3** (minimum 3) |
| Average design MW per site | 1.4 MW |
| Total CAPEX | **EUR 98 m** (facility EUR 42 m, IT EUR 47 m, network EUR 9 m) |
| Annual energy | 30,584 MWh |
| Annual OPEX | **EUR 9 m / yr** (power EUR 4 m, non-power EUR 4 m) |

Full table: `facility_summary.csv`.

## 6. Proposed geography (first-pass hypothesis)

Site posture: hardened (frontline). Separation target: 50-100 km failure domains, dual fibre paths, distinct grid feeds.

| Region | Role | Share | Design MW | Racks | Facility CAPEX | Notes |
|---|---|---:|---:|---:|---:|---|
| Sofia | Primary civil cloud | 40% | 1.7 | 22 | EUR 17 m | SHPC estate, BIX/NetIX, EuroHPC Discoverer; seismic design required. |
| Plovdiv | Sovereign secondary | 27% | 1.1 | 15 | EUR 11 m | Second metro, 150 km separation, Maritsa industrial grid. |
| North-central / Veliko Tarnovo - Pleven | Government / continuity | 22% | 0.9 | 12 | EUR 9 m | Inland, away from the Black Sea frontier and Vrancea influence. |
| Varna | Strategic reserve | 10% | 0.4 | 6 | EUR 4 m | Cable landings, but Black Sea exposure - reserve/edge only. |

These regions encode only the obvious constraints (capital estate, second metro, distance from the frontier,
fault or flood zone). They are to be replaced by the scored site selection in workstream A of the Dutch
`TODO.md` (grid capacity, flood risk, fibre, failure independence, physical security, land, cooling).

## 7. Geography and threat notes

Moderate-high seismic (Vrancea influence; Sofia/Plovdiv zones); Danube floods; cheap abundant land; Black Sea frontline (drone/mine incidents at Varna/Burgas); gas diversified from Russia post-2022; nuclear baseload but ageing grid

## 8. Recommendations specific to Bulgaria

1. **Anchor on Bulgarian eID.** Digital identity is the workload that, if it fails, stops every other
   government service; it belongs in the sovereign core first, active-active across at least two regions.
2. **Build on the existing estate, do not replace it.** State Hybrid Private Cloud (SHPC) for e-Governance - Ministry of e-Government / Information Services JSC (upgraded 2024) is the
   institutional starting point; the sovereign core should be its next generation, with one governance owner.
3. **Site posture: hardened (frontline).** Harden at least one region and plan an out-of-country cold copy.
4. **Power strategy.** Power is not the binding constraint; optimise for fibre diversity and failure-domain separation.
5. **Hybrid tier.** With no in-country hyperscaler region, define now which non-critical workloads may leave the jurisdiction and under what contract terms.

## 9. Open questions

- Replace scaled workload rows with real ministry/agency demand (see `countries/NL/CAPACITY_PLAN.md` for the method).
- Which body owns the sovereign core, and how are agencies compelled or incentivised to migrate?
- Out-of-country reserve: which partner state, under what treaty?
- Site-size assumption: is the 12 MW planning unit right for Bulgaria, or should sites be smaller?
