# Finland - Sovereign Government Data Center Network

> Generated 2026-09-01 by `model/generate_countries.py` from the Dutch reference case
> (`countries/NL/GOAL.md`) and `model/eu27_parameters.csv`. Every number below is a **scaled working
> assumption**, not a sourced figure. Edit the CSVs in this directory and re-run
> `python3 model/capacity_model.py FI` to update the capacity numbers; edit
> `model/eu27_parameters.csv` or `model/scaling_rules.csv` and re-run the generator to update this file.

## 1. Working thesis

Finland does not need to become technologically autarkic. It needs enough independently controlled compute,
storage, networking, identity, cryptography and operational capability that the state can continue functioning
when foreign commercial infrastructure is unavailable, politically constrained, compromised, or no longer
trustworthy. The Dutch design rules (sovereignty is a stack, not a building; 3-5 separated regions; dual fibre
paths; no single hardware supplier; a first-class developer platform) are taken as the starting point and
adjusted below for what is structurally different about Finland.

## 2. Starting point

| | |
|---|---|
| Population | 5.64 m (Eurostat, 1 Jan 2025) |
| GDP | EUR 282 bn (2025, current prices) |
| Public administration employment (NACE O) | 116 k (Eurostat LFS 2025) |
| Non-household electricity price | 74.8 EUR/MWh (Eurostat, band IC, 2025-S2) |
| Renewables in electricity | 54.3% (2024) |
| Land area | 304,316 km2 |
| Live hyperscaler regions in-country | 1 |
| Existing government / sovereign cloud | Valtori (Government ICT Centre) state DCs + public-cloud brokerage; PiTuKri cloud security criteria; Digital Sovereignty Roadmap adopted Apr 2026; no branded sovereign cloud |
| National digital identity (anchor workload) | Suomi.fi e-Identification (DVV) |
| Internet exchange / cable landings | FICIX Helsinki/Espoo/Oulu; C-Lion1 Helsinki-Rostock (damaged Nov 2024) |

Relative to the Dutch baseline: population x0.31, public administration x0.16,
GDP x0.24. Resulting design load: x0.31 the Dutch figure.

## 3. What is structurally different from the Dutch case

- **Frontline exposure.** A land border with Russia or Belarus (or a Black Sea coast facing the war) changes the threat model from *geopolitical supply disruption* to *kinetic and sabotage risk against the facilities themselves*. Defense and security workloads are scaled up 1.5x/1.25x in the baseline, and at least one site should be hardened (EMP/blast, autonomous power for weeks, not hours). A purely national footprint cannot provide the out-of-country cold copy that Estonia's Data Embassy already demonstrates; this is the first item to revisit when the EU federation layer (Dutch GOAL.md section 16) is modelled.
- **Cheap, clean power (75 EUR/MWh, 54% renewables).** The economics favour building larger sites than the 12 MW planning unit and offering spare sovereign capacity to partners - a reason to revisit the site-size assumption.

## 4. Workload demand (scaled from the Dutch baseline)

Scaling weights per workload class are in `model/scaling_rules.csv`; the Dutch rows they scale are in
`countries/NL/workloads_inputs.csv`. Frontline multiplier applied: yes.

| Workload | Class | CPU cores | GPU eq. | Storage (PB) | Avail. factor |
|---|---|---:|---:|---:|---:|
| Digital identity / Suomi.fi e-Identification | Critical government | 5,600 | 0 | 1.2 | 1.5 |
| Core government applications | Government | 13,000 | 0 | 4.3 | 1.35 |
| Data platforms & analytics | Government data | 9,700 | 24 | 16.6 | 1.25 |
| AI / sovereign model serving | AI | 4,300 | 120 | 2.9 | 1.3 |
| Defense classified compute | Defense | 14,100 | 120 | 7.0 | 1.5 |
| Cybersecurity / SOC / telemetry | Security | 7,400 | 8 | 8.4 | 1.4 |
| Scientific / public research | Research | 6,300 | 32 | 4.8 | 1.15 |

