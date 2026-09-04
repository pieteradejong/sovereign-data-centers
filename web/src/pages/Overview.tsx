import { Link } from 'react-router-dom'

import { RankedBar } from '@/charts/RankedBar'
import type { Bundle } from '@/data/types'
import { eur, mw, num } from '@/utils/format'

const CLOSET_MW = 1.0

function Stat({ label, value, note }: { label: string; value: string; note?: string }) {
  return (
    <div className="rounded border border-[var(--color-border)] bg-[var(--color-bg-card)] p-3">
      <div className="text-xs text-[var(--color-fg-secondary)]">{label}</div>
      <div className="text-2xl font-semibold tabular-nums">{value}</div>
      {note ? <div className="mt-1 text-xs text-[var(--color-fg-muted)]">{note}</div> : null}
    </div>
  )
}

export function Overview({ bundle }: { bundle: Bundle }) {
  const countries = Object.values(bundle.countries)

  const perSite = countries
    .map(c => ({
      id: c.iso2,
      label: c.name,
      value: c.capacity.avg_mw_per_site,
      flagged: c.capacity.avg_mw_per_site < CLOSET_MW,
    }))
    .sort((a, b) => b.value - a.value)

  const belowCloset = perSite.filter(d => d.flagged).length
  const floorBound = countries.filter(c => c.capacity.binding_constraint === 'min_sites').length

  return (
    <article>
      <h1 className="mb-1 text-2xl font-semibold">A sovereign core for twenty-seven states</h1>
      <p className="mb-6 max-w-3xl text-[var(--color-fg-secondary)]">
        What it would take for each EU member state to run the workloads it cannot afford to lose on
        infrastructure it controls — and what that costs.
      </p>

      <div className="mb-8 grid grid-cols-2 gap-3 md:grid-cols-4">
        <Stat
          label="Design load, EU-27"
          value={mw(bundle.totals.design_mw)}
          note="across 27 sovereign cores"
        />
        <Stat label="Servers" value={num(bundle.totals.servers)} />
        <Stat label="Sites" value={String(bundle.totals.sites)} />
        <Stat
          label="CAPEX"
          value={eur(bundle.totals.capex_total)}
          note={`${eur(bundle.totals.opex_total)}/yr to run`}
        />
      </div>

      <section className="mb-10">
        <h2 className="mb-1 text-lg font-semibold">The small-state cliff</h2>
        <p className="mb-4 max-w-3xl text-sm text-[var(--color-fg-secondary)]">
          The Dutch design rule — three to five separated regions — does not survive contact with a
          small country. Spreading a sub-3 MW national requirement across three sites produces rooms
          below one megawatt: a closet, not a data centre. <strong>{belowCloset} states</strong>{' '}
          land there.
        </p>
        <RankedBar
          data={perSite}
          threshold={{ value: CLOSET_MW, label: 'below this a "site" is a server room' }}
          unit="MW/site"
          format={v => `${v.toFixed(2)} MW`}
          caption="Average design load per site, after the minimum-sites floor is applied."
        />
      </section>

      <section className="mb-10 max-w-3xl">
        <h2 className="mb-1 text-lg font-semibold">Site count is a political number</h2>
        <p className="text-sm text-[var(--color-fg-secondary)]">
          For <strong>{floorBound} of 27</strong> states, the number of sites is set by a
          hand-entered minimum rather than by how much power the workloads need. Only Germany
          genuinely requires more sites than its floor; France and Italy land exactly on theirs. The
          engineering result is not driving the geography — a policy assumption is, and it deserves
          to be argued about explicitly rather than inherited.
        </p>
      </section>

      <nav className="grid gap-3 sm:grid-cols-2">
        {[
          ['/matrix', 'Sovereignty matrix', 'Eight dimensions of posture, per state.'],
          ['/workloads', 'Workload composition', 'What each state would actually run.'],
          ['/scenario', 'Scenario sandbox', 'Change the assumptions, recompute all 27.'],
          ['/countries', 'Country briefings', 'The full strategy for each member state.'],
        ].map(([to, title, blurb]) => (
          <Link
            key={to}
            to={to!}
            className="rounded border border-[var(--color-border)] bg-[var(--color-bg-card)] p-3 hover:border-[var(--color-accent)]"
          >
            <div className="font-semibold text-[var(--color-accent-text)]">{title}</div>
            <div className="text-sm text-[var(--color-fg-secondary)]">{blurb}</div>
          </Link>
        ))}
      </nav>
    </article>
  )
}
