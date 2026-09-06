# Could the Netherlands build its own frontier model?

**Companion note to the RijksCloud capacity plan.** The sovereign data center model in
this repository sizes *government cloud* — the compute a state needs to run its own
administration. This note asks the adjacent question that comes up whenever that plan is
discussed: **what would it take for the Netherlands to develop its own frontier AI model,
or at least something suitable?**

The two are related but not the same size of problem, and conflating them is the most
common error in the public debate. See "How this relates to the capacity model" below.

Figures are order-of-magnitude estimates current to mid-2026. Treat the frontier-cost
numbers as reconstructed, not sourced — labs do not publish.

---

## The short answer

**A genuine frontier model is out of reach for the Netherlands acting alone, and would be
the wrong goal even if it weren't.** The binding constraint is not money in the abstract —
it is the combination of ~150 MW of firm grid capacity on a congested network, a
Dutch-language corpus roughly two orders of magnitude too small to train on by itself, and
a pool of frontier-scale training talent that numbers in the low hundreds globally.

**"Something suitable" is very much in reach, and is a different project.** The useful
Dutch target is a sovereign, auditable, well-served *mid-scale* model — strong Dutch and
Frisian, clean data provenance, deployable inside government and healthcare — plus
guaranteed access to frontier capability procured elsewhere. That is roughly what GPT-NL
is aiming at, at roughly 1/50th of the budget it would need to be good at it.

Best current estimate: **€1.5–3B over five years** for a credible national capability,
against the **€13.5M** committed to GPT-NL to date.

## How this relates to the capacity model

This is the comparison worth internalising before reading further:

