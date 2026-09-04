# Estonia - Sovereign Government Data Center Network

> Generated 2026-09-01 by `model/generate_countries.py` from the Dutch reference case
> (`countries/NL/GOAL.md`) and `model/eu27_parameters.csv`. Every number below is a **scaled working
> assumption**, not a sourced figure. Edit the CSVs in this directory and re-run
> `python3 model/capacity_model.py EE` to update the capacity numbers; edit
> `model/eu27_parameters.csv` or `model/scaling_rules.csv` and re-run the generator to update this file.

## 1. Working thesis

Estonia does not need to become technologically autarkic. It needs enough independently controlled compute,
storage, networking, identity, cryptography and operational capability that the state can continue functioning
when foreign commercial infrastructure is unavailable, politically constrained, compromised, or no longer
trustworthy. The Dutch design rules (sovereignty is a stack, not a building; 3-5 separated regions; dual fibre
paths; no single hardware supplier; a first-class developer platform) are taken as the starting point and
adjusted below for what is structurally different about Estonia.

## 2. Starting point

| | |
|---|---|
| Population | 1.37 m (Eurostat, 1 Jan 2025) |
| GDP | EUR 42 bn (2025, current prices) |
| Public administration employment (NACE O) | 37 k (Eurostat LFS 2025) |
| Non-household electricity price | 141.0 EUR/MWh (Eurostat, band IC, 2025-S2) |
| Renewables in electricity | 38.9% (2024) |
| Land area | 43,110 km2 |
| Live hyperscaler regions in-country | 0 |
| Existing government / sovereign cloud | Riigipilv (Government Cloud) - RIT (Estonian IT Centre) private state cloud on OCI Dedicated Region + Azure/AWS public-cloud framework (2025); Data Embassy in Luxembourg (2018); X-Road |
| National digital identity (anchor workload) | ID-kaart + Mobiil-ID + Smart-ID |
| Internet exchange / cable landings | TLLIX/RTIX Tallinn; EESF cables to Helsinki; Estlink HVDC |

Relative to the Dutch baseline: population x0.08, public administration x0.05,
GDP x0.04. Resulting design load: x0.10 the Dutch figure.

## 3. What is structurally different from the Dutch case

- **Frontline exposure.** A land border with Russia or Belarus (or a Black Sea coast facing the war) changes the threat model from *geopolitical supply disruption* to *kinetic and sabotage risk against the facilities themselves*. Defense and security workloads are scaled up 1.5x/1.25x in the baseline, and at least one site should be hardened (EMP/blast, autonomous power for weeks, not hours). A purely national footprint cannot provide the out-of-country cold copy that Estonia's Data Embassy already demonstrates; this is the first item to revisit when the EU federation layer (Dutch GOAL.md section 16) is modelled.
- **No hyperscaler region in-country.** Unlike the Netherlands, there is no commercial hyperscale tier to fall back on for non-critical workloads without leaving the jurisdiction. The sovereign core therefore has to be sized for a larger share of total government demand, and the hybrid model (Dutch GOAL.md section 7) needs a cross-border commercial tier.

## 4. Workload demand (scaled from the Dutch baseline)

Scaling weights per workload class are in `model/scaling_rules.csv`; the Dutch rows they scale are in
`countries/NL/workloads_inputs.csv`. Frontline multiplier applied: yes.

| Workload | Class | CPU cores | GPU eq. | Storage (PB) | Avail. factor |
|---|---|---:|---:|---:|---:|
| Digital identity / ID-kaart + Mobiil-ID + Smart-ID | Critical government | 1,400 | 0 | 0.5 | 1.5 |
| Core government applications | Government | 4,400 | 0 | 1.4 | 1.35 |
| Data platforms & analytics | Government data | 2,800 | 8 | 4.8 | 1.25 |
| AI / sovereign model serving | AI | 1,100 | 32 | 0.7 | 1.3 |
| Defense classified compute | Defense | 4,500 | 40 | 2.3 | 1.5 |
| Cybersecurity / SOC / telemetry | Security | 4,100 | 8 | 4.7 | 1.4 |
| Scientific / public research | Research | 1,300 | 8 | 1.0 | 1.15 |

