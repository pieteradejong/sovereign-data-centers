# Poland - Sovereign Government Data Center Network

> Generated 2026-09-03 by `model/generate_countries.py` from the Dutch reference case
> (`countries/NL/GOAL.md`) and `model/eu27_parameters.csv`. Every number below is a **scaled working
> assumption**, not a sourced figure. Edit the CSVs in this directory and re-run
> `python3 model/capacity_model.py PL` to update the capacity numbers; edit
> `model/eu27_parameters.csv` or `model/scaling_rules.csv` and re-run the generator to update this file.

## 1. Working thesis

Poland does not need to become technologically autarkic. It needs enough independently controlled compute,
storage, networking, identity, cryptography and operational capability that the state can continue functioning
when foreign commercial infrastructure is unavailable, politically constrained, compromised, or no longer
trustworthy. The Dutch design rules (sovereignty is a stack, not a building; 3-5 separated regions; dual fibre
paths; no single hardware supplier; a first-class developer platform) are taken as the starting point and
adjusted below for what is structurally different about Poland.

## 2. Starting point

| | |
|---|---|
| Population | 36.50 m (Eurostat, 1 Jan 2025) |
| GDP | EUR 923 bn (2025, current prices) |
| Public administration employment (NACE O) | 1,215 k (Eurostat LFS 2025) |
| Non-household electricity price | 191.5 EUR/MWh (Eurostat, band IC, 2025-S2) |
| Renewables in electricity | 30.4% (2024) |
| Land area | 307,236 km2 |
| Live hyperscaler regions in-country | 2 |
| Existing government / sovereign cloud | WIIP: Rzadowa Chmura Obliczeniowa (RChO, COI/NASK, Ministry of Digital Affairs) + ZUCH public-cloud marketplace; Chmura Krajowa/OChK (PKO BP + PFR) commercial; national sovereign cloud/AI factory debate under EU CADA |
| National digital identity (anchor workload) | Profil Zaufany / mObywatel / e-dowod |
| Internet exchange / cable landings | PLIX and Equinix IX Warsaw; no major subsea landing |

Relative to the Dutch baseline: population x2.02, public administration x1.70,
GDP x0.79. Resulting design load: x1.74 the Dutch figure.

## 3. What is structurally different from the Dutch case

- **Frontline exposure.** A land border with Russia or Belarus (or a Black Sea coast facing the war) changes the threat model from *geopolitical supply disruption* to *kinetic and sabotage risk against the facilities themselves*. Defense and security workloads are scaled up 1.5x/1.25x in the baseline, and at least one site should be hardened (EMP/blast, autonomous power for weeks, not hours). A purely national footprint cannot provide the out-of-country cold copy that Estonia's Data Embassy already demonstrates; this is the first item to revisit when the EU federation layer (Dutch GOAL.md section 16) is modelled.
- **Expensive power (192 EUR/MWh vs. EU average ~184).** Power is the dominant OPEX line; free cooling, heat reuse, and siting near renewables or nuclear baseload move the economics more than server choice does. The model's power OPEX line is the number to attack first.

## 4. Workload demand (scaled from the Dutch baseline)

Scaling weights per workload class are in `model/scaling_rules.csv`; the Dutch rows they scale are in
`countries/NL/workloads_inputs.csv`. Frontline multiplier applied: yes.

| Workload | Class | CPU cores | GPU eq. | Storage (PB) | Avail. factor |
|---|---|---:|---:|---:|---:|
| Digital identity / Profil Zaufany | Critical government | 36,400 | 0 | 8.1 | 1.5 |
| Core government applications | Government | 102,300 | 0 | 33.5 | 1.35 |
| Data platforms & analytics | Government data | 49,200 | 112 | 84.4 | 1.25 |
| AI / sovereign model serving | AI | 14,200 | 400 | 9.5 | 1.3 |
| Defense classified compute | Defense | 91,000 | 776 | 45.5 | 1.5 |
| Cybersecurity / SOC / telemetry | Security | 52,900 | 80 | 60.2 | 1.4 |
| Scientific / public research | Research | 20,500 | 104 | 15.8 | 1.15 |

