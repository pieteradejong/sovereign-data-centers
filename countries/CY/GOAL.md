# Cyprus - Sovereign Government Data Center Network

> Generated 2026-09-01 by `model/generate_countries.py` from the Dutch reference case
> (`countries/NL/GOAL.md`) and `model/eu27_parameters.csv`. Every number below is a **scaled working
> assumption**, not a sourced figure. Edit the CSVs in this directory and re-run
> `python3 model/capacity_model.py CY` to update the capacity numbers; edit
> `model/eu27_parameters.csv` or `model/scaling_rules.csv` and re-run the generator to update this file.

## 1. Working thesis

Cyprus does not need to become technologically autarkic. It needs enough independently controlled compute,
storage, networking, identity, cryptography and operational capability that the state can continue functioning
when foreign commercial infrastructure is unavailable, politically constrained, compromised, or no longer
trustworthy. The Dutch design rules (sovereignty is a stack, not a building; 3-5 separated regions; dual fibre
paths; no single hardware supplier; a first-class developer platform) are taken as the starting point and
adjusted below for what is structurally different about Cyprus.

## 2. Starting point

| | |
|---|---|
| Population | 1.37 m (Eurostat, 1 Jan 2025) |
| GDP | EUR 36 bn (2025, current prices) |
| Public administration employment (NACE O) | 36 k (Eurostat LFS 2025) |
| Non-household electricity price | 242.9 EUR/MWh (Eurostat, band IC, 2025-S2) |
| Renewables in electricity | 24.1% (2024) |
| Land area | 9,213 km2 |
| Live hyperscaler regions in-country | 0 |
| Existing government / sovereign cloud | Government G-Cloud / Government Data Centre - Deputy Ministry of Research, Innovation and Digital Policy (DMRID) + Cyta hosting; RRF hybrid-cloud consolidation |
| National digital identity (anchor workload) | CY Login + Cyprus Digital ID |
| Internet exchange / cable landings | CyIX Nicosia; major East-Med cable hub (2Africa Cadmos Tamares Medusa) |

Relative to the Dutch baseline: population x0.08, public administration x0.05,
GDP x0.03. Resulting design load: x0.09 the Dutch figure.

## 3. What is structurally different from the Dutch case

- **Grid isolation.** The national grid is an electrical island or nearly so (weak or single interconnection). The April 2025 Iberian blackout and Cyprus/Malta interconnector outages show the failure mode. Every site needs on-site generation and storage sized for multi-day ride-through, and the PUE and facility CAPEX assumptions should be revisited upward once site studies exist.
- **Moderate seismic risk.** Seismic zoning should be a site-scoring criterion; at least two regions in different domains.
- **Expensive power (243 EUR/MWh vs. EU average ~184).** Power is the dominant OPEX line; free cooling, heat reuse, and siting near renewables or nuclear baseload move the economics more than server choice does. The model's power OPEX line is the number to attack first.
- **Micro-state geography.** The Dutch rule of 3-5 regions with 50-100 km separation cannot be met inside the national territory. The model therefore assumes two in-country sites carrying 55/45 of the load and no in-country reserve. A credible disaster-recovery posture requires an out-of-country partner site - deferred to the federation layer.
- **No hyperscaler region in-country.** Unlike the Netherlands, there is no commercial hyperscale tier to fall back on for non-critical workloads without leaving the jurisdiction. The sovereign core therefore has to be sized for a larger share of total government demand, and the hybrid model (Dutch GOAL.md section 7) needs a cross-border commercial tier.

## 4. Workload demand (scaled from the Dutch baseline)

Scaling weights per workload class are in `model/scaling_rules.csv`; the Dutch rows they scale are in
`countries/NL/workloads_inputs.csv`. Frontline multiplier applied: no.

