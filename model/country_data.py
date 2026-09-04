#!/usr/bin/env python3
"""
Assemble every fact about one country into a plain dict.

This is the single source the renderers read from. `generate_countries.write_goal()`
turns it into markdown; `export_json.py` turns it into the JSON bundle the web app
consumes. Neither derives facts of its own, so the brief and the app can never disagree.

Nothing here computes capacity: the numbers arrive already computed in a
`capacity_model.Summary`. This module only gathers, derives flags, and scores the
ordinal dimensions used by the sovereignty matrix.
"""
from __future__ import annotations

# Ordinal scales for the sovereignty matrix. Every dimension is scored 0..1 where
# 1 = strongest sovereign posture, so the heatmap reads consistently in one direction.
# These come from explicit ordinal columns in eu27_parameters.csv rather than from
# parsing free text, so the scoring is auditable and can be argued with.
MATURITY = {"none": 0.0, "pilot": 0.33, "operational": 0.67, "federated": 1.0}
CERT_STRENGTH = {"baseline": 0.0, "national": 0.5, "stringent": 1.0}
DEPENDENCY = {"critical": 0.0, "high": 0.33, "medium": 0.67, "low": 1.0}
SEISMIC = {"high": 0.0, "moderate": 0.5, "low": 1.0}

# A site below this is a server room, not a data center. Used for the small-state cliff.
CLOSET_MW = 1.0


def flags(c: dict) -> dict:
    """Structural flags derived from the parameter row."""
    min_sites = int(c["min_sites"])
    return {
        "frontline": int(c["frontline"]) == 1,
        "grid_isolated": int(c["grid_isolated"]) == 1,
        "seismic": c["seismic"],
        "min_sites": min_sites,
        "micro": min_sites <= 2,
        "hyperscaler_regions_live": int(c["hyperscaler_regions_live"]),
    }


def matrix_row(c: dict, s, f: dict) -> dict:
    """The eight sovereignty-matrix dimensions, each with its score and its source text.

    Deliberately NOT summed into a composite score: these dimensions are not
    commensurable, and a single number would imply a precision this dataset does not
    have. The app shows them side by side.
    """
    feasible = f["min_sites"] >= 3 and (s.design_mw / s.sites) >= CLOSET_MW
    hs = f["hyperscaler_regions_live"]
    return {
        "gov_cloud_maturity": {
            "score": MATURITY[c["gov_cloud_maturity"]],
            "label": c["gov_cloud_maturity"],
            "source": c["sovereign_cloud_initiative"],
        },
        "certification": {
            "score": CERT_STRENGTH[c["certification_strength"]],
            "label": c["certification_strength"],
            "source": c["certification_scheme"],
        },
        "hyperscaler_independence": {
            "score": DEPENDENCY[c["hyperscaler_dependency"]],
            "label": c["hyperscaler_dependency"],
            "source": c["hyperscaler_gov_exposure"],
        },
        "commercial_tier": {
            # Availability of an in-jurisdiction commercial fallback. Capped at 3:
            # beyond three regions the hybrid model is equally well served.
            "score": min(hs, 3) / 3.0,
            "label": f"{hs} live region(s)",
            "source": c["hyperscaler_gov_exposure"],
        },
        "geopolitical_exposure": {
            "score": 0.0 if f["frontline"] else 1.0,
            "label": "frontline" if f["frontline"] else "not frontline",
            "source": c["threat_notes"],
        },
        "grid_resilience": {
            "score": 0.0 if f["grid_isolated"] else 1.0,
            "label": "isolated" if f["grid_isolated"] else "interconnected",
            "source": c["threat_notes"],
        },
        "seismic_safety": {
            "score": SEISMIC[f["seismic"]],
            "label": f["seismic"],
            "source": c["threat_notes"],
        },
        "site_feasibility": {
            "score": 1.0 if feasible else 0.0,
            "label": f"{s.design_mw / s.sites:.2f} MW/site over {s.sites} sites",
            "source": (
                "Meets the 3-region rule at viable site size."
                if feasible
                else f"Cannot meet 3 separated regions above {CLOSET_MW:.0f} MW/site."
            ),
        },
    }


