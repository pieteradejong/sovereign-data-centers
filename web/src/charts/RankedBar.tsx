import { num } from '@/utils/format'

export interface RankedDatum {
  id: string
  label: string
  value: number
  /** Marks a datum as below the threshold, which is the point of this chart. */
  flagged?: boolean
}

export interface RankedBarProps {
  data: RankedDatum[]
  threshold?: { value: number; label: string }
  unit: string
  caption: string
  format?: (v: number) => string
}

/**
 * Horizontal ranked bars with an optional threshold rule. Built for the small-state
 * cliff, where the finding is entirely about which countries fall below a line.
 *
 * Bars are thin, anchored to a zero baseline, with rounded data-ends. Flagged bars
 * carry the accent AND a text marker, so the distinction is not colour-only.
 */
export function RankedBar({ data, threshold, unit, caption, format = num }: RankedBarProps) {
  const max = Math.max(...data.map(d => d.value), threshold?.value ?? 0)

  return (
    <figure className="m-0">
      <div className="space-y-1">
        {data.map(d => (
          <div key={d.id} className="flex items-center gap-2 text-xs">
            <span className="w-28 shrink-0 text-right text-[var(--color-fg-secondary)]">
              {d.label}
            </span>
            <span className="relative flex-1">
              <span
                style={{ width: `${Math.max((d.value / max) * 100, 0.5)}%` }}
                className={`block h-3 rounded-r-[4px] ${
                  d.flagged ? 'bg-[var(--color-accent)]' : 'bg-[var(--color-baseline)]'
                }`}
              />
              {threshold ? (
                <span
                  style={{ left: `${(threshold.value / max) * 100}%` }}
                  aria-hidden="true"
                  className="absolute top-0 h-3 w-px bg-[var(--color-fg-primary)]"
                />
              ) : null}
            </span>
            <span className="w-24 shrink-0 tabular-nums text-[var(--color-fg-secondary)]">
              {format(d.value)}
              {d.flagged ? <span className="ml-1 text-[var(--color-accent-text)]">▲</span> : null}
            </span>
          </div>
        ))}
      </div>

      {threshold ? (
        <p className="mt-2 text-xs text-[var(--color-fg-secondary)]">
          <span aria-hidden="true">▲</span> below {format(threshold.value)} {unit} —{' '}
          {threshold.label}
        </p>
      ) : null}

      <figcaption className="mt-2 text-xs italic text-[var(--color-fg-secondary)]">
        {caption}
      </figcaption>
    </figure>
  )
}
