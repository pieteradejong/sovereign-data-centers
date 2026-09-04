# France - Sovereign Government Data Center Network

> Generated 2026-09-03 by `model/generate_countries.py` from the Dutch reference case
> (`countries/NL/GOAL.md`) and `model/eu27_parameters.csv`. Every number below is a **scaled working
> assumption**, not a sourced figure. Edit the CSVs in this directory and re-run
> `python3 model/capacity_model.py FR` to update the capacity numbers; edit
> `model/eu27_parameters.csv` or `model/scaling_rules.csv` and re-run the generator to update this file.

## 1. Working thesis

France does not need to become technologically autarkic. It needs enough independently controlled compute,
storage, networking, identity, cryptography and operational capability that the state can continue functioning
when foreign commercial infrastructure is unavailable, politically constrained, compromised, or no longer
trustworthy. The Dutch design rules (sovereignty is a stack, not a building; 3-5 separated regions; dual fibre
paths; no single hardware supplier; a first-class developer platform) are taken as the starting point and
adjusted below for what is structurally different about France.

## 2. Starting point

| | |
|---|---|
| Population | 68.64 m (Eurostat, 1 Jan 2025) |
| GDP | EUR 2,991 bn (2025, current prices) |
| Public administration employment (NACE O) | 2,272 k (Eurostat LFS 2025) |
| Non-household electricity price | 153.4 EUR/MWh (Eurostat, band IC, 2025-S2) |
| Renewables in electricity | 31.3% (2024) |
| Land area | 633,886 km2 |
| Live hyperscaler regions in-country | 4 |
| Existing government / sovereign cloud | SecNumCloud (ANSSI) / Cloud de confiance doctrine: OVHcloud Outscale Cloud Temple Thales S3NS qualified; Bleu and NumSpot pending (2026); state clouds Nubo (Finance) and Cloud Pi Native (Interior) via DINUM |
| National digital identity (anchor workload) | FranceConnect / FranceConnect+ + France Identite |
| Internet exchange / cable landings | France-IX Paris/Marseille; Marseille Mediterranean gateway; Atlantic landings Vendee/Bordeaux/Brittany |

Relative to the Dutch baseline: population x3.80, public administration x3.17,
GDP x2.56. Resulting design load: x3.24 the Dutch figure.

## 3. What is structurally different from the Dutch case

- **Dense hyperscaler presence (4 live regions).** Commercial capacity, fibre and skills exist in-country; the sovereign core can stay lean and the hybrid model works as designed. The risk is the opposite one: political pressure to declare a hyperscaler region 'sovereign enough' (Dutch GOAL.md section 17: location is not sovereignty).

## 4. Workload demand (scaled from the Dutch baseline)

Scaling weights per workload class are in `model/scaling_rules.csv`; the Dutch rows they scale are in
`countries/NL/workloads_inputs.csv`. Frontline multiplier applied: no.

| Workload | Class | CPU cores | GPU eq. | Storage (PB) | Avail. factor |
|---|---|---:|---:|---:|---:|
| Digital identity / FranceConnect | Critical government | 68,500 | 0 | 15.2 | 1.5 |
| Core government applications | Government | 191,800 | 0 | 62.8 | 1.35 |
| Data platforms & analytics | Government data | 111,300 | 256 | 190.8 | 1.25 |
| AI / sovereign model serving | AI | 46,000 | 1312 | 30.7 | 1.3 |
| Defense classified compute | Defense | 114,100 | 976 | 57.1 | 1.5 |
| Cybersecurity / SOC / telemetry | Security | 79,500 | 112 | 90.4 | 1.4 |
| Scientific / public research | Research | 66,400 | 328 | 51.1 | 1.15 |

## 5. Capacity model output

