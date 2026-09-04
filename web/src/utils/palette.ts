/**
 * Chart palette — validated, not eyeballed.
 *
 * Page and chrome tokens come from the "Warm Neutral + Terracotta" system in
 * ~/dev/design/DESIGN_SYSTEMS.md. That system supplies one accent and no chart ramps,
 * so the data-viz slots below were derived and then run through the dataviz skill's
 * validate_palette.js on both surfaces.
 *
 * Validated 2026-09-04 with scripts/validate_palette.js:
 *
 *   categorical light (surface #faf9f5)  ALL CHECKS PASS
 *     lightness band  all 4 inside L 0.43-0.77
 *     CVD separation  worst adjacent #eda100<->#1baf7a  dE 9.1 protan / 9.6 tritan
 *     normal vision   worst adjacent dE 22.9
 *     contrast        WARN below 3:1 for #1baf7a (2.67) and #eda100 (2.06)
 *                     -> relief required, satisfied by the table view every chart ships with
 *
 *   categorical dark (surface #1a1a19)   ALL CHECKS PASS
 *     lightness band  all 4 inside L 0.48-0.67
 *     CVD separation  worst adjacent #c98500<->#199e70  dE 8.4 protan / 4.0 tritan
 *     normal vision   worst adjacent dE 19.8
 *     contrast        all 4 >= 3:1
 *
 *   diverging poles light  dE 25.6 deutan / 28.1 tritan, all checks pass
 *   diverging poles dark   dE 21.6 protan / 26.1 tritan, all checks pass
 *
 * Two caveats that constrain how these may be used:
 *   1. Dark tritan separation for yellow<->aqua is 4.0, below the 6-8 floor. Legal only
 *      with secondary encoding, so any chart using both slots must also carry direct
 *      labels or a table view. Every chart here does.
 *   2. Light-mode contrast warns for aqua and yellow. Same relief applies.
 *
 * Re-run the validator before changing any value below. test.sh checks the recorded
 * checksum so a silent edit fails.
 */

/** Fixed order, never cycled. A fifth series folds into "Other" rather than extending. */
export const CATEGORICAL_LIGHT = ['#a8462b', '#2a78d6', '#1baf7a', '#eda100'] as const
export const CATEGORICAL_DARK = ['#d17a58', '#3987e5', '#199e70', '#c98500'] as const

/**
 * Diverging: two hues with a NEUTRAL GRAY midpoint. Used for the sovereignty matrix,
 * where 0 = weakest posture and 1 = strongest, so polarity is the job.
 */
export const DIVERGING = {
  light: { low: '#a8462b', mid: '#f0efec', high: '#2a78d6' },
  dark: { low: '#d17a58', mid: '#383835', high: '#3987e5' },
} as const

/**
 * Sequential: one hue, light to dark. Used for the country x workload heatmap, where
 * the job is magnitude. Terracotta, matching the design system's accent.
 */
export const SEQUENTIAL = {
  light: ['#faf1ec', '#f0d3c5', '#e3b09b', '#d28a6c', '#bc6442', '#a8462b'],
  dark: ['#2a1a13', '#4a2a1d', '#6d3d29', '#914f35', '#b56543', '#d17a58'],
} as const

export const SURFACE = { light: '#faf9f5', dark: '#1a1a19' } as const

/** Migration phases 1-4, in fixed order. Phase identity, not magnitude. */
export const PHASE_COLORS = CATEGORICAL_LIGHT

export type Mode = 'light' | 'dark'

export function categorical(mode: Mode): readonly string[] {
  return mode === 'dark' ? CATEGORICAL_DARK : CATEGORICAL_LIGHT
}

export function sequential(mode: Mode): readonly string[] {
  return mode === 'dark' ? SEQUENTIAL.dark : SEQUENTIAL.light
}

export function diverging(mode: Mode) {
  return mode === 'dark' ? DIVERGING.dark : DIVERGING.light
}
