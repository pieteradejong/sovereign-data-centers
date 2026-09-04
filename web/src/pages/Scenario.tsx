import { useMemo, useState } from 'react'

import type { Bundle } from '@/data/types'
import { assumptionsFrom, computeCapacity, type Assumptions } from '@/model/capacity'
import { eur, mw } from '@/utils/format'

/**
 * The scenario sandbox — the one place in the app that recomputes rather than reads.
 *
 * Everything else displays figures straight from the bundle. Here the user changes an
 * assumption and all 27 countries are re-derived in the browser, which is affordable
 * because the whole dataset is ~40 KB and the model is arithmetic.
 *
 * Results are visibly marked as hypothetical. src/__tests__/model/capacity.test.ts
 * gates this page: if the TS port stops matching the Python model, these numbers are
 * wrong and the test fails first.
 */

interface Knob {
  key: keyof Assumptions
  label: string
  min: number
  max: number
  step: number
  help: string
}

const KNOBS: Knob[] = [
  {
    key: 'pue',
    label: 'PUE',
    min: 1.05,
    max: 1.8,
    step: 0.05,
    help: 'Facility power over IT power. Lower is better; 1.25 is the model default.',
  },
  {
    key: 'replication',
    label: 'Storage replication',
    min: 1,
    max: 5,
    step: 0.5,
    help: 'Copies of every logical byte.',
  },
  {
    key: 'mwPerSite',
    label: 'MW per site',
    min: 2,
    max: 30,
    step: 1,
    help: 'Planning capacity of one site. Raising it reduces site count.',
  },
  {
    key: 'minSites',
    label: 'Minimum sites',
    min: 1,
    max: 6,
    step: 1,
    help: 'The political floor. For most states this, not capacity, sets the site count.',
  },
  {
    key: 'headroom',
    label: 'Design headroom',
    min: 0,
    max: 0.5,
    step: 0.05,
    help: 'Spare capacity above facility load.',
  },
  {
    key: 'cpuUtil',
    label: 'CPU utilization',
    min: 0.3,
    max: 0.95,
    step: 0.05,
    help: 'Higher utilization means fewer servers for the same demand.',
  },
]

