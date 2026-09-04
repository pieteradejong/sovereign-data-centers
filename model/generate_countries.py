#!/usr/bin/env python3
"""
Generate per-country input files and a first-pass write-up for every EU-27 member
from the Dutch reference case, then run the capacity model on each.

Reads:
    model/eu27_parameters.csv            country dataset (population, GDP, power price, flags, ...)
    model/scaling_rules.csv              how each workload class scales from the NL baseline
    countries/NL/workloads_inputs.csv    the baseline workload table

Writes, for each country except NL (NL's hand-made inputs are the baseline and are left alone):
    countries/<ISO>/params.csv                    assumption overrides (electricity price, minimum sites)
    countries/<ISO>/workloads_inputs.csv          scaled workload table
    countries/<ISO>/region_allocation_inputs.csv  proposed regions and load shares
    countries/<ISO>/GOAL.md                       write-up (regenerated every run - edit scaling_rules.csv
                                                  or eu27_parameters.csv rather than the .md, or rename
                                                  the file to keep hand edits)
and for NL only params.csv, so the cross-country comparison uses the same price source.

Then runs capacity_model.py --all, and writes countries/SUMMARY.md.

Every number produced here is a scaled placeholder, exactly like the Dutch
"working assumption" rows. The point is a consistent, editable starting grid,
not a forecast.
"""
from __future__ import annotations

import csv
import math
import os
import sys
from datetime import date, datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import capacity_model as cm  # noqa: E402
import country_data  # noqa: E402

ROOT = cm.ROOT
COUNTRIES = cm.COUNTRIES
PARAMS = ROOT / "model" / "eu27_parameters.csv"
RULES = ROOT / "model" / "scaling_rules.csv"
BASELINE = "NL"


def gen_date() -> str:
    """The date stamped into generated files.

    Overridable via SOURCE_DATE_EPOCH (the reproducible-builds convention) so the
    generator is byte-reproducible: re-running on a different day must not produce a
    27-file diff, and tests can pin it to assert the generator is a true no-op.
    """
    epoch = os.environ.get("SOURCE_DATE_EPOCH")
    if epoch:
        return datetime.fromtimestamp(int(epoch), tz=timezone.utc).date().isoformat()
    return date.today().isoformat()