## 5. Capacity model output

| Metric | Value |
|---|---:|
| Physical servers | 574 (CPU 386 / GPU 30 / storage 158) |
| Rack equivalents | ~18 |
| IT critical load | 1.0 MW |
| Facility load (PUE 1.25) | 1.2 MW |
| Facility design load (+20% headroom) | **1.4 MW** |
| Sites by capacity / recommended | 1 / **3** (minimum 3) |
| Average design MW per site | 0.5 MW |
| Total CAPEX | **EUR 35 m** (facility EUR 14 m, IT EUR 17 m, network EUR 3 m) |
| Annual energy | 10,562 MWh |
| Annual OPEX | **EUR 3 m / yr** (power EUR 1 m, non-power EUR 2 m) |

Full table: `facility_summary.csv`.

## 6. Proposed geography (first-pass hypothesis)

Site posture: hardened (frontline). Separation target: 50-100 km failure domains, dual fibre paths, distinct grid feeds.

| Region | Role | Share | Design MW | Racks | Facility CAPEX | Notes |
|---|---|---:|---:|---:|---:|---|
| Tallinn | Primary civil cloud | 40% | 0.6 | 7 | EUR 6 m | RIT Riigipilv estate, TLLIX, EESF cables to Finland. |
| Tartu | Sovereign secondary | 27% | 0.4 | 5 | EUR 4 m | University city, 180 km separation; 60 km from the Russian border - hardened design. |
| Parnu / West | Government / continuity | 22% | 0.3 | 4 | EUR 3 m | Furthest from the eastern frontier; Estonia-Sweden cable. |
| Out-of-country reserve (Data Embassy) | Strategic reserve | 10% | 0.1 | 2 | EUR 1 m | Existing Luxembourg Data Embassy pattern - national-only model cannot close this gap. |

These regions encode only the obvious constraints (capital estate, second metro, distance from the frontier,
fault or flood zone). They are to be replaced by the scored site selection in workstream A of the Dutch
`TODO.md` (grid capacity, flood risk, fibre, failure independence, physical security, land, cooling).

## 7. Geography and threat notes

No seismic/flood; cold climate and land abundant; FRONTLINE: 300 km Russian border; desynchronised from BRELL Feb 2025 (grid via Estlink/LitPol); repeated subsea sabotage 2023-25; 2007 cyberattack precedent; NATO battlegroup

## 8. Recommendations specific to Estonia

1. **Anchor on ID-kaart + Mobiil-ID + Smart-ID.** Digital identity is the workload that, if it fails, stops every other
   government service; it belongs in the sovereign core first, active-active across at least two regions.
2. **Build on the existing estate, do not replace it.** Riigipilv (Government Cloud) - RIT (Estonian IT Centre) private state cloud on OCI Dedicated Region + Azure/AWS public-cloud framework (2025) is the
   institutional starting point; the sovereign core should be its next generation, with one governance owner.
3. **Site posture: hardened (frontline).** Harden at least one region and plan an out-of-country cold copy.
4. **Power strategy.** Power is not the binding constraint; optimise for fibre diversity and failure-domain separation.
5. **Hybrid tier.** With no in-country hyperscaler region, define now which non-critical workloads may leave the jurisdiction and under what contract terms.

## 9. Open questions

- Replace scaled workload rows with real ministry/agency demand (see `countries/NL/CAPACITY_PLAN.md` for the method).
- Which body owns the sovereign core, and how are agencies compelled or incentivised to migrate?
- Out-of-country reserve: which partner state, under what treaty?
- Site-size assumption: is the 12 MW planning unit right for Estonia, or should sites be smaller?

## 10. Legal and regulatory posture

Every member state shares one baseline: GDPR for personal data, NIS2 for the security of essential
entities, the Data Act for switching and access, and the EU Cloud Services Scheme (EUCS) still unresolved
on the sovereignty requirements that would matter most here. That baseline governs *processing*. It does
not, on its own, place infrastructure under national control - which is the gap a sovereign core exists
to close.

