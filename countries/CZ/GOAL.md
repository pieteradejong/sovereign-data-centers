# Czechia - Sovereign Government Data Center Network

> Generated 2026-09-01 by `model/generate_countries.py` from the Dutch reference case
> (`countries/NL/GOAL.md`) and `model/eu27_parameters.csv`. Every number below is a **scaled working
> assumption**, not a sourced figure. Edit the CSVs in this directory and re-run
> `python3 model/capacity_model.py CZ` to update the capacity numbers; edit
> `model/eu27_parameters.csv` or `model/scaling_rules.csv` and re-run the generator to update this file.

## 1. Working thesis

Czechia does not need to become technologically autarkic. It needs enough independently controlled compute,
storage, networking, identity, cryptography and operational capability that the state can continue functioning
when foreign commercial infrastructure is unavailable, politically constrained, compromised, or no longer
trustworthy. The Dutch design rules (sovereignty is a stack, not a building; 3-5 separated regions; dual fibre
paths; no single hardware supplier; a first-class developer platform) are taken as the starting point and
adjusted below for what is structurally different about Czechia.

## 2. Starting point

| | |
|---|---|
| Population | 10.41 m (Eurostat, 1 Jan 2025) |
| GDP | EUR 347 bn (2025, current prices) |
| Public administration employment (NACE O) | 343 k (Eurostat LFS 2025) |
| Non-household electricity price | 182.5 EUR/MWh (Eurostat, band IC, 2025-S2) |
| Renewables in electricity | 17.9% (2024) |
| Land area | 77,212 km2 |
| Live hyperscaler regions in-country | 0 |
| Existing government / sovereign cloud | eGovernment Cloud (eGC) under the Digital and Information Agency (DIA): state part operated by SPCSS (security level 4) + NAKIT; commercial catalogue (Azure OCI Google AWS) |
| National digital identity (anchor workload) | Identita obcana (NIA) / eDoklady / BankID |
| Internet exchange / cable landings | NIX.CZ Prague; landlocked |

Relative to the Dutch baseline: population x0.58, public administration x0.48,
GDP x0.30. Resulting design load: x0.46 the Dutch figure.

## 3. What is structurally different from the Dutch case

- **No hyperscaler region in-country.** Unlike the Netherlands, there is no commercial hyperscale tier to fall back on for non-critical workloads without leaving the jurisdiction. The sovereign core therefore has to be sized for a larger share of total government demand, and the hybrid model (Dutch GOAL.md section 7) needs a cross-border commercial tier.

## 4. Workload demand (scaled from the Dutch baseline)

Scaling weights per workload class are in `model/scaling_rules.csv`; the Dutch rows they scale are in
`countries/NL/workloads_inputs.csv`. Frontline multiplier applied: no.

| Workload | Class | CPU cores | GPU eq. | Storage (PB) | Avail. factor |
|---|---|---:|---:|---:|---:|
| Digital identity / Identita obcana | Critical government | 10,400 | 0 | 2.3 | 1.5 |
| Core government applications | Government | 29,000 | 0 | 9.5 | 1.35 |
| Data platforms & analytics | Government data | 15,300 | 32 | 26.2 | 1.25 |
| AI / sovereign model serving | AI | 5,300 | 152 | 3.6 | 1.3 |
| Defense classified compute | Defense | 17,300 | 144 | 8.7 | 1.5 |
| Cybersecurity / SOC / telemetry | Security | 12,000 | 16 | 13.7 | 1.4 |
| Scientific / public research | Research | 7,700 | 40 | 5.9 | 1.15 |

## 5. Capacity model output

| Metric | Value |
|---|---:|
| Physical servers | 2,692 (CPU 1,883 / GPU 111 / storage 698) |
| Rack equivalents | ~84 |
| IT critical load | 4.3 MW |
| Facility load (PUE 1.25) | 5.4 MW |
| Facility design load (+20% headroom) | **6.5 MW** |
| Sites by capacity / recommended | 1 / **3** (minimum 3) |
| Average design MW per site | 2.2 MW |
| Total CAPEX | **EUR 152 m** (facility EUR 65 m, IT EUR 74 m, network EUR 13 m) |
| Annual energy | 47,162 MWh |
| Annual OPEX | **EUR 15 m / yr** (power EUR 9 m, non-power EUR 7 m) |

Full table: `facility_summary.csv`.

## 6. Proposed geography (first-pass hypothesis)

Site posture: standard. Separation target: 50-100 km failure domains, dual fibre paths, distinct grid feeds.

| Region | Role | Share | Design MW | Racks | Facility CAPEX | Notes |
|---|---|---:|---:|---:|---:|---|
| Prague - Central Bohemia | Primary civil cloud | 40% | 2.6 | 34 | EUR 26 m | SPCSS/NAKIT estate, NIX.CZ; Vltava flood zoning applies. |
| Brno / South Moravia | Sovereign secondary | 27% | 1.7 | 23 | EUR 17 m | Second metro, research cluster, 200 km separation. |
| Ostrava / Moravia-Silesia | Government / continuity | 22% | 1.4 | 19 | EUR 14 m | Industrial grid; post-coal land availability. |
| Plzen / West Bohemia | Strategic reserve | 10% | 0.7 | 8 | EUR 6 m | Western reserve, furthest from the eastern frontier. |

These regions encode only the obvious constraints (capital estate, second metro, distance from the frontier,
fault or flood zone). They are to be replaced by the scored site selection in workstream A of the Dutch
`TODO.md` (grid capacity, flood risk, fibre, failure independence, physical security, land, cooling).

## 7. Geography and threat notes

