#!/usr/bin/env python3
"""
Typeset the book.

    python3 book/build.py                  # the book -> build/book.pdf
    python3 book/build.py --briefs         # 27 standalone A4 briefs -> build/briefs/
    python3 book/build.py --briefs --iso DE
    python3 book/build.py --part 3         # one part, for fast proofing
    python3 book/build.py --typ-only       # emit .typ, skip the typst call

Reads web/public/data/eu27.json — the same country_data.build() dict the markdown
briefs and the web app render from (DECISIONS.md #6), so the book cannot drift from
the model. Nothing here recomputes a canonical figure.

Structure follows DECISIONS.md #27: Parts I, II and V are authored prose in
manuscript/; Parts III and IV are generated here and labelled as reference.

Standard library only, like the rest of the model.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

BOOK = Path(__file__).resolve().parent
ROOT = BOOK.parent
BUNDLE = ROOT / "web" / "public" / "data" / "eu27.json"
MANUSCRIPT = BOOK / "manuscript"
BUILD = BOOK / "build"

TITLE = "Sovereign Data Centers for European States"
SUBTITLE = "A capacity model for twenty-seven national government clouds"

# Authored parts, in order, with the generated parts slotted between them.
AUTHORED = {
    1: "part-1-argument.typ",
    2: "part-2-method.typ",
    5: "part-5-conclusion.typ",
}


# --------------------------------------------------------------------------- #
# Typst escaping
# --------------------------------------------------------------------------- #

_SPECIAL = re.compile(r"([#@$\\<>*_`~\[\]])")


def esc(value) -> str:
    """Escape a plain string for typst content mode."""
    return _SPECIAL.sub(r"\\\1", str(value))


def esc_md(value) -> str:
    """Escape, but keep markdown bold: **x** in the source becomes *x* in typst."""
    parts = re.split(r"\*\*(.+?)\*\*", str(value))
    out = []
    for i, part in enumerate(parts):
        out.append(f"*{esc(part)}*" if i % 2 else esc(part))
    return "".join(out)


def rel(path: Path) -> str:
    """Repo-relative path for logging, falling back to absolute for paths outside it."""
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def num(value, places: int = 0) -> str:
    """Thousands-separated number. CSV-sourced values arrive as strings."""
    return f"{float(value):,.{places}f}".replace(",", " ")


# --------------------------------------------------------------------------- #
# Part III — the gazetteer
# --------------------------------------------------------------------------- #

def stake_line(c: dict) -> str:
    """The one-line summary under a country's name, shared by book and brief."""
    cap, flags = c["capacity"], c["flags"]
    names = [n for n in ("frontline", "grid_isolated") if flags.get(n)]
    if flags.get("seismic") == "high":
        names.append("seismic")
    if flags.get("micro"):
        names.append("micro")
    return (
        f'{num(cap["design_mw"], 1)}#sym.space.thin MW design load #sym.dot.c '
        f'{cap["sites"]} sites #sym.dot.c EUR#sym.space.thin {num(cap["capex_total"])}#sym.space.thin m CAPEX '
        f'#sym.dot.c EUR#sym.space.thin {num(cap["opex_total"])}#sym.space.thin m/yr OPEX '
        f'#sym.dot.c flags: {esc(", ".join(n.replace("_", "-") for n in names) or "none")}'
    )