# ---------------------------------------------------------------------------
# Proposed regions per country: (name, role, resilience, note).
# Order = primary first. The reserve row is added automatically for min_sites >= 3.
# These are first-pass geographic hypotheses to be replaced by the site-scoring
# workstream (GOAL.md section 19.A); they encode only the obvious constraints
# (capital region, second metro, separation from the frontier / fault / flood zone).
# ---------------------------------------------------------------------------
REGIONS: dict[str, list[tuple[str, str, str, str]]] = {
    "AT": [
        ("East / Vienna - Lower Austria", "Primary civil cloud", "Active-active", "VIX connectivity, federal ministries, BRZ estate; Danube flood zoning applies."),
        ("Upper Austria / Linz", "Sovereign secondary", "Active-active", "Industrial grid, hydro power, 180 km from Vienna."),
        ("Styria / Graz", "Government / continuity", "Active-active", "Southern separation, research campus (TU Graz)."),
        ("Tyrol - Salzburg / West", "Strategic reserve", "Warm reserve", "Alpine hydro; expansion or hardened reserve."),
    ],
    "BE": [
        ("Brussels - Flemish Brabant", "Primary civil cloud", "Active-active", "Federal institutions, BNIX, Smals/G-Cloud estate; Elia connection queue is the constraint."),
        ("Wallonia / Mons - Charleroi", "Sovereign secondary", "Active-active", "Existing hyperscale cluster (St. Ghislain) proves power and fibre; south of Meuse flood zone."),
        ("Antwerp - Limburg", "Government / continuity", "Active-active", "Northern separation, port/industrial grid."),
        ("Liege - Ardennes", "Strategic reserve", "Warm reserve", "Eastern reserve; avoid 2021 Vesdre/Ourthe flood plains."),
    ],
    "BG": [
        ("Sofia", "Primary civil cloud", "Active-active", "SHPC estate, BIX/NetIX, EuroHPC Discoverer; seismic design required."),
        ("Plovdiv", "Sovereign secondary", "Active-active", "Second metro, 150 km separation, Maritsa industrial grid."),
        ("North-central / Veliko Tarnovo - Pleven", "Government / continuity", "Active-active", "Inland, away from the Black Sea frontier and Vrancea influence."),
        ("Varna", "Strategic reserve", "Warm reserve", "Cable landings, but Black Sea exposure - reserve/edge only."),
    ],
    "HR": [
        ("Zagreb", "Primary civil cloud", "Active-active", "CDU estate, CIX; 2020 earthquake makes seismic isolation mandatory."),
        ("Osijek / Slavonia", "Sovereign secondary", "Active-active", "Flat land, lower seismicity; Sava/Drava flood zoning applies."),
        ("Split / Dalmatia", "Government / continuity", "Active-active", "Coastal separation, Adriatic cable access; karst siting constraints."),
        ("Rijeka - Istria", "Strategic reserve", "Warm reserve", "Krk LNG and port grid; reserve/expansion."),
    ],
    "CY": [
        ("Nicosia", "Primary civil cloud", "Active-active", "Government DC and CyIX; inland, away from cable landings."),
        ("Limassol - Paphos", "Sovereign secondary", "Active-active", "East-Med cable landings; 80 km separation is the island maximum."),
    ],
    "CZ": [
        ("Prague - Central Bohemia", "Primary civil cloud", "Active-active", "SPCSS/NAKIT estate, NIX.CZ; Vltava flood zoning applies."),
        ("Brno / South Moravia", "Sovereign secondary", "Active-active", "Second metro, research cluster, 200 km separation."),
        ("Ostrava / Moravia-Silesia", "Government / continuity", "Active-active", "Industrial grid; post-coal land availability."),
        ("Plzen / West Bohemia", "Strategic reserve", "Warm reserve", "Western reserve, furthest from the eastern frontier."),
    ],
    "DK": [
        ("Copenhagen / Zealand", "Primary civil cloud", "Active-active", "Statens It estate, DIX/Netnod; Zealand grid queue and storm-surge zoning."),
        ("Jutland / Fredericia - Aarhus", "Sovereign secondary", "Active-active", "Wind surplus, existing hyperscale campuses, Atlantic cable landings."),
        ("Funen / Odense", "Government / continuity", "Active-active", "Central, separated from both metros."),
        ("North Jutland", "Strategic reserve", "Warm reserve", "Cheapest power, reserve/expansion."),
    ],
    "EE": [
        ("Tallinn", "Primary civil cloud", "Active-active", "RIT Riigipilv estate, TLLIX, EESF cables to Finland."),
        ("Tartu", "Sovereign secondary", "Active-active", "University city, 180 km separation; 60 km from the Russian border - hardened design."),
        ("Parnu / West", "Government / continuity", "Active-active", "Furthest from the eastern frontier; Estonia-Sweden cable."),
        ("Out-of-country reserve (Data Embassy)", "Strategic reserve", "Warm reserve", "Existing Luxembourg Data Embassy pattern - national-only model cannot close this gap."),
    ],
    "FI": [
        ("Helsinki - Uusimaa", "Primary civil cloud", "Active-active", "Valtori estate, FICIX, C-Lion1 landing; 30 min from Tallinn."),
        ("Tampere - Pirkanmaa", "Sovereign secondary", "Active-active", "Inland, 180 km separation, strong grid."),
        ("Oulu / North", "Government / continuity", "Active-active", "Cheapest power, free cooling, far from the frontier; adds ~10 ms."),
        ("Kajaani - Kuopio", "Strategic reserve", "Warm reserve", "LUMI (Kajaani) proves power and cooling for large loads."),
    ],
    "FR": [
        ("Ile-de-France", "Primary civil cloud", "Active-active", "DINUM/ministry estate, France-IX; RTE saturation - use designated turnkey sites."),
        ("Auvergne-Rhone-Alpes / Lyon", "Sovereign secondary", "Active-active", "Second metro, nuclear/hydro grid, Alpine seismic zoning."),
        ("Sud-Ouest / Toulouse - Bordeaux", "Defense / industrial", "Active-active", "Defense-aerospace cluster, Atlantic cable landings (Amitie)."),
        ("Ouest / Rennes - Nantes", "Government / continuity", "Active-active", "DGA cyber cluster (Rennes), Brittany cable landings."),
        ("Grand Est - Hauts-de-France", "Strategic reserve", "Warm reserve", "Nuclear grid headroom; reserve/expansion."),
    ],
    "DE": [
        ("Frankfurt - Rhine-Main", "Primary civil cloud", "Active-active", "DE-CIX, ITZBund estate; grid saturated - expect multi-year connection lead time."),
        ("Berlin - Brandenburg", "Sovereign secondary", "Active-active", "Federal ministries, AWS ESC and STACKIT prove grid headroom in the east."),
        ("Munich / Bavaria", "Defense / industrial", "Active-active", "Defense-industrial cluster, Bundeswehr IT; southern separation."),
        ("Hamburg / North", "Government / continuity", "Active-active", "Wind surplus, North Sea cable landings (Norden/Sylt)."),
        ("Leipzig - Saxony", "Strategic reserve", "Warm reserve", "Post-coal land and grid; reserve/expansion."),
    ],
    "EL": [
        ("Attica / Athens", "Primary civil cloud", "Active-active", "GSIS G-Cloud, GR-IX, Microsoft Spata campus; seismic design mandatory."),
        ("Thessaloniki / Central Macedonia", "Sovereign secondary", "Active-active", "Second metro, 300 km separation, Balkan transit."),
        ("Western Greece / Patras", "Government / continuity", "Active-active", "Adriatic cable routes; separate seismic domain."),
        ("Crete / Chania", "Strategic reserve", "Warm reserve", "East-Med cable hub and Great Sea Interconnector; island - reserve/edge only."),
    ],
    "HU": [
        ("Budapest", "Primary civil cloud", "Active-active", "NISZ KAK estate, BIX; Danube flood zoning applies."),
        ("Debrecen / East", "Sovereign secondary", "Active-active", "Industrial grid growth; 130 km from the Ukrainian border - hardened design."),
        ("Szeged - Pecs / South", "Government / continuity", "Active-active", "Solar belt, southern separation."),
        ("Gyor / West", "Strategic reserve", "Warm reserve", "Closest to Vienna/Bratislava transit; reserve."),
    ],
    "IE": [
        ("Dublin", "Primary civil cloud", "Active-active", "OGCIO/Backweston estate, INEX; EirGrid connection moratorium to ~2028 is binding."),
        ("Cork", "Sovereign secondary", "Active-active", "Atlantic cable landings (Kinsale, Amitie), Celtic Interconnector."),
        ("Galway - Limerick / West", "Government / continuity", "Active-active", "Wind surplus, AEC-1 landing (Killala)."),
        ("Midlands / Athlone", "Strategic reserve", "Warm reserve", "Post-peat land and grid; reserve/expansion."),
    ],
    "IT": [
        ("Milan / Lombardy", "Primary civil cloud", "Active-active", "PSN pair, MIX, all four hyperscaler regions nearby; Po flood zoning."),
        ("Rome / Lazio", "Sovereign secondary", "Active-active", "Ministries, Sogei, NAMEX; Apennine seismic zoning."),
        ("Turin / Piedmont", "Government / continuity", "Active-active", "Alpine hydro, TOP-IX; lower seismicity."),
        ("Puglia / Bari", "Defense / industrial", "Active-active", "Southern separation, Adriatic cable landings; renewables belt."),
        ("Emilia / Bologna", "Strategic reserve", "Warm reserve", "EuroHPC Leonardo campus (Tecnopolo); reserve - 2023 flood plains excluded."),
    ],
    "LV": [
        ("Riga", "Primary civil cloud", "Active-active", "LVRTC LVDC estate, LIX; Daugava flood zoning."),
        ("Ventspils / Kurzeme", "Sovereign secondary", "Active-active", "Latvia-Sweden cable landing; furthest from the eastern frontier."),
        ("Valmiera / Vidzeme", "Government / continuity", "Active-active", "Inland separation; Estonia transit."),
        ("Out-of-country reserve", "Strategic reserve", "Warm reserve", "Follow the Estonian Data Embassy pattern - national-only model cannot close this gap."),
    ],
    "LT": [
        ("Vilnius", "Primary civil cloud", "Active-active", "KVTC state DCs, LIXP; 30 km from Belarus - hardened design mandatory."),
        ("Kaunas", "Sovereign secondary", "Active-active", "Second metro, 100 km separation, KV Baltic campus."),
        ("Klaipeda", "Government / continuity", "Active-active", "LNG terminal, NordBalt fibre to Sweden; furthest from Belarus."),
        ("Out-of-country reserve", "Strategic reserve", "Warm reserve", "Follow the Estonian Data Embassy pattern - national-only model cannot close this gap."),
    ],
    "LU": [
        ("Luxembourg City - Bettembourg", "Primary civil cloud", "Active-active", "CTIE and LuxConnect Tier IV estate, LU-CIX."),
        ("Bissen / North", "Sovereign secondary", "Active-active", "30 km separation is the national maximum; Google Bissen site proves grid."),
    ],
    "MT": [
        ("Malta / Marsa - Santa Venera", "Primary civil cloud", "Active-active", "MITA estate; Sicily cable landings."),
        ("Gozo", "Sovereign secondary", "Active-active", "Only physical separation available (~30 km); shares the Sicily power/data corridor."),
    ],
    "PL": [
        ("Warsaw / Mazovia", "Primary civil cloud", "Active-active", "COI/NASK RChO estate, PLIX, both hyperscaler regions."),
        ("Poznan / Greater Poland", "Sovereign secondary", "Active-active", "Western separation, Beyond.pl campus, German transit."),
        ("Krakow / Lesser Poland", "Defense / industrial", "Active-active", "Southern separation, CloudFerro/AI factory ecosystem."),
        ("Gdansk / Pomerania", "Government / continuity", "Active-active", "Baltic cable access, planned nuclear grid; Kaliningrad proximity - hardened."),
        ("Lodz - Wroclaw", "Strategic reserve", "Warm reserve", "Central/SW reserve; 2024 Oder flood plains excluded."),
    ],
    "PT": [
        ("Lisbon", "Primary civil cloud", "Active-active", "AMA/eSPap estate, GigaPIX; seismic/tsunami design mandatory."),
        ("Sines / Alentejo", "Sovereign secondary", "Active-active", "Atlantic cable hub, Start Campus proves 1 GW-class grid; renewables."),
        ("Porto / North", "Government / continuity", "Active-active", "300 km separation, lower seismicity, Douro hydro."),
        ("Coimbra / Centre", "Strategic reserve", "Warm reserve", "Inland reserve between the two metros."),
    ],
    "RO": [
        ("Bucharest", "Primary civil cloud", "Active-active", "STS government cloud, InterLAN/RoNIX; highest-seismic-risk EU capital - base isolation required."),
        ("Cluj / Transylvania", "Sovereign secondary", "Active-active", "IT cluster, outside the Vrancea zone, 400 km separation."),
        ("Timisoara / Banat", "Government / continuity", "Active-active", "Western separation, Hungarian transit, low seismicity."),
        ("Brasov - Sibiu", "Defense / industrial", "Active-active", "Existing STS regional DCs; mountain sites - verify Vrancea distance."),
        ("Craiova / Oltenia", "Strategic reserve", "Warm reserve", "ClusterPower campus; away from the Ukraine/Moldova frontier."),
    ],
    "SK": [
        ("Bratislava", "Primary civil cloud", "Active-active", "MoI Kopcianska and MoF DataCentrum, SIX; Danube flood zoning."),
        ("Banska Bystrica / Centre", "Sovereign secondary", "Active-active", "MoF Tajov backup site; 200 km separation, cheap land."),
        ("Kosice / East", "Government / continuity", "Active-active", "Eastern metro; 80 km from Ukraine - hardened design."),
        ("Zilina / North", "Strategic reserve", "Warm reserve", "Hydro grid, Czech/Polish transit; reserve."),
    ],
    "SI": [
        ("Ljubljana", "Primary civil cloud", "Active-active", "DRO national DC, SIX; Ljubljana basin seismic zoning."),
        ("Maribor / Styria", "Sovereign secondary", "Active-active", "EuroHPC Vega campus, 120 km separation, Drava hydro."),
        ("Koper - Nova Gorica / West", "Government / continuity", "Active-active", "Italian transit and port grid; 2023 flood plains excluded."),
        ("Celje / Savinja", "Strategic reserve", "Warm reserve", "Central reserve; flood-plain siting must be excluded."),
    ],
    "ES": [
        ("Madrid", "Primary civil cloud", "Active-active", "SGAD/AEAT/GISS estate, DE-CIX Madrid/ESpanix, two hyperscaler regions; connection queues."),
        ("Aragon / Zaragoza", "Sovereign secondary", "Active-active", "AWS/Microsoft campuses prove grid; renewables, 300 km separation."),
        ("Catalonia / Barcelona", "Government / continuity", "Active-active", "Mediterranean cable landings (2Africa, Medusa), CATNIX."),
        ("Andalusia / Seville - Malaga", "Defense / industrial", "Active-active", "Southern separation, solar belt; water-stress cooling design."),
        ("Castilla y Leon - Galicia", "Strategic reserve", "Warm reserve", "Wind/hydro surplus, Bilbao Atlantic landings nearby; reserve."),
    ],
    "SE": [
        ("Stockholm - Malardalen", "Primary civil cloud", "Active-active", "State IT providers, Netnod, all three hyperscaler regions; SE3 grid constraints."),
        ("Gavle - Sandviken", "Sovereign secondary", "Active-active", "Azure campus proves grid; SE2 surplus power."),
        ("Lulea - Boden / North", "Government / continuity", "Active-active", "SE1 cheapest power, free cooling, Meta campus; adds ~15 ms."),
        ("Gothenburg / West", "Defense / industrial", "Active-active", "Naval/defense cluster, North Sea routing away from the Baltic."),
    ],
}

