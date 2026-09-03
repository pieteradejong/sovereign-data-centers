#!/usr/bin/env python3
"""
Sovereign data center capacity model — parameterized for any country.

Reproduces the formula flow of countries/NL/dutch_sovereign_data_center_capacity_model.xlsx:

    workloads -> CPU/GPU/storage demand -> servers -> racks -> IT MW
              -> facility MW -> sites -> CAPEX/OPEX

Inputs (all CSV, all editable):
    model/assumptions.csv                          shared engineering/economic defaults
    model/migration_phases.csv                     workload class -> migration phase
    countries/<ISO>/params.csv                     per-country overrides of any assumption (optional)
    countries/<ISO>/workloads_inputs.csv           workload demand rows
    countries/<ISO>/region_allocation_inputs.csv   share of design load per region

Outputs:
    countries/<ISO>/facility_summary.csv
    countries/<ISO>/region_allocation_output.csv
    countries/<ISO>/migration_phases.csv
    model/eu27_results.csv                         one row per country (when run with --all)

Usage:
    python3 model/capacity_model.py NL            # one country, prints summary
    python3 model/capacity_model.py --all         # every dir under countries/
    python3 model/capacity_model.py NL --json     # machine-readable

No dependencies beyond the standard library, on purpose: the CSVs are the interface.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COUNTRIES = ROOT / "countries"
ASSUMPTIONS = ROOT / "model" / "assumptions.csv"
PHASE_MAP = ROOT / "model" / "migration_phases.csv"

# Assumption names exactly as they appear in assumptions.csv column "Assumption".
A = {
    "cores_per_server": "CPU cores per server",
    "gpu_per_server": "GPU equivalents per GPU server",
    "cpu_util": "Average CPU utilization",
    "gpu_util": "Average GPU utilization",
    "pb_per_storage_server": "Usable storage per storage server",
    "replication": "Storage replication factor",
    "servers_per_rack": "Servers per rack",
    "cpu_kw": "CPU server power",
    "gpu_kw": "GPU server power",
    "storage_kw": "Storage server power",
    "net_overhead": "Network/other IT overhead",
    "pue": "PUE",
    "headroom": "Design headroom",
    "mw_per_site": "Critical-load MW per site",
    "min_sites": "Minimum sovereign sites",
    "capex_cpu": "Server CAPEX - CPU",
    "capex_gpu": "Server CAPEX - GPU",
    "capex_storage": "Server CAPEX - storage",
    "capex_network": "Network CAPEX",
    "capex_facility": "Facility CAPEX",
    "elec_price": "Electricity price",
    "opex_nonpower": "Non-power annual OPEX",
}


def read_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def load_assumptions(country_dir: Path | None = None) -> dict[str, float]:
    """Shared defaults, then per-country overrides (params.csv: Assumption,Value[,Notes])."""
    values: dict[str, float] = {}
    for row in read_csv(ASSUMPTIONS):
        values[row["Assumption"]] = float(row["Value"])
    if country_dir is not None:
        override = country_dir / "params.csv"
        if override.exists():
            for row in read_csv(override):
                name = row["Assumption"]
                if name not in values:
                    raise KeyError(f"{override}: unknown assumption {name!r}")
                values[name] = float(row["Value"])
    missing = [v for v in A.values() if v not in values]
    if missing:
        raise KeyError(f"assumptions.csv missing: {missing}")
    return values


@dataclass
class WorkloadResult:
    workload: str
    cls: str
    cpu_servers: int
    gpu_servers: int
    storage_servers: int
    total_servers: int
    rack_equivalents: float
    server_it_mw: float


@dataclass
class Summary:
    iso2: str
    workloads: list[WorkloadResult] = field(default_factory=list)
    cpu_servers: int = 0
    gpu_servers: int = 0
    storage_servers: int = 0
    total_servers: int = 0
    rack_equivalents: float = 0.0
    server_it_mw: float = 0.0
    total_it_mw: float = 0.0
    facility_mw: float = 0.0
    design_mw: float = 0.0
    sites_by_mw: int = 0
    sites: int = 0
    avg_mw_per_site: float = 0.0
    capex_cpu: float = 0.0
    capex_gpu: float = 0.0
    capex_storage: float = 0.0
    capex_network: float = 0.0
    capex_facility: float = 0.0
    capex_total: float = 0.0
    annual_mwh: float = 0.0
    opex_power: float = 0.0
    opex_nonpower: float = 0.0
    opex_total: float = 0.0
    regions: list[dict] = field(default_factory=list)
    phases: list[dict] = field(default_factory=list)


def load_phase_map() -> dict[str, dict]:
    """Workload class -> migration phase. Keyed on Class, not Workload: the generator
    rewrites workload names per country (e.g. "Digital identity / Online-Ausweis eID"),
    but the seven class names are stable across all 27."""
    return {r["Class"]: r for r in read_csv(PHASE_MAP)}


def compute_phases(s: "Summary", a: dict[str, float]) -> list[dict]:
    """Group the already-computed per-workload results into migration phases.

    No new sizing math: this only sums WorkloadResult fields and apportions facility
    CAPEX by each phase's share of server IT load. Phase CAPEX therefore sums to
    Summary.capex_total.

    "Hybrid eligible (class)" is the class-level property only. The country-level gate
    (does an in-jurisdiction commercial region exist?) needs eu27_parameters.csv and is
    applied downstream in country_data.py, so this module stays dependent on nothing but
    a country directory plus assumptions.
    """
    pmap = load_phase_map()
    unknown = sorted({w.cls for w in s.workloads} - pmap.keys())
    if unknown:
        raise KeyError(f"{s.iso2}: workload classes missing from {PHASE_MAP.name}: {unknown}")

    buckets: dict[str, dict] = {}
    for w in s.workloads:
        p = pmap[w.cls]
        b = buckets.setdefault(
            p["Phase"],
            {"name": p["Phase name"], "hybrid": p["Hybrid eligible"], "workloads": [],
             "cpu": 0, "gpu": 0, "storage": 0, "servers": 0, "mw": 0.0},
        )
        b["workloads"].append(w.workload)
        b["cpu"] += w.cpu_servers
        b["gpu"] += w.gpu_servers
        b["storage"] += w.storage_servers
        b["servers"] += w.total_servers
        b["mw"] += w.server_it_mw

    rows, cumulative = [], 0.0
    for phase in sorted(buckets):
        b = buckets[phase]
        share = b["mw"] / s.server_it_mw if s.server_it_mw else 0.0
        capex_servers = (
            b["cpu"] * a[A["capex_cpu"]]
            + b["gpu"] * a[A["capex_gpu"]]
            + b["storage"] * a[A["capex_storage"]]
        )
        capex = capex_servers * (1 + a[A["capex_network"]]) + s.capex_facility * share
        cumulative += capex
        rows.append(
            {
                "Phase": phase,
                "Phase name": b["name"],
                "Workloads": "; ".join(b["workloads"]),
                "Servers": b["servers"],
                "Design MW": round(s.design_mw * share, 2),
                "CAPEX (EUR mm)": round(capex, 1),
                "Cumulative CAPEX %": round(100 * cumulative / s.capex_total, 1) if s.capex_total else 0.0,
                "Hybrid eligible (class)": b["hybrid"],
            }
        )
    return rows


def compute_workload(row: dict, a: dict[str, float]) -> WorkloadResult:
    cores = float(row["CPU cores required"])
    gpus = float(row["GPU eq. required"])
    pb = float(row["Logical storage (PB)"])
    avail = float(row["Availability factor"])

    # ROUNDUP(...,0) in the sheet == math.ceil here.
    cpu_servers = math.ceil(cores * avail / (a[A["cores_per_server"]] * a[A["cpu_util"]]))
    gpu_servers = math.ceil(gpus * avail / (a[A["gpu_per_server"]] * a[A["gpu_util"]]))
    storage_servers = math.ceil(pb * a[A["replication"]] * avail / a[A["pb_per_storage_server"]])
    total = cpu_servers + gpu_servers + storage_servers
    racks = total / a[A["servers_per_rack"]]
    mw = (
        cpu_servers * a[A["cpu_kw"]]
        + gpu_servers * a[A["gpu_kw"]]
        + storage_servers * a[A["storage_kw"]]
    ) / 1000.0
    return WorkloadResult(
        workload=row["Workload"],
        cls=row["Class"],
        cpu_servers=cpu_servers,
        gpu_servers=gpu_servers,
        storage_servers=storage_servers,
        total_servers=total,
        rack_equivalents=racks,
        server_it_mw=mw,
    )


def run_country(iso2: str, write: bool = True) -> Summary:
    cdir = COUNTRIES / iso2
    if not cdir.is_dir():
        raise FileNotFoundError(f"no such country dir: {cdir}")
    a = load_assumptions(cdir)
    s = Summary(iso2=iso2)

    for row in read_csv(cdir / "workloads_inputs.csv"):
        s.workloads.append(compute_workload(row, a))

    s.cpu_servers = sum(w.cpu_servers for w in s.workloads)
    s.gpu_servers = sum(w.gpu_servers for w in s.workloads)
    s.storage_servers = sum(w.storage_servers for w in s.workloads)
    s.total_servers = s.cpu_servers + s.gpu_servers + s.storage_servers
    s.rack_equivalents = s.total_servers / a[A["servers_per_rack"]]
    s.server_it_mw = sum(w.server_it_mw for w in s.workloads)
    s.total_it_mw = s.server_it_mw * (1 + a[A["net_overhead"]])
    s.facility_mw = s.total_it_mw * a[A["pue"]]
    s.design_mw = s.facility_mw * (1 + a[A["headroom"]])
    s.sites_by_mw = math.ceil(s.design_mw / a[A["mw_per_site"]])
    s.sites = max(s.sites_by_mw, int(a[A["min_sites"]]))
    s.avg_mw_per_site = s.design_mw / s.sites

    s.capex_cpu = s.cpu_servers * a[A["capex_cpu"]]
    s.capex_gpu = s.gpu_servers * a[A["capex_gpu"]]
    s.capex_storage = s.storage_servers * a[A["capex_storage"]]
    s.capex_network = (s.capex_cpu + s.capex_gpu + s.capex_storage) * a[A["capex_network"]]
    s.capex_facility = s.design_mw * a[A["capex_facility"]]
    s.capex_total = s.capex_cpu + s.capex_gpu + s.capex_storage + s.capex_network + s.capex_facility

    s.annual_mwh = s.facility_mw * 8760
    s.opex_power = s.annual_mwh * a[A["elec_price"]] / 1_000_000
    s.opex_nonpower = s.capex_total * a[A["opex_nonpower"]]
    s.opex_total = s.opex_power + s.opex_nonpower

    region_file = cdir / "region_allocation_inputs.csv"
    if region_file.exists():
        for r in read_csv(region_file):
            share = float(r["Share of design load"])
            s.regions.append(
                {
                    "Region": r["Region"],
                    "Role": r["Role"],
                    "Share of design load": share,
                    "Design MW": round(s.design_mw * share, 2),
                    "Estimated racks": round(s.rack_equivalents * share, 1),
                    "Indicative facility CAPEX (EUR mm)": round(s.design_mw * share * a[A["capex_facility"]], 1),
                    "Resilience role": r.get("Resilience role", ""),
                    "Notes": r.get("Notes", ""),
                }
            )
        total_share = sum(float(r["Share of design load"]) for r in read_csv(region_file))
        if abs(total_share - 1.0) > 1e-6:
            print(f"warning: {iso2} region shares sum to {total_share:.3f}, not 1.0", file=sys.stderr)

    s.phases = compute_phases(s, a)

    if write:
        write_csv(cdir / "facility_summary.csv", summary_rows(s, a))
        if s.regions:
            write_csv(cdir / "region_allocation_output.csv", s.regions)
        write_csv(cdir / "migration_phases.csv", s.phases)
    return s


def summary_rows(s: Summary, a: dict[str, float]) -> list[dict]:
    def r(metric, value, unit, driver):
        return {"Metric": metric, "Value": value, "Unit": unit, "Formula / Driver": driver}

    return [
        r("CPU servers", s.cpu_servers, "servers", "Workload-derived"),
        r("GPU servers", s.gpu_servers, "servers", "Workload-derived"),
        r("Storage servers", s.storage_servers, "servers", "Workload-derived"),
        r("Total servers", s.total_servers, "servers", "Sum of server classes"),
        r("Rack equivalents", round(s.rack_equivalents, 1), "racks", "Servers / servers per rack"),
        r("Server IT load", round(s.server_it_mw, 3), "MW", "Workload-derived"),
        r("Total IT load", round(s.total_it_mw, 3), "MW", "Adds network/other IT"),
        r("Facility load before headroom", round(s.facility_mw, 3), "MW", "IT x PUE"),
        r("Facility design load", round(s.design_mw, 3), "MW", "Adds design headroom"),
        r("Sites required by MW", s.sites_by_mw, "sites", "Design MW / site capacity"),
        r("Recommended sovereign sites", s.sites, "sites", "Max(capacity, minimum sites)"),
        r("Average design MW/site", round(s.avg_mw_per_site, 2), "MW/site", "Design MW / sites"),
        r("CPU server CAPEX", round(s.capex_cpu, 2), "EUR mm", "CPU servers x unit cost"),
        r("GPU server CAPEX", round(s.capex_gpu, 2), "EUR mm", "GPU servers x unit cost"),
        r("Storage server CAPEX", round(s.capex_storage, 2), "EUR mm", "Storage servers x unit cost"),
        r("Network CAPEX", round(s.capex_network, 2), "EUR mm", "% of server CAPEX"),
        r("Facility CAPEX", round(s.capex_facility, 2), "EUR mm", "Design MW x facility EUR/MW"),
        r("Total CAPEX", round(s.capex_total, 2), "EUR mm", "IT + network + facility"),
        r("Annual energy", round(s.annual_mwh, 0), "MWh/year", "Facility MW x 8,760"),
        r("Electricity price used", a[A["elec_price"]], "EUR/MWh", "Country parameter"),
        r("Annual power OPEX", round(s.opex_power, 2), "EUR mm/year", "MWh x EUR/MWh"),
        r("Annual non-power OPEX", round(s.opex_nonpower, 2), "EUR mm/year", "% of total CAPEX"),
        r("Total annual OPEX", round(s.opex_total, 2), "EUR mm/year", "Power + non-power"),
    ]


def result_row(s: Summary) -> dict:
    return {
        "iso2": s.iso2,
        "cpu_servers": s.cpu_servers,
        "gpu_servers": s.gpu_servers,
        "storage_servers": s.storage_servers,
        "total_servers": s.total_servers,
        "racks": round(s.rack_equivalents, 1),
        "total_it_mw": round(s.total_it_mw, 2),
        "design_mw": round(s.design_mw, 2),
        "sites": s.sites,
        "avg_mw_per_site": round(s.avg_mw_per_site, 2),
        "capex_eur_mm": round(s.capex_total, 1),
        "opex_power_eur_mm_yr": round(s.opex_power, 1),
        "opex_total_eur_mm_yr": round(s.opex_total, 1),
    }


def print_summary(s: Summary) -> None:
    print(f"== {s.iso2} ==")
    print(f"  servers     {s.total_servers:>8,}  (cpu {s.cpu_servers:,} / gpu {s.gpu_servers:,} / storage {s.storage_servers:,})")
    print(f"  racks       {s.rack_equivalents:>8,.0f}")
    print(f"  IT load     {s.total_it_mw:>8.2f} MW   design {s.design_mw:.2f} MW   sites {s.sites} (avg {s.avg_mw_per_site:.1f} MW)")
    print(f"  CAPEX       {s.capex_total:>8.0f} EUR mm   OPEX {s.opex_total:.0f} EUR mm/yr (power {s.opex_power:.0f})")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("iso2", nargs="?", help="country code (directory under countries/)")
    p.add_argument("--all", action="store_true", help="run every country directory")
    p.add_argument("--json", action="store_true", help="print JSON instead of a summary")
    p.add_argument("--no-write", action="store_true", help="do not write output CSVs")
    args = p.parse_args(argv)

    if args.all:
        codes = sorted(d.name for d in COUNTRIES.iterdir() if d.is_dir() and (d / "workloads_inputs.csv").exists())
    elif args.iso2:
        codes = [args.iso2.upper()]
    else:
        p.error("give a country code or --all")

    results = []
    for code in codes:
        s = run_country(code, write=not args.no_write)
        results.append(s)
        if args.json:
            print(json.dumps(result_row(s)))
        else:
            print_summary(s)

    if args.all and not args.no_write:
        write_csv(ROOT / "model" / "eu27_results.csv", [result_row(s) for s in results])
    return 0


if __name__ == "__main__":
    sys.exit(main())
