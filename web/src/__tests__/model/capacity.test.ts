/**
 * TS/Python parity.
 *
 * Asserts src/model/capacity.ts reproduces model/eu27_results.csv — the committed
 * output of the Python model — for all 27 countries. This gates the scenario sandbox:
 * two implementations of the same arithmetic drift silently otherwise, and the sandbox
 * would quietly show different numbers from every other page.
 *
 * Reads the repo's real CSVs rather than a copied fixture, so the test breaks when the
 * model changes rather than validating a stale snapshot.
 */
import { readFileSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'

import { describe, expect, it } from 'vitest'

import { assumptionsFrom, computeCapacity, type WorkloadInput } from '@/model/capacity'

const REPO = join(dirname(fileURLToPath(import.meta.url)), '..', '..', '..', '..')

/** Minimal RFC-4180 reader: the CSVs contain quoted fields with embedded commas. */
function parseCsv(text: string): Record<string, string>[] {
  const rows: string[][] = []
  let row: string[] = []
  let field = ''
  let quoted = false

  for (let i = 0; i < text.length; i++) {
    const c = text[i]
    if (quoted) {
      if (c === '"') {
        if (text[i + 1] === '"') {
          field += '"'
          i++
        } else quoted = false
      } else field += c
    } else if (c === '"') quoted = true
    else if (c === ',') {
      row.push(field)
      field = ''
    } else if (c === '\n') {
      row.push(field)
      rows.push(row)
      row = []
      field = ''
    } else if (c !== '\r') field += c
  }
  if (field !== '' || row.length) {
    row.push(field)
    rows.push(row)
  }

  const header = rows.shift() ?? []
  return rows
    .filter(r => r.length === header.length)
    .map(r => Object.fromEntries(header.map((h, i) => [h, r[i] ?? ''])))
}

function readCsv(...parts: string[]): Record<string, string>[] {
  return parseCsv(readFileSync(join(REPO, ...parts), 'utf8'))
}

const assumptionRows = readCsv('model', 'assumptions.csv')
const expected = readCsv('model', 'eu27_results.csv')

function workloadsFor(iso: string): WorkloadInput[] {
  return readCsv('countries', iso, 'workloads_inputs.csv').map(r => ({
    cores: Number(r['CPU cores required']),
    gpus: Number(r['GPU eq. required']),
    storagePb: Number(r['Logical storage (PB)']),
    availability: Number(r['Availability factor']),
  }))
}

function overridesFor(iso: string) {
  const rows = readCsv('countries', iso, 'params.csv')
  const byName = new Map(rows.map(r => [r['Assumption'] ?? '', Number(r['Value'])]))
  return {
    elecPrice: byName.get('Electricity price'),
    minSites: byName.get('Minimum sovereign sites'),
  } as { elecPrice: number; minSites: number }
}

describe('capacity.ts reproduces the Python model', () => {
  it('has all 27 countries in the fixture', () => {
    expect(expected).toHaveLength(27)
  })

  it.each(expected.map(r => r['iso2'] as string))('%s matches eu27_results.csv', iso => {
    const want = expected.find(r => r['iso2'] === iso)
    if (!want) throw new Error(`no fixture row for ${iso}`)

    const got = computeCapacity(
      workloadsFor(iso),
      assumptionsFrom(assumptionRows, overridesFor(iso)),
    )

    // Server counts are integers and must match exactly — they come from Math.ceil,
    // so any drift here is a real arithmetic difference, not rounding.
    expect(got.cpuServers).toBe(Number(want['cpu_servers']))
    expect(got.gpuServers).toBe(Number(want['gpu_servers']))
    expect(got.storageServers).toBe(Number(want['storage_servers']))
    expect(got.totalServers).toBe(Number(want['total_servers']))
    expect(got.sites).toBe(Number(want['sites']))

    // Floats are compared at the precision the CSV records them to.
    expect(got.racks).toBeCloseTo(Number(want['racks']), 1)
    expect(got.totalItMw).toBeCloseTo(Number(want['total_it_mw']), 2)
    expect(got.designMw).toBeCloseTo(Number(want['design_mw']), 2)
    expect(got.avgMwPerSite).toBeCloseTo(Number(want['avg_mw_per_site']), 2)
    expect(got.capexTotal).toBeCloseTo(Number(want['capex_eur_mm']), 1)
    expect(got.opexPower).toBeCloseTo(Number(want['opex_power_eur_mm_yr']), 1)
    expect(got.opexTotal).toBeCloseTo(Number(want['opex_total_eur_mm_yr']), 1)
  })
})

describe('documented invariants', () => {
  it('reproduces the Dutch spreadsheet', () => {
    const got = computeCapacity(workloadsFor('NL'), assumptionsFrom(assumptionRows, overridesFor('NL')))
    expect(got.totalServers).toBe(5691)
    expect(got.designMw).toBeCloseTo(14.2, 1)
    expect(got.capexTotal).toBeCloseTo(339, 0)
  })

  it('finds site count set by the political floor, not engineering, for 24 of 27', () => {
    // The model's central irony: site count is mostly a political parameter, not an
    // engineering result. If this ever changes, the app's framing must change too.
    //
    // Precisely: 24 countries are strictly floor-bound (min_sites > sites_by_mw).
    // Germany alone genuinely needs more sites than its floor (6 vs 4). France and
    // Italy sit exactly at the tie, where sites_by_mw == min_sites == 4, so their
    // floor happens to match the engineering answer rather than overriding it.
    const rows = expected.map(r => {
      const iso = r['iso2'] as string
      const c = computeCapacity(
        workloadsFor(iso),
        assumptionsFrom(assumptionRows, overridesFor(iso)),
      )
      return { iso, ...c }
    })
    expect(rows.filter(r => r.bindingConstraint === 'min_sites')).toHaveLength(24)

    const atOrAboveFloor = rows.filter(r => r.bindingConstraint === 'capacity')
    expect(atOrAboveFloor.map(r => r.iso).sort()).toEqual(['DE', 'FR', 'IT'])

    // Germany is the only country whose MW demand exceeds its floor outright.
    const de = rows.find(r => r.iso === 'DE')
    expect(de?.sitesByMw).toBe(6)
    expect(rows.filter(r => r.sitesByMw > Math.trunc(assumptionsFrom(assumptionRows, overridesFor(r.iso)).minSites))).toHaveLength(1)
  })
})