Low seismic; Vltava/Elbe/Morava floods (2024); central location with good land; nuclear baseload (new Dukovany units) but coal exit and gas import; NATO; ~300 km from Ukraine; Russian sabotage/espionage incidents 2024-25

## 8. Recommendations specific to Czechia

1. **Anchor on Identita obcana.** Digital identity is the workload that, if it fails, stops every other
   government service; it belongs in the sovereign core first, active-active across at least two regions.
2. **Build on the existing estate, do not replace it.** eGovernment Cloud (eGC) under the Digital and Information Agency (DIA): state part operated by SPCSS (security level 4) + NAKIT is the
   institutional starting point; the sovereign core should be its next generation, with one governance owner.
3. **Site posture: standard.** Standard Tier III+ with 50-100 km separation is sufficient; spend the hardening budget on supply-chain assurance instead.
4. **Power strategy.** Power is not the binding constraint; optimise for fibre diversity and failure-domain separation.
5. **Hybrid tier.** With no in-country hyperscaler region, define now which non-critical workloads may leave the jurisdiction and under what contract terms.

## 9. Open questions

- Replace scaled workload rows with real ministry/agency demand (see `countries/NL/CAPACITY_PLAN.md` for the method).
- Which body owns the sovereign core, and how are agencies compelled or incentivised to migrate?
- Which regions federate with EU partners for mutual disaster recovery, and which stay national-only?
- Site-size assumption: is the 12 MW planning unit right for Czechia, or should sites be smaller?

## 10. Legal and regulatory posture

Every member state shares one baseline: GDPR for personal data, NIS2 for the security of essential
entities, the Data Act for switching and access, and the EU Cloud Services Scheme (EUCS) still unresolved
on the sovereignty requirements that would matter most here. That baseline governs *processing*. It does
not, on its own, place infrastructure under national control - which is the gap a sovereign core exists
to close.

| | |
|---|---|
| Governing instrument | Act 365/2000 on Information Systems of Public Administration; eGovernment Cloud (eGC) catalogue is mandatory route |
| Cloud certification | NUKIB security requirements for the eGC catalogue; no separate cloud certificate |
| Data classification | Act 412/2005 on Protection of Classified Information: Restricted / Confidential / Secret / Top Secret |
| Procurement route | Ministry of the Interior eGC catalogue; commercial entries admitted only after NUKIB assessment |

A binding national standard exists (NUKIB security requirements for the eGC catalogue; no separate cloud certificate), so the sovereign core can be certified against something already recognised rather than inventing its own controls.

The classification ladder is the practical control: it decides which tier of data may leave the
jurisdiction at all, and it should be mapped onto the four migration phases in section 12 before any
procurement starts. Buying capacity before deciding what may sit on it is how sovereign programmes end up
with expensive infrastructure hosting the wrong workloads.

**Foreign jurisdiction exposure.** Microsoft Azure and AWS listed in the eGC commercial catalogue; no in-country hyperscaler region

Dependency on US hyperscalers is **moderate**: national arrangements carry part of the estate, and the sovereign core extends an existing position rather than reversing one. Under the US CLOUD Act and FISA 702, a provider subject to US jurisdiction can face a lawful
order for data it holds, regardless of where the data physically sits. Data residency in-country is
therefore necessary but not sufficient; what matters is who holds the keys and who can be compelled.

## 11. Current state and provider landscape

| | |
|---|---|
| Government cloud | eGovernment Cloud (eGC) under the Digital and Information Agency (DIA): state part operated by SPCSS (security level 4) + NAKIT; commercial catalogue (Azure OCI Google AWS) |
| Maturity | operational |
| Digital identity | Identita obcana (NIA) / eDoklady / BankID |
| In-country commercial regions | 0 |
| Interconnection | NIX.CZ Prague; landlocked |

An operating government platform already exists; the sovereign core should be its next generation, not a parallel build beside it.

Against that starting point, the modelled sovereign core is **6.5 MW of design load across
3 site(s)**, or roughly 2,692 servers. The gap between what runs today and that
figure is the actual programme; the capacity model in sections 4-6 sizes the destination, not the journey.

## 12. Migration path and cost

Workloads are sequenced by how badly loss of control would hurt, not by how easy they are to move. The
phases below are derived from the workload classes in `model/migration_phases.csv`; per-country figures
are in `migration_phases.csv` in this directory.

| Phase | Scope | Servers | Design MW | CAPEX | Cumulative | Hybrid-eligible |
|---|---|---:|---:|---:|---:|---|
| 1 | Sovereign core | 902 | 1.8 | EUR 34 m | 22% | no |
| 2 | Security and defense | 900 | 2.3 | EUR 56 m | 59% | no |
| 3 | State record | 527 | 1.1 | EUR 27 m | 77% | no |
| 4 | Elective | 363 | 1.3 | EUR 34 m | 100% | no |

**Phase 1 is the number that matters: EUR 34 m for 1.8 MW,
22% of total CAPEX.** That is the floor - identity and core government
services - below which no hybrid arrangement helps, because these workloads cannot be foreign-hosted under
any sovereignty posture worth the name. It is also, notably, a small fraction of the full build: sovereignty
for the workloads that define the state is cheaper than the headline figure suggests.

Phases 2 and 3 follow on clearance and legal constraints rather than cost. With no in-country commercial region, even the elective tier has nowhere in-jurisdiction to go: either it stays in the sovereign core, sized accordingly, or it leaves the jurisdiction under explicit terms.

Sequencing caveat: the CAPEX split above apportions facility cost by each phase's share of IT load, which
assumes phases are built into a shared facility programme rather than as separate buildings. Building
phase 1 alone, on its own site, costs disproportionately more - the facility is largely a fixed cost.
