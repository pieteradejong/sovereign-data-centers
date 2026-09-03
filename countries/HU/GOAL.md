# Hungary - Sovereign Government Data Center Network

> Generated 2026-09-01 by `model/generate_countries.py` from the Dutch reference case
> (`countries/NL/GOAL.md`) and `model/eu27_parameters.csv`. Every number below is a **scaled working
> assumption**, not a sourced figure. Edit the CSVs in this directory and re-run
> `python3 model/capacity_model.py HU` to update the capacity numbers; edit
> `model/eu27_parameters.csv` or `model/scaling_rules.csv` and re-run the generator to update this file.

## 1. Working thesis

Hungary does not need to become technologically autarkic. It needs enough independently controlled compute,
storage, networking, identity, cryptography and operational capability that the state can continue functioning
when foreign commercial infrastructure is unavailable, politically constrained, compromised, or no longer
trustworthy. The Dutch design rules (sovereignty is a stack, not a building; 3-5 separated regions; dual fibre
paths; no single hardware supplier; a first-class developer platform) are taken as the starting point and
adjusted below for what is structurally different about Hungary.

## 2. Starting point

| | |
|---|---|
| Population | 9.54 m (Eurostat, 1 Jan 2025) |
| GDP | EUR 219 bn (2025, current prices) |
| Public administration employment (NACE O) | 398 k (Eurostat LFS 2025) |
| Non-household electricity price | 213.2 EUR/MWh (Eurostat, band IC, 2025-S2) |
| Renewables in electricity | 24.1% (2024) |
| Land area | 91,248 km2 |
| Live hyperscaler regions in-country | 0 |
| Existing government / sovereign cloud | Kormanyzati Felho (Government Cloud) + Kormanyzati Adatkozpont (KAK) operated by NISZ Zrt. under the Digital Hungary Agency; ministry IT consolidation by decree |
| National digital identity (anchor workload) | DAP - Digitalis Allampolgarsag app + eSzemelyi eID |
| Internet exchange / cable landings | BIX Budapest; landlocked |

Relative to the Dutch baseline: population x0.53, public administration x0.55,
GDP x0.19. Resulting design load: x0.40 the Dutch figure.

## 3. What is structurally different from the Dutch case

- **Expensive power (213 EUR/MWh vs. EU average ~184).** Power is the dominant OPEX line; free cooling, heat reuse, and siting near renewables or nuclear baseload move the economics more than server choice does. The model's power OPEX line is the number to attack first.
- **No hyperscaler region in-country.** Unlike the Netherlands, there is no commercial hyperscale tier to fall back on for non-critical workloads without leaving the jurisdiction. The sovereign core therefore has to be sized for a larger share of total government demand, and the hybrid model (Dutch GOAL.md section 7) needs a cross-border commercial tier.

## 4. Workload demand (scaled from the Dutch baseline)

Scaling weights per workload class are in `model/scaling_rules.csv`; the Dutch rows they scale are in
`countries/NL/workloads_inputs.csv`. Frontline multiplier applied: no.

| Workload | Class | CPU cores | GPU eq. | Storage (PB) | Avail. factor |
|---|---|---:|---:|---:|---:|
| Digital identity / DAP - Digitalis Allampolgarsag app + eSzemelyi eID | Critical government | 9,500 | 0 | 2.1 | 1.5 |
| Core government applications | Government | 29,800 | 0 | 9.8 | 1.35 |
| Data platforms & analytics | Government data | 12,500 | 32 | 21.5 | 1.25 |
| AI / sovereign model serving | AI | 3,400 | 96 | 2.2 | 1.3 |
| Defense classified compute | Defense | 15,900 | 136 | 7.9 | 1.5 |
| Cybersecurity / SOC / telemetry | Security | 11,800 | 16 | 13.4 | 1.4 |
| Scientific / public research | Research | 4,900 | 24 | 3.7 | 1.15 |

## 5. Capacity model output

| Metric | Value |
|---|---:|
| Physical servers | 2,415 (CPU 1,715 / GPU 90 / storage 610) |
| Rack equivalents | ~75 |
| IT critical load | 3.8 MW |
| Facility load (PUE 1.25) | 4.7 MW |
| Facility design load (+20% headroom) | **5.7 MW** |
| Sites by capacity / recommended | 1 / **3** (minimum 3) |
| Average design MW per site | 1.9 MW |
| Total CAPEX | **EUR 132 m** (facility EUR 57 m, IT EUR 64 m, network EUR 11 m) |
| Annual energy | 41,550 MWh |
| Annual OPEX | **EUR 15 m / yr** (power EUR 9 m, non-power EUR 6 m) |

Full table: `facility_summary.csv`.

## 6. Proposed geography (first-pass hypothesis)

Site posture: standard. Separation target: 50-100 km failure domains, dual fibre paths, distinct grid feeds.

| Region | Role | Share | Design MW | Racks | Facility CAPEX | Notes |
|---|---|---:|---:|---:|---:|---|
| Budapest | Primary civil cloud | 40% | 2.3 | 31 | EUR 23 m | NISZ KAK estate, BIX; Danube flood zoning applies. |
| Debrecen / East | Sovereign secondary | 27% | 1.5 | 20 | EUR 15 m | Industrial grid growth; 130 km from the Ukrainian border - hardened design. |
| Szeged - Pecs / South | Government / continuity | 22% | 1.3 | 17 | EUR 13 m | Solar belt, southern separation. |
| Gyor / West | Strategic reserve | 10% | 0.6 | 8 | EUR 6 m | Closest to Vienna/Bratislava transit; reserve. |

These regions encode only the obvious constraints (capital estate, second metro, distance from the frontier,
fault or flood zone). They are to be replaced by the scored site selection in workstream A of the Dutch
`TODO.md` (grid capacity, flood risk, fibre, failure independence, physical security, land, cooling).

## 7. Geography and threat notes

Low-moderate seismic; Danube/Tisza floods (2024); flat land abundant, water stress rising; Paks nuclear + Paks II (Rosatom) - Russian nuclear fuel and TurkStream gas dependence; ~25% power imports; 4th-highest EU industrial power price; ~130 km from Ukraine

## 8. Recommendations specific to Hungary

1. **Anchor on DAP - Digitalis Allampolgarsag app + eSzemelyi eID.** Digital identity is the workload that, if it fails, stops every other
   government service; it belongs in the sovereign core first, active-active across at least two regions.
2. **Build on the existing estate, do not replace it.** Kormanyzati Felho (Government Cloud) + Kormanyzati Adatkozpont (KAK) operated by NISZ Zrt. under the Digital Hungary Agency is the
   institutional starting point; the sovereign core should be its next generation, with one governance owner.
3. **Site posture: standard.** Standard Tier III+ with 50-100 km separation is sufficient; spend the hardening budget on supply-chain assurance instead.
4. **Power strategy.** Power is the binding constraint; treat grid connection lead time and on-site generation as first-order site criteria.
5. **Hybrid tier.** With no in-country hyperscaler region, define now which non-critical workloads may leave the jurisdiction and under what contract terms.

## 9. Open questions

- Replace scaled workload rows with real ministry/agency demand (see `countries/NL/CAPACITY_PLAN.md` for the method).
- Which body owns the sovereign core, and how are agencies compelled or incentivised to migrate?
- Which regions federate with EU partners for mutual disaster recovery, and which stay national-only?
- Site-size assumption: is the 12 MW planning unit right for Hungary, or should sites be smaller?
