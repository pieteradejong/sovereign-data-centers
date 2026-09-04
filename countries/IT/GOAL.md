# Italy - Sovereign Government Data Center Network

> Generated 2026-09-03 by `model/generate_countries.py` from the Dutch reference case
> (`countries/NL/GOAL.md`) and `model/eu27_parameters.csv`. Every number below is a **scaled working
> assumption**, not a sourced figure. Edit the CSVs in this directory and re-run
> `python3 model/capacity_model.py IT` to update the capacity numbers; edit
> `model/eu27_parameters.csv` or `model/scaling_rules.csv` and re-run the generator to update this file.

## 1. Working thesis

Italy does not need to become technologically autarkic. It needs enough independently controlled compute,
storage, networking, identity, cryptography and operational capability that the state can continue functioning
when foreign commercial infrastructure is unavailable, politically constrained, compromised, or no longer
trustworthy. The Dutch design rules (sovereignty is a stack, not a building; 3-5 separated regions; dual fibre
paths; no single hardware supplier; a first-class developer platform) are taken as the starting point and
adjusted below for what is structurally different about Italy.

## 2. Starting point

| | |
|---|---|
| Population | 58.94 m (Eurostat, 1 Jan 2025) |
| GDP | EUR 2,258 bn (2025, current prices) |
| Public administration employment (NACE O) | 1,159 k (Eurostat LFS 2025) |
| Non-household electricity price | 220.3 EUR/MWh (Eurostat, band IC, 2025-S2) |
| Renewables in electricity | 40.7% (2024) |
| Land area | 297,825 km2 |
| Live hyperscaler regions in-country | 4 |
| Existing government / sovereign cloud | Polo Strategico Nazionale (PSN) - operational since 2023, TIM/Leonardo/CDP/Sogei consortium, 4 DC pairs; ACN cloud qualification regime (Strategia Cloud Italia) |
| National digital identity (anchor workload) | SPID / CIE (IT-Wallet in rollout) |
| Internet exchange / cable landings | MIX Milan; NAMEX Rome; landings Genoa, Sicily, Bari |

Relative to the Dutch baseline: population x3.27, public administration x1.62,
GDP x1.93. Resulting design load: x2.55 the Dutch figure.

## 3. What is structurally different from the Dutch case

- **High seismic risk.** Base isolation or seismic-rated structures are mandatory, not optional, at the primary site; the second and third regions should be chosen in a different seismic domain so a single event cannot take out two regions. Expect facility CAPEX above the EUR 10 m/MW planning figure.
- **Expensive power (220 EUR/MWh vs. EU average ~184).** Power is the dominant OPEX line; free cooling, heat reuse, and siting near renewables or nuclear baseload move the economics more than server choice does. The model's power OPEX line is the number to attack first.
- **Dense hyperscaler presence (4 live regions).** Commercial capacity, fibre and skills exist in-country; the sovereign core can stay lean and the hybrid model works as designed. The risk is the opposite one: political pressure to declare a hyperscaler region 'sovereign enough' (Dutch GOAL.md section 17: location is not sovereignty).

## 4. Workload demand (scaled from the Dutch baseline)

Scaling weights per workload class are in `model/scaling_rules.csv`; the Dutch rows they scale are in
`countries/NL/workloads_inputs.csv`. Frontline multiplier applied: no.

| Workload | Class | CPU cores | GPU eq. | Storage (PB) | Avail. factor |
|---|---|---:|---:|---:|---:|
| Digital identity / SPID | Critical government | 58,800 | 0 | 13.1 | 1.5 |
| Core government applications | Government | 134,300 | 0 | 44.0 | 1.35 |
| Data platforms & analytics | Government data | 90,900 | 208 | 155.9 | 1.25 |
| AI / sovereign model serving | AI | 34,700 | 984 | 23.1 | 1.3 |
| Defense classified compute | Defense | 98,000 | 840 | 49.0 | 1.5 |
| Cybersecurity / SOC / telemetry | Security | 61,000 | 88 | 69.3 | 1.4 |
| Scientific / public research | Research | 50,200 | 248 | 38.6 | 1.15 |