| | |
|---|---|
| Governing instrument | Public Information Act; Data Embassy Act enabling state data held under Estonian jurisdiction abroad |
| Cloud certification | E-ITS national information security standard (successor to ISKE) |
| Data classification | State Secrets and Classified Foreign Information Act: Restricted / Confidential / Secret / Top Secret |
| Procurement route | State Infocommunication Foundation (RIT) as central provider |

A binding national standard exists (E-ITS national information security standard (successor to ISKE)), so the sovereign core can be certified against something already recognised rather than inventing its own controls.

The classification ladder is the practical control: it decides which tier of data may leave the
jurisdiction at all, and it should be mapped onto the four migration phases in section 12 before any
procurement starts. Buying capacity before deciding what may sit on it is how sovereign programmes end up
with expensive infrastructure hosting the wrong workloads.

**Foreign jurisdiction exposure.** No in-country region; data embassy in Luxembourg is the sovereign offshore pattern

Dependency on US hyperscalers is **low** by EU standards. The strategic risk here is complacency: a sovereign posture that is not exercised degrades quietly. Under the US CLOUD Act and FISA 702, a provider subject to US jurisdiction can face a lawful
order for data it holds, regardless of where the data physically sits. Data residency in-country is
therefore necessary but not sufficient; what matters is who holds the keys and who can be compelled.

## 11. Current state and provider landscape

| | |
|---|---|
| Government cloud | Riigipilv (Government Cloud) - RIT (Estonian IT Centre) private state cloud on OCI Dedicated Region + Azure/AWS public-cloud framework (2025); Data Embassy in Luxembourg (2018); X-Road |
| Maturity | operational |
| Digital identity | ID-kaart + Mobiil-ID + Smart-ID |
| In-country commercial regions | 0 |
| Interconnection | TLLIX/RTIX Tallinn; EESF cables to Helsinki; Estlink HVDC |

An operating government platform already exists; the sovereign core should be its next generation, not a parallel build beside it.

Against that starting point, the modelled sovereign core is **1.4 MW of design load across
3 site(s)**, or roughly 574 servers. The gap between what runs today and that
figure is the actual programme; the capacity model in sections 4-6 sizes the destination, not the journey.

## 12. Migration path and cost

Workloads are sequenced by how badly loss of control would hurt, not by how easy they are to move. The
phases below are derived from the workload classes in `model/migration_phases.csv`; per-country figures
are in `migration_phases.csv` in this directory.

| Phase | Scope | Servers | Design MW | CAPEX | Cumulative | Hybrid-eligible |
|---|---|---:|---:|---:|---:|---|
| 1 | Sovereign core | 136 | 0.3 | EUR 5 m | 15% | no |
| 2 | Security and defense | 270 | 0.7 | EUR 17 m | 64% | no |
| 3 | State record | 98 | 0.2 | EUR 6 m | 80% | no |
| 4 | Elective | 70 | 0.3 | EUR 7 m | 100% | no |

**Phase 1 is the number that matters: EUR 5 m for 0.3 MW,
15% of total CAPEX.** That is the floor - identity and core government
services - below which no hybrid arrangement helps, because these workloads cannot be foreign-hosted under
any sovereignty posture worth the name. It is also, notably, a small fraction of the full build: sovereignty
for the workloads that define the state is cheaper than the headline figure suggests.

Phases 2 and 3 follow on clearance and legal constraints rather than cost. With no in-country commercial region, even the elective tier has nowhere in-jurisdiction to go: either it stays in the sovereign core, sized accordingly, or it leaves the jurisdiction under explicit terms.

Sequencing caveat: the CAPEX split above apportions facility cost by each phase's share of IT load, which
assumes phases are built into a shared facility programme rather than as separate buildings. Building
phase 1 alone, on its own site, costs disproportionately more - the facility is largely a fixed cost.