| Workload | Class | CPU cores | GPU eq. | Storage (PB) | Avail. factor |
|---|---|---:|---:|---:|---:|
| Digital identity / CY Login + Cyprus Digital ID | Critical government | 1,400 | 0 | 0.5 | 1.5 |
| Core government applications | Government | 4,400 | 0 | 1.4 | 1.35 |
| Data platforms & analytics | Government data | 2,800 | 8 | 4.8 | 1.25 |
| AI / sovereign model serving | AI | 1,100 | 32 | 0.7 | 1.3 |
| Defense classified compute | Defense | 3,000 | 24 | 1.5 | 1.5 |
| Cybersecurity / SOC / telemetry | Security | 3,300 | 8 | 3.8 | 1.4 |
| Scientific / public research | Research | 1,300 | 8 | 1.0 | 1.15 |

## 5. Capacity model output

| Metric | Value |
|---|---:|
| Physical servers | 502 (CPU 338 / GPU 25 / storage 139) |
| Rack equivalents | ~16 |
| IT critical load | 0.8 MW |
| Facility load (PUE 1.25) | 1.0 MW |
| Facility design load (+20% headroom) | **1.3 MW** |
| Sites by capacity / recommended | 1 / **2** (minimum 2) |
| Average design MW per site | 0.6 MW |
| Total CAPEX | **EUR 30 m** (facility EUR 13 m, IT EUR 15 m, network EUR 3 m) |
| Annual energy | 9,132 MWh |
| Annual OPEX | **EUR 4 m / yr** (power EUR 2 m, non-power EUR 1 m) |

Full table: `facility_summary.csv`.

## 6. Proposed geography (first-pass hypothesis)

Site posture: standard. Separation target: ~30-80 km (island/micro-state maximum).

| Region | Role | Share | Design MW | Racks | Facility CAPEX | Notes |
|---|---|---:|---:|---:|---:|---|
| Nicosia | Primary civil cloud | 55% | 0.7 | 9 | EUR 7 m | Government DC and CyIX; inland, away from cable landings. |
| Limassol - Paphos | Sovereign secondary | 45% | 0.6 | 7 | EUR 6 m | East-Med cable landings; 80 km separation is the island maximum. |

These regions encode only the obvious constraints (capital estate, second metro, distance from the frontier,
fault or flood zone). They are to be replaced by the scored site selection in workstream A of the Dutch
`TODO.md` (grid capacity, flood risk, fibre, failure independence, physical security, land, cooling).

## 7. Geography and threat notes

Moderate seismic (Cyprus Arc); water scarcity and extreme heat; isolated island grid (oil-fired) with no interconnector until Great Sea Interconnector (>2029); divided island; Middle East conflict proximity; non-NATO

## 8. Recommendations specific to Cyprus

1. **Anchor on CY Login + Cyprus Digital ID.** Digital identity is the workload that, if it fails, stops every other
   government service; it belongs in the sovereign core first, active-active across at least two regions.
2. **Build on the existing estate, do not replace it.** Government G-Cloud / Government Data Centre - Deputy Ministry of Research, Innovation and Digital Policy (DMRID) + Cyta hosting is the
   institutional starting point; the sovereign core should be its next generation, with one governance owner.
3. **Site posture: standard.** Standard Tier III+ with 50-100 km separation is sufficient; spend the hardening budget on supply-chain assurance instead.
4. **Power strategy.** Power is the binding constraint; treat grid connection lead time and on-site generation as first-order site criteria.
5. **Hybrid tier.** With no in-country hyperscaler region, define now which non-critical workloads may leave the jurisdiction and under what contract terms.

## 9. Open questions

- Replace scaled workload rows with real ministry/agency demand (see `countries/NL/CAPACITY_PLAN.md` for the method).
- Which body owns the sovereign core, and how are agencies compelled or incentivised to migrate?
- Out-of-country reserve: which partner state, under what treaty?
- Site-size assumption: is the 12 MW planning unit right for Cyprus, or should sites be smaller?
