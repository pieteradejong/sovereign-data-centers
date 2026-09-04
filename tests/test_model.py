#!/usr/bin/env python3
"""
Model and data-integrity tests.

    python3 -m unittest discover -s tests -v

Stdlib unittest, no pytest, consistent with the project's stdlib-only rule.

These exist because 27 generated documents, a JSON bundle and five CSVs per country all
derive from one small pile of arithmetic, so a silent change is invisible until someone
reads a wrong number in print.
"""
from __future__ import annotations

import csv
import hashlib
import os
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "model"))

import capacity_model as cm  # noqa: E402
import country_data  # noqa: E402
import generate_countries as gc  # noqa: E402

PINNED_EPOCH = "1788393600"  # 2026-09-03, so generated output is reproducible


def params() -> dict[str, dict]:
    return {r["iso2"]: r for r in cm.read_csv(gc.PARAMS)}


class DocumentedInvariants(unittest.TestCase):
    """README states the model reproduces the Dutch spreadsheet exactly. A documented
    claim nobody checks is a claim that quietly stops being true."""

    def test_nl_reproduces_the_spreadsheet(self):
        s = cm.run_country("NL", write=False)
        self.assertEqual(s.total_servers, 5691)
        self.assertAlmostEqual(s.design_mw, 14.2, places=1)
        self.assertAlmostEqual(s.capex_total, 339.0, places=0)


class GoldenFile(unittest.TestCase):
    """model/eu27_results.csv is the committed expected output."""

    def test_all_countries_match_committed_results(self):
        expected = {r["iso2"]: r for r in cm.read_csv(ROOT / "model" / "eu27_results.csv")}
        self.assertEqual(len(expected), 27)
        for iso in sorted(expected):
            with self.subTest(iso=iso):
                got = cm.result_row(cm.run_country(iso, write=False))
                for key, want in expected[iso].items():
                    self.assertEqual(
                        str(got[key]), want,
                        f"{iso}.{key}: model gives {got[key]!r}, committed file says {want!r}",
                    )


class Conservation(unittest.TestCase):
    def test_phase_capex_sums_to_total(self):
        for iso in sorted(params()):
            with self.subTest(iso=iso):
                s = cm.run_country(iso, write=False)
                total = sum(p["CAPEX (EUR mm)"] for p in s.phases)
                # Phase rows are rounded to 0.1, so allow drift of half a unit per phase.
                self.assertAlmostEqual(total, s.capex_total, delta=0.05 * len(s.phases))

    def test_region_shares_sum_to_one(self):
        for iso in sorted(params()):
            with self.subTest(iso=iso):
                s = cm.run_country(iso, write=False)
                if s.regions:
                    total = sum(r["Share of design load"] for r in s.regions)
                    self.assertAlmostEqual(total, 1.0, places=6)

    def test_site_count_respects_both_floors(self):
        p = params()
        for iso in sorted(p):
            with self.subTest(iso=iso):
                s = cm.run_country(iso, write=False)
                self.assertGreaterEqual(s.sites, s.sites_by_mw)
                self.assertGreaterEqual(s.sites, int(p[iso]["min_sites"]))


