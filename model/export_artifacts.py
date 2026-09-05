#!/usr/bin/env python3
"""
Export per-country artefacts: a PNG infographic and a PDF briefing for each member state.

    python3 model/export_artifacts.py            # all 27, posters and reports
    python3 model/export_artifacts.py DE MT      # named countries only
    python3 model/export_artifacts.py --posters  # skip the PDFs

Builds the web app, serves the build, and drives headless Chrome over /poster/<ISO> and
/country/<ISO>. Everything rendered comes from web/public/data/eu27.json, which is
written from the same country_data.build() dict as the markdown briefs, so an artefact
cannot disagree with its brief.

Two things this has to get right, both learned the hard way:

  * The app renders client-side, so Chrome must be told to wait. Without
    --virtual-time-budget it captures a loading message, which is indistinguishable
    from a successful export until someone opens the file.
  * Another project in this workspace serves Vite's default preview port, so a
    non-strict bind silently produced screenshots of a completely different
    application. The port here is unusual and bound strictly.
"""
from __future__ import annotations

import argparse
import shutil
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WEB = ROOT / "web"
COUNTRIES = ROOT / "countries"
PORT = 4824  # deliberately not 4173; see module docstring

# Chrome on this machine lives at Chrome.app, not the conventional "Google Chrome.app".
BROWSERS = [
    "/Applications/Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium",
]

POSTER_W = 1024
# Chrome captures the window, not the document, so the height is measured per country
# from the rendered page rather than guessed: region counts vary from 2 to 5.
POSTER_H_FALLBACK = 1400


def find_browser() -> str:
    for b in BROWSERS:
        if Path(b).is_file():
            return b
    raise SystemExit(
        "No Chromium-family browser found. Install Chrome, or set one of:\n  "
        + "\n  ".join(BROWSERS)
    )


def port_free(port: int) -> bool:
    with socket.socket() as s:
        return s.connect_ex(("127.0.0.1", port)) != 0


def wait_for(url: str, timeout: float = 60.0) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=2):
                return
        except (urllib.error.URLError, OSError):
            time.sleep(0.3)
    raise SystemExit(f"preview server did not come up at {url}")


def measure_height(browser: str, url: str) -> int:
    """Render once and read the poster's actual height.

    Chrome's --screenshot captures the window, so a fixed height either clips a
    5-region country or leaves a 2-region one two-thirds blank. --dump-dom gives the
    rendered DOM, and the poster stamps its own height into a data attribute.
    """
    try:
        out = subprocess.run(
            [browser, "--headless", "--disable-gpu", "--no-sandbox",
             "--virtual-time-budget=15000", "--dump-dom", url],
            check=True, capture_output=True, text=True, timeout=90,
        ).stdout
        marker = 'data-poster-height="'
        if marker in out:
            return min(max(int(out.split(marker, 1)[1].split('"', 1)[0]), 600), 4000)
    except (subprocess.SubprocessError, ValueError, IndexError):
        pass
    return POSTER_H_FALLBACK


def run_chrome(browser: str, url: str, *flags: str) -> None:
    subprocess.run(
        [
            browser,
            "--headless",
            "--disable-gpu",
            "--no-sandbox",
            "--hide-scrollbars",
            # Client-side rendering: without this Chrome captures the loading state.
            "--virtual-time-budget=15000",
            *flags,
            url,
        ],
        check=True,
        capture_output=True,
    )


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("iso2", nargs="*", help="country codes; default is all")
    ap.add_argument("--posters", action="store_true", help="posters only, skip PDFs")
    ap.add_argument("--reports", action="store_true", help="PDFs only, skip posters")
    ap.add_argument("--skip-build", action="store_true", help="reuse an existing web/dist")
    args = ap.parse_args(argv)

    browser = find_browser()
    codes = [c.upper() for c in args.iso2] or sorted(
        d.name for d in COUNTRIES.iterdir() if d.is_dir() and (d / "workloads_inputs.csv").exists()
    )
    missing = [c for c in codes if not (COUNTRIES / c).is_dir()]
    if missing:
        raise SystemExit(f"no such country directory: {missing}")

    want_posters = not args.reports
    want_reports = not args.posters

    if not args.skip_build:
        print("building the app...")
        subprocess.run(["npm", "run", "build"], cwd=WEB, check=True, capture_output=True)

    if not port_free(PORT):
        raise SystemExit(f"port {PORT} is in use; stop whatever holds it and retry")

    print(f"serving web/dist on :{PORT}")
    server = subprocess.Popen(
        ["npm", "run", "preview", "--", "--port", str(PORT), "--strictPort"],
        cwd=WEB,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        wait_for(f"http://localhost:{PORT}/data/eu27.json")

        for i, iso in enumerate(codes, 1):
            cdir = COUNTRIES / iso
            print(f"  [{i:>2}/{len(codes)}] {iso}", end="", flush=True)

            if want_posters:
                out = cdir / f"{iso}-infographic.png"
                height = measure_height(browser, f"http://localhost:{PORT}/poster/{iso}")
                run_chrome(
                    browser,
                    f"http://localhost:{PORT}/poster/{iso}",
                    f"--window-size={POSTER_W},{height}",
                    f"--screenshot={out}",
                )
                print(f"  poster {POSTER_W}x{height} {out.stat().st_size // 1024} KB", end="")

            if want_reports:
                out = cdir / f"{iso}-briefing.pdf"
                run_chrome(
                    browser,
                    f"http://localhost:{PORT}/country/{iso}",
                    "--no-pdf-header-footer",
                    f"--print-to-pdf={out}",
                )
                print(f"  pdf {out.stat().st_size // 1024} KB", end="")

            print()
    finally:
        server.terminate()
        try:
            server.wait(timeout=10)
        except subprocess.TimeoutExpired:
            server.kill()

    print(f"\ndone: {len(codes)} countries")
    return 0


if __name__ == "__main__":
    if shutil.which("npm") is None:
        raise SystemExit("npm not found; run ./init.sh first")
    sys.exit(main())
