# Tier 0 & Tier 1 Sizing — Sovereign Record Estimate

**Status:** draft, first pass
**Scope:** per-citizen and national storage footprint for the irreducible state record
**Worked example:** Netherlands (~18.0M population)
**Feeds:** `assumptions.csv`, `workloads.csv` in the capacity model; supersedes nothing yet

---

## 1. Why tier at all

"National data" spans four orders of magnitude per citizen depending on where the line
is drawn. Sizing it as one number produces a meaningless answer. The tiering below is
by **consequence of loss**, not by department:

| Tier | Definition | Per citizen | In scope here |
|---|---|---|---|
| 0 | Identity spine — without it the state cannot say who exists | 1–10 MB | ✅ |
| 1 | Legal/fiscal state — the enforceable relationship between citizen and state | 30–150 MB | ✅ |
| 2 | Health records incl. imaging | 1–5 GB | ❌ deferred |
| 3 | Genomics, archives, video retention, geospatial | 10–50 GB | ❌ deferred |

Tiers 2 and 3 are where the *bytes* are. Tiers 0 and 1 are where the *sovereignty* is.
That asymmetry is the central finding of this document.

---

## 2. Tier 0 — Identity spine

The set of records whose loss or corruption means the state cannot establish identity,
citizenship, or legal personhood. Recovery from a total loss is not possible by
re-derivation; it would require re-enrolling the population.

| Record class | Composition | Per citizen |
|---|---|---|
| Civil registry core | Names, DOB/place, sex, nationality, civil status, parent/child links, full address & mutation history, normalized | 20–80 KB |
| Facial biometric | Master-quality enrolment image retained for re-issuance (not the 15–20 KB eMRTD chip copy) | 200–500 KB |
| Fingerprint biometric | 2× template (~10 KB ea.) or 2× WSQ image (~100 KB ea.) | 20–200 KB |
| Breeder document scans | Birth certificate, naturalisation decision, marriage/divorce, death | 0.5–2 MB |
| Document issuance history | ~10–15 passport/ID records over a lifetime, incl. revocation state | 50–200 KB |
| Digital identity credentials | Key material, assurance level, binding history | <10 KB |
| Authentication audit log | ~100 events/yr × ~200 B, retention-dependent | 20 KB/yr |
| Electoral roll entry | Derived from civil registry; near-zero marginal | <1 KB |

**Per citizen: 1–5 MB typical, 10 MB conservative-high.**
**Netherlands: 18–180 TB logical. Midpoint ~50 TB.**

Notes:
- Almost all of this is either small structured rows or write-once blobs. Compression on
  the structured portion is 5–10×; the imagery is already compressed.
- The audit log is the only component with unbounded growth. Cap it with a retention
  parameter or it silently becomes the largest item in the tier.
- Retention is effectively permanent. NL civil registry entries persist ~110 years from
  birth before transfer to the national archive, so treat Tier 0 as never-deleted and
  size for the full standing population plus the deceased-but-retained cohort
  (multiply by ~1.5–2.0 for a mature registry).

---

## 3. Tier 1 — Legal and fiscal state

Records that establish the enforceable relationship between citizen and state:
what is owed, what is owned, what was adjudicated, what was earned.

| Record class | Sizing basis | Per citizen (amortized) |
|---|---|---|
| Tax | ~1 MB/filing-year (return + attachments/scans); ~72% of population files; 12-yr active window, longer archival | 20–50 MB |
| Benefits & pensions | Payment ledger (~1 KB × ~1,000 lifetime events) + case files and correspondence for the receiving subset | 3–10 MB |
| Land & property registry | ~8M parcels NL; deed scans 1–5 MB each plus cadastral geometry and the pre-digital scanned backfile (1832→) | 3–8 MB |
| Judicial & criminal justice | Police report → prosecution → court → corrections chain; 10–100 MB per case file; ~10–15% of population has a record. **Excludes** bodycam/CCTV (Tier 3) | 5–20 MB |
| Education | Enrolment, diplomas, student finance | 1–3 MB |
| Business registry | ~2M entities, filings + annual accounts ~5 MB each, divided across population | 0.5 MB |
| Vehicle & licensing | Registration, ownership chain, driving entitlement | 0.1–0.5 MB |

**Per citizen: 30–150 MB. Midpoint ~75 MB.**
**Netherlands: 0.5–2.7 PB logical. Midpoint ~1.35 PB.**

**Tier 0 + Tier 1 combined: ~80 MB/citizen → ~1.4 PB logical for NL.**

Growth: Tier 0 tracks population (~+0.3%/yr NL). Tier 1 accumulates transactionally —
roughly 30–60 TB/yr for NL, or ~3–4%/yr against the current base. Model these
separately; they have different drivers and a single growth rate will mislead.

