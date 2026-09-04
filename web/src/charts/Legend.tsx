export interface LegendProps {
  kind: 'sequential' | 'diverging'
  low: string
  high: string
  stops: string[]
}

/**
 * Always present — a heatmap without a legend asks the reader to guess the mapping.
 * Both poles are labelled in text, so identity never rests on colour alone.
 */
export function Legend({ low, high, stops }: LegendProps) {
  return (
    <div className="flex items-center gap-2 text-xs text-[var(--color-fg-secondary)]">
      <span>{low}</span>
      <span className="flex" role="img" aria-label={`Colour scale from ${low} to ${high}`}>
        {stops.map((s, i) => (
          <span
            key={i}
            style={{ background: s }}
            className="h-3 w-5 first:rounded-l-[2px] last:rounded-r-[2px]"
          />
        ))}
      </span>
      <span>{high}</span>
    </div>
  )
}
