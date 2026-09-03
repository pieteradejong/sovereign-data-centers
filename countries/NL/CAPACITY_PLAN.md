# Capacity Model — Plan to Go From Illustrative to Bottom-Up

Context: `dutch_sovereign_data_center_capacity_model.xlsx` plus its three CSV inputs already implement
the flow described in GOAL.md §19.B:

```
workloads → CPU/GPU/storage demand → servers → racks → power+cooling → DC size/cost
```

Every number currently in `assumptions.csv` and `workloads_inputs.csv` is labeled "Working
assumption" — i.e. plausible placeholders, not sourced figures. This plan turns that into a
defensible bottom-up model, per GOAL.md §18 (Capacity questions) and §19.B.

## Goal

Produce a capacity model where every input is either (a) sourced from real government/agency data,
or (b) an explicitly justified planning assumption with a documented rationale — no unlabeled
placeholders.

## Phase 1 — Real workload inventory (replaces `workloads_inputs.csv`)

1. Identify which ministries/agencies to include in scope for a first cut (start with the 7
   illustrative classes already in the sheet: DigiD/identity, core government apps, data
   platforms/analytics, AI/model serving, defense classified, cybersecurity/SOC, research).
2. For each, source or estimate:
   - current CPU core count and utilization (from existing government cloud/data-center contracts,
     hosting invoices, or agency IT inventories)
   - current storage footprint (logical, pre-replication)
   - GPU/accelerator usage, if any
   - an availability/resilience factor (the sheet already models this as a multiplier — validate
     the 1.15–1.5x range against actual SLA requirements per workload class)
3. Flag anything that must stay an estimate (e.g. classified defense compute) and document why —
   this keeps the "explicitly justified assumption" bar from §Goal above.
4. Output: a revised `workloads_inputs.csv` with a `Source` column distinguishing sourced vs.
   estimated rows.

## Phase 2 — Growth projections

1. Add 5-year and 10-year projections per workload class (CAGR or scenario-based — GOAL.md doesn't
   mandate a method, so pick whichever the source data supports).
2. Model at least two scenarios: baseline growth and an "AI-heavy" scenario where GPU/accelerator
   demand grows faster than CPU (the illustrative data already shows AI and data-platform workloads
   as GPU-heavy — this is the most volatile line item).
3. Output: extend the xlsx with a growth-adjusted demand tab, or add `workloads_growth.csv`.

## Phase 3 — Validate engineering assumptions (`assumptions.csv`)

Each row needs either a citation or a named rationale. Priority order (highest-impact / most
speculative first):

- **PUE 1.25** — validate against achievable PUE for planned climate/cooling approach; this
  directly scales facility MW.
- **Critical-load MW/site (12.0)** and **minimum sovereign sites (3)** — tie to Phase A (geographic
  design) once candidate sites are scored; site count and per-site MW are coupled decisions, not
  independent inputs.
- **Storage replication factor (3.0x)** — confirm against the resilience model in GOAL.md §14
  (what failure scenarios is 3x actually protecting against?).
- **CPU/GPU utilization (0.55 / 0.6)** — sanity-check against typical government workload
  utilization (often lower than commercial cloud) rather than assuming commercial-cloud-like
  efficiency.
- **Design headroom (0.2)** — confirm this is sufficient for the failure-domain redundancy model
  in GOAL.md §4 (surviving loss of one full region), not just routine growth headroom.
- **Economics rows** (server/facility CAPEX, electricity price, non-power OPEX) — source from
  recent Dutch data-center/procurement benchmarks; these are the rows most exposed to market
  movement and should be re-validated periodically, not treated as fixed.

Output: revised `assumptions.csv` with a `Source / Status` column that says more than "Working
assumption" — either a citation or "Planning assumption: <rationale>".

## Phase 4 — Sensitivity analysis

1. Identify the 4–5 assumptions with the largest leverage on total server count / MW / CAPEX
   (candidates: utilization, PUE, replication factor, headroom, GPU share of demand).
2. Run the model at ±X% on each independently to produce a tornado chart or simple sensitivity
   table.
3. This directly informs which assumptions in Phase 3 are worth the most effort to nail down first.

## Phase 5 — Tie into regional allocation (`region_allocation_inputs.csv`)

Once Phase A (geographic design, tracked separately in TODO.md) produces real candidate regions,
replace the placeholder West/North/East/South/Reserve shares with allocation driven by the scored
site list rather than assumed even-ish splits.

## Deliverables checklist

- [ ] `workloads_inputs.csv` v2 with sourced/estimated rows distinguished
- [ ] Growth projection tab/CSV (baseline + AI-heavy scenario)
- [ ] `assumptions.csv` v2 with real sourcing or documented rationale per row
- [ ] Sensitivity table/chart identifying highest-leverage assumptions
- [ ] `region_allocation_inputs.csv` v2 once geographic design work lands

## Sequencing note

Phases 1 and 3 can run in parallel (workload data and engineering assumptions are independent
sourcing efforts). Phase 2 depends on Phase 1. Phase 4 depends on Phases 1–3 being at least
draft-complete. Phase 5 depends on the separate geographic-design workstream (TODO.md item A).
