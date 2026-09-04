/**
 * Cell keying for the heatmaps. Lives outside Heatmap.tsx so that file exports only
 * components, which keeps React fast-refresh boundaries intact.
 */
export const cellKey = (row: string, col: string) => `${row} ${col}`
