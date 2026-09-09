#!/usr/bin/env python3
"""
Tracked-artefact integrity: the 27 posters and 27 briefing PDFs under countries/.

    python3 -m unittest discover -s tests -v

These are tracked deliverables (DECISIONS.md #24, #51), which makes them the one part of
the tree CI cannot regenerate: rendering them needs Chrome and a built web app, and the
runner has neither. So they can go stale silently -- and did: f03fde7 changed the bundle and
re-rendered the 27 posters but not the 27 PDFs, which then carried a provenance banner three
days out of date, with nothing complaining.

countries/ARTEFACTS.csv closes that gap by recording, for each artefact, the sha256 of
the JSON bundle it was rendered from. Comparing that against today's bundle needs no
browser, so it runs here.
"""
from __future__ import annotations

import csv
import hashlib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COUNTRIES = ROOT / "countries"
BUNDLE = ROOT / "web" / "public" / "data" / "eu27.json"
MANIFEST = COUNTRIES / "ARTEFACTS.csv"
REBUILD = "run `python3 model/export_artifacts.py` (needs Chrome and npm) and commit the result"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def expected_artefacts() -> list[Path]:
    out = []
    for d in sorted(COUNTRIES.iterdir()):
        if d.is_dir() and (d / "workloads_inputs.csv").exists():
            out += [d / f"{d.name}-infographic.png", d / f"{d.name}-briefing.pdf"]
    return out


class ArtefactsExist(unittest.TestCase):
    def test_every_country_has_both_artefacts(self):
        missing = [p.relative_to(ROOT).as_posix() for p in expected_artefacts() if not p.is_file()]
        self.assertEqual(missing, [], f"missing artefacts; {REBUILD}")


class Manifest(unittest.TestCase):
    def setUp(self):
        self.assertTrue(MANIFEST.is_file(), f"{MANIFEST.name} is missing; {REBUILD}")
        with MANIFEST.open(newline="", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            self.assertEqual(reader.fieldnames, ["path", "sha256", "bundle_sha256"])
            self.rows = list(reader)

    def test_manifest_lists_exactly_the_artefacts_on_disk(self):
        listed = [r["path"] for r in self.rows]
        self.assertEqual(listed, sorted(listed), "manifest is not sorted by path")
        self.assertEqual(
            listed,
            sorted(p.relative_to(ROOT).as_posix() for p in expected_artefacts()),
            f"manifest and countries/ disagree about which artefacts exist; {REBUILD}",
        )

    def test_no_artefact_has_been_modified_since_it_was_rendered(self):
        wrong = [r["path"] for r in self.rows if sha256_file(ROOT / r["path"]) != r["sha256"]]
        self.assertEqual(wrong, [], f"artefact does not match its recorded hash; {REBUILD}")

    def test_artefacts_were_rendered_from_the_current_bundle(self):
        """The staleness gate. A model or data change rewrites the bundle; until the
        artefacts are re-rendered they show the old numbers, and nothing on the page
        says so. Failing here is the intended cost of tracking binaries CI cannot build."""
        current = sha256_file(BUNDLE)
        stale = [r["path"] for r in self.rows if r["bundle_sha256"] != current]
        self.assertEqual(stale, [], f"{len(stale)} artefacts predate the current data; {REBUILD}")


class Reproducibility(unittest.TestCase):
    def test_pdfs_carry_the_pinned_build_date(self):
        """Chrome stamps wall-clock /CreationDate, which made every rebuild a diff.
        export_artifacts.pin_pdf_dates rewrites both date fields to .build-epoch (#34)."""
        import time

        epoch = int((ROOT / ".build-epoch").read_text().strip())
        expected = time.strftime("D:%Y%m%d%H%M%S+00'00'", time.gmtime(epoch)).encode("ascii")
        offenders = []
        for pdf in sorted(COUNTRIES.glob("*/*-briefing.pdf")):
            data = pdf.read_bytes()
            if data.count(b"/CreationDate (" + expected + b")") != 1:
                offenders.append(pdf.relative_to(ROOT).as_posix())
        self.assertEqual(offenders, [], f"PDF carries a wall-clock date; {REBUILD}")


if __name__ == "__main__":
    unittest.main()
