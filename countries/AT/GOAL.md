# Austria - Sovereign Government Data Center Network

> Generated 2026-09-01 by `model/generate_countries.py` from the Dutch reference case
> (`countries/NL/GOAL.md`) and `model/eu27_parameters.csv`. Every number below is a **scaled working
> assumption**, not a sourced figure. Edit the CSVs in this directory and re-run
> `python3 model/capacity_model.py AT` to update the capacity numbers; edit
> `model/eu27_parameters.csv` or `model/scaling_rules.csv` and re-run the generator to update this file.

## 1. Working thesis

Austria does not need to become technologically autarkic. It needs enough independently controlled compute,
storage, networking, identity, cryptography and operational capability that the state can continue functioning
when foreign commercial infrastructure is unavailable, politically constrained, compromised, or no longer
trustworthy. The Dutch design rules (sovereignty is a stack, not a building; 3-5 separated regions; dual fibre
paths; no single hardware supplier; a first-class developer platform) are taken as the starting point and
adjusted below for what is structurally different about Austria.

## 2. Starting point

| | |
|---|---|
| Population | 9.20 m (Eurostat, 1 Jan 2025) |
| GDP | EUR 514 bn (2025, current prices) |
| Public administration employment (NACE O) | 333 k (Eurostat LFS 2025) |
| Non-household electricity price | 198.6 EUR/MWh (Eurostat, band IC, 2025-S2) |
| Renewables in electricity | 90.1% (2024) |
| Land area | 82,519 km2 |
| Live hyperscaler regions in-country | 1 |
| Existing government / sovereign cloud | BRZ (Bundesrechenzentrum) federal computing centre / BRZ Cloud; 2026 Digital Administration Guideline names digital sovereignty as core principle; no branded sovereign cloud |
| National digital identity (anchor workload) | ID Austria |
| Internet exchange / cable landings | VIX Vienna; landlocked (no subsea) |

Relative to the Dutch baseline: population x0.51, public administration x0.46,
GDP x0.44. Resulting design load: x0.48 the Dutch figure.

## 3. What is structurally different from the Dutch case

- **Expensive power (199 EUR/MWh vs. EU average ~184).** Power is the dominant OPEX line; free cooling, heat reuse, and siting near renewables or nuclear baseload move the economics more than server choice does. The model's power OPEX line is the number to attack first.

## 4. Workload demand (scaled from the Dutch baseline)

Scaling weights per workload class are in `model/scaling_rules.csv`; the Dutch rows they scale are in
`countries/NL/workloads_inputs.csv`. Frontline multiplier applied: no.

| Workload | Class | CPU cores | GPU eq. | Storage (PB) | Avail. factor |
|---|---|---:|---:|---:|---:|
| Digital identity / ID Austria | Critical government | 9,200 | 0 | 2.0 | 1.5 |
| Core government applications | Government | 26,800 | 0 | 8.8 | 1.35 |
| Data platforms & analytics | Government data | 16,600 | 40 | 28.5 | 1.25 |
| AI / sovereign model serving | AI | 7,900 | 224 | 5.3 | 1.3 |
| Defense classified compute | Defense | 15,300 | 128 | 7.6 | 1.5 |
| Cybersecurity / SOC / telemetry | Security | 10,900 | 16 | 12.4 | 1.4 |
| Scientific / public research | Research | 11,400 | 56 | 8.8 | 1.15 |

## 5. Capacity model output

| Metric | Value |
|---|---:|
| Physical servers | 2,739 (CPU 1,882 / GPU 131 / storage 726) |
| Rack equivalents | ~86 |
| IT critical load | 4.5 MW |
| Facility load (PUE 1.25) | 5.6 MW |
| Facility design load (+20% headroom) | **6.8 MW** |
| Sites by capacity / recommended | 1 / **3** (minimum 3) |
| Average design MW per site | 2.3 MW |
| Total CAPEX | **EUR 161 m** (facility EUR 68 m, IT EUR 79 m, network EUR 14 m) |
| Annual energy | 49,453 MWh |
| Annual OPEX | **EUR 17 m / yr** (power EUR 10 m, non-power EUR 7 m) |

Full table: `facility_summary.csv`.

## 6. Proposed geography (first-pass hypothesis)

Site posture: standard. Separation target: 50-100 km failure domains, dual fibre paths, distinct grid feeds.

| Region | Role | Share | Design MW | Racks | Facility CAPEX | Notes |
|---|---|---:|---:|---:|---:|---|
| East / Vienna - Lower Austria | Primary civil cloud | 40% | 2.7 | 35 | EUR 27 m | VIX connectivity, federal ministries, BRZ estate; Danube flood zoning applies. |
| Upper Austria / Linz | Sovereign secondary | 27% | 1.8 | 23 | EUR 18 m | Industrial grid, hydro power, 180 km from Vienna. |
| Styria / Graz | Government / continuity | 22% | 1.5 | 19 | EUR 15 m | Southern separation, research campus (TU Graz). |
| Tyrol - Salzburg / West | Strategic reserve | 10% | 0.7 | 9 | EUR 7 m | Alpine hydro; expansion or hardened reserve. |

These regions encode only the obvious constraints (capital estate, second metro, distance from the frontier,
fault or flood zone). They are to be replaced by the scored site selection in workstream A of the Dutch
`TODO.md` (grid capacity, flood risk, fibre, failure independence, physical security, land, cooling).

## 7. Geography and threat notes

Low seismic (Vienna Basin moderate); Danube/Alpine flood risk (2024); flat land concentrated in the east; winter power importer; gas-import dependent; neutral non-NATO; ~500 km from Ukraine