# Load shares by number of active regions (reserve added when min_sites >= 3).
SHARES = {2: [0.55, 0.45], 3: [0.35, 0.30, 0.25], 4: [0.30, 0.20, 0.20, 0.20]}
RESERVE_SHARE = 0.10


def load_rules() -> dict[str, dict]:
    rules = {}
    for r in cm.read_csv(RULES):
        rules[r["Workload"]] = {
            "w_pop": float(r["Population weight"]),
            "w_gov": float(r["Gov employment weight"]),
            "w_gdp": float(r["GDP weight"]),
            "floor": float(r["Small-country floor"]),
            "frontline_x": float(r["Frontline multiplier"]),
            "rationale": r["Rationale"],
        }
    return rules


def round_to(x: float, step: float) -> float:
    return max(step, round(x / step) * step)


def scale_workloads(base_rows: list[dict], c: dict, nl: dict, rules: dict) -> list[dict]:
    pop = float(c["population_m"]) / float(nl["population_m"])
    gov = float(c["gov_employment_k"]) / float(nl["gov_employment_k"])
    gdp = float(c["gdp_eur_bn"]) / float(nl["gdp_eur_bn"])
    frontline = int(c["frontline"]) == 1
    out = []
    for row in base_rows:
        rule = rules[row["Workload"]]
        k = rule["w_pop"] * pop + rule["w_gov"] * gov + rule["w_gdp"] * gdp
        k = max(k, rule["floor"])
        if frontline:
            k *= rule["frontline_x"]
        new = dict(row)
        new["Workload"] = row["Workload"].replace("DigiD", c["digital_id"].split("/")[0].split("(")[0].strip())
        new["CPU cores required"] = int(round_to(float(row["CPU cores required"]) * k, 100))
        g = float(row["GPU eq. required"]) * k
        new["GPU eq. required"] = int(round_to(g, 8)) if g > 0 else 0
        new["Logical storage (PB)"] = round(max(0.5, float(row["Logical storage (PB)"]) * k), 1)
        new["Notes"] = f"Scaled from NL baseline x{k:.2f} ({rule['rationale']})."
        out.append(new)
    return out


