#!/usr/bin/env python3
"""
The verification ledger, model/sources.csv.

    python3 -m unittest discover -s tests -v

The ledger is the gate on everything public-facing (ROADMAP.md, DECISIONS.md #25), so
what it needs from a test is not "does it parse" but "is a row in it actually evidence":
a real country, a sourceable column, an absolute URL, a retrieval date, and a quote long
enough to show the cited page says what the cell claims.

COVERAGE_FLOOR is a ratchet. It may only be raised, and raising it is the commit that
records verification progress. The end state ROADMAP step 3 asks for -- CI failing on any
unsourced legal cell -- is `python3 model/sources.py --strict`; the floor is the honest
interim, because a check that fails on day one gets disabled on day two.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "model"))

import sources  # noqa: E402

# Raise as cells are verified. 189 = 7 sourceable columns x 27 member states.
COVERAGE_FLOOR = 0


class Ledger(unittest.TestCase):
    def setUp(self):
        self.rows = sources.load()  # raises if the header is not exactly FIELDS

    def test_every_row_is_usable_evidence(self):
        self.assertEqual(sources.validate(self.rows), [])

    def test_coverage_never_regresses(self):
        covered = sources.covered_cells(self.rows)
        self.assertGreaterEqual(
            covered,
            COVERAGE_FLOOR,
            f"coverage fell to {covered} from a floor of {COVERAGE_FLOOR}: a source row was "
            "removed. Sources are only ever added, or replaced by a better one.",
        )

    def test_the_floor_is_kept_current(self):
        covered = sources.covered_cells(self.rows)
        self.assertLessEqual(
            covered - COVERAGE_FLOOR,
            0,
            f"{covered} cells are sourced but COVERAGE_FLOOR is still {COVERAGE_FLOOR}. "
            "Raise it in this file so the progress cannot be undone silently.",
        )


class TieringIsWiredToTheData(unittest.TestCase):
    """The column lists are hand-maintained and sit next to a CSV that changes."""

    def test_every_named_column_exists_in_the_parameters(self):
        import csv

        with sources.PARAMETERS.open(newline="", encoding="utf-8") as fh:
            header = set(csv.DictReader(fh).fieldnames or [])
        named = set(sources.TIER1 + sources.TIER2 + sources.JUDGEMENT)
        self.assertEqual(named - header, set(), "sources.py names a column the dataset does not have")

    def test_tiers_do_not_overlap(self):
        self.assertEqual(set(sources.TIER1) & set(sources.TIER2), set())
        self.assertEqual(set(sources.REQUIRED) & set(sources.JUDGEMENT), set())

    def test_all_27_states_are_addressable(self):
        self.assertEqual(len(sources.countries()), 27)


if __name__ == "__main__":
    unittest.main()
