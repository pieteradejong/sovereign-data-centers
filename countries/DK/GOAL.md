# Denmark - Sovereign Government Data Center Network

> Generated 2026-09-01 by `model/generate_countries.py` from the Dutch reference case
> (`countries/NL/GOAL.md`) and `model/eu27_parameters.csv`. Every number below is a **scaled working
> assumption**, not a sourced figure. Edit the CSVs in this directory and re-run
> `python3 model/capacity_model.py DK` to update the capacity numbers; edit
> `model/eu27_parameters.csv` or `model/scaling_rules.csv` and re-run the generator to update this file.

## 1. Working thesis

Denmark does not need to become technologically autarkic. It needs enough independently controlled compute,
storage, networking, identity, cryptography and operational capability that the state can continue functioning
when foreign commercial infrastructure is unavailable, politically constrained, compromised, or no longer
trustworthy. The Dutch design rules (sovereignty is a stack, not a building; 3-5 separated regions; dual fibre
paths; no single hardware supplier; a first-class developer platform) are taken as the starting point and
adjusted below for what is structurally different about Denmark.

## 2. Starting point

| | |
|---|---|
| Population | 5.99 m (Eurostat, 1 Jan 2025) |
| GDP | EUR 418 bn (2025, current prices) |
| Public administration employment (NACE O) | 166 k (Eurostat LFS 2025) |
| Non-household electricity price | 121.6 EUR/MWh (Eurostat, band IC, 2025-S2) |
| Renewables in electricity | 79.7% (2024) |
| Land area | 41,987 km2 |
| Live hyperscaler regions in-country | 1 |
| Existing government / sovereign cloud | No sovereign cloud product; Statens It central hosting; Joint Government Digital Strategy 2026-29 + DKK 80m digital-sovereignty action plan; Ministry of Digitalisation Microsoft phase-out (2025) |
| National digital identity (anchor workload) | MitID |
| Internet exchange / cable landings | DIX Lyngby and Netnod Copenhagen; Blaabjerg/Esbjerg Atlantic landings (Havfrue/AEC-2) |

Relative to the Dutch baseline: population x0.33, public administration x0.23,
GDP x0.36. Resulting design load: x0.33 the Dutch figure.

## 3. What is structurally different from the Dutch case

- No structural flags differ from the Dutch reference case; the Dutch design rules transfer directly.

## 4. Workload demand (scaled from the Dutch baseline)

Scaling weights per workload class are in `model/scaling_rules.csv`; the Dutch rows they scale are in
`countries/NL/workloads_inputs.csv`. Frontline multiplier applied: no.

| Workload | Class | CPU cores | GPU eq. | Storage (PB) | Avail. factor |
|---|---|---:|---:|---:|---:|
| Digital identity / MitID | Critical government | 6,000 | 0 | 1.3 | 1.5 |
| Core government applications | Government | 15,500 | 0 | 5.1 | 1.35 |
| Data platforms & analytics | Government data | 12,100 | 24 | 20.7 | 1.25 |
| AI / sovereign model serving | AI | 6,400 | 184 | 4.3 | 1.3 |
| Defense classified compute | Defense | 10,000 | 88 | 5.0 | 1.5 |
| Cybersecurity / SOC / telemetry | Security | 6,600 | 8 | 7.6 | 1.4 |
| Scientific / public research | Research | 9,300 | 48 | 7.1 | 1.15 |

## 5. Capacity model output

| Metric | Value |
|---|---:|
| Physical servers | 1,861 (CPU 1,258 / GPU 100 / storage 503) |
| Rack equivalents | ~58 |
| IT critical load | 3.2 MW |
| Facility load (PUE 1.25) | 3.9 MW |
| Facility design load (+20% headroom) | **4.7 MW** |
| Sites by capacity / recommended | 1 / **3** (minimum 3) |
| Average design MW per site | 1.6 MW |
| Total CAPEX | **EUR 114 m** (facility EUR 47 m, IT EUR 57 m, network EUR 10 m) |
| Annual energy | 34,494 MWh |
| Annual OPEX | **EUR 9 m / yr** (power EUR 4 m, non-power EUR 5 m) |

Full table: `facility_summary.csv`.

## 6. Proposed geography (first-pass hypothesis)

Site posture: standard. Separation target: 50-100 km failure domains, dual fibre paths, distinct grid feeds.

| Region | Role | Share | Design MW | Racks | Facility CAPEX | Notes |
|---|---|---:|---:|---:|---:|---|
| Copenhagen / Zealand | Primary civil cloud | 40% | 1.9 | 24 | EUR 19 m | Statens It estate, DIX/Netnod; Zealand grid queue and storm-surge zoning. |
| Jutland / Fredericia - Aarhus | Sovereign secondary | 27% | 1.3 | 16 | EUR 13 m | Wind surplus, existing hyperscale campuses, Atlantic cable landings. |
| Funen / Odense | Government / continuity | 22% | 1.1 | 13 | EUR 11 m | Central, separated from both metros. |
| North Jutland | Strategic reserve | 10% | 0.5 | 6 | EUR 5 m | Cheapest power, reserve/expansion. |

These regions encode only the obvious constraints (capital estate, second metro, distance from the frontier,
fault or flood zone). They are to be replaced by the scored site selection in workstream A of the Dutch
`TODO.md` (grid capacity, flood risk, fibre, failure independence, physical security, land, cooling).

## 7. Geography and threat notes

Negligible seismic; low-lying storm-surge risk; land available in Jutland; wind surplus and strong interconnectors (Viking Link) but Zealand connection queues; energy net exporter; Baltic Sea cable/pipeline sabotage exposure; NATO

