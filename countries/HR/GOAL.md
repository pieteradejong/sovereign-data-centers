# Croatia - Sovereign Government Data Center Network

> Generated 2026-09-03 by `model/generate_countries.py` from the Dutch reference case
> (`countries/NL/GOAL.md`) and `model/eu27_parameters.csv`. Every number below is a **scaled working
> assumption**, not a sourced figure. Edit the CSVs in this directory and re-run
> `python3 model/capacity_model.py HR` to update the capacity numbers; edit
> `model/eu27_parameters.csv` or `model/scaling_rules.csv` and re-run the generator to update this file.

## 1. Working thesis

Croatia does not need to become technologically autarkic. It needs enough independently controlled compute,
storage, networking, identity, cryptography and operational capability that the state can continue functioning
when foreign commercial infrastructure is unavailable, politically constrained, compromised, or no longer
trustworthy. The Dutch design rules (sovereignty is a stack, not a building; 3-5 separated regions; dual fibre
paths; no single hardware supplier; a first-class developer platform) are taken as the starting point and
adjusted below for what is structurally different about Croatia.

## 2. Starting point

| | |
|---|---|
| Population | 3.87 m (Eurostat, 1 Jan 2025) |
| GDP | EUR 93 bn (2025, current prices) |
| Public administration employment (NACE O) | 110 k (Eurostat LFS 2025) |
| Non-household electricity price | 154.8 EUR/MWh (Eurostat, band IC, 2025-S2) |
| Renewables in electricity | 58.0% (2024) |
| Land area | 55,896 km2 |
| Live hyperscaler regions in-country | 0 |
| Existing government / sovereign cloud | Centar dijeljenih usluga (CDU / Shared Services Centre) state cloud - APIS IT for Ministry of Justice, Public Administration and Digital Transformation; two HA data centres; NRRP-funded |
| National digital identity (anchor workload) | e-Gradani / NIAS + eOI eID card |
| Internet exchange / cable landings | CIX Zagreb; Dubrovnik (Adria-1) Adriatic links to Italy |

Relative to the Dutch baseline: population x0.21, public administration x0.15,
GDP x0.08. Resulting design load: x0.16 the Dutch figure.

## 3. What is structurally different from the Dutch case

- **High seismic risk.** Base isolation or seismic-rated structures are mandatory, not optional, at the primary site; the second and third regions should be chosen in a different seismic domain so a single event cannot take out two regions. Expect facility CAPEX above the EUR 10 m/MW planning figure.
- **No hyperscaler region in-country.** Unlike the Netherlands, there is no commercial hyperscale tier to fall back on for non-critical workloads without leaving the jurisdiction. The sovereign core therefore has to be sized for a larger share of total government demand, and the hybrid model (Dutch GOAL.md section 7) needs a cross-border commercial tier.

## 4. Workload demand (scaled from the Dutch baseline)

Scaling weights per workload class are in `model/scaling_rules.csv`; the Dutch rows they scale are in
`countries/NL/workloads_inputs.csv`. Frontline multiplier applied: no.

| Workload | Class | CPU cores | GPU eq. | Storage (PB) | Avail. factor |
|---|---|---:|---:|---:|---:|
| Digital identity / e-Gradani | Critical government | 3,900 | 0 | 0.9 | 1.5 |
| Core government applications | Government | 10,100 | 0 | 3.3 | 1.35 |
| Data platforms & analytics | Government data | 5,100 | 8 | 8.8 | 1.25 |
| AI / sovereign model serving | AI | 1,400 | 40 | 1.0 | 1.3 |
| Defense classified compute | Defense | 6,400 | 56 | 3.2 | 1.5 |
| Cybersecurity / SOC / telemetry | Security | 4,300 | 8 | 4.9 | 1.4 |
| Scientific / public research | Research | 2,100 | 8 | 1.6 | 1.15 |

## 5. Capacity model output

