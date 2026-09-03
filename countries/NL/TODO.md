# TODO

Derived from GOAL.md §18 (Questions still to answer) and §19 (Recommended next analytical work).
Status reflects what's actually in this repo today.

## A. Geographic design — not started
- [ ] Define scoring criteria weights (grid capacity, flood risk, fiber connectivity, failure independence, physical security, land availability, cooling/environmental constraints)
- [ ] Identify candidate sites/regions beyond the placeholder West/North/East/South/Reserve labels in `region_allocation_inputs.csv`
- [ ] Score and rank candidates
- [ ] Decide whether a hardened/bunker-style facility is warranted

## B. Capacity model — in progress
- [x] First-pass formula-driven model (`dutch_sovereign_data_center_capacity_model.xlsx`)
- [x] Engineering/economic assumptions drafted (`assumptions.csv`)
- [x] Illustrative workload demand inputs (`workloads_inputs.csv`)
- [x] Illustrative regional allocation (`region_allocation_inputs.csv`)
- [ ] Replace "working assumption" values with sourced figures (see draft plan)
- [ ] Replace illustrative workload rows with real ministry/agency demand
- [ ] Add 5- and 10-year growth projections
- [ ] Sensitivity analysis on key assumptions (utilization, PUE, replication factor, headroom)

See `CAPACITY_PLAN.md` for the detailed plan to close these gaps.

## C. Network graph — not started
- [ ] Model data centers, fiber paths, IXPs, power dependencies, critical services as a graph
- [ ] Compute failure domains, min-cuts, centrality
- [ ] Identify consequences of losing specific nodes/edges

## D. Threat model — not started
- [ ] Enumerate adversaries and failure scenarios (hardware failure → nation-state attack → geopolitical supply disruption)
- [ ] Map scenarios from GOAL.md §14 to specific mitigations and RPO/RTO targets
- [ ] Document per-service recovery targets

## E. Cost model — not started
- [ ] Estimate CAPEX/OPEX for 3-, 4-, and 5-region architectures
- [ ] Compare against continued hyperscaler dependence
- [ ] Sensitivity on electricity price, server CAPEX, facility CAPEX/MW

## Open questions (GOAL.md §18) not yet assigned to a workstream
- [ ] Governance: which ministry/independent authority owns RijksCloud?
- [ ] Governance: how are agencies compelled/incentivized to migrate critical workloads?
- [ ] Governance: how should defense/intelligence governance differ from civil?
- [ ] European integration: which services stay national-only vs. federate with EU partners?
- [ ] European integration: what mutual DR arrangements make sense?
