# Portugal - Sovereign Government Data Center Network

> Generated 2026-09-01 by `model/generate_countries.py` from the Dutch reference case
> (`countries/NL/GOAL.md`) and `model/eu27_parameters.csv`. Every number below is a **scaled working
> assumption**, not a sourced figure. Edit the CSVs in this directory and re-run
> `python3 model/capacity_model.py PT` to update the capacity numbers; edit
> `model/eu27_parameters.csv` or `model/scaling_rules.csv` and re-run the generator to update this file.

## 1. Working thesis

Portugal does not need to become technologically autarkic. It needs enough independently controlled compute,
storage, networking, identity, cryptography and operational capability that the state can continue functioning
when foreign commercial infrastructure is unavailable, politically constrained, compromised, or no longer
trustworthy. The Dutch design rules (sovereignty is a stack, not a building; 3-5 separated regions; dual fibre
paths; no single hardware supplier; a first-class developer platform) are taken as the starting point and
adjusted below for what is structurally different about Portugal.

## 2. Starting point

| | |
|---|---|
| Population | 10.75 m (Eurostat, 1 Jan 2025) |
| GDP | EUR 307 bn (2025, current prices) |
| Public administration employment (NACE O) | 342 k (Eurostat LFS 2025) |
| Non-household electricity price | 132.9 EUR/MWh (Eurostat, band IC, 2025-S2) |
| Renewables in electricity | 65.8% (2024) |
| Land area | 90,996 km2 |
| Live hyperscaler regions in-country | 0 |
| Existing government / sovereign cloud | Plano Nacional de Nuvem Soberana - approved May 2026 (ARTE): data classification, technical requirements, phased state sovereign-cloud infrastructure; builds on Nuvem da AP (AMA/eSPap) |
| National digital identity (anchor workload) | Chave Movel Digital / Cartao de Cidadao |
| Internet exchange / cable landings | GigaPIX Lisbon; Sines landing hub (EllaLink 2Africa Equiano Medusa) |

Relative to the Dutch baseline: population x0.60, public administration x0.48,
GDP x0.26. Resulting design load: x0.45 the Dutch figure.

## 3. What is structurally different from the Dutch case

- **Grid isolation.** The national grid is an electrical island or nearly so (weak or single interconnection). The April 2025 Iberian blackout and Cyprus/Malta interconnector outages show the failure mode. Every site needs on-site generation and storage sized for multi-day ride-through, and the PUE and facility CAPEX assumptions should be revisited upward once site studies exist.
- **High seismic risk.** Base isolation or seismic-rated structures are mandatory, not optional, at the primary site; the second and third regions should be chosen in a different seismic domain so a single event cannot take out two regions. Expect facility CAPEX above the EUR 10 m/MW planning figure.
- **No hyperscaler region in-country.** Unlike the Netherlands, there is no commercial hyperscale tier to fall back on for non-critical workloads without leaving the jurisdiction. The sovereign core therefore has to be sized for a larger share of total government demand, and the hybrid model (Dutch GOAL.md section 7) needs a cross-border commercial tier.

## 4. Workload demand (scaled from the Dutch baseline)

Scaling weights per workload class are in `model/scaling_rules.csv`; the Dutch rows they scale are in
`countries/NL/workloads_inputs.csv`. Frontline multiplier applied: no.

| Workload | Class | CPU cores | GPU eq. | Storage (PB) | Avail. factor |
|---|---|---:|---:|---:|---:|
| Digital identity / Chave Movel Digital | Critical government | 10,700 | 0 | 2.4 | 1.5 |
| Core government applications | Government | 29,500 | 0 | 9.7 | 1.35 |
| Data platforms & analytics | Government data | 15,000 | 32 | 25.7 | 1.25 |
| AI / sovereign model serving | AI | 4,700 | 136 | 3.1 | 1.3 |
| Defense classified compute | Defense | 17,900 | 152 | 8.9 | 1.5 |
| Cybersecurity / SOC / telemetry | Security | 12,300 | 16 | 14.0 | 1.4 |
| Scientific / public research | Research | 6,800 | 32 | 5.2 | 1.15 |

