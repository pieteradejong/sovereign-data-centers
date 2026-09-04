/** Formatting helpers. Kept in one place so every page renders numbers identically. */

const nf = new Intl.NumberFormat('en-GB')

export const num = (v: number) => nf.format(Math.round(v))

export const mw = (v: number) => `${v.toFixed(1)} MW`

/** Money is always EUR millions in this model (capacity_model.py works in EUR mm). */
export function eur(millions: number): string {
  if (millions >= 1000) return `EUR ${(millions / 1000).toFixed(2)} bn`
  return `EUR ${Math.round(millions)} m`
}

export const pct = (v: number, digits = 0) => `${(v * 100).toFixed(digits)}%`

/** Title-cases an ordinal label like 'operational' for display. */
export const titleCase = (s: string) => s.charAt(0).toUpperCase() + s.slice(1)
