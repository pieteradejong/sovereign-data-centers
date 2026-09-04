import type { Bundle } from './types'

/**
 * The whole model is ~40 KB gzipped, so the app fetches it once and holds it in
 * memory. No API, no per-page requests, and the scenario sandbox can recompute all 27
 * countries on every slider tick without touching the network.
 */
let cached: Promise<Bundle> | null = null

export function loadBundle(): Promise<Bundle> {
  if (!cached) {
    cached = fetch(`${import.meta.env.BASE_URL}data/eu27.json`).then(r => {
      if (!r.ok) throw new Error(`failed to load data bundle: ${r.status} ${r.statusText}`)
      return r.json() as Promise<Bundle>
    })
  }
  return cached
}

/** Test seam: inject a bundle instead of fetching. */
export function __setBundle(b: Bundle | null) {
  cached = b ? Promise.resolve(b) : null
}