| Metric | Value |
|---|---:|
| Physical servers | 930 (CPU 653 / GPU 37 / storage 240) |
| Rack equivalents | ~29 |
| IT critical load | 1.5 MW |
| Facility load (PUE 1.25) | 1.8 MW |
| Facility design load (+20% headroom) | **2.2 MW** |
| Sites by capacity / recommended | 1 / **3** (minimum 3) |
| Average design MW per site | 0.7 MW |
| Total CAPEX | **EUR 52 m** (facility EUR 22 m, IT EUR 25 m, network EUR 5 m) |
| Annual energy | 16,184 MWh |
| Annual OPEX | **EUR 5 m / yr** (power EUR 3 m, non-power EUR 2 m) |

Full table: `facility_summary.csv`.

## 6. Proposed geography (first-pass hypothesis)

Site posture: standard. Separation target: 50-100 km failure domains, dual fibre paths, distinct grid feeds.

| Region | Role | Share | Design MW | Racks | Facility CAPEX | Notes |
|---|---|---:|---:|---:|---:|---|
| Zagreb | Primary civil cloud | 40% | 0.9 | 12 | EUR 9 m | CDU estate, CIX; 2020 earthquake makes seismic isolation mandatory. |
| Osijek / Slavonia | Sovereign secondary | 27% | 0.6 | 8 | EUR 6 m | Flat land, lower seismicity; Sava/Drava flood zoning applies. |
| Split / Dalmatia | Government / continuity | 22% | 0.5 | 6 | EUR 5 m | Coastal separation, Adriatic cable access; karst siting constraints. |
| Rijeka - Istria | Strategic reserve | 10% | 0.2 | 3 | EUR 2 m | Krk LNG and port grid; reserve/expansion. |

These regions encode only the obvious constraints (capital estate, second metro, distance from the frontier,
fault or flood zone). They are to be replaced by the scored site selection in workstream A of the Dutch
`TODO.md` (grid capacity, flood risk, fibre, failure independence, physical security, land, cooling).

## 7. Geography and threat notes

High seismic (2020 Zagreb M5.5, Petrinja M6.4); karst coast with limited flat land; Sava/Danube floods in Slavonia; ~30% electricity imports; Krk LNG terminal gives gas security; NATO

## 8. Recommendations specific to Croatia

1. **Anchor on e-Gradani.** Digital identity is the workload that, if it fails, stops every other
   government service; it belongs in the sovereign core first, active-active across at least two regions.
2. **Build on the existing estate, do not replace it.** Centar dijeljenih usluga (CDU / Shared Services Centre) state cloud - APIS IT for Ministry of Justice, Public Administration and Digital Transformation is the
   institutional starting point; the sovereign core should be its next generation, with one governance owner.
3. **Site posture: standard.** Standard Tier III+ with 50-100 km separation is sufficient; spend the hardening budget on supply-chain assurance instead.
4. **Power strategy.** Power is not the binding constraint; optimise for fibre diversity and failure-domain separation.
5. **Hybrid tier.** With no in-country hyperscaler region, define now which non-critical workloads may leave the jurisdiction and under what contract terms.

## 9. Open questions

- Replace scaled workload rows with real ministry/agency demand (see `countries/NL/CAPACITY_PLAN.md` for the method).
- Which body owns the sovereign core, and how are agencies compelled or incentivised to migrate?
- Which regions federate with EU partners for mutual disaster recovery, and which stay national-only?
- Site-size assumption: is the 12 MW planning unit right for Croatia, or should sites be smaller?

## 10. Legal and regulatory posture

Every member state shares one baseline: GDPR for personal data, NIS2 for the security of essential
entities, the Data Act for switching and access, and the EU Cloud Services Scheme (EUCS) still unresolved
on the sovereignty requirements that would matter most here. That baseline governs *processing*. It does
not, on its own, place infrastructure under national control - which is the gap a sovereign core exists
to close.

