# Slovenia - Sovereign Government Data Center Network

> Generated 2026-09-01 by `model/generate_countries.py` from the Dutch reference case
> (`countries/NL/GOAL.md`) and `model/eu27_parameters.csv`. Every number below is a **scaled working
> assumption**, not a sourced figure. Edit the CSVs in this directory and re-run
> `python3 model/capacity_model.py SI` to update the capacity numbers; edit
> `model/eu27_parameters.csv` or `model/scaling_rules.csv` and re-run the generator to update this file.

## 1. Working thesis

Slovenia does not need to become technologically autarkic. It needs enough independently controlled compute,
storage, networking, identity, cryptography and operational capability that the state can continue functioning
when foreign commercial infrastructure is unavailable, politically constrained, compromised, or no longer
trustworthy. The Dutch design rules (sovereignty is a stack, not a building; 3-5 separated regions; dual fibre
paths; no single hardware supplier; a first-class developer platform) are taken as the starting point and
adjusted below for what is structurally different about Slovenia.

## 2. Starting point

| | |
|---|---|
| Population | 2.13 m (Eurostat, 1 Jan 2025) |
| GDP | EUR 70 bn (2025, current prices) |
| Public administration employment (NACE O) | 51 k (Eurostat LFS 2025) |
| Non-household electricity price | 150.3 EUR/MWh (Eurostat, band IC, 2025-S2) |
| Renewables in electricity | 43.1% (2024) |
| Land area | 20,145 km2 |
| Live hyperscaler regions in-country | 0 |
| Existing government / sovereign cloud | Drzavni racunalniski oblak (DRO) - Ministry of Digital Transformation state cloud in the national government DC (Ljubljana) + DR site; EuroHPC Vega (Maribor) |
| National digital identity (anchor workload) | SI-PASS / smsPASS / eOsebna eID card |
| Internet exchange / cable landings | SIX (ARNES) Ljubljana; no major landing (Koper) |

Relative to the Dutch baseline: population x0.12, public administration x0.07,
GDP x0.06. Resulting design load: x0.10 the Dutch figure.

## 3. What is structurally different from the Dutch case

- **Moderate seismic risk.** Seismic zoning should be a site-scoring criterion; at least two regions in different domains.
- **No hyperscaler region in-country.** Unlike the Netherlands, there is no commercial hyperscale tier to fall back on for non-critical workloads without leaving the jurisdiction. The sovereign core therefore has to be sized for a larger share of total government demand, and the hybrid model (Dutch GOAL.md section 7) needs a cross-border commercial tier.

## 4. Workload demand (scaled from the Dutch baseline)

Scaling weights per workload class are in `model/scaling_rules.csv`; the Dutch rows they scale are in
`countries/NL/workloads_inputs.csv`. Frontline multiplier applied: no.

| Workload | Class | CPU cores | GPU eq. | Storage (PB) | Avail. factor |
|---|---|---:|---:|---:|---:|
| Digital identity / SI-PASS | Critical government | 2,100 | 0 | 0.5 | 1.5 |
| Core government applications | Government | 5,200 | 0 | 1.7 | 1.35 |
| Data platforms & analytics | Government data | 3,100 | 8 | 5.3 | 1.25 |
| AI / sovereign model serving | AI | 1,100 | 32 | 0.7 | 1.3 |
| Defense classified compute | Defense | 3,500 | 32 | 1.8 | 1.5 |
| Cybersecurity / SOC / telemetry | Security | 3,300 | 8 | 3.8 | 1.4 |
| Scientific / public research | Research | 1,600 | 8 | 1.2 | 1.15 |

## 5. Capacity model output

| Metric | Value |
|---|---:|
| Physical servers | 570 (CPU 390 / GPU 27 / storage 153) |
| Rack equivalents | ~18 |
| IT critical load | 0.9 MW |
| Facility load (PUE 1.25) | 1.2 MW |
| Facility design load (+20% headroom) | **1.4 MW** |
| Sites by capacity / recommended | 1 / **3** (minimum 3) |
| Average design MW per site | 0.5 MW |
| Total CAPEX | **EUR 34 m** (facility EUR 14 m, IT EUR 17 m, network EUR 3 m) |
| Annual energy | 10,265 MWh |
| Annual OPEX | **EUR 3 m / yr** (power EUR 2 m, non-power EUR 2 m) |

Full table: `facility_summary.csv`.

## 6. Proposed geography (first-pass hypothesis)

Site posture: standard. Separation target: 50-100 km failure domains, dual fibre paths, distinct grid feeds.

| Region | Role | Share | Design MW | Racks | Facility CAPEX | Notes |
|---|---|---:|---:|---:|---:|---|
| Ljubljana | Primary civil cloud | 40% | 0.6 | 7 | EUR 6 m | DRO national DC, SIX; Ljubljana basin seismic zoning. |
| Maribor / Styria | Sovereign secondary | 27% | 0.4 | 5 | EUR 4 m | EuroHPC Vega campus, 120 km separation, Drava hydro. |
| Koper - Nova Gorica / West | Government / continuity | 22% | 0.3 | 4 | EUR 3 m | Italian transit and port grid; 2023 flood plains excluded. |
| Celje / Savinja | Strategic reserve | 10% | 0.1 | 2 | EUR 1 m | Central reserve; flood-plain siting must be excluded. |

These regions encode only the obvious constraints (capital estate, second metro, distance from the frontier,
fault or flood zone). They are to be replaced by the scored site selection in workstream A of the Dutch
`TODO.md` (grid capacity, flood risk, fibre, failure independence, physical security, land, cooling).

## 7. Geography and threat notes

