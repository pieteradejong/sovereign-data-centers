# Romania - Sovereign Government Data Center Network

> Generated 2026-09-01 by `model/generate_countries.py` from the Dutch reference case
> (`countries/NL/GOAL.md`) and `model/eu27_parameters.csv`. Every number below is a **scaled working
> assumption**, not a sourced figure. Edit the CSVs in this directory and re-run
> `python3 model/capacity_model.py RO` to update the capacity numbers; edit
> `model/eu27_parameters.csv` or `model/scaling_rules.csv` and re-run the generator to update this file.

## 1. Working thesis

Romania does not need to become technologically autarkic. It needs enough independently controlled compute,
storage, networking, identity, cryptography and operational capability that the state can continue functioning
when foreign commercial infrastructure is unavailable, politically constrained, compromised, or no longer
trustworthy. The Dutch design rules (sovereignty is a stack, not a building; 3-5 separated regions; dual fibre
paths; no single hardware supplier; a first-class developer platform) are taken as the starting point and
adjusted below for what is structurally different about Romania.

## 2. Starting point

| | |
|---|---|
| Population | 19.04 m (Eurostat, 1 Jan 2025) |
| GDP | EUR 380 bn (2025, current prices) |
| Public administration employment (NACE O) | 396 k (Eurostat LFS 2025) |
| Non-household electricity price | 188.7 EUR/MWh (Eurostat, band IC, 2025-S2) |
| Renewables in electricity | 47.6% (2024) |
| Land area | 234,270 km2 |
| Live hyperscaler regions in-country | 0 |
| Existing government / sovereign cloud | Cloud Privat Guvernamental - STS-operated, PNRR-funded (~EUR 560m package with SRI/ADR), 4 regional DCs (Bucharest, Timis, Brasov, Sibiu), national operational phase Mar 2026 |
| National digital identity (anchor workload) | ROeID / electronic ID card (CEI) |
| Internet exchange / cable landings | InterLAN and RoNIX Bucharest; Black Sea KAFOS at Constanta |

Relative to the Dutch baseline: population x1.06, public administration x0.55,
GDP x0.32. Resulting design load: x0.84 the Dutch figure.

## 3. What is structurally different from the Dutch case

- **Frontline exposure.** A land border with Russia or Belarus (or a Black Sea coast facing the war) changes the threat model from *geopolitical supply disruption* to *kinetic and sabotage risk against the facilities themselves*. Defense and security workloads are scaled up 1.5x/1.25x in the baseline, and at least one site should be hardened (EMP/blast, autonomous power for weeks, not hours). A purely national footprint cannot provide the out-of-country cold copy that Estonia's Data Embassy already demonstrates; this is the first item to revisit when the EU federation layer (Dutch GOAL.md section 16) is modelled.
- **High seismic risk.** Base isolation or seismic-rated structures are mandatory, not optional, at the primary site; the second and third regions should be chosen in a different seismic domain so a single event cannot take out two regions. Expect facility CAPEX above the EUR 10 m/MW planning figure.
- **No hyperscaler region in-country.** Unlike the Netherlands, there is no commercial hyperscale tier to fall back on for non-critical workloads without leaving the jurisdiction. The sovereign core therefore has to be sized for a larger share of total government demand, and the hybrid model (Dutch GOAL.md section 7) needs a cross-border commercial tier.

## 4. Workload demand (scaled from the Dutch baseline)

Scaling weights per workload class are in `model/scaling_rules.csv`; the Dutch rows they scale are in
`countries/NL/workloads_inputs.csv`. Frontline multiplier applied: yes.

| Workload | Class | CPU cores | GPU eq. | Storage (PB) | Avail. factor |
|---|---|---:|---:|---:|---:|
| Digital identity / ROeID | Critical government | 19,000 | 0 | 4.2 | 1.5 |
| Core government applications | Government | 44,200 | 0 | 14.5 | 1.35 |
| Data platforms & analytics | Government data | 24,200 | 56 | 41.4 | 1.25 |
| AI / sovereign model serving | AI | 5,800 | 168 | 3.9 | 1.3 |
| Defense classified compute | Defense | 47,500 | 408 | 23.7 | 1.5 |
| Cybersecurity / SOC / telemetry | Security | 24,900 | 40 | 28.3 | 1.4 |
| Scientific / public research | Research | 8,400 | 40 | 6.5 | 1.15 |

