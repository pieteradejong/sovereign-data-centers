# Czechia - Sovereign Government Data Center Network

> Generated 2026-09-01 by `model/generate_countries.py` from the Dutch reference case
> (`countries/NL/GOAL.md`) and `model/eu27_parameters.csv`. Every number below is a **scaled working
> assumption**, not a sourced figure. Edit the CSVs in this directory and re-run
> `python3 model/capacity_model.py CZ` to update the capacity numbers; edit
> `model/eu27_parameters.csv` or `model/scaling_rules.csv` and re-run the generator to update this file.

## 1. Working thesis

Czechia does not need to become technologically autarkic. It needs enough independently controlled compute,
storage, networking, identity, cryptography and operational capability that the state can continue functioning
when foreign commercial infrastructure is unavailable, politically constrained, compromised, or no longer
trustworthy. The Dutch design rules (sovereignty is a stack, not a building; 3-5 separated regions; dual fibre
paths; no single hardware supplier; a first-class developer platform) are taken as the starting point and
adjusted below for what is structurally different about Czechia.

## 2. Starting point

| | |
|---|---|
| Population | 10.41 m (Eurostat, 1 Jan 2025) |
| GDP | EUR 347 bn (2025, current prices) |
| Public administration employment (NACE O) | 343 k (Eurostat LFS 2025) |
| Non-household electricity price | 182.5 EUR/MWh (Eurostat, band IC, 2025-S2) |
| Renewables in electricity | 17.9% (2024) |
| Land area | 77,212 km2 |
| Live hyperscaler regions in-country | 0 |
| Existing government / sovereign cloud | eGovernment Cloud (eGC) under the Digital and Information Agency (DIA): state part operated by SPCSS (security level 4) + NAKIT; commercial catalogue (Azure OCI Google AWS) |
| National digital identity (anchor workload) | Identita obcana (NIA) / eDoklady / BankID |
| Internet exchange / cable landings | NIX.CZ Prague; landlocked |

Relative to the Dutch baseline: population x0.58, public administration x0.48,
GDP x0.30. Resulting design load: x0.46 the Dutch figure.

## 3. What is structurally different from the Dutch case

- **No hyperscaler region in-country.** Unlike the Netherlands, there is no commercial hyperscale tier to fall back on for non-critical workloads without leaving the jurisdiction. The sovereign core therefore has to be sized for a larger share of total government demand, and the hybrid model (Dutch GOAL.md section 7) needs a cross-border commercial tier.

## 4. Workload demand (scaled from the Dutch baseline)

Scaling weights per workload class are in `model/scaling_rules.csv`; the Dutch rows they scale are in
`countries/NL/workloads_inputs.csv`. Frontline multiplier applied: no.

| Workload | Class | CPU cores | GPU eq. | Storage (PB) | Avail. factor |
|---|---|---:|---:|---:|---:|
| Digital identity / Identita obcana | Critical government | 10,400 | 0 | 2.3 | 1.5 |
| Core government applications | Government | 29,000 | 0 | 9.5 | 1.35 |
| Data platforms & analytics | Government data | 15,300 | 32 | 26.2 | 1.25 |
| AI / sovereign model serving | AI | 5,300 | 152 | 3.6 | 1.3 |
| Defense classified compute | Defense | 17,300 | 144 | 8.7 | 1.5 |
| Cybersecurity / SOC / telemetry | Security | 12,000 | 16 | 13.7 | 1.4 |
| Scientific / public research | Research | 7,700 | 40 | 5.9 | 1.15 |

## 5. Capacity model output

| Metric | Value |
|---|---:|
| Physical servers | 2,692 (CPU 1,883 / GPU 111 / storage 698) |
| Rack equivalents | ~84 |
| IT critical load | 4.3 MW |
| Facility load (PUE 1.25) | 5.4 MW |
| Facility design load (+20% headroom) | **6.5 MW** |
| Sites by capacity / recommended | 1 / **3** (minimum 3) |
| Average design MW per site | 2.2 MW |
| Total CAPEX | **EUR 152 m** (facility EUR 65 m, IT EUR 74 m, network EUR 13 m) |
| Annual energy | 47,162 MWh |
| Annual OPEX | **EUR 15 m / yr** (power EUR 9 m, non-power EUR 7 m) |

Full table: `facility_summary.csv`.

## 6. Proposed geography (first-pass hypothesis)

Site posture: standard. Separation target: 50-100 km failure domains, dual fibre paths, distinct grid feeds.

| Region | Role | Share | Design MW | Racks | Facility CAPEX | Notes |
|---|---|---:|---:|---:|---:|---|
| Prague - Central Bohemia | Primary civil cloud | 40% | 2.6 | 34 | EUR 26 m | SPCSS/NAKIT estate, NIX.CZ; Vltava flood zoning applies. |
| Brno / South Moravia | Sovereign secondary | 27% | 1.7 | 23 | EUR 17 m | Second metro, research cluster, 200 km separation. |
| Ostrava / Moravia-Silesia | Government / continuity | 22% | 1.4 | 19 | EUR 14 m | Industrial grid; post-coal land availability. |
| Plzen / West Bohemia | Strategic reserve | 10% | 0.7 | 8 | EUR 6 m | Western reserve, furthest from the eastern frontier. |

These regions encode only the obvious constraints (capital estate, second metro, distance from the frontier,
fault or flood zone). They are to be replaced by the scored site selection in workstream A of the Dutch
`TODO.md` (grid capacity, flood risk, fibre, failure independence, physical security, land, cooling).

## 7. Geography and threat notes

Low seismic; Vltava/Elbe/Morava floods (2024); central location with good land; nuclear baseload (new Dukovany units) but coal exit and gas import; NATO; ~300 km from Ukraine; Russian sabotage/espionage incidents 2024-25

## 8. Recommendations specific to Czechia

1. **Anchor on Identita obcana.** Digital identity is the workload that, if it fails, stops every other
   government service; it belongs in the sovereign core first, active-active across at least two regions.
2. **Build on the existing estate, do not replace it.** eGovernment Cloud (eGC) under the Digital and Information Agency (DIA): state part operated by SPCSS (security level 4) + NAKIT is the
   institutional starting point; the sovereign core should be its next generation, with one governance owner.
3. **Site posture: standard.** Standard Tier III+ with 50-100 km separation is sufficient; spend the hardening budget on supply-chain assurance instead.
4. **Power strategy.** Power is not the binding constraint; optimise for fibre diversity and failure-domain separation.
5. **Hybrid tier.** With no in-country hyperscaler region, define now which non-critical workloads may leave the jurisdiction and under what contract terms.

## 9. Open questions

- Replace scaled workload rows with real ministry/agency demand (see `countries/NL/CAPACITY_PLAN.md` for the method).
- Which body owns the sovereign core, and how are agencies compelled or incentivised to migrate?
- Which regions federate with EU partners for mutual disaster recovery, and which stay national-only?
- Site-size assumption: is the 12 MW planning unit right for Czechia, or should sites be smaller?
