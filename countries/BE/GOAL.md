# Belgium - Sovereign Government Data Center Network

> Generated 2026-09-01 by `model/generate_countries.py` from the Dutch reference case
> (`countries/NL/GOAL.md`) and `model/eu27_parameters.csv`. Every number below is a **scaled working
> assumption**, not a sourced figure. Edit the CSVs in this directory and re-run
> `python3 model/capacity_model.py BE` to update the capacity numbers; edit
> `model/eu27_parameters.csv` or `model/scaling_rules.csv` and re-run the generator to update this file.

## 1. Working thesis

Belgium does not need to become technologically autarkic. It needs enough independently controlled compute,
storage, networking, identity, cryptography and operational capability that the state can continue functioning
when foreign commercial infrastructure is unavailable, politically constrained, compromised, or no longer
trustworthy. The Dutch design rules (sovereignty is a stack, not a building; 3-5 separated regions; dual fibre
paths; no single hardware supplier; a first-class developer platform) are taken as the starting point and
adjusted below for what is structurally different about Belgium.

## 2. Starting point

| | |
|---|---|
| Population | 11.90 m (Eurostat, 1 Jan 2025) |
| GDP | EUR 642 bn (2025, current prices) |
| Public administration employment (NACE O) | 447 k (Eurostat LFS 2025) |
| Non-household electricity price | 186.6 EUR/MWh (Eurostat, band IC, 2025-S2) |
| Renewables in electricity | 31.3% (2024) |
| Land area | 30,452 km2 |
| Live hyperscaler regions in-country | 2 |
| Existing government / sovereign cloud | Federal G-Cloud (BOSA/Smals community cloud); Smals selected Google Cloud as public-cloud pillar (Jun 2026) under federal sovereignty/portability rules |
| National digital identity (anchor workload) | Belgian eID card + itsme (CSAM) |
| Internet exchange / cable landings | BNIX Brussels; transit via Amsterdam/London |

Relative to the Dutch baseline: population x0.66, public administration x0.62,
GDP x0.55. Resulting design load: x0.61 the Dutch figure.

## 3. What is structurally different from the Dutch case

- No structural flags differ from the Dutch reference case; the Dutch design rules transfer directly.

## 4. Workload demand (scaled from the Dutch baseline)

Scaling weights per workload class are in `model/scaling_rules.csv`; the Dutch rows they scale are in
`countries/NL/workloads_inputs.csv`. Frontline multiplier applied: no.

| Workload | Class | CPU cores | GPU eq. | Storage (PB) | Avail. factor |
|---|---|---:|---:|---:|---:|
| Digital identity / Belgian eID card + itsme | Critical government | 11,900 | 0 | 2.6 | 1.5 |
| Core government applications | Government | 35,300 | 0 | 11.6 | 1.35 |
| Data platforms & analytics | Government data | 21,100 | 48 | 36.2 | 1.25 |
| AI / sovereign model serving | AI | 9,900 | 280 | 6.6 | 1.3 |
| Defense classified compute | Defense | 19,800 | 168 | 9.9 | 1.5 |
| Cybersecurity / SOC / telemetry | Security | 14,300 | 24 | 16.2 | 1.4 |
| Scientific / public research | Research | 14,300 | 72 | 11.0 | 1.15 |

## 5. Capacity model output

| Metric | Value |
|---|---:|
| Physical servers | 3,528 (CPU 2,430 / GPU 167 / storage 931) |
| Rack equivalents | ~110 |
| IT critical load | 5.8 MW |
| Facility load (PUE 1.25) | 7.3 MW |
| Facility design load (+20% headroom) | **8.7 MW** |
| Sites by capacity / recommended | 1 / **3** (minimum 3) |
| Average design MW per site | 2.9 MW |
| Total CAPEX | **EUR 207 m** (facility EUR 87 m, IT EUR 102 m, network EUR 18 m) |
| Annual energy | 63,564 MWh |
| Annual OPEX | **EUR 21 m / yr** (power EUR 12 m, non-power EUR 9 m) |

Full table: `facility_summary.csv`.

## 6. Proposed geography (first-pass hypothesis)

Site posture: standard. Separation target: 50-100 km failure domains, dual fibre paths, distinct grid feeds.

| Region | Role | Share | Design MW | Racks | Facility CAPEX | Notes |
|---|---|---:|---:|---:|---:|---|
| Brussels - Flemish Brabant | Primary civil cloud | 40% | 3.5 | 45 | EUR 35 m | Federal institutions, BNIX, Smals/G-Cloud estate; Elia connection queue is the constraint. |
| Wallonia / Mons - Charleroi | Sovereign secondary | 27% | 2.4 | 30 | EUR 24 m | Existing hyperscale cluster (St. Ghislain) proves power and fibre; south of Meuse flood zone. |
| Antwerp - Limburg | Government / continuity | 22% | 2.0 | 25 | EUR 20 m | Northern separation, port/industrial grid. |
| Liege - Ardennes | Strategic reserve | 10% | 0.9 | 11 | EUR 9 m | Eastern reserve; avoid 2021 Vesdre/Ourthe flood plains. |

These regions encode only the obvious constraints (capital estate, second metro, distance from the frontier,
fault or flood zone). They are to be replaced by the scored site selection in workstream A of the Dutch
`TODO.md` (grid capacity, flood risk, fibre, failure independence, physical security, land, cooling).

## 7. Geography and threat notes

No seismic; dense and land-constrained; Meuse flood risk (2021); Elia grid connection queues around Brussels/Antwerp; nuclear extension to 2035; gas/electricity import dependent; NATO/EU HQ host (hybrid/cyber target)