def region_rows(iso2: str, min_sites: int) -> list[dict]:
    regs = REGIONS[iso2]
    if min_sites <= 2:
        active, reserve = regs[:2], []
    else:
        n_active = min(len(regs) - 1, 4)
        active, reserve = regs[:n_active], regs[n_active:n_active + 1]
    shares = SHARES[len(active)]
    if reserve:
        shares = [round(s * (1 - RESERVE_SHARE), 3) for s in shares]
    rows = []
    for (name, role, res, note), share in zip(active, shares):
        rows.append({"Region": name, "Role": role, "Share of design load": share, "Resilience role": res, "Notes": note})
    for name, role, res, note in reserve:
        rows.append({"Region": name, "Role": role, "Share of design load": RESERVE_SHARE, "Resilience role": res, "Notes": note})
    total = sum(r["Share of design load"] for r in rows)
    rows[0]["Share of design load"] = round(rows[0]["Share of design load"] + (1 - total), 3)
    return rows


def params_rows(c: dict) -> list[dict]:
    return [
        {"Assumption": "Electricity price", "Value": c["elec_price_eur_mwh"], "Notes": "Eurostat nrg_pc_205, band IC (500-2,000 MWh), excl. VAT, 2025-S2."},
        {"Assumption": "Minimum sovereign sites", "Value": c["min_sites"], "Notes": "2 for micro-states where 50-100 km separation is impossible; 4 for the five largest states."},
    ]


