= Part II — The method

// DRAFT SCAFFOLD. Authored prose, ~8k words when written out (DECISIONS.md #27).
// This part has to carry the model's honesty burden: it is where the reader learns
// exactly how much of Part III is derived rather than observed.

== The Dutch reference case

Every number in this book descends from one hand-built model of a Dutch government
cloud: 5,691 servers, 14.2 MW of design load, EUR 339 m of capital. That model was built
from published Dutch government IT inventories and a set of engineering assumptions
listed in Part IV. The other twenty-six countries are scaled from it.

// Spine:
// - Where the Dutch workload inventory came from
// - The workload classes and why they scale differently
// - Servers to racks to MW to sites: the chain, with the PUE and headroom assumptions
// - Reproducibility: the model regenerates the xlsx exactly

== Scaling to twenty-six more

// Spine:
// - The three drivers: population, GDP, public-administration employment
// - Why weights differ by workload class
// - The small-state floor, and why 24 of 27 countries hit it
// - The frontline multiplier, and what evidence it rests on
// - The four flags: frontline, grid-isolated, seismic, micro

== What this model is not

A scaled model is a hypothesis generator, not a forecast. It says what a country of this
size and this exposure would plausibly need if its government IT resembled the
Netherlands'. It does not know any country's actual workload inventory, and where a real
inventory exists the real number should replace the scaled one.

// Spine:
// - The honest error bars: which figures are engineering, which are guesses
// - 73.5% mean prose similarity across the generated briefs, and what that admits
// - The legal columns are a different epistemic category (DECISIONS.md #25)
// - How to falsify any entry in Part III, and where to send the correction

== The geography is a hypothesis

// Spine:
// - First-pass regions encode only obvious constraints: capital, second metro, separation
// - What a real site-scoring workstream would add: grid queue, flood, seismic, land
// - Why no coordinates appear anywhere in this book