## 8. Recommendations specific to Belgium

1. **Anchor on Belgian eID card + itsme.** Digital identity is the workload that, if it fails, stops every other
   government service; it belongs in the sovereign core first, active-active across at least two regions.
2. **Build on the existing estate, do not replace it.** Federal G-Cloud (BOSA/Smals community cloud) is the
   institutional starting point; the sovereign core should be its next generation, with one governance owner.
3. **Site posture: standard.** Standard Tier III+ with 50-100 km separation is sufficient; spend the hardening budget on supply-chain assurance instead.
4. **Power strategy.** Power is not the binding constraint; optimise for fibre diversity and failure-domain separation.
5. **Hybrid tier.** Use in-country commercial regions for the non-critical tier, but keep identity, defense, security telemetry and registries in the sovereign core.

## 9. Open questions

- Replace scaled workload rows with real ministry/agency demand (see `countries/NL/CAPACITY_PLAN.md` for the method).
- Which body owns the sovereign core, and how are agencies compelled or incentivised to migrate?
- Which regions federate with EU partners for mutual disaster recovery, and which stay national-only?
- Site-size assumption: is the 12 MW planning unit right for Belgium, or should sites be smaller?

## 10. Legal and regulatory posture

Every member state shares one baseline: GDPR for personal data, NIS2 for the security of essential
entities, the Data Act for switching and access, and the EU Cloud Services Scheme (EUCS) still unresolved
on the sovereignty requirements that would matter most here. That baseline governs *processing*. It does
not, on its own, place infrastructure under national control - which is the gap a sovereign core exists
to close.

| | |
|---|---|
| Governing instrument | Federal cloud policy via FPS BOSA; Smals framework rules on sovereignty and portability (2026) |
| Cloud certification | No national scheme; ISO 27001 plus EU cloud code of conduct |
| Data classification | Classification Act 1998: Vertrouwelijk / Geheim / Zeer Geheim |
| Procurement route | FPS BOSA federal framework; Smals for social-security IT |

There is no national cloud certification scheme; assurance rests on ISO 27001 and contract terms. The choice is to adopt EUCS when it lands or to recognise a peer scheme (BSI C5, SecNumCloud, ENS) by equivalence - writing a national scheme from scratch for a state this size is not worth the effort.

The classification ladder is the practical control: it decides which tier of data may leave the
jurisdiction at all, and it should be mapped onto the four migration phases in section 12 before any
procurement starts. Buying capacity before deciding what may sit on it is how sovereign programmes end up
with expensive infrastructure hosting the wrong workloads.

**Foreign jurisdiction exposure.** Google Cloud selected as federal public-cloud pillar (Jun 2026); Microsoft 365 already broadly deployed

Dependency on US hyperscalers is **high**: they carry significant government workloads, most visibly productivity and collaboration. The sovereign core does not displace that overnight; it establishes somewhere for the workloads that must never have been there in the first place. Under the US CLOUD Act and FISA 702, a provider subject to US jurisdiction can face a lawful
order for data it holds, regardless of where the data physically sits. Data residency in-country is
therefore necessary but not sufficient; what matters is who holds the keys and who can be compelled.

## 11. Current state and provider landscape

| | |
|---|---|
| Government cloud | Federal G-Cloud (BOSA/Smals community cloud); Smals selected Google Cloud as public-cloud pillar (Jun 2026) under federal sovereignty/portability rules |
| Maturity | operational |
| Digital identity | Belgian eID card + itsme (CSAM) |
| In-country commercial regions | 2 |
| Interconnection | BNIX Brussels; transit via Amsterdam/London |

An operating government platform already exists; the sovereign core should be its next generation, not a parallel build beside it.

Against that starting point, the modelled sovereign core is **8.7 MW of design load across
3 site(s)**, or roughly 3,528 servers. The gap between what runs today and that
figure is the actual programme; the capacity model in sections 4-6 sizes the destination, not the journey.

## 12. Migration path and cost

Workloads are sequenced by how badly loss of control would hurt, not by how easy they are to move. The
phases below are derived from the workload classes in `model/migration_phases.csv`; per-country figures
are in `migration_phases.csv` in this directory.

| Phase | Scope | Servers | Design MW | CAPEX | Cumulative | Hybrid-eligible |
|---|---|---:|---:|---:|---:|---|
| 1 | Sovereign core | 1,079 | 2.1 | EUR 41 m | 20% | no |
| 2 | Security and defense | 1,050 | 2.7 | EUR 66 m | 51% | no |
| 3 | State record | 728 | 1.5 | EUR 38 m | 70% | no |
| 4 | Elective | 671 | 2.4 | EUR 63 m | 100% | yes |

**Phase 1 is the number that matters: EUR 41 m for 2.1 MW,
20% of total CAPEX.** That is the floor - identity and core government
services - below which no hybrid arrangement helps, because these workloads cannot be foreign-hosted under
any sovereignty posture worth the name. It is also, notably, a small fraction of the full build: sovereignty
for the workloads that define the state is cheaper than the headline figure suggests.

Phases 2 and 3 follow on clearance and legal constraints rather than cost. Phase 4 can use in-country commercial capacity (2 live region(s)) under sovereign-held keys, which is what keeps the sovereign core small.

Sequencing caveat: the CAPEX split above apportions facility cost by each phase's share of IT load, which
assumes phases are built into a shared facility programme rather than as separate buildings. Building
phase 1 alone, on its own site, costs disproportionately more - the facility is largely a fixed cost.
