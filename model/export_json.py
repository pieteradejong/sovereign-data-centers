#!/usr/bin/env python3
"""
Export every fact about all 27 member states as one JSON bundle for the web app.

    python3 model/export_json.py [-o web/public/data/eu27.json]

Reads the same country_data.build() dict the markdown briefs are rendered from, so
the app and the briefs cannot disagree. The whole bundle is ~26 KB gzipped, which is
why the app ships the entire model client-side and needs no API.

Keys prefixed with "_" are dropped: they carry Python objects (the raw Summary
dataclass) that exist only so the markdown renderer can format unrounded values.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import capacity_model as cm  # noqa: E402
import country_data  # noqa: E402
import generate_countries as gc  # noqa: E402

SCHEMA_VERSION = 1
DEFAULT_OUT = cm.ROOT / "web" / "public" / "data" / "eu27.json"


def strip_private(obj):
    """Drop "_"-prefixed keys recursively; they hold Python objects, not data."""
    if isinstance(obj, dict):
        return {k: strip_private(v) for k, v in obj.items() if not k.startswith("_")}
    if isinstance(obj, list):
        return [strip_private(v) for v in obj]
    return obj


def build_bundle() -> dict:
    params = {r["iso2"]: r for r in cm.read_csv(gc.PARAMS)}
    nl = params[gc.BASELINE]
    nl_summary = cm.run_country(gc.BASELINE, write=False)

    countries = {}
    for iso, c in sorted(params.items()):
        s = cm.run_country(iso, write=False)
        wl = cm.read_csv(cm.COUNTRIES / iso / "workloads_inputs.csv")
        countries[iso] = strip_private(country_data.build(c, nl, s, wl, nl_summary))

    totals = {
        "servers": sum(c["capacity"]["total_servers"] for c in countries.values()),
        "design_mw": round(sum(c["capacity"]["design_mw"] for c in countries.values()), 1),
        "sites": sum(c["capacity"]["sites"] for c in countries.values()),
        "capex_total": round(sum(c["capacity"]["capex_total"] for c in countries.values()), 1),
        "opex_total": round(sum(c["capacity"]["opex_total"] for c in countries.values()), 1),
    }

    return {
        "schema_version": SCHEMA_VERSION,
        "generated": gc.gen_date(),
        "provenance": (
            "Every figure is a scaled working assumption derived from the Dutch reference "
            "case, not a sourced forecast. Legal and regulatory entries were researched in "
            "September 2026 and will date. See /methodology."
        ),
        "assumptions": cm.read_csv(cm.ASSUMPTIONS),
        "phase_map": cm.read_csv(cm.PHASE_MAP),
        "countries": countries,
        "totals": totals,
    }


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("-o", "--out", type=Path, default=DEFAULT_OUT)
    args = p.parse_args(argv)

    bundle = build_bundle()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    # sort_keys so the bundle is byte-reproducible and diffs stay readable.
    args.out.write_text(json.dumps(bundle, indent=1, sort_keys=True, ensure_ascii=False), encoding="utf-8")

    size = args.out.stat().st_size
    print(f"{args.out}: {len(bundle['countries'])} countries, {size:,} bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
