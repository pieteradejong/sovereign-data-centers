/** Shapes of web/public/data/eu27.json, written by model/export_json.py. */

export interface MatrixCell {
  score: number
  label: string
  source: string
}

/** The eight sovereignty dimensions, in display order. Never summed — see DECISIONS.md #10. */
export const MATRIX_DIMENSIONS = [
  'gov_cloud_maturity',
  'certification',
  'hyperscaler_independence',
  'commercial_tier',
  'geopolitical_exposure',
  'grid_resilience',
  'seismic_safety',
  'site_feasibility',
] as const

export type MatrixDimension = (typeof MATRIX_DIMENSIONS)[number]

export const DIMENSION_LABELS: Record<MatrixDimension, string> = {
  gov_cloud_maturity: 'Gov cloud maturity',
  certification: 'Certification regime',
  hyperscaler_independence: 'Hyperscaler independence',
  commercial_tier: 'In-country commercial tier',
  geopolitical_exposure: 'Geopolitical exposure',
  grid_resilience: 'Grid resilience',
  seismic_safety: 'Seismic safety',
  site_feasibility: 'Site feasibility',
}

export interface Capacity {
  cpu_servers: number
  gpu_servers: number
  storage_servers: number
  total_servers: number
  racks: number
  total_it_mw: number
  facility_mw: number
  design_mw: number
  sites_by_mw: number
  sites: number
  avg_mw_per_site: number
  /** Which constraint set the site count. Strictly 'min_sites' for 24 of 27 — see DECISIONS.md #12. */
  binding_constraint: 'min_sites' | 'capacity'
  capex_total: number
  capex_facility: number
  capex_it: number
  capex_network: number
  annual_mwh: number
  opex_total: number
  opex_power: number
  opex_nonpower: number
}

export interface Workload {
  Workload: string
  Class: string
  'CPU cores required': string
  'GPU eq. required': string
  'Logical storage (PB)': string
  'Availability factor': string
  Notes: string
}

export interface Region {
  Region: string
  Role: string
  'Share of design load': number
  'Design MW': number
  'Estimated racks': number
  'Indicative facility CAPEX (EUR mm)': number
  'Resilience role': string
  Notes: string
}

export interface Phase {
  Phase: string
  'Phase name': string
  Workloads: string
  Servers: number
  'Design MW': number
  'CAPEX (EUR mm)': number
  'Cumulative CAPEX %': number
  'Hybrid eligible': string
  'Hybrid eligible (class)': string
}

export interface Flags {
  frontline: boolean
  grid_isolated: boolean
  seismic: 'low' | 'moderate' | 'high'
  min_sites: number
  micro: boolean
  hyperscaler_regions_live: number
}

export interface Scale {
  population_m: number
  gdp_eur_bn: number
  gov_employment_k: number
  elec_price_eur_mwh: number
  renewables_pct: number
  land_km2: number
  pop_ratio: number
  gov_ratio: number
  gdp_ratio: number
  design_ratio: number
}

export interface Country {
  iso2: string
  name: string
  params: Record<string, string>
  flags: Flags
  scale: Scale
  capacity: Capacity
  structural_differences: string[]
  workloads: Workload[]
  regions: Region[]
  phases: Phase[]
  matrix: Record<MatrixDimension, MatrixCell>
}

export interface Bundle {
  schema_version: number
  generated: string
  provenance: string
  assumptions: Record<string, string>[]
  phase_map: Record<string, string>[]
  countries: Record<string, Country>
  totals: {
    servers: number
    design_mw: number
    sites: number
    capex_total: number
    opex_total: number
  }
}