| | |
|---|---|
| Governing instrument | Act on the State Information Infrastructure; central state cloud operated by APIS IT |
| Cloud certification | No national scheme; ISO 27001 |
| Data classification | Data Secrecy Act: Restricted / Confidential / Secret / Top Secret |
| Procurement route | Central State Office for Digital Society Development (SDURDD) |

There is no national cloud certification scheme; assurance rests on ISO 27001 and contract terms. The choice is to adopt EUCS when it lands or to recognise a peer scheme (BSI C5, SecNumCloud, ENS) by equivalence - writing a national scheme from scratch for a state this size is not worth the effort.

The classification ladder is the practical control: it decides which tier of data may leave the
jurisdiction at all, and it should be mapped onto the four migration phases in section 12 before any
procurement starts. Buying capacity before deciding what may sit on it is how sovereign programmes end up
with expensive infrastructure hosting the wrong workloads.

**Foreign jurisdiction exposure.** No in-country region; Microsoft 365 in parts of administration via EU regions

Dependency on US hyperscalers is **high**: they carry significant government workloads, most visibly productivity and collaboration. The sovereign core does not displace that overnight; it establishes somewhere for the workloads that must never have been there in the first place. Under the US CLOUD Act and FISA 702, a provider subject to US jurisdiction can face a lawful
order for data it holds, regardless of where the data physically sits. Data residency in-country is
therefore necessary but not sufficient; what matters is who holds the keys and who can be compelled.

## 11. Current state and provider landscape

| | |
|---|---|
| Government cloud | Centar dijeljenih usluga (CDU / Shared Services Centre) state cloud - APIS IT for Ministry of Justice, Public Administration and Digital Transformation; two HA data centres; NRRP-funded |
| Maturity | operational |
| Digital identity | e-Gradani / NIAS + eOI eID card |
| In-country commercial regions | 0 |
| Interconnection | CIX Zagreb; Dubrovnik (Adria-1) Adriatic links to Italy |

An operating government platform already exists; the sovereign core should be its next generation, not a parallel build beside it.

Against that starting point, the modelled sovereign core is **2.2 MW of design load across
3 site(s)**, or roughly 930 servers. The gap between what runs today and that
figure is the actual programme; the capacity model in sections 4-6 sizes the destination, not the journey.

## 12. Migration path and cost

Workloads are sequenced by how badly loss of control would hurt, not by how easy they are to move. The
phases below are derived from the workload classes in `model/migration_phases.csv`; per-country figures
are in `migration_phases.csv` in this directory.

| Phase | Scope | Servers | Design MW | CAPEX | Cumulative | Hybrid-eligible |
|---|---|---:|---:|---:|---:|---|
| 1 | Sovereign core | 323 | 0.6 | EUR 12 m | 24% | no |
| 2 | Security and defense | 332 | 0.9 | EUR 22 m | 65% | no |
| 3 | State record | 177 | 0.4 | EUR 9 m | 83% | no |
| 4 | Elective | 98 | 0.3 | EUR 9 m | 100% | no |

**Phase 1 is the number that matters: EUR 12 m for 0.6 MW,
24% of total CAPEX.** That is the floor - identity and core government
services - below which no hybrid arrangement helps, because these workloads cannot be foreign-hosted under
any sovereignty posture worth the name. It is also, notably, a small fraction of the full build: sovereignty
for the workloads that define the state is cheaper than the headline figure suggests.

Phases 2 and 3 follow on clearance and legal constraints rather than cost. With no in-country commercial region, even the elective tier has nowhere in-jurisdiction to go: either it stays in the sovereign core, sized accordingly, or it leaves the jurisdiction under explicit terms.

Sequencing caveat: the CAPEX split above apportions facility cost by each phase's share of IT load, which
assumes phases are built into a shared facility programme rather than as separate buildings. Building
phase 1 alone, on its own site, costs disproportionately more - the facility is largely a fixed cost.