## 5. Capacity model output

| Metric | Value |
|---|---:|
| Physical servers | 4,894 (CPU 3,438 / GPU 211 / storage 1,245) |
| Rack equivalents | ~153 |
| IT critical load | 7.9 MW |
| Facility load (PUE 1.25) | 9.9 MW |
| Facility design load (+20% headroom) | **11.9 MW** |
| Sites by capacity / recommended | 1 / **4** (minimum 4) |
| Average design MW per site | 3.0 MW |
| Total CAPEX | **EUR 278 m** (facility EUR 119 m, IT EUR 135 m, network EUR 24 m) |
| Annual energy | 86,567 MWh |
| Annual OPEX | **EUR 29 m / yr** (power EUR 16 m, non-power EUR 13 m) |

Full table: `facility_summary.csv`.

## 6. Proposed geography (first-pass hypothesis)

Site posture: hardened (frontline). Separation target: 50-100 km failure domains, dual fibre paths, distinct grid feeds.

| Region | Role | Share | Design MW | Racks | Facility CAPEX | Notes |
|---|---|---:|---:|---:|---:|---|
| Bucharest | Primary civil cloud | 36% | 4.3 | 55 | EUR 43 m | STS government cloud, InterLAN/RoNIX; highest-seismic-risk EU capital - base isolation required. |
| Cluj / Transylvania | Sovereign secondary | 18% | 2.1 | 28 | EUR 21 m | IT cluster, outside the Vrancea zone, 400 km separation. |
| Timisoara / Banat | Government / continuity | 18% | 2.1 | 28 | EUR 21 m | Western separation, Hungarian transit, low seismicity. |
| Brasov - Sibiu | Defense / industrial | 18% | 2.1 | 28 | EUR 21 m | Existing STS regional DCs; mountain sites - verify Vrancea distance. |
| Craiova / Oltenia | Strategic reserve | 10% | 1.2 | 15 | EUR 12 m | ClusterPower campus; away from the Ukraine/Moldova frontier. |

These regions encode only the obvious constraints (capital estate, second metro, distance from the frontier,
fault or flood zone). They are to be replaced by the scored site selection in workstream A of the Dutch
`TODO.md` (grid capacity, flood risk, fibre, failure independence, physical security, land, cooling).

## 7. Geography and threat notes

Vrancea intermediate-depth seismic zone - Bucharest highest-risk EU capital (1977 M7.2); Danube/flash floods; borders Ukraine and Moldova with drone-debris incidents 2023-25; energy largely self-sufficient (gas, nuclear, hydro) but grid reinforcement lagging

## 8. Recommendations specific to Romania

1. **Anchor on ROeID.** Digital identity is the workload that, if it fails, stops every other
   government service; it belongs in the sovereign core first, active-active across at least two regions.
2. **Build on the existing estate, do not replace it.** Cloud Privat Guvernamental - STS-operated, PNRR-funded (~EUR 560m package with SRI/ADR), 4 regional DCs (Bucharest, Timis, Brasov, Sibiu), national operational phase Mar 2026 is the
   institutional starting point; the sovereign core should be its next generation, with one governance owner.
3. **Site posture: hardened (frontline).** Harden at least one region and plan an out-of-country cold copy.
4. **Power strategy.** Power is not the binding constraint; optimise for fibre diversity and failure-domain separation.
5. **Hybrid tier.** With no in-country hyperscaler region, define now which non-critical workloads may leave the jurisdiction and under what contract terms.

## 9. Open questions

- Replace scaled workload rows with real ministry/agency demand (see `countries/NL/CAPACITY_PLAN.md` for the method).
- Which body owns the sovereign core, and how are agencies compelled or incentivised to migrate?
- Out-of-country reserve: which partner state, under what treaty?
- Site-size assumption: is the 12 MW planning unit right for Romania, or should sites be smaller?

## 10. Legal and regulatory posture

Every member state shares one baseline: GDPR for personal data, NIS2 for the security of essential
entities, the Data Act for switching and access, and the EU Cloud Services Scheme (EUCS) still unresolved
on the sovereignty requirements that would matter most here. That baseline governs *processing*. It does
not, on its own, place infrastructure under national control - which is the gap a sovereign core exists
to close.

