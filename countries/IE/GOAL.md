# Ireland - Sovereign Government Data Center Network

> Generated 2026-09-01 by `model/generate_countries.py` from the Dutch reference case
> (`countries/NL/GOAL.md`) and `model/eu27_parameters.csv`. Every number below is a **scaled working
> assumption**, not a sourced figure. Edit the CSVs in this directory and re-run
> `python3 model/capacity_model.py IE` to update the capacity numbers; edit
> `model/eu27_parameters.csv` or `model/scaling_rules.csv` and re-run the generator to update this file.

## 1. Working thesis

Ireland does not need to become technologically autarkic. It needs enough independently controlled compute,
storage, networking, identity, cryptography and operational capability that the state can continue functioning
when foreign commercial infrastructure is unavailable, politically constrained, compromised, or no longer
trustworthy. The Dutch design rules (sovereignty is a stack, not a building; 3-5 separated regions; dual fibre
paths; no single hardware supplier; a first-class developer platform) are taken as the starting point and
adjusted below for what is structurally different about Ireland.

## 2. Starting point

| | |
|---|---|
| Population | 5.42 m (Eurostat, 1 Jan 2025) |
| GDP | EUR 602 bn (2025, current prices) |
| Public administration employment (NACE O) | 144 k (Eurostat LFS 2025) |
| Non-household electricity price | 255.2 EUR/MWh (Eurostat, band IC, 2025-S2) |
| Renewables in electricity | 41.3% (2024) |
| Land area | 68,655 km2 |
| Live hyperscaler regions in-country | 2 |
| Existing government / sovereign cloud | No sovereign cloud; OGCIO Build to Share + Government Cloud Network + Backweston government DCs; cloud-first Advice Note; Digital Decade 2025 report flags DC grid limits |
| National digital identity (anchor workload) | MyGovID (Public Services Card) |
| Internet exchange / cable landings | INEX Dublin/Cork; Atlantic landings Killala Kinsale Cork |

Relative to the Dutch baseline: population x0.30, public administration x0.20,
GDP x0.51. Resulting design load: x0.38 the Dutch figure.

## 3. What is structurally different from the Dutch case

- **Grid isolation.** The national grid is an electrical island or nearly so (weak or single interconnection). The April 2025 Iberian blackout and Cyprus/Malta interconnector outages show the failure mode. Every site needs on-site generation and storage sized for multi-day ride-through, and the PUE and facility CAPEX assumptions should be revisited upward once site studies exist.
- **Expensive power (255 EUR/MWh vs. EU average ~184).** Power is the dominant OPEX line; free cooling, heat reuse, and siting near renewables or nuclear baseload move the economics more than server choice does. The model's power OPEX line is the number to attack first.

## 4. Workload demand (scaled from the Dutch baseline)

Scaling weights per workload class are in `model/scaling_rules.csv`; the Dutch rows they scale are in
`countries/NL/workloads_inputs.csv`. Frontline multiplier applied: no.

| Workload | Class | CPU cores | GPU eq. | Storage (PB) | Avail. factor |
|---|---|---:|---:|---:|---:|
| Digital identity / MyGovID | Critical government | 5,400 | 0 | 1.2 | 1.5 |
| Core government applications | Government | 13,800 | 0 | 4.5 | 1.35 |
| Data platforms & analytics | Government data | 14,300 | 32 | 24.5 | 1.25 |
| AI / sovereign model serving | AI | 9,300 | 264 | 6.2 | 1.3 |
| Defense classified compute | Defense | 9,000 | 80 | 4.5 | 1.5 |
| Cybersecurity / SOC / telemetry | Security | 5,900 | 8 | 6.8 | 1.4 |
| Scientific / public research | Research | 13,400 | 64 | 10.3 | 1.15 |

## 5. Capacity model output

