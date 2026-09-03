# Portugal - Sovereign Government Data Center Network

> Generated 2026-09-01 by `model/generate_countries.py` from the Dutch reference case
> (`countries/NL/GOAL.md`) and `model/eu27_parameters.csv`. Every number below is a **scaled working
> assumption**, not a sourced figure. Edit the CSVs in this directory and re-run
> `python3 model/capacity_model.py PT` to update the capacity numbers; edit
> `model/eu27_parameters.csv` or `model/scaling_rules.csv` and re-run the generator to update this file.

## 1. Working thesis

Portugal does not need to become technologically autarkic. It needs enough independently controlled compute,
storage, networking, identity, cryptography and operational capability that the state can continue functioning
when foreign commercial infrastructure is unavailable, politically constrained, compromised, or no longer
trustworthy. The Dutch design rules (sovereignty is a stack, not a building; 3-5 separated regions; dual fibre
paths; no single hardware supplier; a first-class developer platform) are taken as the starting point and
adjusted below for what is structurally different about Portugal.

## 2. Starting point

| | |
|---|---|
| Population | 10.75 m (Eurostat, 1 Jan 2025) |
| GDP | EUR 307 bn (2025, current prices) |
| Public administration employment (NACE O) | 342 k (Eurostat LFS 2025) |
| Non-household electricity price | 132.9 EUR/MWh (Eurostat, band IC, 2025-S2) |
| Renewables in electricity | 65.8% (2024) |
| Land area | 90,996 km2 |
| Live hyperscaler regions in-country | 0 |
| Existing government / sovereign cloud | Plano Nacional de Nuvem Soberana - approved May 2026 (ARTE): data classification, technical requirements, phased state sovereign-cloud infrastructure; builds on Nuvem da AP (AMA/eSPap) |
| National digital identity (anchor workload) | Chave Movel Digital / Cartao de Cidadao |
| Internet exchange / cable landings | GigaPIX Lisbon; Sines landing hub (EllaLink 2Africa Equiano Medusa) |

Relative to the Dutch baseline: population x0.60, public administration x0.48,
GDP x0.26. Resulting design load: x0.45 the Dutch figure.

## 3. What is structurally different from the Dutch case

- **Grid isolation.** The national grid is an electrical island or nearly so (weak or single interconnection). The April 2025 Iberian blackout and Cyprus/Malta interconnector outages show the failure mode. Every site needs on-site generation and storage sized for multi-day ride-through, and the PUE and facility CAPEX assumptions should be revisited upward once site studies exist.
- **High seismic risk.** Base isolation or seismic-rated structures are mandatory, not optional, at the primary site; the second and third regions should be chosen in a different seismic domain so a single event cannot take out two regions. Expect facility CAPEX above the EUR 10 m/MW planning figure.
- **No hyperscaler region in-country.** Unlike the Netherlands, there is no commercial hyperscale tier to fall back on for non-critical workloads without leaving the jurisdiction. The sovereign core therefore has to be sized for a larger share of total government demand, and the hybrid model (Dutch GOAL.md section 7) needs a cross-border commercial tier.

## 4. Workload demand (scaled from the Dutch baseline)

Scaling weights per workload class are in `model/scaling_rules.csv`; the Dutch rows they scale are in
`countries/NL/workloads_inputs.csv`. Frontline multiplier applied: no.

| Workload | Class | CPU cores | GPU eq. | Storage (PB) | Avail. factor |
|---|---|---:|---:|---:|---:|
| Digital identity / Chave Movel Digital | Critical government | 10,700 | 0 | 2.4 | 1.5 |
| Core government applications | Government | 29,500 | 0 | 9.7 | 1.35 |
| Data platforms & analytics | Government data | 15,000 | 32 | 25.7 | 1.25 |
| AI / sovereign model serving | AI | 4,700 | 136 | 3.1 | 1.3 |
| Defense classified compute | Defense | 17,900 | 152 | 8.9 | 1.5 |
| Cybersecurity / SOC / telemetry | Security | 12,300 | 16 | 14.0 | 1.4 |
| Scientific / public research | Research | 6,800 | 32 | 5.2 | 1.15 |

## 5. Capacity model output

| Metric | Value |
|---|---:|
| Physical servers | 2,685 (CPU 1,887 / GPU 107 / storage 691) |
| Rack equivalents | ~84 |
| IT critical load | 4.3 MW |
| Facility load (PUE 1.25) | 5.3 MW |
| Facility design load (+20% headroom) | **6.4 MW** |
| Sites by capacity / recommended | 1 / **3** (minimum 3) |
| Average design MW per site | 2.1 MW |
| Total CAPEX | **EUR 150 m** (facility EUR 64 m, IT EUR 73 m, network EUR 13 m) |
| Annual energy | 46,743 MWh |
| Annual OPEX | **EUR 13 m / yr** (power EUR 6 m, non-power EUR 7 m) |

Full table: `facility_summary.csv`.

## 6. Proposed geography (first-pass hypothesis)

Site posture: standard. Separation target: 50-100 km failure domains, dual fibre paths, distinct grid feeds.

| Region | Role | Share | Design MW | Racks | Facility CAPEX | Notes |
|---|---|---:|---:|---:|---:|---|
| Lisbon | Primary civil cloud | 40% | 2.6 | 34 | EUR 26 m | AMA/eSPap estate, GigaPIX; seismic/tsunami design mandatory. |
| Sines / Alentejo | Sovereign secondary | 27% | 1.7 | 23 | EUR 17 m | Atlantic cable hub, Start Campus proves 1 GW-class grid; renewables. |
| Porto / North | Government / continuity | 22% | 1.4 | 19 | EUR 14 m | 300 km separation, lower seismicity, Douro hydro. |
| Coimbra / Centre | Strategic reserve | 10% | 0.6 | 8 | EUR 6 m | Inland reserve between the two metros. |

These regions encode only the obvious constraints (capital estate, second metro, distance from the frontier,
fault or flood zone). They are to be replaced by the scored site selection in workstream A of the Dutch
`TODO.md` (grid capacity, flood risk, fibre, failure independence, physical security, land, cooling).

## 7. Geography and threat notes

Seismic/tsunami exposure Lisbon-Algarve-Azores (1755 fault systems); wildfire and drought inland; Iberian grid island with weak links to France (Apr 2025 blackout) but cheap high-renewable power and land near Sines; very low geopolitical risk

## 8. Recommendations specific to Portugal

1. **Anchor on Chave Movel Digital.** Digital identity is the workload that, if it fails, stops every other
   government service; it belongs in the sovereign core first, active-active across at least two regions.
2. **Build on the existing estate, do not replace it.** Plano Nacional de Nuvem Soberana - approved May 2026 (ARTE): data classification, technical requirements, phased state sovereign-cloud infrastructure is the
   institutional starting point; the sovereign core should be its next generation, with one governance owner.
3. **Site posture: standard.** Standard Tier III+ with 50-100 km separation is sufficient; spend the hardening budget on supply-chain assurance instead.
4. **Power strategy.** Power is the binding constraint; treat grid connection lead time and on-site generation as first-order site criteria.
5. **Hybrid tier.** With no in-country hyperscaler region, define now which non-critical workloads may leave the jurisdiction and under what contract terms.

## 9. Open questions

- Replace scaled workload rows with real ministry/agency demand (see `countries/NL/CAPACITY_PLAN.md` for the method).
- Which body owns the sovereign core, and how are agencies compelled or incentivised to migrate?
- Which regions federate with EU partners for mutual disaster recovery, and which stay national-only?
- Site-size assumption: is the 12 MW planning unit right for Portugal, or should sites be smaller?