## 5. Capacity model output

| Metric | Value |
|---|---:|
| Physical servers | 14,774 (CPU 10,208 / GPU 671 / storage 3,895) |
| Rack equivalents | ~462 |
| IT critical load | 24.1 MW |
| Facility load (PUE 1.25) | 30.1 MW |
| Facility design load (+20% headroom) | **36.1 MW** |
| Sites by capacity / recommended | 4 / **4** (minimum 4) |
| Average design MW per site | 9.0 MW |
| Total CAPEX | **EUR 857 m** (facility EUR 361 m, IT EUR 420 m, network EUR 76 m) |
| Annual energy | 263,831 MWh |
| Annual OPEX | **EUR 97 m / yr** (power EUR 58 m, non-power EUR 39 m) |

Full table: `facility_summary.csv`.

## 6. Proposed geography (first-pass hypothesis)

Site posture: standard. Separation target: 50-100 km failure domains, dual fibre paths, distinct grid feeds.

| Region | Role | Share | Design MW | Racks | Facility CAPEX | Notes |
|---|---|---:|---:|---:|---:|---|
| Milan / Lombardy | Primary civil cloud | 36% | 13.0 | 166 | EUR 130 m | PSN pair, MIX, all four hyperscaler regions nearby; Po flood zoning. |
| Rome / Lazio | Sovereign secondary | 18% | 6.5 | 83 | EUR 65 m | Ministries, Sogei, NAMEX; Apennine seismic zoning. |
| Turin / Piedmont | Government / continuity | 18% | 6.5 | 83 | EUR 65 m | Alpine hydro, TOP-IX; lower seismicity. |
| Puglia / Bari | Defense / industrial | 18% | 6.5 | 83 | EUR 65 m | Southern separation, Adriatic cable landings; renewables belt. |
| Emilia / Bologna | Strategic reserve | 10% | 3.6 | 46 | EUR 36 m | EuroHPC Leonardo campus (Tecnopolo); reserve - 2023 flood plains excluded. |

These regions encode only the obvious constraints (capital estate, second metro, distance from the frontier,
fault or flood zone). They are to be replaced by the scored site selection in workstream A of the Dutch
`TODO.md` (grid capacity, flood risk, fibre, failure independence, physical security, land, cooling).

## 7. Geography and threat notes

High seismic/volcanic (Apennines, Naples, Etna); Po/Emilia floods (2023); gas-import dependent with structurally high power price; north-south grid bottlenecks (Lombardy hosts most capacity); low geopolitical frontline risk

## 8. Recommendations specific to Italy

1. **Anchor on SPID.** Digital identity is the workload that, if it fails, stops every other
   government service; it belongs in the sovereign core first, active-active across at least two regions.
2. **Build on the existing estate, do not replace it.** Polo Strategico Nazionale (PSN) - operational since 2023, TIM/Leonardo/CDP/Sogei consortium, 4 DC pairs is the
   institutional starting point; the sovereign core should be its next generation, with one governance owner.
3. **Site posture: standard.** Standard Tier III+ with 50-100 km separation is sufficient; spend the hardening budget on supply-chain assurance instead.
4. **Power strategy.** Power is the binding constraint; treat grid connection lead time and on-site generation as first-order site criteria.
5. **Hybrid tier.** Use in-country commercial regions for the non-critical tier, but keep identity, defense, security telemetry and registries in the sovereign core.

## 9. Open questions

- Replace scaled workload rows with real ministry/agency demand (see `countries/NL/CAPACITY_PLAN.md` for the method).
- Which body owns the sovereign core, and how are agencies compelled or incentivised to migrate?
- Which regions federate with EU partners for mutual disaster recovery, and which stay national-only?
- Site-size assumption: is the 12 MW planning unit right for Italy, or should sites be larger?

## 10. Legal and regulatory posture

