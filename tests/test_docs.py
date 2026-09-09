#!/usr/bin/env python3
"""
Documentation integrity: the decision register and the references into it.

    python3 -m unittest discover -s tests -v

`ROADMAP.md` names the pattern these tests exist to break: "a document asserts a rule,
the tree quietly stops matching it, and nothing complains", and concludes that the
countermeasure is a check that fails the build, not a more carefully written sentence.

The concrete failure being guarded here: DECISIONS.md carried two entries numbered 38,
two numbered 39, two numbered 40 and two numbered 41 for three days. `README.md` cited
"#41" meaning "no generated PDF is ever committed" while `ROADMAP.md` cited "#41" meaning
the domain choice, and both were right, which is the worst way for a reference to be
wrong. Renumbered to 47-50 on 2026-09-08; see #54.
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DECISIONS = ROOT / "DECISIONS.md"

HEADING = re.compile(r"^### (\d+)\. ", re.M)
# `#41` but not the `#898781` of a hex colour: one or two digits, then a non-word char.
REFERENCE = re.compile(r"(?<![\w#])#(\d{1,2})(?![0-9A-Za-z])")

# Files that cite decisions by number. Country briefs are generated and cite none.
CITING = ["README.md", "ROADMAP.md", "CHANGELOG.md", "ASSETS.md", "OUTREACH.md",
          "VERIFICATION.md", "DECISIONS.md", ".gitignore", "model/README.md", "book/README.md"]


def numbers() -> list[int]:
    return [int(n) for n in HEADING.findall(DECISIONS.read_text())]


class Register(unittest.TestCase):
    def test_numbers_are_unique(self):
        seen, dupes = set(), []
        for n in numbers():
            (dupes.append(n) if n in seen else None)
            seen.add(n)
        self.assertEqual(dupes, [], "two decisions share a number; every reference to it is ambiguous")

    def test_numbers_are_contiguous_from_one(self):
        ns = numbers()
        self.assertEqual(sorted(ns), list(range(1, len(ns) + 1)), "a decision number is missing or skipped")


class References(unittest.TestCase):
    def test_every_cited_decision_exists(self):
        known = set(numbers())
        dangling = []
        for name in CITING:
            f = ROOT / name
            if not f.is_file():
                continue
            for n in {int(m) for m in REFERENCE.findall(f.read_text())}:
                if n not in known:
                    dangling.append(f"{name} cites #{n}")
        self.assertEqual(dangling, [], "a document points at a decision that does not exist")


if __name__ == "__main__":
    unittest.main()