def fmt_money(x: float) -> str:
    return f"EUR {x:,.0f} m"


def write_goal(d: dict) -> str:
    """Render the country brief from the assembled fact dict.

    Pure dict -> markdown: every fact and every derived judgement comes from
    country_data.build(), so this function and the web app cannot disagree.
    """
    c, s = d["params"], d["_summary"]
    iso, name = d["iso2"], d["name"]
    sc, fl = d["scale"], d["flags"]
    pop, gdp, gov = sc["population_m"], sc["gdp_eur_bn"], sc["gov_employment_k"]
    price, res = sc["elec_price_eur_mwh"], sc["renewables_pct"]
    frontline, isolated = fl["frontline"], fl["grid_isolated"]
    min_sites, micro, hs = fl["min_sites"], fl["micro"], fl["hyperscaler_regions_live"]
    wl_rows = d["workloads"]
    differs = d["structural_differences"]

    ratio = sc["design_ratio"]

    def wl_table():
        lines = ["| Workload | Class | CPU cores | GPU eq. | Storage (PB) | Avail. factor |", "|---|---|---:|---:|---:|---:|"]
        for r in wl_rows:
            lines.append(f"| {r['Workload']} | {r['Class']} | {int(r['CPU cores required']):,} | {r['GPU eq. required']} | {r['Logical storage (PB)']} | {r['Availability factor']} |")
        return "\n".join(lines)

    def reg_table():
        lines = ["| Region | Role | Share | Design MW | Racks | Facility CAPEX | Notes |", "|---|---|---:|---:|---:|---:|---|"]
        for r in s.regions:
            lines.append(f"| {r['Region']} | {r['Role']} | {r['Share of design load']:.0%} | {r['Design MW']:.1f} | {r['Estimated racks']:.0f} | {fmt_money(r['Indicative facility CAPEX (EUR mm)'])} | {r['Notes']} |")
        return "\n".join(lines)

    hard = "hardened (frontline)" if frontline else "standard"

    # --- Sections 10-12: legal posture, landscape, migration ------------------
    def phase_table():
        lines = ["| Phase | Scope | Servers | Design MW | CAPEX | Cumulative | Hybrid-eligible |", "|---|---|---:|---:|---:|---:|---|"]
        for p in d["phases"]:
            lines.append(
                f"| {p['Phase']} | {p['Phase name']} | {p['Servers']:,} | {p['Design MW']:.1f} | "
                f"{fmt_money(p['CAPEX (EUR mm)'])} | {p['Cumulative CAPEX %']:.0f}% | {p['Hybrid eligible']} |"
            )
        return "\n".join(lines)

    cert_note = {
        "stringent": (
            f"{c['certification_scheme']} is among the most demanding cloud assurance regimes in the Union. "
            "The sovereign core inherits a mature control baseline and, more usefully, an existing qualification "
            "path that suppliers already know how to pass."
        ),
        "national": (
            f"A binding national standard exists ({c['certification_scheme']}), so the sovereign core can be "
            "certified against something already recognised rather than inventing its own controls."
        ),
        "baseline": (
            "There is no national cloud certification scheme; assurance rests on ISO 27001 and contract terms. "
            "The choice is to adopt EUCS when it lands or to recognise a peer scheme (BSI C5, SecNumCloud, ENS) "
            "by equivalence - writing a national scheme from scratch for a state this size is not worth the effort."
        ),
    }[c["certification_strength"]]

    dep_note = {
        "critical": (
            "Dependency on US hyperscalers is **critical**: they hold production government workloads and there is "
            "no national alternative in service. Migration is therefore a contractual and political problem before "
            "it is a technical one, and the exit terms of existing agreements are the first thing to read."
        ),
        "high": (
            "Dependency on US hyperscalers is **high**: they carry significant government workloads, most visibly "
            "productivity and collaboration. The sovereign core does not displace that overnight; it establishes "
            "somewhere for the workloads that must never have been there in the first place."
        ),
        "medium": (
            "Dependency on US hyperscalers is **moderate**: national arrangements carry part of the estate, and the "
            "sovereign core extends an existing position rather than reversing one."
        ),
        "low": (
            "Dependency on US hyperscalers is **low** by EU standards. The strategic risk here is complacency: a "
            "sovereign posture that is not exercised degrades quietly."
        ),
    }[c["hyperscaler_dependency"]]

    maturity_note = {
        "none": "There is no operating government cloud to build on; the sovereign core would be a greenfield build.",
        "pilot": "What exists is a pilot rather than an operating platform; the sovereign core would be its first production incarnation.",
        "operational": "An operating government platform already exists; the sovereign core should be its next generation, not a parallel build beside it.",
        "federated": "A federated government cloud is already in production. The open question is consolidation and governance, not construction.",
    }[c["gov_cloud_maturity"]]

    p1 = d["phases"][0]
    elective = [p for p in d["phases"] if p["Hybrid eligible"] == "yes"]
    hybrid_note = (
        f"Phase 4 can use in-country commercial capacity ({hs} live region(s)) under sovereign-held keys, "
        "which is what keeps the sovereign core small."
        if elective
        else "With no in-country commercial region, even the elective tier has nowhere in-jurisdiction to go: "
        "either it stays in the sovereign core, sized accordingly, or it leaves the jurisdiction under explicit terms."
    )

    body = f"""# {name} - Sovereign Government Data Center Network

> Generated {gen_date()} by `model/generate_countries.py` from the Dutch reference case
> (`countries/NL/GOAL.md`) and `model/eu27_parameters.csv`. Every number below is a **scaled working
> assumption**, not a sourced figure. Edit the CSVs in this directory and re-run
> `python3 model/capacity_model.py {iso}` to update the capacity numbers; edit
> `model/eu27_parameters.csv` or `model/scaling_rules.csv` and re-run the generator to update this file.

## 1. Working thesis

{name} does not need to become technologically autarkic. It needs enough independently controlled compute,
storage, networking, identity, cryptography and operational capability that the state can continue functioning
when foreign commercial infrastructure is unavailable, politically constrained, compromised, or no longer
trustworthy. The Dutch design rules (sovereignty is a stack, not a building; 3-5 separated regions; dual fibre
paths; no single hardware supplier; a first-class developer platform) are taken as the starting point and
adjusted below for what is structurally different about {name}.

## 2. Starting point

| | |
|---|---|
| Population | {pop:.2f} m (Eurostat, 1 Jan 2025) |
| GDP | EUR {gdp:,.0f} bn (2025, current prices) |
| Public administration employment (NACE O) | {gov:,.0f} k (Eurostat LFS 2025) |
| Non-household electricity price | {price:.1f} EUR/MWh (Eurostat, band IC, 2025-S2) |
| Renewables in electricity | {res:.1f}% (2024) |
| Land area | {int(c['land_km2']):,} km2 |
| Live hyperscaler regions in-country | {hs} |
| Existing government / sovereign cloud | {c['sovereign_cloud_initiative']} |
| National digital identity (anchor workload) | {c['digital_id']} |
| Internet exchange / cable landings | {c['ixp']} |

Relative to the Dutch baseline: population x{sc['pop_ratio']:.2f}, public administration x{sc['gov_ratio']:.2f},
GDP x{sc['gdp_ratio']:.2f}. Resulting design load: x{ratio:.2f} the Dutch figure.

## 3. What is structurally different from the Dutch case

{chr(10).join('- ' + d for d in differs)}

## 4. Workload demand (scaled from the Dutch baseline)

Scaling weights per workload class are in `model/scaling_rules.csv`; the Dutch rows they scale are in
`countries/NL/workloads_inputs.csv`. Frontline multiplier applied: {'yes' if frontline else 'no'}.

{wl_table()}

## 5. Capacity model output

| Metric | Value |
|---|---:|
| Physical servers | {s.total_servers:,} (CPU {s.cpu_servers:,} / GPU {s.gpu_servers:,} / storage {s.storage_servers:,}) |
| Rack equivalents | ~{s.rack_equivalents:,.0f} |
| IT critical load | {s.total_it_mw:.1f} MW |
| Facility load (PUE 1.25) | {s.facility_mw:.1f} MW |
| Facility design load (+20% headroom) | **{s.design_mw:.1f} MW** |
| Sites by capacity / recommended | {s.sites_by_mw} / **{s.sites}** (minimum {min_sites}) |
| Average design MW per site | {s.avg_mw_per_site:.1f} MW |
| Total CAPEX | **{fmt_money(s.capex_total)}** (facility {fmt_money(s.capex_facility)}, IT {fmt_money(s.capex_cpu + s.capex_gpu + s.capex_storage)}, network {fmt_money(s.capex_network)}) |
| Annual energy | {s.annual_mwh:,.0f} MWh |
| Annual OPEX | **{fmt_money(s.opex_total)} / yr** (power {fmt_money(s.opex_power)}, non-power {fmt_money(s.opex_nonpower)}) |

Full table: `facility_summary.csv`.

## 6. Proposed geography (first-pass hypothesis)

Site posture: {hard}. Separation target: {'~30-80 km (island/micro-state maximum)' if micro else '50-100 km failure domains, dual fibre paths, distinct grid feeds'}.

{reg_table()}

These regions encode only the obvious constraints (capital estate, second metro, distance from the frontier,
fault or flood zone). They are to be replaced by the scored site selection in workstream A of the Dutch
`TODO.md` (grid capacity, flood risk, fibre, failure independence, physical security, land, cooling).

## 7. Geography and threat notes

{c['threat_notes']}

## 8. Recommendations specific to {name}

1. **Anchor on {c['digital_id'].split('/')[0].split('(')[0].strip()}.** Digital identity is the workload that, if it fails, stops every other
   government service; it belongs in the sovereign core first, active-active across at least two regions.
2. **Build on the existing estate, do not replace it.** {c['sovereign_cloud_initiative'].split(';')[0].strip()} is the
   institutional starting point; the sovereign core should be its next generation, with one governance owner.
3. **Site posture: {hard}.** {'Harden at least one region and plan an out-of-country cold copy.' if frontline else 'Standard Tier III+ with 50-100 km separation is sufficient; spend the hardening budget on supply-chain assurance instead.'}
4. **Power strategy.** {'Power is the binding constraint; treat grid connection lead time and on-site generation as first-order site criteria.' if (price > 190 or isolated) else 'Power is not the binding constraint; optimise for fibre diversity and failure-domain separation.'}
5. **Hybrid tier.** {'With no in-country hyperscaler region, define now which non-critical workloads may leave the jurisdiction and under what contract terms.' if hs == 0 else 'Use in-country commercial regions for the non-critical tier, but keep identity, defense, security telemetry and registries in the sovereign core.'}

## 9. Open questions

- Replace scaled workload rows with real ministry/agency demand (see `countries/NL/CAPACITY_PLAN.md` for the method).
- Which body owns the sovereign core, and how are agencies compelled or incentivised to migrate?
- {'Out-of-country reserve: which partner state, under what treaty?' if (frontline or micro) else 'Which regions federate with EU partners for mutual disaster recovery, and which stay national-only?'}
- Site-size assumption: is the 12 MW planning unit right for {name}, or should sites be {'smaller' if s.design_mw < 20 else 'larger'}?

## 10. Legal and regulatory posture

Every member state shares one baseline: GDPR for personal data, NIS2 for the security of essential
entities, the Data Act for switching and access, and the EU Cloud Services Scheme (EUCS) still unresolved
on the sovereignty requirements that would matter most here. That baseline governs *processing*. It does
not, on its own, place infrastructure under national control - which is the gap a sovereign core exists
to close.

| | |
|---|---|
| Governing instrument | {c['legal_instrument']} |
| Cloud certification | {c['certification_scheme']} |
| Data classification | {c['data_classification']} |
| Procurement route | {c['procurement_vehicle']} |

{cert_note}

The classification ladder is the practical control: it decides which tier of data may leave the
jurisdiction at all, and it should be mapped onto the four migration phases in section 12 before any
procurement starts. Buying capacity before deciding what may sit on it is how sovereign programmes end up
with expensive infrastructure hosting the wrong workloads.

**Foreign jurisdiction exposure.** {c['hyperscaler_gov_exposure']}

{dep_note} Under the US CLOUD Act and FISA 702, a provider subject to US jurisdiction can face a lawful
order for data it holds, regardless of where the data physically sits. Data residency in-country is
therefore necessary but not sufficient; what matters is who holds the keys and who can be compelled.

## 11. Current state and provider landscape

| | |
|---|---|
| Government cloud | {c['sovereign_cloud_initiative']} |
| Maturity | {c['gov_cloud_maturity']} |
| Digital identity | {c['digital_id']} |
| In-country commercial regions | {hs} |
| Interconnection | {c['ixp']} |

{maturity_note}

Against that starting point, the modelled sovereign core is **{s.design_mw:.1f} MW of design load across
{s.sites} site(s)**, or roughly {s.total_servers:,} servers. The gap between what runs today and that
figure is the actual programme; the capacity model in sections 4-6 sizes the destination, not the journey.

## 12. Migration path and cost

Workloads are sequenced by how badly loss of control would hurt, not by how easy they are to move. The
phases below are derived from the workload classes in `model/migration_phases.csv`; per-country figures
are in `migration_phases.csv` in this directory.

{phase_table()}

**Phase 1 is the number that matters: {fmt_money(p1['CAPEX (EUR mm)'])} for {p1['Design MW']:.1f} MW,
{p1['Cumulative CAPEX %']:.0f}% of total CAPEX.** That is the floor - identity and core government
services - below which no hybrid arrangement helps, because these workloads cannot be foreign-hosted under
any sovereignty posture worth the name. It is also, notably, a small fraction of the full build: sovereignty
for the workloads that define the state is cheaper than the headline figure suggests.

Phases 2 and 3 follow on clearance and legal constraints rather than cost. {hybrid_note}

Sequencing caveat: the CAPEX split above apportions facility cost by each phase's share of IT load, which
assumes phases are built into a shared facility programme rather than as separate buildings. Building
phase 1 alone, on its own site, costs disproportionately more - the facility is largely a fixed cost.
"""
    return body