## 5. Capacity model output

| Metric | Value |
|---|---:|
| Physical servers | 10,231 (CPU 7,201 / GPU 431 / storage 2,599) |
| Rack equivalents | ~320 |
| IT critical load | 16.5 MW |
| Facility load (PUE 1.25) | 20.6 MW |
| Facility design load (+20% headroom) | **24.7 MW** |
| Sites by capacity / recommended | 3 / **4** (minimum 4) |
| Average design MW per site | 6.2 MW |
| Total CAPEX | **EUR 578 m** (facility EUR 247 m, IT EUR 281 m, network EUR 51 m) |
| Annual energy | 180,136 MWh |
| Annual OPEX | **EUR 61 m / yr** (power EUR 34 m, non-power EUR 26 m) |

Full table: `facility_summary.csv`.

## 6. Proposed geography (first-pass hypothesis)

Site posture: hardened (frontline). Separation target: 50-100 km failure domains, dual fibre paths, distinct grid feeds.

| Region | Role | Share | Design MW | Racks | Facility CAPEX | Notes |
|---|---|---:|---:|---:|---:|---|
| Warsaw / Mazovia | Primary civil cloud | 36% | 8.9 | 115 | EUR 89 m | COI/NASK RChO estate, PLIX, both hyperscaler regions. |
| Poznan / Greater Poland | Sovereign secondary | 18% | 4.4 | 58 | EUR 44 m | Western separation, Beyond.pl campus, German transit. |
| Krakow / Lesser Poland | Defense / industrial | 18% | 4.4 | 58 | EUR 44 m | Southern separation, CloudFerro/AI factory ecosystem. |
| Gdansk / Pomerania | Government / continuity | 18% | 4.4 | 58 | EUR 44 m | Baltic cable access, planned nuclear grid; Kaliningrad proximity - hardened. |
| Lodz - Wroclaw | Strategic reserve | 10% | 2.5 | 32 | EUR 25 m | Central/SW reserve; 2024 Oder flood plains excluded. |

These regions encode only the obvious constraints (capital estate, second metro, distance from the frontier,
fault or flood zone). They are to be replaced by the scored site selection in workstream A of the Dutch
`TODO.md` (grid capacity, flood risk, fibre, failure independence, physical security, land, cooling).

## 7. Geography and threat notes

Frontline: borders Kaliningrad, Belarus and Ukraine; recurring sabotage/arson and drone incursions (2025); GNSS jamming; no seismic; Oder/Vistula floods (2024); coal-heavy expensive grid with connection constraints; nuclear planned mid-2030s

## 8. Recommendations specific to Poland

1. **Anchor on Profil Zaufany.** Digital identity is the workload that, if it fails, stops every other
   government service; it belongs in the sovereign core first, active-active across at least two regions.
2. **Build on the existing estate, do not replace it.** WIIP: Rzadowa Chmura Obliczeniowa (RChO, COI/NASK, Ministry of Digital Affairs) + ZUCH public-cloud marketplace is the
   institutional starting point; the sovereign core should be its next generation, with one governance owner.
3. **Site posture: hardened (frontline).** Harden at least one region and plan an out-of-country cold copy.
4. **Power strategy.** Power is the binding constraint; treat grid connection lead time and on-site generation as first-order site criteria.
5. **Hybrid tier.** Use in-country commercial regions for the non-critical tier, but keep identity, defense, security telemetry and registries in the sovereign core.

## 9. Open questions

- Replace scaled workload rows with real ministry/agency demand (see `countries/NL/CAPACITY_PLAN.md` for the method).
- Which body owns the sovereign core, and how are agencies compelled or incentivised to migrate?
- Out-of-country reserve: which partner state, under what treaty?
- Site-size assumption: is the 12 MW planning unit right for Poland, or should sites be larger?

## 10. Legal and regulatory posture

Every member state shares one baseline: GDPR for personal data, NIS2 for the security of essential
entities, the Data Act for switching and access, and the EU Cloud Services Scheme (EUCS) still unresolved
on the sovereignty requirements that would matter most here. That baseline governs *processing*. It does
not, on its own, place infrastructure under national control - which is the gap a sovereign core exists
to close.

