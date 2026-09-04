import { scaleQuantize } from 'd3'
import { useMemo, useState } from 'react'

import { Heatmap, type HeatmapCell } from '@/charts/Heatmap'
import { cellKey } from '@/charts/keys'
import type { Bundle } from '@/data/types'
import { sequential, type Mode } from '@/utils/palette'

/** The seven workload classes, in the order the model lists them. */
const CLASSES = [
  'Critical government',
  'Government',
  'Government data',
  'AI',
  'Defense',
  'Security',
  'Research',
] as const

const SHORT: Record<string, string> = {
  'Critical government': 'Identity',
  Government: 'Core gov',
  'Government data': 'Data',
  AI: 'AI',
  Defense: 'Defense',
  Security: 'Security',
  Research: 'Research',
}

/**
 * Country x workload class, with an absolute / row-normalized toggle.
 *
 * The normalized view is the point of the page. Absolute MW just shows that Germany is
 * large. Normalized shows composition, which is where the finding is: small states are
 * dominated by the identity and SOC floors, large states by analytics and AI.
 */
export function Workloads({ bundle, mode }: { bundle: Bundle; mode: Mode }) {
  const [normalized, setNormalized] = useState(true)

  const isos = useMemo(
    () =>
      Object.keys(bundle.countries).sort(
        (a, b) =>
          (bundle.countries[b]?.capacity.design_mw ?? 0) -
          (bundle.countries[a]?.capacity.design_mw ?? 0),
      ),
    [bundle],
  )

  const { cells, maxAbs } = useMemo(() => {
    const m = new Map<string, HeatmapCell>()
    let max = 0

    for (const iso of Object.keys(bundle.countries)) {
      const c = bundle.countries[iso]
      if (!c) continue

      // Cores are the only per-class demand figure carried per country, and they track
      // MW closely enough to show composition. Absolute MW per class is not in the
      // bundle, so this is deliberately labelled as share of CPU demand.
      const byClass = new Map<string, number>()
      for (const w of c.workloads) {
        const cores = Number(w['CPU cores required'])
        byClass.set(w.Class, (byClass.get(w.Class) ?? 0) + (Number.isFinite(cores) ? cores : 0))
      }
      const total = [...byClass.values()].reduce((a, b) => a + b, 0)

      for (const cls of CLASSES) {
        const v = byClass.get(cls) ?? 0
        max = Math.max(max, v)
        m.set(cellKey(iso, cls), {
          row: iso,
          col: cls,
          value: normalized ? (total ? v / total : 0) : v,
          display: normalized
            ? `${((total ? v / total : 0) * 100).toFixed(1)}% of national CPU demand`
            : `${v.toLocaleString('en-GB')} cores`,
        })
      }
    }
    return { cells: m, maxAbs: max }
  }, [bundle, normalized])

  const stops = sequential(mode)
  const domainMax = normalized ? 0.4 : maxAbs
  const scale = scaleQuantize<string>()
    .domain([0, domainMax])
    .range([...stops])

  return (
    <article>
      <h1 className="mb-1 text-2xl font-semibold">Workload composition</h1>
      <p className="mb-4 max-w-3xl text-[var(--color-fg-secondary)]">
        CPU demand by workload class. Countries are ordered by design load, largest first.
      </p>

      <fieldset className="mb-4">
        <legend className="sr-only">Value shown</legend>
        <div className="inline-flex overflow-hidden rounded border border-[var(--color-border)] text-xs">
          {(
            [
              [true, 'Share of country'],
              [false, 'Absolute cores'],
            ] as const
          ).map(([v, label]) => (
            <button
              key={label}
              type="button"
              aria-pressed={normalized === v}
              onClick={() => setNormalized(v)}
              className={
                normalized === v
                  ? 'bg-[var(--color-accent)] px-3 py-1 text-[#262625]'
                  : 'px-3 py-1 text-[var(--color-fg-secondary)]'
              }
            >
              {label}
            </button>
          ))}
        </div>
      </fieldset>

      <Heatmap
        rows={isos}
        cols={[...CLASSES]}
        rowLabel={iso => bundle.countries[iso]?.name ?? iso}
        colLabel={c => SHORT[c] ?? c}
        cells={cells}
        scale={v => scale(v) ?? stops[0] ?? '#eee'}
        legend={{
          kind: 'sequential',
          low: normalized ? 'Small share' : 'Few cores',
          high: normalized ? 'Large share' : 'Many cores',
          stops: [...stops],
        }}
        caption={
          normalized
            ? 'Row-normalized: each row sums to 100% of that country’s CPU demand.'
            : 'Absolute CPU cores, on a shared scale across all countries.'
        }
      />

      <section className="mt-8 max-w-3xl text-sm text-[var(--color-fg-secondary)]">
        <h2 className="mb-2 font-semibold text-[var(--color-fg-primary)]">
          What the normalized view shows
        </h2>
        <p>
          Small states are dominated by their floors. An identity platform and a security operations
          centre have a minimum viable size regardless of population, so in Malta or Cyprus they
          consume a far larger share of national demand than in Germany. Large states, with those
          floors long since cleared, are dominated instead by analytics and AI — capacity that is an
          economic-policy choice rather than a continuity requirement. The absolute view hides this
          completely.
        </p>
      </section>
    </article>
  )
}