| Metric | Value |
|---|---:|
| Physical servers | 2,024 (CPU 1,336 / GPU 125 / storage 563) |
| Rack equivalents | ~63 |
| IT critical load | 3.5 MW |
| Facility load (PUE 1.25) | 4.4 MW |
| Facility design load (+20% headroom) | **5.3 MW** |
| Sites by capacity / recommended | 1 / **3** (minimum 3) |
| Average design MW per site | 1.8 MW |
| Total CAPEX | **EUR 131 m** (facility EUR 53 m, IT EUR 66 m, network EUR 12 m) |
| Annual energy | 38,830 MWh |
| Annual OPEX | **EUR 16 m / yr** (power EUR 10 m, non-power EUR 6 m) |

Full table: `facility_summary.csv`.

## 6. Proposed geography (first-pass hypothesis)

Site posture: standard. Separation target: 50-100 km failure domains, dual fibre paths, distinct grid feeds.

| Region | Role | Share | Design MW | Racks | Facility CAPEX | Notes |
|---|---|---:|---:|---:|---:|---|
| Dublin | Primary civil cloud | 40% | 2.1 | 26 | EUR 22 m | OGCIO/Backweston estate, INEX; EirGrid connection moratorium to ~2028 is binding. |
| Cork | Sovereign secondary | 27% | 1.4 | 17 | EUR 14 m | Atlantic cable landings (Kinsale, Amitie), Celtic Interconnector. |
| Galway - Limerick / West | Government / continuity | 22% | 1.2 | 14 | EUR 12 m | Wind surplus, AEC-1 landing (Killala). |
| Midlands / Athlone | Strategic reserve | 10% | 0.5 | 6 | EUR 5 m | Post-peat land and grid; reserve/expansion. |

These regions encode only the obvious constraints (capital estate, second metro, distance from the frontier,
fault or flood zone). They are to be replaced by the scored site selection in workstream A of the Dutch
`TODO.md` (grid capacity, flood risk, fibre, failure independence, physical security, land, cooling).

## 7. Geography and threat notes

Negligible seismic; Atlantic storm/coastal and river floods; GRID IS BINDING: EirGrid Dublin DC connection moratorium to ~2028, DCs ~21% of national electricity; most expensive EU power; single UK gas pipeline until Celtic Interconnector (~2027); neutral non-NATO; subsea cable vulnerability

## 8. Recommendations specific to Ireland

1. **Anchor on MyGovID.** Digital identity is the workload that, if it fails, stops every other
   government service; it belongs in the sovereign core first, active-active across at least two regions.
2. **Build on the existing estate, do not replace it.** No sovereign cloud is the
   institutional starting point; the sovereign core should be its next generation, with one governance owner.
3. **Site posture: standard.** Standard Tier III+ with 50-100 km separation is sufficient; spend the hardening budget on supply-chain assurance instead.
4. **Power strategy.** Power is the binding constraint; treat grid connection lead time and on-site generation as first-order site criteria.
5. **Hybrid tier.** Use in-country commercial regions for the non-critical tier, but keep identity, defense, security telemetry and registries in the sovereign core.

## 9. Open questions

- Replace scaled workload rows with real ministry/agency demand (see `countries/NL/CAPACITY_PLAN.md` for the method).
- Which body owns the sovereign core, and how are agencies compelled or incentivised to migrate?
- Which regions federate with EU partners for mutual disaster recovery, and which stay national-only?
- Site-size assumption: is the 12 MW planning unit right for Ireland, or should sites be smaller?

## 10. Legal and regulatory posture

Every member state shares one baseline: GDPR for personal data, NIS2 for the security of essential
entities, the Data Act for switching and access, and the EU Cloud Services Scheme (EUCS) still unresolved
on the sovereignty requirements that would matter most here. That baseline governs *processing*. It does
not, on its own, place infrastructure under national control - which is the gap a sovereign core exists
to close.

