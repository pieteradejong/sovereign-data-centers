# Lithuania - Sovereign Government Data Center Network

> Generated 2026-09-01 by `model/generate_countries.py` from the Dutch reference case
> (`countries/NL/GOAL.md`) and `model/eu27_parameters.csv`. Every number below is a **scaled working
> assumption**, not a sourced figure. Edit the CSVs in this directory and re-run
> `python3 model/capacity_model.py LT` to update the capacity numbers; edit
> `model/eu27_parameters.csv` or `model/scaling_rules.csv` and re-run the generator to update this file.

## 1. Working thesis

Lithuania does not need to become technologically autarkic. It needs enough independently controlled compute,
storage, networking, identity, cryptography and operational capability that the state can continue functioning
when foreign commercial infrastructure is unavailable, politically constrained, compromised, or no longer
trustworthy. The Dutch design rules (sovereignty is a stack, not a building; 3-5 separated regions; dual fibre
paths; no single hardware supplier; a first-class developer platform) are taken as the starting point and
adjusted below for what is structurally different about Lithuania.

## 2. Starting point

| | |
|---|---|
| Population | 2.89 m (Eurostat, 1 Jan 2025) |
| GDP | EUR 84 bn (2025, current prices) |
| Public administration employment (NACE O) | 94 k (Eurostat LFS 2025) |
| Non-household electricity price | 159.1 EUR/MWh (Eurostat, band IC, 2025-S2) |
| Renewables in electricity | 49.0% (2024) |
| Land area | 62,643 km2 |
| Live hyperscaler regions in-country | 0 |
| Existing government / sovereign cloud | Valstybes debesija (State Cloud) - operated by KVTC under the Ministry of National Defence in state data centres |
| National digital identity (anchor workload) | eID / Mobile-ID / Smart-ID |
| Internet exchange / cable landings | LIXP Vilnius/Kaunas; no own subsea (NordBalt fibre to SE) |

Relative to the Dutch baseline: population x0.16, public administration x0.13,
GDP x0.07. Resulting design load: x0.15 the Dutch figure.

## 3. What is structurally different from the Dutch case

- **Frontline exposure.** A land border with Russia or Belarus (or a Black Sea coast facing the war) changes the threat model from *geopolitical supply disruption* to *kinetic and sabotage risk against the facilities themselves*. Defense and security workloads are scaled up 1.5x/1.25x in the baseline, and at least one site should be hardened (EMP/blast, autonomous power for weeks, not hours). A purely national footprint cannot provide the out-of-country cold copy that Estonia's Data Embassy already demonstrates; this is the first item to revisit when the EU federation layer (Dutch GOAL.md section 16) is modelled.
- **No hyperscaler region in-country.** Unlike the Netherlands, there is no commercial hyperscale tier to fall back on for non-critical workloads without leaving the jurisdiction. The sovereign core therefore has to be sized for a larger share of total government demand, and the hybrid model (Dutch GOAL.md section 7) needs a cross-border commercial tier.

## 4. Workload demand (scaled from the Dutch baseline)

Scaling weights per workload class are in `model/scaling_rules.csv`; the Dutch rows they scale are in
`countries/NL/workloads_inputs.csv`. Frontline multiplier applied: yes.

| Workload | Class | CPU cores | GPU eq. | Storage (PB) | Avail. factor |
|---|---|---:|---:|---:|---:|
| Digital identity / eID | Critical government | 2,900 | 0 | 0.6 | 1.5 |
| Core government applications | Government | 8,000 | 0 | 2.6 | 1.35 |
| Data platforms & analytics | Government data | 4,100 | 8 | 7.0 | 1.25 |
| AI / sovereign model serving | AI | 1,300 | 40 | 0.9 | 1.3 |
| Defense classified compute | Defense | 7,200 | 64 | 3.6 | 1.5 |
| Cybersecurity / SOC / telemetry | Security | 4,200 | 8 | 4.7 | 1.4 |
| Scientific / public research | Research | 1,900 | 8 | 1.4 | 1.15 |

## 5. Capacity model output

| Metric | Value |
|---|---:|
| Physical servers | 836 (CPU 584 / GPU 39 / storage 213) |
| Rack equivalents | ~26 |
| IT critical load | 1.4 MW |
| Facility load (PUE 1.25) | 1.7 MW |
| Facility design load (+20% headroom) | **2.1 MW** |
| Sites by capacity / recommended | 1 / **3** (minimum 3) |
| Average design MW per site | 0.7 MW |
| Total CAPEX | **EUR 49 m** (facility EUR 21 m, IT EUR 24 m, network EUR 4 m) |
| Annual energy | 15,033 MWh |
| Annual OPEX | **EUR 5 m / yr** (power EUR 2 m, non-power EUR 2 m) |

Full table: `facility_summary.csv`.

## 6. Proposed geography (first-pass hypothesis)

Site posture: hardened (frontline). Separation target: 50-100 km failure domains, dual fibre paths, distinct grid feeds.

| Region | Role | Share | Design MW | Racks | Facility CAPEX | Notes |
|---|---|---:|---:|---:|---:|---|
| Vilnius | Primary civil cloud | 40% | 0.8 | 11 | EUR 8 m | KVTC state DCs, LIXP; 30 km from Belarus - hardened design mandatory. |
| Kaunas | Sovereign secondary | 27% | 0.6 | 7 | EUR 6 m | Second metro, 100 km separation, KV Baltic campus. |
| Klaipeda | Government / continuity | 22% | 0.5 | 6 | EUR 5 m | LNG terminal, NordBalt fibre to Sweden; furthest from Belarus. |
| Out-of-country reserve | Strategic reserve | 10% | 0.2 | 3 | EUR 2 m | Follow the Estonian Data Embassy pattern - national-only model cannot close this gap. |

These regions encode only the obvious constraints (capital estate, second metro, distance from the frontier,
fault or flood zone). They are to be replaced by the scored site selection in workstream A of the Dutch
`TODO.md` (grid capacity, flood risk, fibre, failure independence, physical security, land, cooling).

## 7. Geography and threat notes

Between Kaliningrad and Belarus (Suwalki Gap) - highest frontline exposure; drone/GNSS incidents; no seismic; post-Ignalina electricity importer, Klaipeda LNG, Continental sync 2025; limited grid headroom for large loads

## 8. Recommendations specific to Lithuania

1. **Anchor on eID.** Digital identity is the workload that, if it fails, stops every other
   government service; it belongs in the sovereign core first, active-active across at least two regions.
2. **Build on the existing estate, do not replace it.** Valstybes debesija (State Cloud) - operated by KVTC under the Ministry of National Defence in state data centres is the
   institutional starting point; the sovereign core should be its next generation, with one governance owner.
3. **Site posture: hardened (frontline).** Harden at least one region and plan an out-of-country cold copy.
4. **Power strategy.** Power is not the binding constraint; optimise for fibre diversity and failure-domain separation.
5. **Hybrid tier.** With no in-country hyperscaler region, define now which non-critical workloads may leave the jurisdiction and under what contract terms.

## 9. Open questions

- Replace scaled workload rows with real ministry/agency demand (see `countries/NL/CAPACITY_PLAN.md` for the method).
- Which body owns the sovereign core, and how are agencies compelled or incentivised to migrate?
- Out-of-country reserve: which partner state, under what treaty?
- Site-size assumption: is the 12 MW planning unit right for Lithuania, or should sites be smaller?