---

## 4. Physical implications

Apply a 3.5× multiplier over logical for replication, erasure-coding overhead,
geo-redundancy and backup generations:

```
Tier 0 + 1 logical         ~1.4 PB
× 3.5 redundancy/overhead  ~5 PB raw
```

**On flash (the correct choice — see below): ~5–10 W/TB → 25–50 kW IT load.**
**On HDD: ~1 W/TB → ~5 kW.**

Against the 14 MW base case, Tier 0 + Tier 1 for the entire Dutch population is
**0.2–0.4% of the facility budget**, occupying on the order of **1–2 racks per site**.

### Consequences for the capacity model

1. **Storage is not the sizing driver.** If site count or MW is currently derived from
   storage volume, the driver is inverted. 14 MW is justified by *serving* — inference,
   analytics, query load, hosted government workloads — not by holding bytes.
   Recommend restructuring the model so storage is a derived line item, not an input to
   site count.

2. **Specify flash, not capacity HDD.** Tier 0/1 is a small-object, high-IOPS,
   low-latency, high-concurrency workload: identity lookups, authentication, benefit
   eligibility checks. It is IOPS-bound, not capacity-bound. At 5 PB raw the cost delta
   between NVMe and HDD is small enough to be irrelevant against the facility CAPEX,
   and the power delta (~45 kW) is inside the model's noise floor.

3. **Redundancy is nearly free here.** Because the tier is so small, 5-way replication
   with full geographic separation plus offline golden copies costs single-digit kW.
   There is no capacity argument for economising on Tier 0 durability. Budget for
   paranoid replication and spend the design effort on key custody and audit instead.

4. **Tier the sovereignty, not just the storage.** Tier 0 alone is ~50 TB — one rack,
   air-gappable, physically containable in a hardened facility. This makes a defensible
   policy argument: absolute national control over Tier 0/1, and a looser posture
   (EU-federated, or commercially hosted with sovereign-held keys) for the Tier 2/3
   bulk. Worth developing as a section in the country write-ups, since it decouples the
   political sovereignty argument from the expensive capacity argument.

---

## 5. Parameters to expose in the model

Move these out of the prose and into `assumptions.csv` so other EU-27 cases re-derive
rather than re-estimate:

| Parameter | NL value | Notes |
|---|---|---|
| `population` | 18.0M | |
| `registry_retention_multiplier` | 1.5–2.0 | Living + retained deceased cohort |
| `tier0_mb_per_citizen` | 3.0 | Midpoint |
| `auth_log_bytes_per_event` | 200 | |
| `auth_events_per_citizen_year` | 100 | |
| `auth_log_retention_years` | 7 | **Sensitive** — dominates Tier 0 if unbounded |
| `tax_filer_fraction` | 0.72 | |
| `tax_mb_per_filing_year` | 1.0 | |
| `tax_retention_years` | 12 | Active window |
| `parcels` | 8.0M | |
| `deed_mb_per_parcel` | 3.0 | Incl. scanned backfile |
| `judicial_record_fraction` | 0.12 | |
| `judicial_mb_per_case` | 40 | Excl. video |
| `redundancy_multiplier` | 3.5 | |
| `watts_per_tb_flash` | 7.5 | |

---

## 6. Confidence

- **Tier 0: good to within ~2×.** Derived from documented record schemas and biometric
  standards. The main uncertainty is master-image retention policy and audit log depth.
- **Tier 1: good to within ~3×.** The scanned-backfile volumes (land registry, judicial)
  are the weak spot — they depend on national digitisation programmes that vary widely
  and are poorly documented from outside.
- **Power figures:** 2026-era device densities, improving ~15–20%/yr. Treat as a
  ceiling for anything built after 2028.
- Every figure here is an order-of-magnitude estimate built from public schema
  documentation and standard media sizes, not from any national statistics office
  publication. Before this goes into a public write-up, the NL numbers should be
  validated against Kadaster, Belastingdienst and RvIG annual reports.

---

## 7. Open items

- [ ] Validate NL figures against primary sources (Kadaster, RvIG, Belastingdienst)
- [ ] Decide whether the deceased-retained cohort is modelled explicitly or as a multiplier
- [ ] Add IOPS/latency requirements — the actual binding constraint for this tier
- [ ] Determine whether the same tiering holds for a large state (DE, FR) where the
      flat non-per-citizen component becomes negligible, and a small one (MT, LU, EE)
      where it dominates
- [ ] Draft the "tiered sovereignty" argument as a reusable section for country write-ups
- [ ] Reconcile against `CAPACITY_PLAN.md` — check whether storage is currently an input
      to site count