| | |
|---|---|
| Governing instrument | Public Service ICT Strategy and OGCIO cloud-first policy; no sovereignty carve-out |
| Cloud certification | No national scheme; ISO 27001 |
| Data classification | Official Secrets Act; departmental classification rather than a single statutory ladder |
| Procurement route | Office of Government Procurement (OGP) |

There is no national cloud certification scheme; assurance rests on ISO 27001 and contract terms. The choice is to adopt EUCS when it lands or to recognise a peer scheme (BSI C5, SecNumCloud, ENS) by equivalence - writing a national scheme from scratch for a state this size is not worth the effort.

The classification ladder is the practical control: it decides which tier of data may leave the
jurisdiction at all, and it should be mapped onto the four migration phases in section 12 before any
procurement starts. Buying capacity before deciding what may sit on it is how sovereign programmes end up
with expensive infrastructure hosting the wrong workloads.

**Foreign jurisdiction exposure.** Highest exposure in the EU-27: AWS eu-west-1 and Azure North Europe are both anchored in Dublin and government is a direct consumer under a cloud-first policy with no sovereignty carve-out

Dependency on US hyperscalers is **critical**: they hold production government workloads and there is no national alternative in service. Migration is therefore a contractual and political problem before it is a technical one, and the exit terms of existing agreements are the first thing to read. Under the US CLOUD Act and FISA 702, a provider subject to US jurisdiction can face a lawful
order for data it holds, regardless of where the data physically sits. Data residency in-country is
therefore necessary but not sufficient; what matters is who holds the keys and who can be compelled.

## 11. Current state and provider landscape

| | |
|---|---|
| Government cloud | No sovereign cloud; OGCIO Build to Share + Government Cloud Network + Backweston government DCs; cloud-first Advice Note; Digital Decade 2025 report flags DC grid limits |
| Maturity | pilot |
| Digital identity | MyGovID (Public Services Card) |
| In-country commercial regions | 2 |
| Interconnection | INEX Dublin/Cork; Atlantic landings Killala Kinsale Cork |

What exists is a pilot rather than an operating platform; the sovereign core would be its first production incarnation.

Against that starting point, the modelled sovereign core is **5.3 MW of design load across
3 site(s)**, or roughly 2,024 servers. The gap between what runs today and that
figure is the actual programme; the capacity model in sections 4-6 sizes the destination, not the journey.

## 12. Migration path and cost

Workloads are sequenced by how badly loss of control would hurt, not by how easy they are to move. The
phases below are derived from the workload classes in `model/migration_phases.csv`; per-country figures
are in `migration_phases.csv` in this directory.

| Phase | Scope | Servers | Design MW | CAPEX | Cumulative | Hybrid-eligible |
|---|---|---:|---:|---:|---:|---|
| 1 | Sovereign core | 441 | 0.9 | EUR 17 m | 13% | no |
| 2 | Security and defense | 461 | 1.2 | EUR 30 m | 35% | no |
| 3 | State record | 493 | 1.0 | EUR 26 m | 55% | no |
| 4 | Elective | 629 | 2.2 | EUR 59 m | 100% | yes |

**Phase 1 is the number that matters: EUR 17 m for 0.9 MW,
13% of total CAPEX.** That is the floor - identity and core government
services - below which no hybrid arrangement helps, because these workloads cannot be foreign-hosted under
any sovereignty posture worth the name. It is also, notably, a small fraction of the full build: sovereignty
for the workloads that define the state is cheaper than the headline figure suggests.

Phases 2 and 3 follow on clearance and legal constraints rather than cost. Phase 4 can use in-country commercial capacity (2 live region(s)) under sovereign-held keys, which is what keeps the sovereign core small.

Sequencing caveat: the CAPEX split above apportions facility cost by each phase's share of IT load, which
assumes phases are built into a shared facility programme rather than as separate buildings. Building
phase 1 alone, on its own site, costs disproportionately more - the facility is largely a fixed cost.
