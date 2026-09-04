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


def write_goal(c: dict, nl: dict, s: cm.Summary, wl_rows: list[dict], reg_rows: list[dict], nl_s: cm.Summary) -> str:
    iso, name = c["iso2"], c["country"]
    pop, gdp, gov = float(c["population_m"]), float(c["gdp_eur_bn"]), float(c["gov_employment_k"])
    price, res = float(c["elec_price_eur_mwh"]), float(c["renewables_pct"])
    frontline, isolated = int(c["frontline"]) == 1, int(c["grid_isolated"]) == 1
    seismic, min_sites = c["seismic"], int(c["min_sites"])
    hs = int(c["hyperscaler_regions_live"])
    micro = min_sites <= 2

    # --- Flag-driven guidance -------------------------------------------------
    differs = []
    if frontline:
        differs.append(
            "**Frontline exposure.** A land border with Russia or Belarus (or a Black Sea coast facing the war) changes the "
            "threat model from *geopolitical supply disruption* to *kinetic and sabotage risk against the facilities themselves*. "
            "Defense and security workloads are scaled up 1.5x/1.25x in the baseline, and at least one site should be hardened "
            "(EMP/blast, autonomous power for weeks, not hours). A purely national footprint cannot provide the out-of-country "
            "cold copy that Estonia's Data Embassy already demonstrates; this is the first item to revisit when the EU federation "
            "layer (Dutch GOAL.md section 16) is modelled."
        )
    if isolated:
        differs.append(
            "**Grid isolation.** The national grid is an electrical island or nearly so (weak or single interconnection). "
            "The April 2025 Iberian blackout and Cyprus/Malta interconnector outages show the failure mode. Every site needs "
            "on-site generation and storage sized for multi-day ride-through, and the PUE and facility CAPEX assumptions "
            "should be revisited upward once site studies exist."
        )
    if seismic == "high":
        differs.append(
            "**High seismic risk.** Base isolation or seismic-rated structures are mandatory, not optional, at the primary "
            "site; the second and third regions should be chosen in a different seismic domain so a single event cannot "
            "take out two regions. Expect facility CAPEX above the EUR 10 m/MW planning figure."
        )
    elif seismic == "moderate":
        differs.append("**Moderate seismic risk.** Seismic zoning should be a site-scoring criterion; at least two regions in different domains.")
    if price > 190:
        differs.append(
            f"**Expensive power ({price:.0f} EUR/MWh vs. EU average ~184).** Power is the dominant OPEX line; free cooling, "
            "heat reuse, and siting near renewables or nuclear baseload move the economics more than server choice does. "
            "The model's power OPEX line is the number to attack first."
        )
    elif price < 110:
        differs.append(
            f"**Cheap, clean power ({price:.0f} EUR/MWh, {res:.0f}% renewables).** The economics favour building larger sites than "
            "the 12 MW planning unit and offering spare sovereign capacity to partners - a reason to revisit the site-size assumption."
        )
    if micro:
        differs.append(
            "**Micro-state geography.** The Dutch rule of 3-5 regions with 50-100 km separation cannot be met inside the "
            "national territory. The model therefore assumes two in-country sites carrying 55/45 of the load and no in-country "
            "reserve. A credible disaster-recovery posture requires an out-of-country partner site - deferred to the federation layer."
        )
    if hs == 0:
        differs.append(
            "**No hyperscaler region in-country.** Unlike the Netherlands, there is no commercial hyperscale tier to fall back on "
            "for non-critical workloads without leaving the jurisdiction. The sovereign core therefore has to be sized for a larger "
            "share of total government demand, and the hybrid model (Dutch GOAL.md section 7) needs a cross-border commercial tier."
        )
    elif hs >= 3:
        differs.append(
            f"**Dense hyperscaler presence ({hs} live regions).** Commercial capacity, fibre and skills exist in-country; the "
            "sovereign core can stay lean and the hybrid model works as designed. The risk is the opposite one: political "
            "pressure to declare a hyperscaler region 'sovereign enough' (Dutch GOAL.md section 17: location is not sovereignty)."
        )
    if not differs:
        differs.append("No structural flags differ from the Dutch reference case; the Dutch design rules transfer directly.")

    ratio = s.design_mw / nl_s.design_mw

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

Relative to the Dutch baseline: population x{pop/float(nl['population_m']):.2f}, public administration x{gov/float(nl['gov_employment_k']):.2f},
GDP x{gdp/float(nl['gdp_eur_bn']):.2f}. Resulting design load: x{ratio:.2f} the Dutch figure.

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
        (cdir / "GOAL.md").write_text(write_goal(c, nl, s, wl, rg, nl_summary), encoding="utf-8")
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