def write_summary(results: list[tuple[dict, cm.Summary]]) -> None:
    lines = [
        "# EU-27 sovereign data center capacity - summary",
        "",
        f"Generated {gen_date()} by `model/generate_countries.py`. All figures are scaled working assumptions "
        "derived from the Dutch reference case; see each country's `GOAL.md`.",
        "",
        "| ISO | Country | Pop (m) | Servers | Racks | IT MW | Design MW | Sites | CAPEX (EUR m) | OPEX (EUR m/yr) | Power price | Flags |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    tot = {"servers": 0, "design_mw": 0.0, "capex": 0.0, "opex": 0.0, "sites": 0}
    for c, s in sorted(results, key=lambda t: -t[1].design_mw):
        flags = []
        if int(c["frontline"]):
            flags.append("frontline")
        if int(c["grid_isolated"]):
            flags.append("grid-isolated")
        if c["seismic"] == "high":
            flags.append("seismic")
        if int(c["min_sites"]) <= 2:
            flags.append("micro")
        lines.append(
            f"| {c['iso2']} | {c['country']} | {float(c['population_m']):.1f} | {s.total_servers:,} | {s.rack_equivalents:,.0f} | "
            f"{s.total_it_mw:.1f} | {s.design_mw:.1f} | {s.sites} | {s.capex_total:,.0f} | {s.opex_total:,.0f} | "
            f"{float(c['elec_price_eur_mwh']):.0f} | {', '.join(flags)} |"
        )
        tot["servers"] += s.total_servers
        tot["design_mw"] += s.design_mw
        tot["capex"] += s.capex_total
        tot["opex"] += s.opex_total
        tot["sites"] += s.sites
    lines.append(
        f"| | **EU-27 total** | | **{tot['servers']:,}** | | | **{tot['design_mw']:,.0f}** | **{tot['sites']}** | "
        f"**{tot['capex']:,.0f}** | **{tot['opex']:,.0f}** | | |"
    )
    lines += [
        "",
        "Flags: *frontline* = land border with Russia/Belarus or Black Sea war exposure (defense/security workloads scaled up, "
        "hardened site posture); *grid-isolated* = electrical island or near-island; *seismic* = high seismic risk at the "
        "capital region; *micro* = two in-country sites only.",
        "",
        "Machine-readable: `model/eu27_results.csv`.",
    ]
    (COUNTRIES / "SUMMARY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    params = {r["iso2"]: r for r in cm.read_csv(PARAMS)}
    rules = load_rules()
    nl = params[BASELINE]
    base_rows = cm.read_csv(COUNTRIES / BASELINE / "workloads_inputs.csv")
    missing = sorted(set(params) - set(REGIONS) - {BASELINE})
    if missing:
        raise SystemExit(f"no REGIONS entry for {missing}")

    # Baseline params (price source consistency) and run.
    cm.write_csv(COUNTRIES / BASELINE / "params.csv", params_rows(nl))
    nl_summary = cm.run_country(BASELINE)

    results = [(nl, nl_summary)]
    for iso, c in sorted(params.items()):
        if iso == BASELINE:
            continue
        cdir = COUNTRIES / iso
        cdir.mkdir(parents=True, exist_ok=True)
        wl = scale_workloads(base_rows, c, nl, rules)
        rg = region_rows(iso, int(c["min_sites"]))
        cm.write_csv(cdir / "params.csv", params_rows(c))
        cm.write_csv(cdir / "workloads_inputs.csv", wl)
        cm.write_csv(cdir / "region_allocation_inputs.csv", rg)
        s = cm.run_country(iso)
        d = country_data.build(c, nl, s, wl, nl_summary)
        (cdir / "GOAL.md").write_text(write_goal(d), encoding="utf-8")
        results.append((c, s))
        cm.print_summary(s)

    # Sort by ISO so this file is identical whether written here or by
    # `capacity_model.py --all`, which sorts alphabetically. Without this the two
    # writers disagree on row order and any golden-file comparison is noise.
    results.sort(key=lambda pair: pair[0]["iso2"])
    cm.write_csv(ROOT / "model" / "eu27_results.csv", [cm.result_row(s) for _, s in results])
    write_summary(results)
    return 0


if __name__ == "__main__":
    sys.exit(main())