| | Design load | CAPEX | Sites |
|---|---|---|---|
| **RijksCloud** (this repo's NL case) | **14.2 MW** | **€339M** | 3 |
| A single frontier training cluster | **~150 MW** | **$4–6B** | 1 |

**A frontier training cluster is more than ten times the power draw of the entire
proposed Dutch sovereign government cloud, and an order of magnitude more capital, for one
purpose.** RijksCloud's 281 GPU servers exist to serve inference and analytics for the
Dutch state; they are not, and are not meant to be, a training fleet.

Two consequences for this project:

1. **Do not let the frontier question capture the capacity plan.** They compete for the
   same scarce input — grid connections — and the frontier ask is large enough to make
   the government-cloud ask politically unaffordable if they are bundled. The
   sovereign-cloud case stands on its own and should be argued on its own.
2. **The siting analysis transfers, and it is the most valuable thing here.** Everything
   this repo establishes about Dutch grid congestion, regional load allocation, and the
   northern power advantage (see `region_allocation_output.csv`: North is the sovereign
   secondary precisely because of power and land) applies with far more force to a
   training cluster, because a training cluster is a single 150 MW point load rather than
   a 14 MW load split across five regions.

## 1. What "frontier" actually costs

| | Scale | Notes |
|---|---|---|
| Frontier training run (compute alone) | **$0.5–2B** | Rental-equivalent, 2026-class run |
| Llama-3.1-405B-class run (2024) | **~$40–60M** | ~16k H100 × ~54 days ≈ 21M GPU-hours |
| Cluster to train at the frontier | **100k+ accelerators** | xAI, Meta, OpenAI, Anthropic all in this band |
| Capex for such a cluster | **$4–6B** | GPUs, networking, building, power |
| Power draw | **~150 MW** sustained | ~1.4 kW per accelerator all-in, incl. cooling |
| Frontier training talent | **low hundreds worldwide** | People who have led a >10²⁵ FLOP run |
| Time from standing start | **3–5 years** | Site, grid, silicon delivery, team, one failed run |

Two things follow. First, the training run is the *small* number — the cluster, the power
contract and the team dominate. Second, this is a state-scale expenditure, not a
research-grant one.

## 2. What the Netherlands has today

**GPT-NL.** A sovereign Dutch language model built by TNO, SURF and the Netherlands
Forensic Institute, funded with **€13.5M** from the Ministry of Economic Affairs via RVO.
As of early 2026 it is in beta: five organisations ran feasibility studies from late
February, growing toward ten by spring, with broader availability planned for the second
half of 2026. Its design premise — training only on data with clean provenance and
licensing — is genuinely distinctive and is the most defensible thing about it.

For scale: **GPT-NL's entire budget is about a quarter of the compute cost of one
Llama-3.1-405B run, and roughly 1% of a single 2026 frontier run.** It is not competing in
that category and does not claim to.

**Snellius.** The national supercomputer at SURF, Amsterdam Science Park. After its 2024
expansion: **352 NVIDIA H100 and 288 A100 GPUs**, ~38 PFlop/s theoretical. An excellent
national research machine, and roughly **0.35% of a frontier training cluster**. It is
shared across all Dutch science and cannot be monopolised for a year-long training run.

**EuroHPC and the AI gigafactories.** The EU route: up to seven AI Gigafactories, four at
≥75,000 accelerators and three at ≥100,000, under InvestAI's ~€20B facility inside a
~€200B mobilisation target. The June 2025 expression-of-interest round drew 76 submissions
across 60 sites in 16 member states; the formal EuroHPC call followed in July 2026.
Announced consortia cluster around Germany, France, Portugal, Finland and Romania.
**The Netherlands is not visibly leading any of them.** That is the single most
consequential fact in this note: the one vehicle at the right scale is being built, and
Dutch participation is currently passive.

## 3. The five binding constraints

### Compute — solvable with money
Nothing about buying 100k accelerators is technically hard for a country with the Dutch
balance sheet, and export controls are not a barrier for an EU/NATO member. Purely
fiscal, and the least interesting constraint.

### Power — the actual hard constraint
The Netherlands has structural grid congestion (*netcongestie*); TenneT's connection queue
runs to years across large parts of the country, and new large-load connections in the
Randstad are effectively unavailable. A 150 MW firm connection is a political decision
about queue priority, not a procurement.

The one strong Dutch card is **Eemshaven** — existing hyperscale presence, proximity to
offshore wind landfall, and grid headroom the Randstad lacks. Any serious proposal is a
Groningen proposal, which makes it a regional development question and changes its
politics considerably. This is the same logic that puts the sovereign secondary in the
North in `region_allocation_inputs.csv`, applied to a load ten times larger.

### Data — the constraint that kills the naive version
Dutch has roughly 25M speakers including Flanders. After deduplication and quality
filtering, total available high-quality Dutch text is plausibly on the order of
**10²–10³ billion tokens**. Frontier models train on **10⁴ billion tokens and up**.
Dutch-language data is therefore around **1% of a frontier training corpus** — and
GPT-NL's licensing-clean constraint cuts that further.

This forces a definition most public discussion elides. **"A Dutch model" means at least
three different projects:**

1. **Dutch-language** — best-in-class Dutch, Frisian and Dutch institutional register.
   Achievable at mid-scale; mostly a data-curation and evaluation problem, not a compute one.
2. **Dutch-owned** — weights and pipeline under Dutch control, so no foreign vendor can
   revoke, alter or price-gouge access. Achievable, and the real content of "sovereignty".
3. **Dutch-governed** — capability inside Dutch legal jurisdiction for classified,
   judicial or medical use. Achievable at small scale *today*, and arguably the
   highest-value near-term target. It is also the one that maps directly onto the
   classification and certification posture columns in `model/eu27_parameters.csv`.

Only a confused version of the goal requires all three at frontier scale.

### People — the constraint money buys slowly
The Netherlands has genuine depth in ML research (Amsterdam, Delft, Nijmegen, Eindhoven)
and in the semiconductor supply chain everyone else depends on. It has very little
experience *operating* a large training run — a distinct, mostly-unpublished engineering
discipline. A national programme's first year is hiring and its second is a failed run.
Budget accordingly.

### Money — available, but not currently flowing
€1.5–3B over five years is roughly 0.15–0.3% of annual Dutch government expenditure. It is
affordable. But the National Growth Fund (*Nationaal Groeifonds*), which funded the AiNed
programme and was the natural vehicle, had its further rounds curtailed by the 2024
coalition. There is currently **no Dutch funding instrument sized to this question**,
which is why the EU gigafactory route matters more than it otherwise would.

## 4. What it would actually take — three tiers

### Tier 1 — Sovereign deployment capability · €50–150M · 18 months
Fine-tune and serve open-weight frontier models on Dutch soil, under Dutch law, with
Dutch-curated data and evaluation. No pretraining. Buys jurisdictional control, no vendor
lock-in on inference, real Dutch/Frisian quality, usable inside NFI, ministries and
hospitals. **Does not buy** independence from the upstream model's existence or licence.

*Highest return per euro on this page, and mostly unbuilt.* It also fits inside
RijksCloud's existing GPU envelope rather than requiring a new one.

### Tier 2 — Sovereign mid-scale pretraining · €1.5–3B · 5 years
A 5,000–20,000 accelerator national cluster at Eemshaven with a firm power contract; a
permanent 100–200 person training organisation; models in the 30B–200B class, trained
multilingually with Dutch heavily weighted. Roughly the Mistral trajectory, publicly
financed. Buys a real, renewable national capability and a seat at the table.
**Does not buy** frontier parity — these models trail by 12–24 months, permanently.

### Tier 3 — Frontier parity · €15–30B+ · 8–10 years · not unilaterally feasible
100k+ accelerators, 150 MW firm, continuous refresh cycles, and successful recruitment
against labs paying more than the Dutch state legally can. **Only reachable as lead
partner in an EU gigafactory consortium.** As a national project it fails on talent
before it fails on money.

## 5. The recommendation

1. **Do Tier 1 now.** Cheap, fast, and it delivers the sovereignty property people
   actually care about — control over deployment — years before pretraining could.
2. **Fund GPT-NL properly or stop.** €13.5M is not a serious number for the attached
   ambition. The provenance-clean premise deserves an order of magnitude more, or an
   honest redefinition as a research project.
3. **Bid for a gigafactory, from Eemshaven, with partners.** The only path to Tier 3 and
   the cheapest path to Tier 2. Dutch leverage is the semiconductor supply chain and
   northern grid capacity, not domestic AI scale.
4. **Treat frontier access as procurement, with terms.** Continuity guarantees,
   weight escrow and price-shock protection buy more real security per euro than a
   domestic frontier run.
5. **Spend on evaluation.** Whoever defines what "good in Dutch" means for healthcare,
   courts and government holds durable influence regardless of who trains the models.
   Nearly free, and nobody is doing it.

## 6. The strongest case against all of this

Worth stating properly, because it may be right:

- **Sovereignty is a category error for a fungible input.** The Netherlands does not make
  its own jet engines. Frontier models are becoming commodity infrastructure with multiple
  competing suppliers; buying well beats building badly.
- **A permanently trailing model is worse than no model**, because it creates a domestic
  constituency for mandating its own use.
- **Depreciation is brutal.** A 2026 accelerator fleet is substantially obsolete by 2029.
  Not a bridge — an annuity payment.
- **The counterfactual spend is strong.** €2B into grid capacity, education, or the
  ASML-adjacent supply chain plausibly does more for Dutch technological position.
- **The real chokepoint is already Dutch.** Leverage over EUV lithography is worth more
  than a domestic model, and nothing here puts it at risk.

Note that the first and third of these arguments are *weaker* against the sovereign data
center case than against the frontier case: government cloud is not a fungible input
(jurisdiction is the whole point), and buildings depreciate over decades rather than
years. The asymmetry is the reason to keep the two proposals separate.

## Status

Early, and none of this is settled. Figures are reconstructed order-of-magnitude estimates
current to mid-2026 and are the part most likely to be wrong. Unlike the rest of this
repository, **nothing here is generated from the model** — this is an authored note, and
`run.sh data` will not touch it.

## Sources

- [GPT-NL — TNO](https://www.tno.nl/en/digital/artificial-intelligence/gpt-nl/)
- [The Netherlands starts realisation of GPT-NL — SURF](https://www.surf.nl/en/news/the-netherlands-starts-realisation-gpt-nl-its-own-open-ai-language-model)
- [Dutch government agencies to pilot GPT-NL — NL Times, Feb 2026](https://nltimes.nl/2026/02/26/dutch-government-agencies-pilot-homegrown-ai-model-gpt-nl)
- [Netherlands moves GPT-NL from lab to live — Computer Weekly](https://www.computerweekly.com/news/366642524/Netherlands-moves-GPT-NL-from-lab-to-live-first-pilots-under-way)
- [GPU expansion of supercomputer Snellius — SURF](https://www.surf.nl/en/news/gpu-expansion-of-supercomputer-snellius-enables-even-faster-data-processing-for-dutch)
- [SURF Snellius H100 upgrade — HPCwire](https://www.hpcwire.com/off-the-wire/surfs-latest-snellius-upgrade-enhances-ai-research-capabilities-with-nvidia-h100-gpus/)
- [Snellius system description — SURF user knowledge base](https://servicedesk.surf.nl/wiki/spaces/WIKI/pages/30660184/Snellius)
- [AI Gigafactories — European Commission](https://commission.europa.eu/topics/competitiveness/competitiveness-coordination-tool-projects/ai-gigafactories_en)
- [The EU's AI Gigafactory initiative — STL Partners](https://stlpartners.com/articles/data-centres/eu-ai-gigafactory-initiative/)
- [AI gigafactories: built for purpose? — interface](https://www.interface-eu.org/publications/ai-gigafactories)
- [European AI gigafactories: the true, the false and the uncertain — Polytechnique Insights](https://www.polytechnique-insights.com/en/columns/digital/european-ai-gigafactories-the-true-the-false-and-the-uncertain/)