class CsvIntegrity(unittest.TestCase):
    """The IT/ES bug: unquoted commas shifted every later field, silently corrupting
    the generated threat notes. csv.DictReader signals it with a None key."""

    def all_csvs(self):
        return sorted(ROOT.glob("model/*.csv")) + sorted(ROOT.glob("countries/*/*.csv"))

    def test_no_row_has_stray_fields(self):
        for path in self.all_csvs():
            with self.subTest(csv=str(path.relative_to(ROOT))):
                with path.open(newline="", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    width = len(reader.fieldnames or [])
                    for i, row in enumerate(reader, start=2):
                        self.assertNotIn(
                            None, row,
                            f"line {i} has more fields than the {width}-column header "
                            "(usually an unquoted comma)",
                        )
                        self.assertFalse(
                            any(v is None for v in row.values()),
                            f"line {i} has fewer fields than the header",
                        )

    def test_enum_columns(self):
        allowed = {
            "seismic": {"low", "moderate", "high"},
            "gov_cloud_maturity": {"none", "pilot", "operational", "federated"},
            "certification_strength": {"baseline", "national", "stringent"},
            "hyperscaler_dependency": {"low", "medium", "high", "critical"},
            "frontline": {"0", "1"},
            "grid_isolated": {"0", "1"},
        }
        for r in cm.read_csv(gc.PARAMS):
            for col, ok in allowed.items():
                with self.subTest(iso=r["iso2"], column=col):
                    self.assertIn(r[col], ok)

    def test_numeric_ranges(self):
        bounds = {
            "population_m": (0.1, 100.0),
            "gdp_eur_bn": (1.0, 6000.0),
            "elec_price_eur_mwh": (50.0, 400.0),
            "renewables_pct": (0.0, 100.0),
            "min_sites": (1, 8),
            "hyperscaler_regions_live": (0, 20),
        }
        for r in cm.read_csv(gc.PARAMS):
            for col, (lo, hi) in bounds.items():
                with self.subTest(iso=r["iso2"], column=col):
                    self.assertTrue(lo <= float(r[col]) <= hi, f"{r[col]} outside [{lo}, {hi}]")


class ReferentialIntegrity(unittest.TestCase):
    def test_every_workload_class_has_a_phase(self):
        phases = cm.load_phase_map()
        for iso in sorted(params()):
            with self.subTest(iso=iso):
                classes = {r["Class"] for r in cm.read_csv(cm.COUNTRIES / iso / "workloads_inputs.csv")}
                self.assertTrue(classes <= phases.keys(), f"unmapped: {sorted(classes - phases.keys())}")

    def test_scaling_rules_match_the_nl_baseline(self):
        """A renamed workload in one file and not the other raises a bare KeyError deep
        inside the generator; catch it here with a readable message instead."""
        rules = {r["Workload"] for r in cm.read_csv(gc.RULES)}
        baseline = {r["Workload"] for r in cm.read_csv(cm.COUNTRIES / "NL" / "workloads_inputs.csv")}
        self.assertEqual(rules, baseline)

    def test_every_country_has_regions_and_a_directory(self):
        for iso in sorted(params()):
            with self.subTest(iso=iso):
                self.assertTrue((cm.COUNTRIES / iso).is_dir())
                if iso != gc.BASELINE:
                    self.assertIn(iso, gc.REGIONS)


class MatrixScoring(unittest.TestCase):
    def test_scores_are_normalised(self):
        p, nl = params(), None
        nl = p[gc.BASELINE]
        nl_s = cm.run_country(gc.BASELINE, write=False)
        for iso in sorted(p):
            s = cm.run_country(iso, write=False)
            wl = cm.read_csv(cm.COUNTRIES / iso / "workloads_inputs.csv")
            d = country_data.build(p[iso], nl, s, wl, nl_s)
            for dim, cell in d["matrix"].items():
                with self.subTest(iso=iso, dimension=dim):
                    self.assertTrue(0.0 <= cell["score"] <= 1.0)
                    self.assertTrue(cell["source"], "every score needs its source text")

    def test_matrix_discriminates(self):
        """Guards against a matrix that has stopped telling countries apart.

        The check is per-column variance and overall spread, NOT whether a leader tops
        out. France currently scores 1.00 on all eight dimensions and Germany on seven;
        that is a genuine finding (France does lead the EU on sovereign-cloud doctrine),
        not a defect. What would be a defect is a dimension that scores every country
        the same, or a distribution so flat that ranking is noise.
        """
        p = params()
        nl, nl_s = p[gc.BASELINE], cm.run_country(gc.BASELINE, write=False)
        rows = {}
        for iso in sorted(p):
            s = cm.run_country(iso, write=False)
            wl = cm.read_csv(cm.COUNTRIES / iso / "workloads_inputs.csv")
            rows[iso] = country_data.build(p[iso], nl, s, wl, nl_s)["matrix"]

        for dim in next(iter(rows.values())):
            with self.subTest(dimension=dim):
                distinct = {rows[iso][dim]["score"] for iso in rows}
                self.assertGreater(len(distinct), 1, f"{dim} scores every country identically")

        totals = [sum(c["score"] for c in m.values()) for m in rows.values()]
        self.assertGreater(
            max(totals) - min(totals), 2.0,
            "total scores are too tightly clustered for the ranking to mean anything",
        )


class GeneratorDeterminism(unittest.TestCase):
    def test_regeneration_is_a_no_op(self):
        """With the date pinned, running the generator twice must change nothing."""
        env = {**os.environ, "SOURCE_DATE_EPOCH": PINNED_EPOCH}

        def fingerprint():
            h = hashlib.sha256()
            for f in sorted(ROOT.glob("countries/*/GOAL.md")):
                h.update(f.read_bytes())
            h.update((ROOT / "countries" / "SUMMARY.md").read_bytes())
            return h.hexdigest()

        run = lambda: subprocess.run(  # noqa: E731
            [sys.executable, str(ROOT / "model" / "generate_countries.py")],
            cwd=ROOT, env=env, capture_output=True, check=True,
        )
        run()
        before = fingerprint()
        run()
        self.assertEqual(before, fingerprint(), "generator is not byte-reproducible")

    def test_nl_narrative_is_never_regenerated(self):
        """countries/NL/GOAL.md is the hand-written source the whole model derives from."""
        nl_goal = cm.COUNTRIES / "NL" / "GOAL.md"
        before = nl_goal.read_bytes()
        subprocess.run(
            [sys.executable, str(ROOT / "model" / "generate_countries.py")],
            cwd=ROOT, env={**os.environ, "SOURCE_DATE_EPOCH": PINNED_EPOCH},
            capture_output=True, check=True,
        )
        self.assertEqual(before, nl_goal.read_bytes())


if __name__ == "__main__":
    unittest.main()