## 5. Capacity model output

| Metric | Value |
|---|---:|
| Physical servers | 1,717 (CPU 1,175 / GPU 89 / storage 453) |
| Rack equivalents | ~54 |
| IT critical load | 2.9 MW |
| Facility load (PUE 1.25) | 3.6 MW |
| Facility design load (+20% headroom) | **4.3 MW** |
| Sites by capacity / recommended | 1 / **3** (minimum 3) |
| Average design MW per site | 1.4 MW |
| Total CAPEX | **EUR 104 m** (facility EUR 43 m, IT EUR 51 m, network EUR 9 m) |
| Annual energy | 31,580 MWh |
| Annual OPEX | **EUR 7 m / yr** (power EUR 2 m, non-power EUR 5 m) |

Full table: `facility_summary.csv`.

## 6. Proposed geography (first-pass hypothesis)

Site posture: hardened (frontline). Separation target: 50-100 km failure domains, dual fibre paths, distinct grid feeds.

| Region | Role | Share | Design MW | Racks | Facility CAPEX | Notes |
|---|---|---:|---:|---:|---:|---|
| Helsinki - Uusimaa | Primary civil cloud | 40% | 1.8 | 22 | EUR 18 m | Valtori estate, FICIX, C-Lion1 landing; 30 min from Tallinn. |
| Tampere - Pirkanmaa | Sovereign secondary | 27% | 1.2 | 14 | EUR 12 m | Inland, 180 km separation, strong grid. |
| Oulu / North | Government / continuity | 22% | 1.0 | 12 | EUR 10 m | Cheapest power, free cooling, far from the frontier; adds ~10 ms. |
| Kajaani - Kuopio | Strategic reserve | 10% | 0.4 | 5 | EUR 4 m | LUMI (Kajaani) proves power and cooling for large loads. |

These regions encode only the obvious constraints (capital estate, second metro, distance from the frontier,
fault or flood zone). They are to be replaced by the scored site selection in workstream A of the Dutch
`TODO.md` (grid capacity, flood risk, fibre, failure independence, physical security, land, cooling).

## 7. Geography and threat notes

Very low seismic/flood; abundant land, cold climate, cheapest EU power (nuclear+wind+hydro); 1,340 km Russian border (NATO since 2023); Baltic Sea subsea sabotage risk; continental grid link only via Sweden/Estonia

## 8. Recommendations specific to Finland

1. **Anchor on Suomi.fi e-Identification.** Digital identity is the workload that, if it fails, stops every other
   government service; it belongs in the sovereign core first, active-active across at least two regions.
2. **Build on the existing estate, do not replace it.** Valtori (Government ICT Centre) state DCs + public-cloud brokerage is the
   institutional starting point; the sovereign core should be its next generation, with one governance owner.
3. **Site posture: hardened (frontline).** Harden at least one region and plan an out-of-country cold copy.
4. **Power strategy.** Power is not the binding constraint; optimise for fibre diversity and failure-domain separation.
5. **Hybrid tier.** Use in-country commercial regions for the non-critical tier, but keep identity, defense, security telemetry and registries in the sovereign core.

## 9. Open questions

- Replace scaled workload rows with real ministry/agency demand (see `countries/NL/CAPACITY_PLAN.md` for the method).
- Which body owns the sovereign core, and how are agencies compelled or incentivised to migrate?
- Out-of-country reserve: which partner state, under what treaty?
- Site-size assumption: is the 12 MW planning unit right for Finland, or should sites be smaller?

## 10. Legal and regulatory posture

Every member state shares one baseline: GDPR for personal data, NIS2 for the security of essential
entities, the Data Act for switching and access, and the EU Cloud Services Scheme (EUCS) still unresolved
on the sovereignty requirements that would matter most here. That baseline governs *processing*. It does
not, on its own, place infrastructure under national control - which is the gap a sovereign core exists
to close.

