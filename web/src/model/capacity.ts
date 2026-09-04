/**
 * TypeScript port of model/capacity_model.py.
 *
 * This exists ONLY for the scenario sandbox, where the user changes assumptions and all
 * 27 countries recompute live. Every canonical figure displayed elsewhere is read from
 * the JSON bundle, not recomputed here — two implementations of one arithmetic drift
 * silently otherwise.
 *
 * src/__tests__/model/capacity.test.ts asserts this reproduces model/eu27_results.csv
 * for all 27 countries. That test gates the sandbox: if it fails, this file is wrong,
 * not the fixture.
 *
 * Mirrors capacity_model.py:150-205. Python's math.ceil is Math.ceil here; the
 * spreadsheet lineage is ROUNDUP(x, 0).
 */

export interface Assumptions {
  coresPerServer: number
  cpuUtil: number
  gpuPerServer: number
  gpuUtil: number
  pbPerStorageServer: number
  replication: number
  serversPerRack: number
  cpuKw: number
  gpuKw: number
  storageKw: number
  netOverhead: number
  pue: number
  headroom: number
  mwPerSite: number
  minSites: number
  capexCpu: number
  capexGpu: number
  capexStorage: number
  capexNetwork: number
  capexFacility: number
  elecPrice: number
  opexNonpower: number
}

export interface WorkloadInput {
  cores: number
  gpus: number
  storagePb: number
  availability: number
}

export interface CapacityResult {
  cpuServers: number
  gpuServers: number
  storageServers: number
  totalServers: number
  racks: number
  serverItMw: number
  totalItMw: number
  facilityMw: number
  designMw: number
  sitesByMw: number
  sites: number
  avgMwPerSite: number
  capexTotal: number
  annualMwh: number
  opexPower: number
  opexNonpower: number
  opexTotal: number
  /** Which constraint actually set the site count. */
  bindingConstraint: 'min_sites' | 'capacity'
}

export function computeCapacity(workloads: WorkloadInput[], a: Assumptions): CapacityResult {
  let cpuServers = 0
  let gpuServers = 0
  let storageServers = 0
  let serverItMw = 0

  for (const w of workloads) {
    const cpu = Math.ceil((w.cores * w.availability) / (a.coresPerServer * a.cpuUtil))
    const gpu = Math.ceil((w.gpus * w.availability) / (a.gpuPerServer * a.gpuUtil))
    const storage = Math.ceil(
      (w.storagePb * a.replication * w.availability) / a.pbPerStorageServer,
    )
    cpuServers += cpu
    gpuServers += gpu
    storageServers += storage
    serverItMw += (cpu * a.cpuKw + gpu * a.gpuKw + storage * a.storageKw) / 1000
  }

  const totalServers = cpuServers + gpuServers + storageServers
  const racks = totalServers / a.serversPerRack
  const totalItMw = serverItMw * (1 + a.netOverhead)
  const facilityMw = totalItMw * a.pue
  const designMw = facilityMw * (1 + a.headroom)
  const sitesByMw = Math.ceil(designMw / a.mwPerSite)
  const sites = Math.max(sitesByMw, Math.trunc(a.minSites))

  const capexCpu = cpuServers * a.capexCpu
  const capexGpu = gpuServers * a.capexGpu
  const capexStorage = storageServers * a.capexStorage
  const capexNetwork = (capexCpu + capexGpu + capexStorage) * a.capexNetwork
  const capexFacility = designMw * a.capexFacility
  const capexTotal = capexCpu + capexGpu + capexStorage + capexNetwork + capexFacility

  const annualMwh = facilityMw * 8760
  const opexPower = (annualMwh * a.elecPrice) / 1_000_000
  const opexNonpower = capexTotal * a.opexNonpower

  return {
    cpuServers,
    gpuServers,
    storageServers,
    totalServers,
    racks,
    serverItMw,
    totalItMw,
    facilityMw,
    designMw,
    sitesByMw,
    sites,
    avgMwPerSite: designMw / sites,
    capexTotal,
    annualMwh,
    opexPower,
    opexNonpower,
    opexTotal: opexPower + opexNonpower,
    bindingConstraint: sites > sitesByMw ? 'min_sites' : 'capacity',
  }
}

/** Assumption names exactly as they appear in model/assumptions.csv. */
const ASSUMPTION_KEYS: Record<keyof Assumptions, string> = {
  coresPerServer: 'CPU cores per server',
  cpuUtil: 'Average CPU utilization',
  gpuPerServer: 'GPU equivalents per GPU server',
  gpuUtil: 'Average GPU utilization',
  pbPerStorageServer: 'Usable storage per storage server',
  replication: 'Storage replication factor',
  serversPerRack: 'Servers per rack',
  cpuKw: 'CPU server power',
  gpuKw: 'GPU server power',
  storageKw: 'Storage server power',
  netOverhead: 'Network/other IT overhead',
  pue: 'PUE',
  headroom: 'Design headroom',
  mwPerSite: 'Critical-load MW per site',
  minSites: 'Minimum sovereign sites',
  capexCpu: 'Server CAPEX - CPU',
  capexGpu: 'Server CAPEX - GPU',
  capexStorage: 'Server CAPEX - storage',
  capexNetwork: 'Network CAPEX',
  capexFacility: 'Facility CAPEX',
  elecPrice: 'Electricity price',
  opexNonpower: 'Non-power annual OPEX',
}

/**
 * Build an Assumptions object from the bundle's assumptions rows plus a country's
 * two per-country overrides (electricity price, minimum sites).
 */
export function assumptionsFrom(
  rows: Record<string, string>[],
  overrides: Partial<Record<keyof Assumptions, number>> = {},
): Assumptions {
  const byName = new Map(rows.map(r => [r['Assumption'] ?? '', Number(r['Value'])]))
  const out = {} as Assumptions
  for (const [key, name] of Object.entries(ASSUMPTION_KEYS) as [keyof Assumptions, string][]) {
    const v = byName.get(name)
    if (v === undefined || Number.isNaN(v)) throw new Error(`missing assumption: ${name}`)
    out[key] = v
  }
  return { ...out, ...overrides }
}
