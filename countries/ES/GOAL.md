# Spain - Sovereign Government Data Center Network

> Generated 2026-09-01 by `model/generate_countries.py` from the Dutch reference case
> (`countries/NL/GOAL.md`) and `model/eu27_parameters.csv`. Every number below is a **scaled working
> assumption**, not a sourced figure. Edit the CSVs in this directory and re-run
> `python3 model/capacity_model.py ES` to update the capacity numbers; edit
> `model/eu27_parameters.csv` or `model/scaling_rules.csv` and re-run the generator to update this file.

## 1. Working thesis

Spain does not need to become technologically autarkic. It needs enough independently controlled compute,
storage, networking, identity, cryptography and operational capability that the state can continue functioning
when foreign commercial infrastructure is unavailable, politically constrained, compromised, or no longer
trustworthy. The Dutch design rules (sovereignty is a stack, not a building; 3-5 separated regions; dual fibre
paths; no single hardware supplier; a first-class developer platform) are taken as the starting point and
adjusted below for what is structurally different about Spain.

## 2. Starting point

| | |
|---|---|
| Population | 49.13 m (Eurostat, 1 Jan 2025) |
| GDP | EUR 1,687 bn (2025, current prices) |
| Public administration employment (NACE O) | 1,401 k (Eurostat LFS 2025) |
| Non-household electricity price | 132.4 EUR/MWh (Eurostat, band IC, 2025-S2) |
| Renewables in electricity | 59.7% (2024) |
| Land area | 502,654 km2 |
| Live hyperscaler regions in-country | 3 |
| Existing government / sovereign cloud | No single state cloud: Nube SARA / SGAD common services, sectoral ENS-Alta clouds (AEAT, GISS); regional sovereign clouds emerging (Madrid 2026); Telefonica/IBM, Indra, Oracle sovereign offers under ENS |
| National digital identity (anchor workload) | Cl@ve / DNIe |
| Internet exchange / cable landings | DE-CIX Madrid and ESpanix; landings Bilbao (MAREA |

Relative to the Dutch baseline: population x2.72, public administration x1.96,
GDP x1.44. Resulting design load: x2.13 the Dutch figure.

## 3. What is structurally different from the Dutch case

- **Grid isolation.** The national grid is an electrical island or nearly so (weak or single interconnection). The April 2025 Iberian blackout and Cyprus/Malta interconnector outages show the failure mode. Every site needs on-site generation and storage sized for multi-day ride-through, and the PUE and facility CAPEX assumptions should be revisited upward once site studies exist.
- **Dense hyperscaler presence (3 live regions).** Commercial capacity, fibre and skills exist in-country; the sovereign core can stay lean and the hybrid model works as designed. The risk is the opposite one: political pressure to declare a hyperscaler region 'sovereign enough' (Dutch GOAL.md section 17: location is not sovereignty).

## 4. Workload demand (scaled from the Dutch baseline)

Scaling weights per workload class are in `model/scaling_rules.csv`; the Dutch rows they scale are in
`countries/NL/workloads_inputs.csv`. Frontline multiplier applied: no.

| Workload | Class | CPU cores | GPU eq. | Storage (PB) | Avail. factor |
|---|---|---:|---:|---:|---:|
| Digital identity / Cl@ve | Critical government | 49,000 | 0 | 10.9 | 1.5 |
| Core government applications | Government | 128,700 | 0 | 42.1 | 1.35 |
| Data platforms & analytics | Government data | 72,900 | 168 | 124.9 | 1.25 |
| AI / sovereign model serving | AI | 25,900 | 736 | 17.3 | 1.3 |
| Defense classified compute | Defense | 81,700 | 696 | 40.9 | 1.5 |
| Cybersecurity / SOC / telemetry | Security | 54,800 | 80 | 62.3 | 1.4 |
| Scientific / public research | Research | 37,500 | 184 | 28.8 | 1.15 |

## 5. Capacity model output

| Metric | Value |
|---|---:|
| Physical servers | 12,517 (CPU 8,731 / GPU 531 / storage 3,255) |
| Rack equivalents | ~391 |
| IT critical load | 20.1 MW |
| Facility load (PUE 1.25) | 25.2 MW |
| Facility design load (+20% headroom) | **30.2 MW** |
| Sites by capacity / recommended | 3 / **4** (minimum 4) |
| Average design MW per site | 7.6 MW |
| Total CAPEX | **EUR 711 m** (facility EUR 302 m, IT EUR 346 m, network EUR 62 m) |
| Annual energy | 220,509 MWh |
| Annual OPEX | **EUR 61 m / yr** (power EUR 29 m, non-power EUR 32 m) |

Full table: `facility_summary.csv`.

## 6. Proposed geography (first-pass hypothesis)

Site posture: standard. Separation target: 50-100 km failure domains, dual fibre paths, distinct grid feeds.

| Region | Role | Share | Design MW | Racks | Facility CAPEX | Notes |
|---|---|---:|---:|---:|---:|---|
| Madrid | Primary civil cloud | 36% | 10.9 | 141 | EUR 109 m | SGAD/AEAT/GISS estate, DE-CIX Madrid/ESpanix, two hyperscaler regions; connection queues. |
| Aragon / Zaragoza | Sovereign secondary | 18% | 5.4 | 70 | EUR 54 m | AWS/Microsoft campuses prove grid; renewables, 300 km separation. |
| Catalonia / Barcelona | Government / continuity | 18% | 5.4 | 70 | EUR 54 m | Mediterranean cable landings (2Africa, Medusa), CATNIX. |
| Andalusia / Seville - Malaga | Defense / industrial | 18% | 5.4 | 70 | EUR 54 m | Southern separation, solar belt; water-stress cooling design. |
| Castilla y Leon - Galicia | Strategic reserve | 10% | 3.0 | 39 | EUR 30 m | Wind/hydro surplus, Bilbao Atlantic landings nearby; reserve. |

These regions encode only the obvious constraints (capital estate, second metro, distance from the frontier,
fault or flood zone). They are to be replaced by the scored site selection in workstream A of the Dutch
`TODO.md` (grid capacity, flood risk, fibre, failure independence, physical security, land, cooling).

## 7. Geography and threat notes

 Grace Hopper) and Barcelona (2Africa

## 8. Recommendations specific to Spain

1. **Anchor on Cl@ve.** Digital identity is the workload that, if it fails, stops every other
   government service; it belongs in the sovereign core first, active-active across at least two regions.
2. **Build on the existing estate, do not replace it.** No single state cloud: Nube SARA / SGAD common services, sectoral ENS-Alta clouds (AEAT, GISS) is the
   institutional starting point; the sovereign core should be its next generation, with one governance owner.
3. **Site posture: standard.** Standard Tier III+ with 50-100 km separation is sufficient; spend the hardening budget on supply-chain assurance instead.
4. **Power strategy.** Power is the binding constraint; treat grid connection lead time and on-site generation as first-order site criteria.
5. **Hybrid tier.** Use in-country commercial regions for the non-critical tier, but keep identity, defense, security telemetry and registries in the sovereign core.

## 9. Open questions

- Replace scaled workload rows with real ministry/agency demand (see `countries/NL/CAPACITY_PLAN.md` for the method).
- Which body owns the sovereign core, and how are agencies compelled or incentivised to migrate?
- Which regions federate with EU partners for mutual disaster recovery, and which stay national-only?
- Site-size assumption: is the 12 MW planning unit right for Spain, or should sites be larger?