| | |
|---|---|
| Governing instrument | Act on Computerisation of Public Entities; Wspolna Infrastruktura Informatyczna Panstwa (WIIP) programme |
| Cloud certification | No national scheme; KRI regulation plus ISO 27001 |
| Data classification | Act on the Protection of Classified Information (2010): Zastrzezone / Poufne / Tajne / Scisle tajne |
| Procurement route | Centralny Osrodek Informatyki (COI) and central framework agreements |

There is no national cloud certification scheme; assurance rests on ISO 27001 and contract terms. The choice is to adopt EUCS when it lands or to recognise a peer scheme (BSI C5, SecNumCloud, ENS) by equivalence - writing a national scheme from scratch for a state this size is not worth the effort.

The classification ladder is the practical control: it decides which tier of data may leave the
jurisdiction at all, and it should be mapped onto the four migration phases in section 12 before any
procurement starts. Buying capacity before deciding what may sit on it is how sovereign programmes end up
with expensive infrastructure hosting the wrong workloads.

**Foreign jurisdiction exposure.** Azure (Poland Central) and Google (Warsaw) regions live; ZUCH catalogue mediates government consumption

Dependency on US hyperscalers is **high**: they carry significant government workloads, most visibly productivity and collaboration. The sovereign core does not displace that overnight; it establishes somewhere for the workloads that must never have been there in the first place. Under the US CLOUD Act and FISA 702, a provider subject to US jurisdiction can face a lawful
order for data it holds, regardless of where the data physically sits. Data residency in-country is
therefore necessary but not sufficient; what matters is who holds the keys and who can be compelled.

## 11. Current state and provider landscape

| | |
|---|---|
| Government cloud | WIIP: Rzadowa Chmura Obliczeniowa (RChO, COI/NASK, Ministry of Digital Affairs) + ZUCH public-cloud marketplace; Chmura Krajowa/OChK (PKO BP + PFR) commercial; national sovereign cloud/AI factory debate under EU CADA |
| Maturity | operational |
| Digital identity | Profil Zaufany / mObywatel / e-dowod |
| In-country commercial regions | 2 |
| Interconnection | PLIX and Equinix IX Warsaw; no major subsea landing |

An operating government platform already exists; the sovereign core should be its next generation, not a parallel build beside it.

Against that starting point, the modelled sovereign core is **24.7 MW of design load across
4 site(s)**, or roughly 10,231 servers. The gap between what runs today and that
figure is the actual programme; the capacity model in sections 4-6 sizes the destination, not the journey.

## 12. Migration path and cost

Workloads are sequenced by how badly loss of control would hurt, not by how easy they are to move. The
phases below are derived from the workload classes in `model/migration_phases.csv`; per-country figures
are in `migration_phases.csv` in this directory.

| Phase | Scope | Servers | Design MW | CAPEX | Cumulative | Hybrid-eligible |
|---|---|---:|---:|---:|---:|---|
| 1 | Sovereign core | 3,170 | 6.2 | EUR 119 m | 21% | no |
| 2 | Security and defense | 4,403 | 11.5 | EUR 281 m | 69% | no |
| 3 | State record | 1,696 | 3.5 | EUR 88 m | 84% | no |
| 4 | Elective | 962 | 3.4 | EUR 90 m | 100% | yes |

**Phase 1 is the number that matters: EUR 119 m for 6.2 MW,
21% of total CAPEX.** That is the floor - identity and core government
services - below which no hybrid arrangement helps, because these workloads cannot be foreign-hosted under
any sovereignty posture worth the name. It is also, notably, a small fraction of the full build: sovereignty
for the workloads that define the state is cheaper than the headline figure suggests.

Phases 2 and 3 follow on clearance and legal constraints rather than cost. Phase 4 can use in-country commercial capacity (2 live region(s)) under sovereign-held keys, which is what keeps the sovereign core small.

Sequencing caveat: the CAPEX split above apportions facility cost by each phase's share of IT load, which
assumes phases are built into a shared facility programme rather than as separate buildings. Building
phase 1 alone, on its own site, costs disproportionately more - the facility is largely a fixed cost.