def structural_differences(c: dict, f: dict) -> list[str]:
    """Flag-driven prose on how this country departs from the Dutch reference case.

    Lives here rather than in the markdown renderer so the web app renders the same
    text as the brief.
    """
    price, res = float(c["elec_price_eur_mwh"]), float(c["renewables_pct"])
    hs = f["hyperscaler_regions_live"]
    differs = []
    if f["frontline"]:
        differs.append(
            "**Frontline exposure.** A land border with Russia or Belarus (or a Black Sea coast facing the war) changes the "
            "threat model from *geopolitical supply disruption* to *kinetic and sabotage risk against the facilities themselves*. "
            "Defense and security workloads are scaled up 1.5x/1.25x in the baseline, and at least one site should be hardened "
            "(EMP/blast, autonomous power for weeks, not hours). A purely national footprint cannot provide the out-of-country "
            "cold copy that Estonia's Data Embassy already demonstrates; this is the first item to revisit when the EU federation "
            "layer (Dutch GOAL.md section 16) is modelled."
        )
    if f["grid_isolated"]:
        differs.append(
            "**Grid isolation.** The national grid is an electrical island or nearly so (weak or single interconnection). "
            "The April 2025 Iberian blackout and Cyprus/Malta interconnector outages show the failure mode. Every site needs "
            "on-site generation and storage sized for multi-day ride-through, and the PUE and facility CAPEX assumptions "
            "should be revisited upward once site studies exist."
        )
    if f["seismic"] == "high":
        differs.append(
            "**High seismic risk.** Base isolation or seismic-rated structures are mandatory, not optional, at the primary "
            "site; the second and third regions should be chosen in a different seismic domain so a single event cannot "
            "take out two regions. Expect facility CAPEX above the EUR 10 m/MW planning figure."
        )
    elif f["seismic"] == "moderate":
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
    if f["micro"]:
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
    return differs


def build(c: dict, nl: dict, s, wl_rows: list[dict], nl_s) -> dict:
    """Everything the renderers need about one country."""
    f = flags(c)
    pop, gdp, gov = float(c["population_m"]), float(c["gdp_eur_bn"]), float(c["gov_employment_k"])

    # The country-level hybrid gate: a class may be hybrid-eligible, but without an
    # in-jurisdiction commercial region there is nowhere in-jurisdiction to put it.
    # capacity_model.py deliberately does not know this (it reads no parameter file).
    phases = []
    for p in s.phases:
        p = dict(p)
        p["Hybrid eligible"] = (
            "yes" if p["Hybrid eligible (class)"] == "yes" and f["hyperscaler_regions_live"] > 0 else "no"
        )
        phases.append(p)

    return {
        "iso2": c["iso2"],
        "name": c["country"],
        "params": dict(c),
        "flags": f,
        "scale": {
            "population_m": pop,
            "gdp_eur_bn": gdp,
            "gov_employment_k": gov,
            "elec_price_eur_mwh": float(c["elec_price_eur_mwh"]),
            "renewables_pct": float(c["renewables_pct"]),
            "land_km2": int(c["land_km2"]),
            "pop_ratio": pop / float(nl["population_m"]),
            "gov_ratio": gov / float(nl["gov_employment_k"]),
            "gdp_ratio": gdp / float(nl["gdp_eur_bn"]),
            "design_ratio": s.design_mw / nl_s.design_mw,
        },
        "capacity": {
            "cpu_servers": s.cpu_servers,
            "gpu_servers": s.gpu_servers,
            "storage_servers": s.storage_servers,
            "total_servers": s.total_servers,
            "racks": round(s.rack_equivalents, 1),
            "total_it_mw": round(s.total_it_mw, 2),
            "facility_mw": round(s.facility_mw, 2),
            "design_mw": round(s.design_mw, 2),
            "sites_by_mw": s.sites_by_mw,
            "sites": s.sites,
            "avg_mw_per_site": round(s.avg_mw_per_site, 2),
            # Which constraint actually set the site count. For 26 of 27 it is the
            # hand-set minimum, not the engineering result — the model's central irony.
            "binding_constraint": "min_sites" if s.sites > s.sites_by_mw else "capacity",
            "capex_total": round(s.capex_total, 1),
            "capex_facility": round(s.capex_facility, 1),
            "capex_it": round(s.capex_cpu + s.capex_gpu + s.capex_storage, 1),
            "capex_network": round(s.capex_network, 1),
            "annual_mwh": round(s.annual_mwh),
            "opex_total": round(s.opex_total, 2),
            "opex_power": round(s.opex_power, 2),
            "opex_nonpower": round(s.opex_nonpower, 2),
        },
        "structural_differences": structural_differences(c, f),
        "workloads": wl_rows,
        "regions": s.regions,
        "phases": phases,
        "matrix": matrix_row(c, s, f),
    }