Every member state shares one baseline: GDPR for personal data, NIS2 for the security of essential
entities, the Data Act for switching and access, and the EU Cloud Services Scheme (EUCS) still unresolved
on the sovereignty requirements that would matter most here. That baseline governs *processing*. It does
not, on its own, place infrastructure under national control - which is the gap a sovereign core exists
to close.

| | |
|---|---|
| Governing instrument | Polo Strategico Nazionale (PSN) with mandatory migration deadlines for central administrations |
| Cloud certification | ACN cloud qualification (formerly AgID) with ordinary/critical/strategic data tiers |
| Data classification | Legge 124/2007: Riservato / Riservatissimo / Segreto / Segretissimo |
| Procurement route | Consip central purchasing; PSN concession held by TIM, CDP, Leonardo and Sogei |

A binding national standard exists (ACN cloud qualification (formerly AgID) with ordinary/critical/strategic data tiers), so the sovereign core can be certified against something already recognised rather than inventing its own controls.

The classification ladder is the practical control: it decides which tier of data may leave the
jurisdiction at all, and it should be mapped onto the four migration phases in section 12 before any
procurement starts. Buying capacity before deciding what may sit on it is how sovereign programmes end up
with expensive infrastructure hosting the wrong workloads.

**Foreign jurisdiction exposure.** PSN runs Azure, Google and Oracle technology under Italian operator control; strategic data must stay on the national stack

Dependency on US hyperscalers is **moderate**: national arrangements carry part of the estate, and the sovereign core extends an existing position rather than reversing one. Under the US CLOUD Act and FISA 702, a provider subject to US jurisdiction can face a lawful
order for data it holds, regardless of where the data physically sits. Data residency in-country is
therefore necessary but not sufficient; what matters is who holds the keys and who can be compelled.

## 11. Current state and provider landscape

| | |
|---|---|
| Government cloud | Polo Strategico Nazionale (PSN) - operational since 2023, TIM/Leonardo/CDP/Sogei consortium, 4 DC pairs; ACN cloud qualification regime (Strategia Cloud Italia) |
| Maturity | federated |
| Digital identity | SPID / CIE (IT-Wallet in rollout) |
| In-country commercial regions | 4 |
| Interconnection | MIX Milan; NAMEX Rome; landings Genoa, Sicily, Bari |

A federated government cloud is already in production. The open question is consolidation and governance, not construction.

Against that starting point, the modelled sovereign core is **36.1 MW of design load across
4 site(s)**, or roughly 14,774 servers. The gap between what runs today and that
figure is the actual programme; the capacity model in sections 4-6 sizes the destination, not the journey.

## 12. Migration path and cost

Workloads are sequenced by how badly loss of control would hurt, not by how easy they are to move. The
phases below are derived from the workload classes in `model/migration_phases.csv`; per-country figures
are in `migration_phases.csv` in this directory.

| Phase | Scope | Servers | Design MW | CAPEX | Cumulative | Hybrid-eligible |
|---|---|---:|---:|---:|---:|---|
| 1 | Sovereign core | 4,423 | 8.7 | EUR 166 m | 19% | no |
| 2 | Security and defense | 4,872 | 12.7 | EUR 308 m | 55% | no |
| 3 | State record | 3,131 | 6.5 | EUR 163 m | 74% | no |
| 4 | Elective | 2,348 | 8.3 | EUR 219 m | 100% | yes |

**Phase 1 is the number that matters: EUR 166 m for 8.7 MW,
19% of total CAPEX.** That is the floor - identity and core government
services - below which no hybrid arrangement helps, because these workloads cannot be foreign-hosted under
any sovereignty posture worth the name. It is also, notably, a small fraction of the full build: sovereignty
for the workloads that define the state is cheaper than the headline figure suggests.

Phases 2 and 3 follow on clearance and legal constraints rather than cost. Phase 4 can use in-country commercial capacity (4 live region(s)) under sovereign-held keys, which is what keeps the sovereign core small.

Sequencing caveat: the CAPEX split above apportions facility cost by each phase's share of IT load, which
assumes phases are built into a shared facility programme rather than as separate buildings. Building
phase 1 alone, on its own site, costs disproportionately more - the facility is largely a fixed cost.