Moderate seismic (Ljubljana basin; Bovec 1998/2004); catastrophic Aug 2023 floods (Savinja/Sava); mountainous with limited flat land; Krsko NPP shared with Croatia; low geopolitical risk

## 8. Recommendations specific to Slovenia

1. **Anchor on SI-PASS.** Digital identity is the workload that, if it fails, stops every other
   government service; it belongs in the sovereign core first, active-active across at least two regions.
2. **Build on the existing estate, do not replace it.** Drzavni racunalniski oblak (DRO) - Ministry of Digital Transformation state cloud in the national government DC (Ljubljana) + DR site is the
   institutional starting point; the sovereign core should be its next generation, with one governance owner.
3. **Site posture: standard.** Standard Tier III+ with 50-100 km separation is sufficient; spend the hardening budget on supply-chain assurance instead.
4. **Power strategy.** Power is not the binding constraint; optimise for fibre diversity and failure-domain separation.
5. **Hybrid tier.** With no in-country hyperscaler region, define now which non-critical workloads may leave the jurisdiction and under what contract terms.

## 9. Open questions

- Replace scaled workload rows with real ministry/agency demand (see `countries/NL/CAPACITY_PLAN.md` for the method).
- Which body owns the sovereign core, and how are agencies compelled or incentivised to migrate?
- Which regions federate with EU partners for mutual disaster recovery, and which stay national-only?
- Site-size assumption: is the 12 MW planning unit right for Slovenia, or should sites be smaller?

## 10. Legal and regulatory posture

Every member state shares one baseline: GDPR for personal data, NIS2 for the security of essential
entities, the Data Act for switching and access, and the EU Cloud Services Scheme (EUCS) still unresolved
on the sovereignty requirements that would matter most here. That baseline governs *processing*. It does
not, on its own, place infrastructure under national control - which is the gap a sovereign core exists
to close.

| | |
|---|---|
| Governing instrument | State cloud (Drzavni racunalniski oblak, DRO) under the Ministry of Digital Transformation |
| Cloud certification | No national scheme; ISO 27001 |
| Data classification | Classified Information Act: Interno / Zaupno / Tajno / Strogo tajno |
| Procurement route | Ministry of Public Administration central procurement |

There is no national cloud certification scheme; assurance rests on ISO 27001 and contract terms. The choice is to adopt EUCS when it lands or to recognise a peer scheme (BSI C5, SecNumCloud, ENS) by equivalence - writing a national scheme from scratch for a state this size is not worth the effort.

The classification ladder is the practical control: it decides which tier of data may leave the
jurisdiction at all, and it should be mapped onto the four migration phases in section 12 before any
procurement starts. Buying capacity before deciding what may sit on it is how sovereign programmes end up
with expensive infrastructure hosting the wrong workloads.

**Foreign jurisdiction exposure.** No in-country region; limited Microsoft use via EU regions

Dependency on US hyperscalers is **high**: they carry significant government workloads, most visibly productivity and collaboration. The sovereign core does not displace that overnight; it establishes somewhere for the workloads that must never have been there in the first place. Under the US CLOUD Act and FISA 702, a provider subject to US jurisdiction can face a lawful
order for data it holds, regardless of where the data physically sits. Data residency in-country is
therefore necessary but not sufficient; what matters is who holds the keys and who can be compelled.

## 11. Current state and provider landscape

| | |
|---|---|
| Government cloud | Drzavni racunalniski oblak (DRO) - Ministry of Digital Transformation state cloud in the national government DC (Ljubljana) + DR site; EuroHPC Vega (Maribor) |
| Maturity | operational |
| Digital identity | SI-PASS / smsPASS / eOsebna eID card |
| In-country commercial regions | 0 |
| Interconnection | SIX (ARNES) Ljubljana; no major landing (Koper) |

An operating government platform already exists; the sovereign core should be its next generation, not a parallel build beside it.

Against that starting point, the modelled sovereign core is **1.4 MW of design load across
3 site(s)**, or roughly 570 servers. The gap between what runs today and that
figure is the actual programme; the capacity model in sections 4-6 sizes the destination, not the journey.

## 12. Migration path and cost

Workloads are sequenced by how badly loss of control would hurt, not by how easy they are to move. The
phases below are derived from the workload classes in `model/migration_phases.csv`; per-country figures
are in `migration_phases.csv` in this directory.

| Phase | Scope | Servers | Design MW | CAPEX | Cumulative | Hybrid-eligible |
|---|---|---:|---:|---:|---:|---|
| 1 | Sovereign core | 169 | 0.3 | EUR 6 m | 19% | no |
| 2 | Security and defense | 215 | 0.6 | EUR 14 m | 60% | no |
| 3 | State record | 109 | 0.2 | EUR 6 m | 78% | no |
| 4 | Elective | 77 | 0.3 | EUR 7 m | 100% | no |

**Phase 1 is the number that matters: EUR 6 m for 0.3 MW,
19% of total CAPEX.** That is the floor - identity and core government
services - below which no hybrid arrangement helps, because these workloads cannot be foreign-hosted under
any sovereignty posture worth the name. It is also, notably, a small fraction of the full build: sovereignty
for the workloads that define the state is cheaper than the headline figure suggests.

Phases 2 and 3 follow on clearance and legal constraints rather than cost. With no in-country commercial region, even the elective tier has nowhere in-jurisdiction to go: either it stays in the sovereign core, sized accordingly, or it leaves the jurisdiction under explicit terms.

Sequencing caveat: the CAPEX split above apportions facility cost by each phase's share of IT load, which
assumes phases are built into a shared facility programme rather than as separate buildings. Building
phase 1 alone, on its own site, costs disproportionately more - the facility is largely a fixed cost.