| Metric | Value |
|---|---:|
| Physical servers | 18,833 (CPU 13,063 / GPU 840 / storage 4,930) |
| Rack equivalents | ~589 |
| IT critical load | 30.6 MW |
| Facility load (PUE 1.25) | 38.3 MW |
| Facility design load (+20% headroom) | **45.9 MW** |
| Sites by capacity / recommended | 4 / **4** (minimum 4) |
| Average design MW per site | 11.5 MW |
| Total CAPEX | **EUR 1,086 m** (facility EUR 459 m, IT EUR 531 m, network EUR 96 m) |
| Annual energy | 335,121 MWh |
| Annual OPEX | **EUR 100 m / yr** (power EUR 51 m, non-power EUR 49 m) |

Full table: `facility_summary.csv`.

## 6. Proposed geography (first-pass hypothesis)

Site posture: standard. Separation target: 50-100 km failure domains, dual fibre paths, distinct grid feeds.

| Region | Role | Share | Design MW | Racks | Facility CAPEX | Notes |
|---|---|---:|---:|---:|---:|---|
| Ile-de-France | Primary civil cloud | 36% | 16.5 | 212 | EUR 165 m | DINUM/ministry estate, France-IX; RTE saturation - use designated turnkey sites. |
| Auvergne-Rhone-Alpes / Lyon | Sovereign secondary | 18% | 8.3 | 106 | EUR 83 m | Second metro, nuclear/hydro grid, Alpine seismic zoning. |
| Sud-Ouest / Toulouse - Bordeaux | Defense / industrial | 18% | 8.3 | 106 | EUR 83 m | Defense-aerospace cluster, Atlantic cable landings (Amitie). |
| Ouest / Rennes - Nantes | Government / continuity | 18% | 8.3 | 106 | EUR 83 m | DGA cyber cluster (Rennes), Brittany cable landings. |
| Grand Est - Hauts-de-France | Strategic reserve | 10% | 4.6 | 59 | EUR 46 m | Nuclear grid headroom; reserve/expansion. |

These regions encode only the obvious constraints (capital estate, second metro, distance from the frontier,
fault or flood zone). They are to be replaced by the scored site selection in workstream A of the Dutch
`TODO.md` (grid capacity, flood risk, fibre, failure independence, physical security, land, cooling).

## 7. Geography and threat notes

Low seismic (Alps/Pyrenees moderate); Seine/Rhone flood plains; land plentiful outside Ile-de-France; RTE grid saturation Paris/Marseille (state designated turnkey DC sites 2025); nuclear gives low import dependence; terrorism/cyber main threats

## 8. Recommendations specific to France

1. **Anchor on FranceConnect.** Digital identity is the workload that, if it fails, stops every other
   government service; it belongs in the sovereign core first, active-active across at least two regions.
2. **Build on the existing estate, do not replace it.** SecNumCloud (ANSSI) / Cloud de confiance doctrine: OVHcloud Outscale Cloud Temple Thales S3NS qualified is the
   institutional starting point; the sovereign core should be its next generation, with one governance owner.
3. **Site posture: standard.** Standard Tier III+ with 50-100 km separation is sufficient; spend the hardening budget on supply-chain assurance instead.
4. **Power strategy.** Power is not the binding constraint; optimise for fibre diversity and failure-domain separation.
5. **Hybrid tier.** Use in-country commercial regions for the non-critical tier, but keep identity, defense, security telemetry and registries in the sovereign core.

## 9. Open questions

- Replace scaled workload rows with real ministry/agency demand (see `countries/NL/CAPACITY_PLAN.md` for the method).
- Which body owns the sovereign core, and how are agencies compelled or incentivised to migrate?
- Which regions federate with EU partners for mutual disaster recovery, and which stay national-only?
- Site-size assumption: is the 12 MW planning unit right for France, or should sites be larger?

## 10. Legal and regulatory posture

Every member state shares one baseline: GDPR for personal data, NIS2 for the security of essential
entities, the Data Act for switching and access, and the EU Cloud Services Scheme (EUCS) still unresolved
on the sovereignty requirements that would matter most here. That baseline governs *processing*. It does
not, on its own, place infrastructure under national control - which is the gap a sovereign core exists
to close.