## 5. Capacity model output

| Metric | Value |
|---|---:|
| Physical servers | 2,685 (CPU 1,887 / GPU 107 / storage 691) |
| Rack equivalents | ~84 |
| IT critical load | 4.3 MW |
| Facility load (PUE 1.25) | 5.3 MW |
| Facility design load (+20% headroom) | **6.4 MW** |
| Sites by capacity / recommended | 1 / **3** (minimum 3) |
| Average design MW per site | 2.1 MW |
| Total CAPEX | **EUR 150 m** (facility EUR 64 m, IT EUR 73 m, network EUR 13 m) |
| Annual energy | 46,743 MWh |
| Annual OPEX | **EUR 13 m / yr** (power EUR 6 m, non-power EUR 7 m) |

Full table: `facility_summary.csv`.

## 6. Proposed geography (first-pass hypothesis)

Site posture: standard. Separation target: 50-100 km failure domains, dual fibre paths, distinct grid feeds.

| Region | Role | Share | Design MW | Racks | Facility CAPEX | Notes |
|---|---|---:|---:|---:|---:|---|
| Lisbon | Primary civil cloud | 40% | 2.6 | 34 | EUR 26 m | AMA/eSPap estate, GigaPIX; seismic/tsunami design mandatory. |
| Sines / Alentejo | Sovereign secondary | 27% | 1.7 | 23 | EUR 17 m | Atlantic cable hub, Start Campus proves 1 GW-class grid; renewables. |
| Porto / North | Government / continuity | 22% | 1.4 | 19 | EUR 14 m | 300 km separation, lower seismicity, Douro hydro. |
| Coimbra / Centre | Strategic reserve | 10% | 0.6 | 8 | EUR 6 m | Inland reserve between the two metros. |

These regions encode only the obvious constraints (capital estate, second metro, distance from the frontier,
fault or flood zone). They are to be replaced by the scored site selection in workstream A of the Dutch
`TODO.md` (grid capacity, flood risk, fibre, failure independence, physical security, land, cooling).

## 7. Geography and threat notes

Seismic/tsunami exposure Lisbon-Algarve-Azores (1755 fault systems); wildfire and drought inland; Iberian grid island with weak links to France (Apr 2025 blackout) but cheap high-renewable power and land near Sines; very low geopolitical risk

## 8. Recommendations specific to Portugal

1. **Anchor on Chave Movel Digital.** Digital identity is the workload that, if it fails, stops every other
   government service; it belongs in the sovereign core first, active-active across at least two regions.
2. **Build on the existing estate, do not replace it.** Plano Nacional de Nuvem Soberana - approved May 2026 (ARTE): data classification, technical requirements, phased state sovereign-cloud infrastructure is the
   institutional starting point; the sovereign core should be its next generation, with one governance owner.
3. **Site posture: standard.** Standard Tier III+ with 50-100 km separation is sufficient; spend the hardening budget on supply-chain assurance instead.
4. **Power strategy.** Power is the binding constraint; treat grid connection lead time and on-site generation as first-order site criteria.
5. **Hybrid tier.** With no in-country hyperscaler region, define now which non-critical workloads may leave the jurisdiction and under what contract terms.

## 9. Open questions

- Replace scaled workload rows with real ministry/agency demand (see `countries/NL/CAPACITY_PLAN.md` for the method).
- Which body owns the sovereign core, and how are agencies compelled or incentivised to migrate?
- Which regions federate with EU partners for mutual disaster recovery, and which stay national-only?
- Site-size assumption: is the 12 MW planning unit right for Portugal, or should sites be smaller?

## 10. Legal and regulatory posture

Every member state shares one baseline: GDPR for personal data, NIS2 for the security of essential
entities, the Data Act for switching and access, and the EU Cloud Services Scheme (EUCS) still unresolved
on the sovereignty requirements that would matter most here. That baseline governs *processing*. It does
not, on its own, place infrastructure under national control - which is the gap a sovereign core exists
to close.

