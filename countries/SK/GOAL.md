# Slovakia - Sovereign Government Data Center Network

> Generated 2026-09-01 by `model/generate_countries.py` from the Dutch reference case
> (`countries/NL/GOAL.md`) and `model/eu27_parameters.csv`. Every number below is a **scaled working
> assumption**, not a sourced figure. Edit the CSVs in this directory and re-run
> `python3 model/capacity_model.py SK` to update the capacity numbers; edit
> `model/eu27_parameters.csv` or `model/scaling_rules.csv` and re-run the generator to update this file.

## 1. Working thesis

Slovakia does not need to become technologically autarkic. It needs enough independently controlled compute,
storage, networking, identity, cryptography and operational capability that the state can continue functioning
when foreign commercial infrastructure is unavailable, politically constrained, compromised, or no longer
trustworthy. The Dutch design rules (sovereignty is a stack, not a building; 3-5 separated regions; dual fibre
paths; no single hardware supplier; a first-class developer platform) are taken as the starting point and
adjusted below for what is structurally different about Slovakia.

## 2. Starting point

| | |
|---|---|
| Population | 5.42 m (Eurostat, 1 Jan 2025) |
| GDP | EUR 137 bn (2025, current prices) |
| Public administration employment (NACE O) | 210 k (Eurostat LFS 2025) |
| Non-household electricity price | 209.0 EUR/MWh (Eurostat, band IC, 2025-S2) |
| Renewables in electricity | 24.9% (2024) |
| Land area | 48,702 km2 |
| Live hyperscaler regions in-country | 0 |
| Existing government / sovereign cloud | Vladny cloud (Government Cloud) - Ministry of Interior Datacentrum Kopcianska + MoF DataCentrum (backup Tajov); MIRRI governance; hybrid extension to certified providers |
| National digital identity (anchor workload) | eID (obciansky preukaz s cipom) / Slovensko v mobile |
| Internet exchange / cable landings | SIX Bratislava and NIX.SK; landlocked |

Relative to the Dutch baseline: population x0.30, public administration x0.29,
GDP x0.12. Resulting design load: x0.23 the Dutch figure.

## 3. What is structurally different from the Dutch case

- **Moderate seismic risk.** Seismic zoning should be a site-scoring criterion; at least two regions in different domains.
- **Expensive power (209 EUR/MWh vs. EU average ~184).** Power is the dominant OPEX line; free cooling, heat reuse, and siting near renewables or nuclear baseload move the economics more than server choice does. The model's power OPEX line is the number to attack first.
- **No hyperscaler region in-country.** Unlike the Netherlands, there is no commercial hyperscale tier to fall back on for non-critical workloads without leaving the jurisdiction. The sovereign core therefore has to be sized for a larger share of total government demand, and the hybrid model (Dutch GOAL.md section 7) needs a cross-border commercial tier.

## 4. Workload demand (scaled from the Dutch baseline)

Scaling weights per workload class are in `model/scaling_rules.csv`; the Dutch rows they scale are in
`countries/NL/workloads_inputs.csv`. Frontline multiplier applied: no.

| Workload | Class | CPU cores | GPU eq. | Storage (PB) | Avail. factor |
|---|---|---:|---:|---:|---:|
| Digital identity / eID | Critical government | 5,400 | 0 | 1.2 | 1.5 |
| Core government applications | Government | 16,300 | 0 | 5.3 | 1.35 |
| Data platforms & analytics | Government data | 7,300 | 16 | 12.5 | 1.25 |
| AI / sovereign model serving | AI | 2,100 | 56 | 1.4 | 1.3 |
| Defense classified compute | Defense | 9,000 | 80 | 4.5 | 1.5 |
| Cybersecurity / SOC / telemetry | Security | 6,600 | 8 | 7.5 | 1.4 |
| Scientific / public research | Research | 3,000 | 16 | 2.3 | 1.15 |

## 5. Capacity model output

| Metric | Value |
|---|---:|
| Physical servers | 1,375 (CPU 972 / GPU 53 / storage 350) |
| Rack equivalents | ~43 |
| IT critical load | 2.2 MW |
| Facility load (PUE 1.25) | 2.7 MW |
| Facility design load (+20% headroom) | **3.3 MW** |
| Sites by capacity / recommended | 1 / **3** (minimum 3) |
| Average design MW per site | 1.1 MW |
| Total CAPEX | **EUR 76 m** (facility EUR 33 m, IT EUR 37 m, network EUR 7 m) |
| Annual energy | 23,797 MWh |
| Annual OPEX | **EUR 8 m / yr** (power EUR 5 m, non-power EUR 3 m) |

Full table: `facility_summary.csv`.

## 6. Proposed geography (first-pass hypothesis)

Site posture: standard. Separation target: 50-100 km failure domains, dual fibre paths, distinct grid feeds.

| Region | Role | Share | Design MW | Racks | Facility CAPEX | Notes |
|---|---|---:|---:|---:|---:|---|
| Bratislava | Primary civil cloud | 40% | 1.3 | 17 | EUR 13 m | MoI Kopcianska and MoF DataCentrum, SIX; Danube flood zoning. |
| Banska Bystrica / Centre | Sovereign secondary | 27% | 0.9 | 12 | EUR 9 m | MoF Tajov backup site; 200 km separation, cheap land. |
| Kosice / East | Government / continuity | 22% | 0.7 | 10 | EUR 7 m | Eastern metro; 80 km from Ukraine - hardened design. |
| Zilina / North | Strategic reserve | 10% | 0.3 | 4 | EUR 3 m | Hydro grid, Czech/Polish transit; reserve. |

These regions encode only the obvious constraints (capital estate, second metro, distance from the frontier,
fault or flood zone). They are to be replaced by the scored site selection in workstream A of the Dutch
`TODO.md` (grid capacity, flood risk, fibre, failure independence, physical security, land, cooling).

## 7. Geography and threat notes

Low-moderate seismic (Zilina/Komarno zones); Danube/Vah floods (2024); short Ukraine border; gas-transit dependency (Russian transit ended Jan 2025); nuclear ~60% reliable baseload but high industrial price; cheap land in centre/east

## 8. Recommendations specific to Slovakia

1. **Anchor on eID.** Digital identity is the workload that, if it fails, stops every other
   government service; it belongs in the sovereign core first, active-active across at least two regions.
2. **Build on the existing estate, do not replace it.** Vladny cloud (Government Cloud) - Ministry of Interior Datacentrum Kopcianska + MoF DataCentrum (backup Tajov) is the
   institutional starting point; the sovereign core should be its next generation, with one governance owner.
3. **Site posture: standard.** Standard Tier III+ with 50-100 km separation is sufficient; spend the hardening budget on supply-chain assurance instead.
4. **Power strategy.** Power is the binding constraint; treat grid connection lead time and on-site generation as first-order site criteria.
5. **Hybrid tier.** With no in-country hyperscaler region, define now which non-critical workloads may leave the jurisdiction and under what contract terms.

## 9. Open questions

- Replace scaled workload rows with real ministry/agency demand (see `countries/NL/CAPACITY_PLAN.md` for the method).
- Which body owns the sovereign core, and how are agencies compelled or incentivised to migrate?
- Which regions federate with EU partners for mutual disaster recovery, and which stay national-only?
- Site-size assumption: is the 12 MW planning unit right for Slovakia, or should sites be smaller?