| | |
|---|---|
| Governing instrument | Law 242/2022 establishing the Government Cloud (Cloud Guvernamental), PNRR-funded and under construction |
| Cloud certification | No national scheme; ISO 27001 |
| Data classification | Law 182/2002 on Classified Information: Secret de serviciu / Secret / Strict secret / Strict secret de importanta deosebita |
| Procurement route | Autoritatea pentru Digitalizarea Romaniei (ADR) and ONAC |

There is no national cloud certification scheme; assurance rests on ISO 27001 and contract terms. The choice is to adopt EUCS when it lands or to recognise a peer scheme (BSI C5, SecNumCloud, ENS) by equivalence - writing a national scheme from scratch for a state this size is not worth the effort.

The classification ladder is the practical control: it decides which tier of data may leave the
jurisdiction at all, and it should be mapped onto the four migration phases in section 12 before any
procurement starts. Buying capacity before deciding what may sit on it is how sovereign programmes end up
with expensive infrastructure hosting the wrong workloads.

**Foreign jurisdiction exposure.** No in-country region; the government cloud is intended to displace ad hoc ministry hosting

Dependency on US hyperscalers is **high**: they carry significant government workloads, most visibly productivity and collaboration. The sovereign core does not displace that overnight; it establishes somewhere for the workloads that must never have been there in the first place. Under the US CLOUD Act and FISA 702, a provider subject to US jurisdiction can face a lawful
order for data it holds, regardless of where the data physically sits. Data residency in-country is
therefore necessary but not sufficient; what matters is who holds the keys and who can be compelled.

## 11. Current state and provider landscape

| | |
|---|---|
| Government cloud | Cloud Privat Guvernamental - STS-operated, PNRR-funded (~EUR 560m package with SRI/ADR), 4 regional DCs (Bucharest, Timis, Brasov, Sibiu), national operational phase Mar 2026 |
| Maturity | pilot |
| Digital identity | ROeID / electronic ID card (CEI) |
| In-country commercial regions | 0 |
| Interconnection | InterLAN and RoNIX Bucharest; Black Sea KAFOS at Constanta |

What exists is a pilot rather than an operating platform; the sovereign core would be its first production incarnation.

Against that starting point, the modelled sovereign core is **11.9 MW of design load across
4 site(s)**, or roughly 4,894 servers. The gap between what runs today and that
figure is the actual programme; the capacity model in sections 4-6 sizes the destination, not the journey.

## 12. Migration path and cost

Workloads are sequenced by how badly loss of control would hurt, not by how easy they are to move. The
phases below are derived from the workload classes in `model/migration_phases.csv`; per-country figures
are in `migration_phases.csv` in this directory.

| Phase | Scope | Servers | Design MW | CAPEX | Cumulative | Hybrid-eligible |
|---|---|---:|---:|---:|---:|---|
| 1 | Sovereign core | 1,448 | 2.9 | EUR 54 m | 20% | no |
| 2 | Security and defense | 2,214 | 5.9 | EUR 143 m | 71% | no |
| 3 | State record | 834 | 1.7 | EUR 44 m | 87% | no |
| 4 | Elective | 398 | 1.4 | EUR 37 m | 100% | no |

**Phase 1 is the number that matters: EUR 54 m for 2.9 MW,
20% of total CAPEX.** That is the floor - identity and core government
services - below which no hybrid arrangement helps, because these workloads cannot be foreign-hosted under
any sovereignty posture worth the name. It is also, notably, a small fraction of the full build: sovereignty
for the workloads that define the state is cheaper than the headline figure suggests.

Phases 2 and 3 follow on clearance and legal constraints rather than cost. With no in-country commercial region, even the elective tier has nowhere in-jurisdiction to go: either it stays in the sovereign core, sized accordingly, or it leaves the jurisdiction under explicit terms.

Sequencing caveat: the CAPEX split above apportions facility cost by each phase's share of IT load, which
assumes phases are built into a shared facility programme rather than as separate buildings. Building
phase 1 alone, on its own site, costs disproportionately more - the facility is largely a fixed cost.
