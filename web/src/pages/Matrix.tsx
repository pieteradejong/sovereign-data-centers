import { scaleLinear } from 'd3'
import { useMemo, useState } from 'react'

import { Heatmap, type HeatmapCell } from '@/charts/Heatmap'
import { cellKey } from '@/charts/keys'
import {
  DIMENSION_LABELS,
  MATRIX_DIMENSIONS,
  type Bundle,
  type MatrixDimension,
} from '@/data/types'
import { diverging, type Mode } from '@/utils/palette'
import { titleCase } from '@/utils/format'

/**
 * The Sovereignty Readiness Matrix.
 *
 * Eight ordinal dimensions per country, shown side by side and deliberately never
 * summed. See DECISIONS.md #10: the dimensions are not commensurable, and a composite
 * score would imply a precision this dataset does not have while being the first thing
 * quoted out of context.
 */
export function Matrix({ bundle, mode }: { bundle: Bundle; mode: Mode }) {
  const [sortedBy, setSortedBy] = useState<MatrixDimension | null>(null)
  const [selected, setSelected] = useState<HeatmapCell | null>(null)

  const isos = useMemo(() => {
    const all = Object.keys(bundle.countries)
    if (!sortedBy) return all.sort((a, b) => a.localeCompare(b))
    return all.sort(
      (a, b) =>
        (bundle.countries[b]?.matrix[sortedBy]?.score ?? 0) -
          (bundle.countries[a]?.matrix[sortedBy]?.score ?? 0) || a.localeCompare(b),
    )
  }, [bundle, sortedBy])

  const pal = diverging(mode)
  // Diverging: two hues with a neutral gray midpoint. 0 = weakest posture, 1 = strongest.
  const scale = scaleLinear<string>().domain([0, 0.5, 1]).range([pal.low, pal.mid, pal.high])

  const cells = useMemo(() => {
    const m = new Map<string, HeatmapCell>()
    for (const iso of Object.keys(bundle.countries)) {
      const c = bundle.countries[iso]
      if (!c) continue
      for (const dim of MATRIX_DIMENSIONS) {
        const cell = c.matrix[dim]
        if (!cell) continue
        m.set(cellKey(iso, dim), {
          row: iso,
          col: dim,
          value: cell.score,
          display: titleCase(cell.label),
          detail: cell.source,
        })
      }
    }
    return m
  }, [bundle])

  return (
    <article>
      <h1 className="mb-1 text-2xl font-semibold">Sovereignty readiness matrix</h1>
      <p className="mb-6 max-w-3xl text-[var(--color-fg-secondary)]">
        Eight dimensions of sovereign posture for each member state. Darker blue is a stronger
        position, terracotta a weaker one. Click any column heading to sort by it; click a cell to
        see the underlying source.
      </p>

      <Heatmap
        rows={isos}
        cols={[...MATRIX_DIMENSIONS]}
        rowLabel={iso => bundle.countries[iso]?.name ?? iso}
        colLabel={c => DIMENSION_LABELS[c as MatrixDimension] ?? c}
        cells={cells}
        scale={v => scale(v) ?? pal.mid}
        legend={{
          kind: 'diverging',
          low: 'Weaker posture',
          high: 'Stronger posture',
          stops: [pal.low, pal.mid, pal.high],
        }}
        caption="Each dimension is scored 0–1 in the same direction, so the row reads consistently. Scores come from explicit ordinal columns in eu27_parameters.csv, not from parsing prose."
        onSort={c => setSortedBy(c as MatrixDimension)}
        sortedBy={sortedBy ?? undefined}
        onCellClick={setSelected}
      />

      {selected ? (
        <aside className="mt-4 rounded border border-[var(--color-border)] bg-[var(--color-bg-card)] p-3 text-sm">
          <h2 className="mb-1 font-semibold">
            {bundle.countries[selected.row]?.name} ·{' '}
            {DIMENSION_LABELS[selected.col as MatrixDimension]}
          </h2>
          <p className="mb-1 text-[var(--color-fg-secondary)]">
            Rated <strong>{selected.display}</strong> (score {selected.value.toFixed(2)})
          </p>
          <p className="text-[var(--color-fg-muted)]">{selected.detail}</p>
        </aside>
      ) : null}

      <section className="mt-8 max-w-3xl text-sm text-[var(--color-fg-secondary)]">
        <h2 className="mb-2 font-semibold text-[var(--color-fg-primary)]">
          Why there is no single score
        </h2>
        <p className="mb-2">
          Certification strength and seismic risk do not add up to anything. Summing these
          dimensions would produce a league table that looks authoritative and means very little,
          and it would be the number every article quoted. They are shown side by side instead.
        </p>
        <p>
          Note also that three dimensions — geopolitical exposure, grid resilience and seismic
          safety — are exogenous geography rather than policy. A state does not become more
          sovereign by having no earthquakes. They matter for siting, which is why they are here,
          but they are not achievements.
        </p>
      </section>
    </article>
  )
}