## 8. Recommendations specific to Austria

1. **Anchor on ID Austria.** Digital identity is the workload that, if it fails, stops every other
   government service; it belongs in the sovereign core first, active-active across at least two regions.
2. **Build on the existing estate, do not replace it.** BRZ (Bundesrechenzentrum) federal computing centre / BRZ Cloud is the
   institutional starting point; the sovereign core should be its next generation, with one governance owner.
3. **Site posture: standard.** Standard Tier III+ with 50-100 km separation is sufficient; spend the hardening budget on supply-chain assurance instead.
4. **Power strategy.** Power is the binding constraint; treat grid connection lead time and on-site generation as first-order site criteria.
5. **Hybrid tier.** Use in-country commercial regions for the non-critical tier, but keep identity, defense, security telemetry and registries in the sovereign core.

## 9. Open questions

- Replace scaled workload rows with real ministry/agency demand (see `countries/NL/CAPACITY_PLAN.md` for the method).
- Which body owns the sovereign core, and how are agencies compelled or incentivised to migrate?
- Which regions federate with EU partners for mutual disaster recovery, and which stay national-only?
- Site-size assumption: is the 12 MW planning unit right for Austria, or should sites be smaller?

## 10. Legal and regulatory posture

Every member state shares one baseline: GDPR for personal data, NIS2 for the security of essential
entities, the Data Act for switching and access, and the EU Cloud Services Scheme (EUCS) still unresolved
on the sovereignty requirements that would matter most here. That baseline governs *processing*. It does
not, on its own, place infrastructure under national control - which is the gap a sovereign core exists
to close.

| | |
|---|---|
| Governing instrument | E-Government Act (E-GovG); 2026 Digital Administration Guideline names digital sovereignty a core principle |
| Cloud certification | No national cloud scheme; ISO 27001 and German BSI C5 referenced in practice |
| Data classification | Informationssicherheitsgesetz (InfoSiG): Eingeschraenkt / Vertraulich / Geheim / Streng Geheim |
| Procurement route | Bundesbeschaffung GmbH (BBG) federal framework contracts |

There is no national cloud certification scheme; assurance rests on ISO 27001 and contract terms. The choice is to adopt EUCS when it lands or to recognise a peer scheme (BSI C5, SecNumCloud, ENS) by equivalence - writing a national scheme from scratch for a state this size is not worth the effort.

The classification ladder is the practical control: it decides which tier of data may leave the
jurisdiction at all, and it should be mapped onto the four migration phases in section 12 before any
procurement starts. Buying capacity before deciding what may sit on it is how sovereign programmes end up
with expensive infrastructure hosting the wrong workloads.

**Foreign jurisdiction exposure.** Microsoft 365 and Azure widely used across federal administration; no national carve-out negotiated

Dependency on US hyperscalers is **high**: they carry significant government workloads, most visibly productivity and collaboration. The sovereign core does not displace that overnight; it establishes somewhere for the workloads that must never have been there in the first place. Under the US CLOUD Act and FISA 702, a provider subject to US jurisdiction can face a lawful
order for data it holds, regardless of where the data physically sits. Data residency in-country is
therefore necessary but not sufficient; what matters is who holds the keys and who can be compelled.

## 11. Current state and provider landscape

| | |
|---|---|
| Government cloud | BRZ (Bundesrechenzentrum) federal computing centre / BRZ Cloud; 2026 Digital Administration Guideline names digital sovereignty as core principle; no branded sovereign cloud |
| Maturity | operational |
| Digital identity | ID Austria |
| In-country commercial regions | 1 |
| Interconnection | VIX Vienna; landlocked (no subsea) |

An operating government platform already exists; the sovereign core should be its next generation, not a parallel build beside it.

Against that starting point, the modelled sovereign core is **6.8 MW of design load across
3 site(s)**, or roughly 2,739 servers. The gap between what runs today and that
figure is the actual programme; the capacity model in sections 4-6 sizes the destination, not the journey.

## 12. Migration path and cost

Workloads are sequenced by how badly loss of control would hurt, not by how easy they are to move. The
phases below are derived from the workload classes in `model/migration_phases.csv`; per-country figures
are in `migration_phases.csv` in this directory.

| Phase | Scope | Servers | Design MW | CAPEX | Cumulative | Hybrid-eligible |
|---|---|---:|---:|---:|---:|---|
| 1 | Sovereign core | 824 | 1.6 | EUR 31 m | 19% | no |
| 2 | Security and defense | 805 | 2.1 | EUR 50 m | 50% | no |
| 3 | State record | 574 | 1.2 | EUR 30 m | 69% | no |
| 4 | Elective | 536 | 1.9 | EUR 50 m | 100% | yes |

**Phase 1 is the number that matters: EUR 31 m for 1.6 MW,
19% of total CAPEX.** That is the floor - identity and core government
services - below which no hybrid arrangement helps, because these workloads cannot be foreign-hosted under
any sovereignty posture worth the name. It is also, notably, a small fraction of the full build: sovereignty
for the workloads that define the state is cheaper than the headline figure suggests.

Phases 2 and 3 follow on clearance and legal constraints rather than cost. Phase 4 can use in-country commercial capacity (1 live region(s)) under sovereign-held keys, which is what keeps the sovereign core small.

Sequencing caveat: the CAPEX split above apportions facility cost by each phase's share of IT load, which
assumes phases are built into a shared facility programme rather than as separate buildings. Building
phase 1 alone, on its own site, costs disproportionately more - the facility is largely a fixed cost.