export function Scenario({ bundle }: { bundle: Bundle }) {
  const base = useMemo(() => assumptionsFrom(bundle.assumptions), [bundle])
  const [overrides, setOverrides] = useState<Partial<Assumptions>>({})

  const rows = useMemo(() => {
    return Object.values(bundle.countries)
      .map(c => {
        const workloads = c.workloads.map(w => ({
          cores: Number(w['CPU cores required']),
          gpus: Number(w['GPU eq. required']),
          storagePb: Number(w['Logical storage (PB)']),
          availability: Number(w['Availability factor']),
        }))
        const a: Assumptions = {
          ...base,
          elecPrice: c.scale.elec_price_eur_mwh,
          minSites: c.flags.min_sites,
          ...overrides,
        }
        const r = computeCapacity(workloads, a)
        return { iso: c.iso2, name: c.name, baseline: c.capacity, scenario: r }
      })
      .sort((a, b) => b.scenario.designMw - a.scenario.designMw)
  }, [bundle, base, overrides])

  const totals = rows.reduce(
    (acc, r) => ({
      designMw: acc.designMw + r.scenario.designMw,
      sites: acc.sites + r.scenario.sites,
      capex: acc.capex + r.scenario.capexTotal,
      baseMw: acc.baseMw + r.baseline.design_mw,
      baseSites: acc.baseSites + r.baseline.sites,
      baseCapex: acc.baseCapex + r.baseline.capex_total,
    }),
    { designMw: 0, sites: 0, capex: 0, baseMw: 0, baseSites: 0, baseCapex: 0 },
  )

  const dirty = Object.keys(overrides).length > 0

  return (
    <article>
      <h1 className="mb-1 text-2xl font-semibold">Scenario sandbox</h1>
      <p className="mb-6 max-w-3xl text-[var(--color-fg-secondary)]">
        Change an assumption and every member state is recomputed in your browser. Nothing here is
        saved, and these are not the published figures.
      </p>

      <div className="mb-6 grid gap-4 md:grid-cols-2">
        {KNOBS.map(k => {
          const value = overrides[k.key] ?? base[k.key]
          return (
            <div key={k.key}>
              <label className="flex items-baseline justify-between text-sm" htmlFor={k.key}>
                <span>{k.label}</span>
                <span className="tabular-nums text-[var(--color-fg-secondary)]">
                  {value}
                  {overrides[k.key] !== undefined ? (
                    <span className="ml-1 text-[var(--color-accent-text)]">changed</span>
                  ) : null}
                </span>
              </label>
              <input
                id={k.key}
                type="range"
                min={k.min}
                max={k.max}
                step={k.step}
                value={value}
                aria-describedby={`${k.key}-help`}
                onChange={e => setOverrides(o => ({ ...o, [k.key]: Number(e.target.value) }))}
                className="w-full accent-[var(--color-accent)]"
              />
              <p id={`${k.key}-help`} className="text-xs text-[var(--color-fg-muted)]">
                {k.help}
              </p>
            </div>
          )
        })}
      </div>

      {dirty ? (
        <button
          type="button"
          onClick={() => setOverrides({})}
          className="mb-6 rounded border border-[var(--color-border)] px-3 py-1 text-sm"
        >
          Reset to published assumptions
        </button>
      ) : null}

      <div
        className={`mb-6 rounded border p-3 ${
          dirty
            ? 'border-[var(--color-accent)] bg-[var(--color-bg-emphasis)]'
            : 'border-[var(--color-border)] bg-[var(--color-bg-card)]'
        }`}
      >
        <h2 className="mb-2 text-sm font-semibold">
          {dirty ? 'Hypothetical EU-27 total' : 'Published EU-27 total'}
        </h2>
        <div className="grid grid-cols-3 gap-3 text-sm">
          <div>
            <div className="text-xs text-[var(--color-fg-secondary)]">Design load</div>
            <div className="text-xl tabular-nums">{mw(totals.designMw)}</div>
            {dirty ? (
              <div className="text-xs text-[var(--color-fg-muted)]">
                published {mw(totals.baseMw)}
              </div>
            ) : null}
          </div>
          <div>
            <div className="text-xs text-[var(--color-fg-secondary)]">Sites</div>
            <div className="text-xl tabular-nums">{totals.sites}</div>
            {dirty ? (
              <div className="text-xs text-[var(--color-fg-muted)]">
                published {totals.baseSites}
              </div>
            ) : null}
          </div>
          <div>
            <div className="text-xs text-[var(--color-fg-secondary)]">CAPEX</div>
            <div className="text-xl tabular-nums">{eur(totals.capex)}</div>
            {dirty ? (
              <div className="text-xs text-[var(--color-fg-muted)]">
                published {eur(totals.baseCapex)}
              </div>
            ) : null}
          </div>
        </div>
      </div>

      <div className="scroll-x">
        <table className="w-full border-collapse text-xs">
          <caption className="sr-only">Per-country results under the current assumptions</caption>
          <thead>
            <tr className="border-b border-[var(--color-border)] text-left">
              <th scope="col" className="p-1">
                Country
              </th>
              <th scope="col" className="p-1 text-right">
                Design MW
              </th>
              <th scope="col" className="p-1 text-right">
                Sites
              </th>
              <th scope="col" className="p-1 text-right">
                MW/site
              </th>
              <th scope="col" className="p-1 text-right">
                CAPEX
              </th>
              <th scope="col" className="p-1">
                Site count set by
              </th>
            </tr>
          </thead>
          <tbody>
            {rows.map(r => (
              <tr key={r.iso} className="border-b border-[var(--color-border)]">
                <th scope="row" className="p-1 text-left font-normal">
                  {r.name}
                </th>
                <td className="p-1 text-right tabular-nums">{r.scenario.designMw.toFixed(1)}</td>
                <td className="p-1 text-right tabular-nums">{r.scenario.sites}</td>
                <td className="p-1 text-right tabular-nums">
                  {r.scenario.avgMwPerSite.toFixed(2)}
                </td>
                <td className="p-1 text-right tabular-nums">{eur(r.scenario.capexTotal)}</td>
                <td className="p-1 text-[var(--color-fg-secondary)]">
                  {r.scenario.bindingConstraint === 'min_sites' ? 'floor' : 'capacity'}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </article>
  )
}
