# Assets

Provenance for every non-code, non-generated asset in this repository: where it came from, how it was
made, and which parts of it are derived from the model rather than drawn.

Recorded because a reader cannot otherwise tell a figure computed by `capacity_model.py` from a number an
image model invented, and because one asset here carries embedded provenance metadata that would
otherwise reveal itself before the repository did.

---

## `countries/NL/Rijkscloud-Dutch_Sovereign_Data_Center_Network.png`

**AI-generated concept artwork. Not a Dutch government document.**

| | |
|---|---|
| Origin | Generated with OpenAI `gpt-image` v2.0 via the OpenAI Media Service API |
| Created | 2026-08-13 |
| Provenance | C2PA Content Credentials embedded in the PNG's `caBX` chunk, signed by OpenAI OpCo, LLC |
| IPTC classification | `trainedAlgorithmicMedia` — fully AI-generated |
| Watermark | Carries `c2pa.watermarked.unbound` (an invisible watermark) |
| Dimensions | 1024 × 1536, 2.2 MB |
| Added in | `605ab80`, later moved to `countries/NL/` |

### What it is, and is not

It is a twelve-panel concept poster made early in the project to visualise what a Dutch sovereign cloud
programme might look like. **It is not an official document, and "RijksCloud" is a proposed name, not an
existing programme.** No such programme exists in the Netherlands. The country's own brief hedges the name
as "*provisionally* RijksCloud"; the image does not, and images get shared without the page around them —
hence this file.

The poster uses a crowned emblem and wordmark in the visual register of Dutch state identity, plus copy
written in the state's voice. That was a stylistic choice in an early draft and, with hindsight, the wrong
one for an artefact in a public repository. It is kept for its historical role as the project's first
visual, with this disclosure attached. **Newer artwork does not do this** — see below.

### Which numbers are real

Some figures reconcile with the capacity model and some were drawn by the image model. Treat only the
first group as meaningful:

| Reconciles with the model | Drawn by the image model, derived from nothing here |
|---|---|
| 5,691 servers | The 380 kV power-backbone routing |
| 14.2 MW design load | Subsea cable landing placements |
| EUR 339 m CAPEX | The ten-year growth curves and their three scenarios |
| Three sites | The facility cutaway interior |

**It is also stale.** It shows PUE 1.70 and OPEX EUR 25.1 m/yr; the model now says 1.25 and EUR 35.9 m/yr.
It labels `3,897` as "Total vCPU" and `1,513 TB` as raw storage, when both are *server counts*
(`cpu_servers` and `storage_servers`). This drift is exactly why the per-country posters below are
generated from the model instead.

---

## `countries/<ISO>/<ISO>-infographic.png` — 27 files

**Generated from the model. No AI image generation involved.**

| | |
|---|---|
| Origin | Rendered by headless Chrome from the app's `/poster/:iso` route |
| Produced by | `model/export_artifacts.py` (`./run.sh export`) |
| Source of every figure | `country_data.build()` via `web/public/data/eu27.json` |
| Reproducible | Yes — delete and regenerate; the numbers come from the model, not from a prompt |

Deliberately different from the Dutch artwork above, per `DECISIONS.md` #38:

- **Every figure traces to the model.** A poster cannot disagree with its country's brief.
- **No state emblems, flags, crowns or official-looking wordmarks.** These are concept studies for a
  programme that exists in no member state, and each one says so on its face.
- **The caveat is printed on the poster**, not only in the repository, because an image travels alone.

## `countries/<ISO>/<ISO>-briefing.pdf` — 27 files

Same pipeline, printed from the app's `/country/:iso` route. Same provenance and same reproducibility.

---

## `countries/NL/dutch_sovereign_data_center_capacity_model.xlsx`

The original hand-built Dutch spreadsheet the Python model reproduces. Kept as the reference the model is
checked against: `tests/test_model.py` asserts 5,691 servers, 14.2 MW and EUR 339 m, which are its
figures. Document metadata (`docProps/core.xml`, `app.xml`) is absent, so it leaks no author details.

---

## Third-party content

**None.** No vendored libraries, fonts, images or datasets. Web dependencies are all resolved through
`web/package.json` and its lockfile, and no file in this repository was copied from another project.

If that changes, the `~/dev/CLAUDE.md` rule applies: a vendored file carries its source, version and
licence text alongside it, and gets a row here.

---

## Licensing

Assets are covered by neither `LICENSE` (code) nor `LICENSE-DATA` (the dataset). The generated posters and
briefings are outputs of the model and follow the data licence, CC BY 4.0. The AI-generated Dutch artwork
is a separate case: it is published here for reference, and anyone reusing it should be aware of both its
AI provenance and the state-iconography issue described above.