| | |
|---|---|
| Governing instrument | Act on Information Management in Public Administration (906/2019) |
| Cloud certification | Katakri and PiTuKri criteria (Traficom NCSA-FI) for classified and cloud assessment |
| Data classification | Security Classification Decree: Restricted (IV) / Confidential (III) / Secret (II) / Top Secret (I) |
| Procurement route | Hansel Oy central purchasing body |

A binding national standard exists (Katakri and PiTuKri criteria (Traficom NCSA-FI) for classified and cloud assessment), so the sovereign core can be certified against something already recognised rather than inventing its own controls.

The classification ladder is the practical control: it decides which tier of data may leave the
jurisdiction at all, and it should be mapped onto the four migration phases in section 12 before any
procurement starts. Buying capacity before deciding what may sit on it is how sovereign programmes end up
with expensive infrastructure hosting the wrong workloads.

**Foreign jurisdiction exposure.** Azure and Google regions live in Finland; TUVE network carries classified traffic outside them

Dependency on US hyperscalers is **moderate**: national arrangements carry part of the estate, and the sovereign core extends an existing position rather than reversing one. Under the US CLOUD Act and FISA 702, a provider subject to US jurisdiction can face a lawful
order for data it holds, regardless of where the data physically sits. Data residency in-country is
therefore necessary but not sufficient; what matters is who holds the keys and who can be compelled.

## 11. Current state and provider landscape

| | |
|---|---|
| Government cloud | Valtori (Government ICT Centre) state DCs + public-cloud brokerage; PiTuKri cloud security criteria; Digital Sovereignty Roadmap adopted Apr 2026; no branded sovereign cloud |
| Maturity | operational |
| Digital identity | Suomi.fi e-Identification (DVV) |
| In-country commercial regions | 1 |
| Interconnection | FICIX Helsinki/Espoo/Oulu; C-Lion1 Helsinki-Rostock (damaged Nov 2024) |

An operating government platform already exists; the sovereign core should be its next generation, not a parallel build beside it.

Against that starting point, the modelled sovereign core is **4.3 MW of design load across
3 site(s)**, or roughly 1,717 servers. The gap between what runs today and that
figure is the actual programme; the capacity model in sections 4-6 sizes the destination, not the journey.

## 12. Migration path and cost

Workloads are sequenced by how badly loss of control would hurt, not by how easy they are to move. The
phases below are derived from the workload classes in `model/migration_phases.csv`; per-country figures
are in `migration_phases.csv` in this directory.

| Phase | Scope | Servers | Design MW | CAPEX | Cumulative | Hybrid-eligible |
|---|---|---:|---:|---:|---:|---|
| 1 | Sovereign core | 428 | 0.8 | EUR 16 m | 16% | no |
| 2 | Security and defense | 658 | 1.7 | EUR 42 m | 56% | no |
| 3 | State record | 336 | 0.7 | EUR 18 m | 74% | no |
| 4 | Elective | 295 | 1.0 | EUR 28 m | 100% | yes |

**Phase 1 is the number that matters: EUR 16 m for 0.8 MW,
16% of total CAPEX.** That is the floor - identity and core government
services - below which no hybrid arrangement helps, because these workloads cannot be foreign-hosted under
any sovereignty posture worth the name. It is also, notably, a small fraction of the full build: sovereignty
for the workloads that define the state is cheaper than the headline figure suggests.

Phases 2 and 3 follow on clearance and legal constraints rather than cost. Phase 4 can use in-country commercial capacity (1 live region(s)) under sovereign-held keys, which is what keeps the sovereign core small.

Sequencing caveat: the CAPEX split above apportions facility cost by each phase's share of IT load, which
assumes phases are built into a shared facility programme rather than as separate buildings. Building
phase 1 alone, on its own site, costs disproportionately more - the facility is largely a fixed cost.