| | |
|---|---|
| Governing instrument | Doctrine 'Cloud au centre' (DINUM, revised 2023): sovereign-qualified cloud required for sensitive state data |
| Cloud certification | SecNumCloud (ANSSI) qualification; the most demanding national scheme in the EU-27 |
| Data classification | IGI 1300: Diffusion Restreinte / Secret / Tres Secret |
| Procurement route | UGAP and DINUM interministerial frameworks |

SecNumCloud (ANSSI) qualification; the most demanding national scheme in the EU-27 is among the most demanding cloud assurance regimes in the Union. The sovereign core inherits a mature control baseline and, more usefully, an existing qualification path that suppliers already know how to pass.

The classification ladder is the practical control: it decides which tier of data may leave the
jurisdiction at all, and it should be mapped onto the four migration phases in section 12 before any
procurement starts. Buying capacity before deciding what may sit on it is how sovereign programmes end up
with expensive infrastructure hosting the wrong workloads.

**Foreign jurisdiction exposure.** Bleu (Microsoft) and S3NS (Google) trusted-cloud joint ventures under French control; native AWS/Azure/GCP regions excluded from sensitive workloads

Dependency on US hyperscalers is **low** by EU standards. The strategic risk here is complacency: a sovereign posture that is not exercised degrades quietly. Under the US CLOUD Act and FISA 702, a provider subject to US jurisdiction can face a lawful
order for data it holds, regardless of where the data physically sits. Data residency in-country is
therefore necessary but not sufficient; what matters is who holds the keys and who can be compelled.

## 11. Current state and provider landscape

| | |
|---|---|
| Government cloud | SecNumCloud (ANSSI) / Cloud de confiance doctrine: OVHcloud Outscale Cloud Temple Thales S3NS qualified; Bleu and NumSpot pending (2026); state clouds Nubo (Finance) and Cloud Pi Native (Interior) via DINUM |
| Maturity | federated |
| Digital identity | FranceConnect / FranceConnect+ + France Identite |
| In-country commercial regions | 4 |
| Interconnection | France-IX Paris/Marseille; Marseille Mediterranean gateway; Atlantic landings Vendee/Bordeaux/Brittany |

A federated government cloud is already in production. The open question is consolidation and governance, not construction.

Against that starting point, the modelled sovereign core is **45.9 MW of design load across
4 site(s)**, or roughly 18,833 servers. The gap between what runs today and that
figure is the actual programme; the capacity model in sections 4-6 sizes the destination, not the journey.

## 12. Migration path and cost

Workloads are sequenced by how badly loss of control would hurt, not by how easy they are to move. The
phases below are derived from the workload classes in `model/migration_phases.csv`; per-country figures
are in `migration_phases.csv` in this directory.

| Phase | Scope | Servers | Design MW | CAPEX | Cumulative | Hybrid-eligible |
|---|---|---:|---:|---:|---:|---|
| 1 | Sovereign core | 5,945 | 11.7 | EUR 223 m | 21% | no |
| 2 | Security and defense | 5,944 | 15.3 | EUR 371 m | 55% | no |
| 3 | State record | 3,833 | 7.9 | EUR 200 m | 73% | no |
| 4 | Elective | 3,111 | 11.0 | EUR 291 m | 100% | yes |

**Phase 1 is the number that matters: EUR 223 m for 11.7 MW,
21% of total CAPEX.** That is the floor - identity and core government
services - below which no hybrid arrangement helps, because these workloads cannot be foreign-hosted under
any sovereignty posture worth the name. It is also, notably, a small fraction of the full build: sovereignty
for the workloads that define the state is cheaper than the headline figure suggests.

Phases 2 and 3 follow on clearance and legal constraints rather than cost. Phase 4 can use in-country commercial capacity (4 live region(s)) under sovereign-held keys, which is what keeps the sovereign core small.

Sequencing caveat: the CAPEX split above apportions facility cost by each phase's share of IT load, which
assumes phases are built into a shared facility programme rather than as separate buildings. Building
phase 1 alone, on its own site, costs disproportionately more - the facility is largely a fixed cost.