def country_entry(c: dict, standalone: bool = False) -> str:
    """One country, as a book chapter (standalone=False) or a whole brief (True).

    Standalone promotes every section heading by a level, because the brief's title
    block already carries the country name that the book puts in a `==` chapter head.
    """
    cap, params = c["capacity"], c["params"]
    h2 = "==" if standalone else "==="

    lines = []
    if not standalone:
        lines += [
            f'== {esc(c["name"])}',
            "",
            "#standfirst[",
            f"  {stake_line(c)}",
            "]",
            "",
        ]
    lines += [
        f"{h2} Capacity",
        "",
        "#datatable(",
        "  columns: (1fr, auto),",
        "  align: (left, right),",
        "  table.hline(stroke: 0.6pt),",
        "  [Metric], [Value],",
        "  table.hline(stroke: 0.3pt),",
    ]
    rows = [
        ("Total servers", num(cap["total_servers"])),
        ("Rack equivalents", num(cap["racks"])),
        ("IT load (MW)", num(cap["total_it_mw"], 1)),
        ("Facility design load (MW)", num(cap["design_mw"], 1)),
        ("Sites", str(cap["sites"])),
        ("Average MW per site", num(cap["avg_mw_per_site"], 2)),
        ("Total CAPEX (EUR m)", num(cap["capex_total"])),
        ("Annual OPEX (EUR m)", num(cap["opex_total"])),
        ("Electricity price (EUR/MWh)", num(params["elec_price_eur_mwh"], 1)),
    ]
    for label, value in rows:
        lines.append(f"  [{esc(label)}], [{value}],")
    lines += [
        "  table.hline(stroke: 0.6pt),",
        f'  caption: [Binding constraint: {esc(cap["binding_constraint"])}.],',
        ")",
        "",
        f"{h2} Proposed geography",
        "",
        "#datatable(",
        "  columns: (1.4fr, 1fr, auto),",
        "  align: (left, left, right),",
        "  table.hline(stroke: 0.6pt),",
        "  [Region], [Role], [MW],",
        "  table.hline(stroke: 0.3pt),",
    ]
    for r in c["regions"]:
        lines.append(
            f'  [{esc(r["Region"])}], [{esc(r["Role"])}], [{num(r["Design MW"], 2)}],'
        )
    lines += [
        "  table.hline(stroke: 0.6pt),",
        "  caption: [First-pass geographic hypothesis, not a site selection. See Part II.],",
        ")",
        "",
        f"{h2} What is structurally different",
        "",
    ]
    for d in c["structural_differences"]:
        lines.append(f"- {esc_md(d)}")
        lines.append("")

    lines += [f"{h2} Legal and institutional posture", ""]
    posture = [
        ("Legal instrument", params["legal_instrument"]),
        ("Sovereign cloud initiative", params["sovereign_cloud_initiative"]),
        ("Certification scheme", params["certification_scheme"]),
        ("Procurement vehicle", params["procurement_vehicle"]),
        ("Digital identity", params["digital_id"]),
        ("Internet exchange", params["ixp"]),
    ]
    lines += [
        "#datatable(",
        "  columns: (auto, 1fr),",
        "  align: (left, left),",
        "  table.hline(stroke: 0.6pt),",
        "  [Dimension], [Position],",
        "  table.hline(stroke: 0.3pt),",
    ]
    for label, value in posture:
        lines.append(f"  [{esc(label)}], [{esc(value)}],")
    lines += [
        "  table.hline(stroke: 0.6pt),",
        "  caption: [Researched September 2026. Legal entries are factual claims and will date.],",
        ")",
        "",
    ]
    return "\n".join(lines)


def gazetteer(bundle: dict) -> str:
    order = sorted(
        bundle["countries"].values(),
        key=lambda c: -c["capacity"]["design_mw"],
    )
    head = [
        "= Part III — The twenty-seven",
        "",
        "This part is *reference*, not argument. Each entry follows the same template and is",
        "generated from the model; the entries are meant to be consulted, not read through.",
        "The argument is in Parts I, II and V.",
        "",
        "Every figure is a scaled working assumption derived from the Dutch reference case in",
        "Part II. None of it is a sourced national forecast.",
        "",
    ]
    return "\n".join(head) + "\n" + "\n".join(country_entry(c) for c in order)


# --------------------------------------------------------------------------- #
# Part IV — cross-country reference tables
# --------------------------------------------------------------------------- #

def reference(bundle: dict) -> str:
    order = sorted(bundle["countries"].values(), key=lambda c: -c["capacity"]["design_mw"])
    t = bundle["totals"]

    lines = [
        "= Part IV — Reference tables",
        "",
        "== The model in one table",
        "",
        "#datatable(",
        "  columns: (auto, 1fr, auto, auto, auto, auto),",
        "  align: (left, left, right, right, right, right),",
        "  table.hline(stroke: 0.6pt),",
        "  [ISO], [Country], [Servers], [MW], [Sites], [CAPEX],",
        "  table.hline(stroke: 0.3pt),",
    ]
    for c in order:
        cap = c["capacity"]
        lines.append(
            f'  [{esc(c["iso2"])}], [{esc(c["name"])}], [{num(cap["total_servers"])}], '
            f'[{num(cap["design_mw"], 1)}], [{cap["sites"]}], [{num(cap["capex_total"])}],'
        )
    lines += [
        "  table.hline(stroke: 0.3pt),",
        f'  [], [*EU-27*], [*{num(t["servers"])}*], [*{num(t["design_mw"], 0)}*], '
        f'[*{t["sites"]}*], [*{num(t["capex_total"])}*],',
        "  table.hline(stroke: 0.6pt),",
        "  caption: [CAPEX in EUR millions. Generated "
        f'{esc(bundle["generated"])} from `model/eu27_results.csv`.],',
        ")",
        "",
        "== Shared assumptions",
        "",
        "#datatable(",
        "  columns: (1fr, auto),",
        "  align: (left, right),",
        "  table.hline(stroke: 0.6pt),",
    ]
    for row in bundle["assumptions"]:
        keys = list(row)
        label, value = row[keys[0]], row[keys[1]] if len(keys) > 1 else ""
        lines.append(f"  [{esc(label)}], [{esc(value)}],")
    lines += [
        "  table.hline(stroke: 0.6pt),",
        "  caption: [From `model/assumptions.csv` — the Dutch working assumptions.],",
        ")",
        "",
    ]
    return "\n".join(lines)


# --------------------------------------------------------------------------- #
# Standalone country briefs
# --------------------------------------------------------------------------- #

