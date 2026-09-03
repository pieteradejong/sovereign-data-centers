# Greece - Sovereign Government Data Center Network

> Generated 2026-09-01 by `model/generate_countries.py` from the Dutch reference case
> (`countries/NL/GOAL.md`) and `model/eu27_parameters.csv`. Every number below is a **scaled working
> assumption**, not a sourced figure. Edit the CSVs in this directory and re-run
> `python3 model/capacity_model.py EL` to update the capacity numbers; edit
> `model/eu27_parameters.csv` or `model/scaling_rules.csv` and re-run the generator to update this file.

## 1. Working thesis

Greece does not need to become technologically autarkic. It needs enough independently controlled compute,
storage, networking, identity, cryptography and operational capability that the state can continue functioning
when foreign commercial infrastructure is unavailable, politically constrained, compromised, or no longer
trustworthy. The Dutch design rules (sovereignty is a stack, not a building; 3-5 separated regions; dual fibre
paths; no single hardware supplier; a first-class developer platform) are taken as the starting point and
adjusted below for what is structurally different about Greece.

## 2. Starting point

| | |
|---|---|
| Population | 10.59 m (Eurostat, 1 Jan 2025) |
| GDP | EUR 248 bn (2025, current prices) |
| Public administration employment (NACE O) | 346 k (Eurostat LFS 2025) |
| Non-household electricity price | 174.0 EUR/MWh (Eurostat, band IC, 2025-S2) |
| Renewables in electricity | 51.2% (2024) |
| Land area | 130,048 km2 |
| Live hyperscaler regions in-country | 0 |
| Existing government / sovereign cloud | G-Cloud (Single Government Cloud) - GSIS / Ministry of Digital Governance Tier-3 DC on SYZEFXIS; GRNET research cloud/HPC and EUDI wallet lead; hybrid policy for non-critical data |
| National digital identity (anchor workload) | gov.gr Wallet (TaxisNet-based) |
| Internet exchange / cable landings | GR-IX Athens; Crete (Chania) and Attica East-Med landings |

Relative to the Dutch baseline: population x0.59, public administration x0.48,
GDP x0.21. Resulting design load: x0.43 the Dutch figure.

## 3. What is structurally different from the Dutch case

- **High seismic risk.** Base isolation or seismic-rated structures are mandatory, not optional, at the primary site; the second and third regions should be chosen in a different seismic domain so a single event cannot take out two regions. Expect facility CAPEX above the EUR 10 m/MW planning figure.
- **No hyperscaler region in-country.** Unlike the Netherlands, there is no commercial hyperscale tier to fall back on for non-critical workloads without leaving the jurisdiction. The sovereign core therefore has to be sized for a larger share of total government demand, and the hybrid model (Dutch GOAL.md section 7) needs a cross-border commercial tier.

## 4. Workload demand (scaled from the Dutch baseline)

Scaling weights per workload class are in `model/scaling_rules.csv`; the Dutch rows they scale are in
`countries/NL/workloads_inputs.csv`. Frontline multiplier applied: no.

| Workload | Class | CPU cores | GPU eq. | Storage (PB) | Avail. factor |
|---|---|---:|---:|---:|---:|
| Digital identity / gov.gr Wallet | Critical government | 10,600 | 0 | 2.3 | 1.5 |
| Core government applications | Government | 29,400 | 0 | 9.6 | 1.35 |
| Data platforms & analytics | Government data | 14,000 | 32 | 24.0 | 1.25 |
| AI / sovereign model serving | AI | 3,800 | 112 | 2.5 | 1.3 |
| Defense classified compute | Defense | 17,600 | 152 | 8.8 | 1.5 |
| Cybersecurity / SOC / telemetry | Security | 12,200 | 16 | 13.9 | 1.4 |
| Scientific / public research | Research | 5,500 | 24 | 4.2 | 1.15 |

## 5. Capacity model output

| Metric | Value |
|---|---:|
| Physical servers | 2,573 (CPU 1,818 / GPU 99 / storage 656) |
| Rack equivalents | ~80 |
| IT critical load | 4.1 MW |
| Facility load (PUE 1.25) | 5.1 MW |
| Facility design load (+20% headroom) | **6.1 MW** |
| Sites by capacity / recommended | 1 / **3** (minimum 3) |
| Average design MW per site | 2.0 MW |
| Total CAPEX | **EUR 142 m** (facility EUR 61 m, IT EUR 69 m, network EUR 12 m) |
| Annual energy | 44,513 MWh |
| Annual OPEX | **EUR 14 m / yr** (power EUR 8 m, non-power EUR 6 m) |

Full table: `facility_summary.csv`.

## 6. Proposed geography (first-pass hypothesis)

Site posture: standard. Separation target: 50-100 km failure domains, dual fibre paths, distinct grid feeds.

| Region | Role | Share | Design MW | Racks | Facility CAPEX | Notes |
|---|---|---:|---:|---:|---:|---|
| Attica / Athens | Primary civil cloud | 40% | 2.5 | 33 | EUR 25 m | GSIS G-Cloud, GR-IX, Microsoft Spata campus; seismic design mandatory. |
| Thessaloniki / Central Macedonia | Sovereign secondary | 27% | 1.6 | 22 | EUR 16 m | Second metro, 300 km separation, Balkan transit. |
| Western Greece / Patras | Government / continuity | 22% | 1.4 | 18 | EUR 14 m | Adriatic cable routes; separate seismic domain. |
| Crete / Chania | Strategic reserve | 10% | 0.6 | 8 | EUR 6 m | East-Med cable hub and Great Sea Interconnector; island - reserve/edge only. |

These regions encode only the obvious constraints (capital estate, second metro, distance from the frontier,
fault or flood zone). They are to be replaced by the scored site selection in workstream A of the Dutch
`TODO.md` (grid capacity, flood risk, fibre, failure independence, physical security, land, cooling).

## 7. Geography and threat notes

HIGH seismic (Aegean arc; Athens 1999; Crete 2021) - seismic design mandatory; wildfire/extreme heat; flash floods (Thessaly 2023); mountainous with sites in Attica/Thessaloniki; Attica grid needs upgrade; LNG gas import; NATO; Turkey tensions

## 8. Recommendations specific to Greece

1. **Anchor on gov.gr Wallet.** Digital identity is the workload that, if it fails, stops every other
   government service; it belongs in the sovereign core first, active-active across at least two regions.
2. **Build on the existing estate, do not replace it.** G-Cloud (Single Government Cloud) - GSIS / Ministry of Digital Governance Tier-3 DC on SYZEFXIS is the
   institutional starting point; the sovereign core should be its next generation, with one governance owner.
3. **Site posture: standard.** Standard Tier III+ with 50-100 km separation is sufficient; spend the hardening budget on supply-chain assurance instead.
4. **Power strategy.** Power is not the binding constraint; optimise for fibre diversity and failure-domain separation.
5. **Hybrid tier.** With no in-country hyperscaler region, define now which non-critical workloads may leave the jurisdiction and under what contract terms.

## 9. Open questions

- Replace scaled workload rows with real ministry/agency demand (see `countries/NL/CAPACITY_PLAN.md` for the method).
- Which body owns the sovereign core, and how are agencies compelled or incentivised to migrate?
- Which regions federate with EU partners for mutual disaster recovery, and which stay national-only?
- Site-size assumption: is the 12 MW planning unit right for Greece, or should sites be smaller?
