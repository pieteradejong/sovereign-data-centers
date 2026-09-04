import { useId, useState } from 'react'

import { cellKey } from './keys'
import { Legend } from './Legend'

export interface HeatmapCell {
  row: string
  col: string
  /** Normalised 0..1, drives the colour. */
  value: number
  /** What to show in the tooltip and the table view. */
  display: string
  /** Optional longer explanation, revealed on click. */
  detail?: string
}

export interface HeatmapProps {
  rows: string[]
  cols: string[]
  /** Row label shown to the reader; keyed by the row id. */
  rowLabel: (row: string) => string
  colLabel: (col: string) => string
  cells: Map<string, HeatmapCell>
  /** Maps a 0..1 value to a fill. */
  scale: (v: number) => string
  legend: { kind: 'sequential' | 'diverging'; low: string; high: string; stops: string[] }
  caption: string
  onSort?: (col: string) => void
  sortedBy?: string
  onCellClick?: (cell: HeatmapCell) => void
}

/**
 * A row-per-country heatmap rendered as an HTML grid rather than SVG.
 *
 * HTML because every cell must be individually focusable and screen-reader
 * addressable, which is far cheaper with real DOM elements and a <table> than with
 * SVG rects plus ARIA plumbing. The dataviz rules that bind here: a legend is always
 * present, a table view always exists, and no state is carried by colour alone —
 * every cell also has a text value in its tooltip and in the table.
 */
export function Heatmap({
  rows,
  cols,
  rowLabel,
  colLabel,
  cells,
  scale,
  legend,
  caption,
  onSort,
  sortedBy,
  onCellClick,
}: HeatmapProps) {
  const [hover, setHover] = useState<HeatmapCell | null>(null)
  const [showTable, setShowTable] = useState(false)
  const tableId = useId()

  return (
    <figure className="m-0">
      <div className="mb-3 flex flex-wrap items-center justify-between gap-3">
        <Legend {...legend} />
        <button
          type="button"
          aria-expanded={showTable}
          aria-controls={tableId}
          onClick={() => setShowTable(v => !v)}
          className="rounded border border-[var(--color-border)] px-2 py-1 text-xs text-[var(--color-fg-secondary)] hover:bg-[var(--color-bg-emphasis)]"
        >
          {showTable ? 'Hide' : 'Show'} data table
        </button>
      </div>

      <div className="scroll-x">
        <table className="border-collapse text-xs">
          <caption className="sr-only">{caption}</caption>
          <thead>
            <tr>
              <th
                scope="col"
                className="sticky left-0 z-10 bg-[var(--color-bg-page)] p-1 text-left"
              />
              {cols.map(c => (
                <th
                  key={c}
                  scope="col"
                  className="p-1 align-bottom"
                  aria-sort={onSort ? (sortedBy === c ? 'descending' : 'none') : undefined}
                >
                  {onSort ? (
                    <button
                      type="button"
                      onClick={() => onSort(c)}
                      className="w-6 origin-bottom-left -rotate-45 whitespace-nowrap text-left text-[10px] text-[var(--color-fg-secondary)] hover:text-[var(--color-accent-text)]"
                    >
                      {colLabel(c)}
                      {sortedBy === c ? ' ▾' : ''}
                    </button>
                  ) : (
                    <span className="block w-6 origin-bottom-left -rotate-45 whitespace-nowrap text-left text-[10px] text-[var(--color-fg-secondary)]">
                      {colLabel(c)}
                    </span>
                  )}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map(r => (
              <tr key={r}>
                <th
                  scope="row"
                  className="sticky left-0 z-10 bg-[var(--color-bg-page)] py-0.5 pr-2 text-right font-normal whitespace-nowrap text-[var(--color-fg-secondary)]"
                >
                  {rowLabel(r)}
                </th>
                {cols.map(c => {
                  const cell = cells.get(cellKey(r, c))
                  if (!cell) return <td key={c} className="p-0" />
                  return (
                    <td key={c} className="p-0">
                      <button
                        type="button"
                        // 2px surface gap between fills, per the mark spec.
                        style={{ background: scale(cell.value) }}
                        className="m-[1px] block h-6 w-6 rounded-[2px] focus-visible:ring-2"
                        onMouseEnter={() => setHover(cell)}
                        onMouseLeave={() => setHover(null)}
                        onFocus={() => setHover(cell)}
                        onBlur={() => setHover(null)}
                        onClick={() => onCellClick?.(cell)}
                        aria-label={`${rowLabel(r)}, ${colLabel(c)}: ${cell.display}`}
                      />
                    </td>
                  )
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Live region rather than a floating tooltip: it works for pointer and keyboard
          alike, and never clips at the edge of a scrolling container. */}
      <div
        aria-live="polite"
        className="mt-3 min-h-12 rounded border border-[var(--color-border)] bg-[var(--color-bg-card)] p-2 text-xs"
      >
        {hover ? (
          <>
            <strong className="text-[var(--color-fg-primary)]">
              {rowLabel(hover.row)} · {colLabel(hover.col)}
            </strong>{' '}
            <span className="text-[var(--color-fg-secondary)]">{hover.display}</span>
            {hover.detail ? (
              <p className="mt-1 text-[var(--color-fg-muted)]">{hover.detail}</p>
            ) : null}
          </>
        ) : (
          <span className="text-[var(--color-fg-muted)]">
            Hover or tab to a cell for its value and source.
          </span>
        )}
      </div>

      <figcaption className="mt-2 text-xs italic text-[var(--color-fg-secondary)]">
        {caption}
      </figcaption>

      {showTable ? (
        <div id={tableId} className="scroll-x mt-3">
          <table className="w-full border-collapse text-xs">
            <thead>
              <tr className="border-b border-[var(--color-border)]">
                <th scope="col" className="p-1 text-left">
                  Country
                </th>
                {cols.map(c => (
                  <th key={c} scope="col" className="p-1 text-left">
                    {colLabel(c)}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {rows.map(r => (
                <tr key={r} className="border-b border-[var(--color-border)]">
                  <th scope="row" className="p-1 text-left font-normal">
                    {rowLabel(r)}
                  </th>
                  {cols.map(c => (
                    <td key={c} className="p-1 text-[var(--color-fg-secondary)]">
                      {cells.get(cellKey(r, c))?.display ?? '—'}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : null}
    </figure>
  )
}