## 8. Recommendations specific to Denmark

1. **Anchor on MitID.** Digital identity is the workload that, if it fails, stops every other
   government service; it belongs in the sovereign core first, active-active across at least two regions.
2. **Build on the existing estate, do not replace it.** No sovereign cloud product is the
   institutional starting point; the sovereign core should be its next generation, with one governance owner.
3. **Site posture: standard.** Standard Tier III+ with 50-100 km separation is sufficient; spend the hardening budget on supply-chain assurance instead.
4. **Power strategy.** Power is not the binding constraint; optimise for fibre diversity and failure-domain separation.
5. **Hybrid tier.** Use in-country commercial regions for the non-critical tier, but keep identity, defense, security telemetry and registries in the sovereign core.

## 9. Open questions

- Replace scaled workload rows with real ministry/agency demand (see `countries/NL/CAPACITY_PLAN.md` for the method).
- Which body owns the sovereign core, and how are agencies compelled or incentivised to migrate?
- Which regions federate with EU partners for mutual disaster recovery, and which stay national-only?
- Site-size assumption: is the 12 MW planning unit right for Denmark, or should sites be smaller?

## 10. Legal and regulatory posture

Every member state shares one baseline: GDPR for personal data, NIS2 for the security of essential
entities, the Data Act for switching and access, and the EU Cloud Services Scheme (EUCS) still unresolved
on the sovereignty requirements that would matter most here. That baseline governs *processing*. It does
not, on its own, place infrastructure under national control - which is the gap a sovereign core exists
to close.

| | |
|---|---|
| Governing instrument | Danish Agency for Digital Government cloud strategy; ISO 27001 mandatory across state bodies |
| Cloud certification | No national cloud scheme; ISO 27001 is the binding baseline |
| Data classification | Sikkerhedscirkulaeret: Til tjenestebrug / Fortroligt / Hemmeligt / Yderst hemmeligt |
| Procurement route | SKI and Statens Indkoeb central framework agreements |

There is no national cloud certification scheme; assurance rests on ISO 27001 and contract terms. The choice is to adopt EUCS when it lands or to recognise a peer scheme (BSI C5, SecNumCloud, ENS) by equivalence - writing a national scheme from scratch for a state this size is not worth the effort.

The classification ladder is the practical control: it decides which tier of data may leave the
jurisdiction at all, and it should be mapped onto the four migration phases in section 12 before any
procurement starts. Buying capacity before deciding what may sit on it is how sovereign programmes end up
with expensive infrastructure hosting the wrong workloads.

**Foreign jurisdiction exposure.** Heavy Microsoft dependency (Azure and M365) across state and municipalities; Datatilsynet has challenged municipal use

Dependency on US hyperscalers is **critical**: they hold production government workloads and there is no national alternative in service. Migration is therefore a contractual and political problem before it is a technical one, and the exit terms of existing agreements are the first thing to read. Under the US CLOUD Act and FISA 702, a provider subject to US jurisdiction can face a lawful
order for data it holds, regardless of where the data physically sits. Data residency in-country is
therefore necessary but not sufficient; what matters is who holds the keys and who can be compelled.

## 11. Current state and provider landscape

| | |
|---|---|
| Government cloud | No sovereign cloud product; Statens It central hosting; Joint Government Digital Strategy 2026-29 + DKK 80m digital-sovereignty action plan; Ministry of Digitalisation Microsoft phase-out (2025) |
| Maturity | pilot |
| Digital identity | MitID |
| In-country commercial regions | 1 |
| Interconnection | DIX Lyngby and Netnod Copenhagen; Blaabjerg/Esbjerg Atlantic landings (Havfrue/AEC-2) |

What exists is a pilot rather than an operating platform; the sovereign core would be its first production incarnation.

Against that starting point, the modelled sovereign core is **4.7 MW of design load across
3 site(s)**, or roughly 1,861 servers. The gap between what runs today and that
figure is the actual programme; the capacity model in sections 4-6 sizes the destination, not the journey.

## 12. Migration path and cost

Workloads are sequenced by how badly loss of control would hurt, not by how easy they are to move. The
phases below are derived from the workload classes in `model/migration_phases.csv`; per-country figures
are in `migration_phases.csv` in this directory.

| Phase | Scope | Servers | Design MW | CAPEX | Cumulative | Hybrid-eligible |
|---|---|---:|---:|---:|---:|---|
| 1 | Sovereign core | 493 | 1.0 | EUR 18 m | 16% | no |
| 2 | Security and defense | 514 | 1.3 | EUR 33 m | 45% | no |
| 3 | State record | 417 | 0.9 | EUR 22 m | 64% | no |
| 4 | Elective | 437 | 1.6 | EUR 41 m | 100% | yes |

**Phase 1 is the number that matters: EUR 18 m for 1.0 MW,
16% of total CAPEX.** That is the floor - identity and core government
services - below which no hybrid arrangement helps, because these workloads cannot be foreign-hosted under
any sovereignty posture worth the name. It is also, notably, a small fraction of the full build: sovereignty
for the workloads that define the state is cheaper than the headline figure suggests.

Phases 2 and 3 follow on clearance and legal constraints rather than cost. Phase 4 can use in-country commercial capacity (1 live region(s)) under sovereign-held keys, which is what keeps the sovereign core small.

Sequencing caveat: the CAPEX split above apportions facility cost by each phase's share of IT load, which
assumes phases are built into a shared facility programme rather than as separate buildings. Building
phase 1 alone, on its own site, costs disproportionately more - the facility is largely a fixed cost.