| | |
|---|---|
| Governing instrument | Cloud policy under AMA (Administrative Modernisation Agency); iAP interoperability platform |
| Cloud certification | No national scheme; ISO 27001 |
| Data classification | Lei do Segredo de Estado: Reservado / Confidencial / Secreto / Muito Secreto |
| Procurement route | ESPAP shared-services agency central frameworks |

There is no national cloud certification scheme; assurance rests on ISO 27001 and contract terms. The choice is to adopt EUCS when it lands or to recognise a peer scheme (BSI C5, SecNumCloud, ENS) by equivalence - writing a national scheme from scratch for a state this size is not worth the effort.

The classification ladder is the practical control: it decides which tier of data may leave the
jurisdiction at all, and it should be mapped onto the four migration phases in section 12 before any
procurement starts. Buying capacity before deciding what may sit on it is how sovereign programmes end up
with expensive infrastructure hosting the wrong workloads.

**Foreign jurisdiction exposure.** No major in-country region; Microsoft and AWS consumed from Spanish and Irish regions

Dependency on US hyperscalers is **high**: they carry significant government workloads, most visibly productivity and collaboration. The sovereign core does not displace that overnight; it establishes somewhere for the workloads that must never have been there in the first place. Under the US CLOUD Act and FISA 702, a provider subject to US jurisdiction can face a lawful
order for data it holds, regardless of where the data physically sits. Data residency in-country is
therefore necessary but not sufficient; what matters is who holds the keys and who can be compelled.

## 11. Current state and provider landscape

| | |
|---|---|
| Government cloud | Plano Nacional de Nuvem Soberana - approved May 2026 (ARTE): data classification, technical requirements, phased state sovereign-cloud infrastructure; builds on Nuvem da AP (AMA/eSPap) |
| Maturity | operational |
| Digital identity | Chave Movel Digital / Cartao de Cidadao |
| In-country commercial regions | 0 |
| Interconnection | GigaPIX Lisbon; Sines landing hub (EllaLink 2Africa Equiano Medusa) |

An operating government platform already exists; the sovereign core should be its next generation, not a parallel build beside it.

Against that starting point, the modelled sovereign core is **6.4 MW of design load across
3 site(s)**, or roughly 2,685 servers. The gap between what runs today and that
figure is the actual programme; the capacity model in sections 4-6 sizes the destination, not the journey.

## 12. Migration path and cost

Workloads are sequenced by how badly loss of control would hurt, not by how easy they are to move. The
phases below are derived from the workload classes in `model/migration_phases.csv`; per-country figures
are in `migration_phases.csv` in this directory.

| Phase | Scope | Servers | Design MW | CAPEX | Cumulative | Hybrid-eligible |
|---|---|---:|---:|---:|---:|---|
| 1 | Sovereign core | 920 | 1.8 | EUR 35 m | 23% | no |
| 2 | Security and defense | 928 | 2.4 | EUR 58 m | 62% | no |
| 3 | State record | 517 | 1.1 | EUR 27 m | 80% | no |
| 4 | Elective | 320 | 1.1 | EUR 30 m | 100% | no |

**Phase 1 is the number that matters: EUR 35 m for 1.8 MW,
23% of total CAPEX.** That is the floor - identity and core government
services - below which no hybrid arrangement helps, because these workloads cannot be foreign-hosted under
any sovereignty posture worth the name. It is also, notably, a small fraction of the full build: sovereignty
for the workloads that define the state is cheaper than the headline figure suggests.

Phases 2 and 3 follow on clearance and legal constraints rather than cost. With no in-country commercial region, even the elective tier has nowhere in-jurisdiction to go: either it stays in the sovereign core, sized accordingly, or it leaves the jurisdiction under explicit terms.

Sequencing caveat: the CAPEX split above apportions facility cost by each phase's share of IT load, which
assumes phases are built into a shared facility programme rather than as separate buildings. Building
phase 1 alone, on its own site, costs disproportionately more - the facility is largely a fixed cost.