def brief_doc(c: dict, bundle: dict) -> str:
    """One country as a self-contained A4 document.

    Same renderer as the book's gazetteer entry (DECISIONS.md #6) — only the wrapper
    differs, so a brief and its chapter can never disagree.
    """
    return "\n".join([
        '#import "/templates/style.typ": brief, datatable, standfirst',
        "",
        "#show: brief.with(",
        f'  country: "{c["name"]}",',
        f'  iso: "{c["iso2"]}",',
        f"  standfirst: [{stake_line(c)}],",
        f'  generated: "{bundle["generated"]}",',
        f'  provenance: "Scaled working assumptions, not a sourced forecast. '
        f'sovereign-data-centers, generated {bundle["generated"]}",',
        ")",
        "",
        country_entry(c, standalone=True),
    ])


def build_briefs(bundle: dict, isos: list[str], out_dir: Path, compile_pdf: bool) -> int:
    src = BUILD / "briefs"
    src.mkdir(parents=True, exist_ok=True)
    out_dir.mkdir(parents=True, exist_ok=True)

    for iso in isos:
        c = bundle["countries"][iso]
        typ = src / f"{iso}.typ"
        typ.write_text(brief_doc(c, bundle), encoding="utf-8")
        if compile_pdf:
            subprocess.run(
                ["typst", "compile", "--root", str(BOOK), str(typ), str(out_dir / f"{iso}.pdf")],
                check=True,
            )

    if compile_pdf:
        total = sum((out_dir / f"{iso}.pdf").stat().st_size for iso in isos)
        print(f"{rel(out_dir)}: {len(isos)} briefs, {total:,} bytes")
    else:
        print(f"{rel(src)}: {len(isos)} .typ files")
    return 0


# --------------------------------------------------------------------------- #
# Assembly
# --------------------------------------------------------------------------- #

def assemble(bundle: dict, parts: list[int]) -> str:
    # Root-absolute: --root is book/, so this resolves from any output depth.
    rel = "/templates/style.typ"
    out = [
        f'#import "{rel}": book, datatable, standfirst',
        "",
        "#show: book.with(",
        f'  title: "{TITLE}",',
        f'  subtitle: "{SUBTITLE}",',
        f'  generated: "{bundle["generated"]}",',
        '  provenance: "Scaled working assumptions, not a sourced forecast. '
        'sovereign-data-centers, generated ' + bundle["generated"] + '",',
        ")",
        "",
        "#outline(title: [Contents], depth: 2, indent: 1em)",
        "",
    ]
    for n in parts:
        if n in AUTHORED:
            src = MANUSCRIPT / AUTHORED[n]
            if not src.exists():
                raise SystemExit(f"missing manuscript file: {src.relative_to(ROOT)}")
            out.append(src.read_text(encoding="utf-8"))
        elif n == 3:
            out.append(gazetteer(bundle))
        elif n == 4:
            out.append(reference(bundle))
        out.append("")
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    p.add_argument("--typ-only", action="store_true", help="emit .typ without compiling")
    p.add_argument("--part", type=int, action="append", choices=[1, 2, 3, 4, 5],
                   help="compile only these parts (repeatable)")
    p.add_argument("--briefs", action="store_true",
                   help="build standalone per-country PDFs instead of the book")
    p.add_argument("--iso", action="append", help="limit --briefs to these countries")
    p.add_argument("-o", "--out", type=Path, help="output path (default depends on mode)")
    args = p.parse_args(argv)

    if not BUNDLE.exists():
        raise SystemExit(
            f"missing {BUNDLE.relative_to(ROOT)} — run ./run.sh data first"
        )
    bundle = json.loads(BUNDLE.read_text(encoding="utf-8"))

    if args.briefs:
        known = bundle["countries"]
        isos = [i.upper() for i in args.iso] if args.iso else sorted(known)
        unknown = [i for i in isos if i not in known]
        if unknown:
            raise SystemExit(f"unknown country code(s): {', '.join(unknown)}")
        out_dir = args.out.resolve() if args.out else (BUILD / "briefs")
        return build_briefs(bundle, isos, out_dir, compile_pdf=not args.typ_only)

    if args.iso:
        raise SystemExit("--iso only applies with --briefs")

    parts = sorted(set(args.part)) if args.part else [1, 2, 3, 4, 5]
    BUILD.mkdir(exist_ok=True)
    typ = BUILD / "book.typ"
    typ.write_text(assemble(bundle, parts), encoding="utf-8")
    print(f"{rel(typ)}: parts {', '.join(map(str, parts))}")

    if args.typ_only:
        return 0
    if not shutil.which("typst"):
        raise SystemExit("typst is not installed. Install with: brew install typst")

    # --root so the generated .typ under build/ can import ../templates/style.typ.
    out = args.out.resolve() if args.out else (BUILD / "book.pdf")
    subprocess.run(
        ["typst", "compile", "--root", str(BOOK), str(typ), str(out)], check=True
    )
    print(f"{rel(out)}: {out.stat().st_size:,} bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
