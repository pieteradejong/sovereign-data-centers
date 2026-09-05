import { useEffect, useRef } from 'react'
import { useParams } from 'react-router-dom'

import type { Bundle, Country } from '@/data/types'
import { eur, mw, num, pct } from '@/utils/format'
import { CATEGORICAL_LIGHT } from '@/utils/palette'
import { NotFound } from './NotFound'

/**
 * One-page infographic per country, rendered at 1024 x 1536 for export to PNG by
 * headless Chrome (model/export_artifacts.py).
 *
 * Every figure here comes from country_data.build() via the JSON bundle, so a poster
 * cannot drift from that country's brief. This is the deliberate contrast with
 * countries/NL/Rijkscloud-...png, which was AI-generated: its 380 kV routing, cable
 * landings and growth curves were drawn by an image model and derive from nothing in
 * this repo, and it still shows PUE 1.70 against the model's 1.25 (see ASSETS.md).
 *
 * Two rules this layout follows, both from the security audit:
 *   1. No state emblems, flags, crowns or official-looking wordmarks. These are
 *      concept posters for a programme that does not exist in any member state.
 *   2. The provenance caveat is ON the poster, because images travel separately from
 *      the page that explains them.
 */

const PANEL = 'border border-[#e3ded0] bg-white rounded p-3'
const H = 'text-[11px] font-semibold uppercase tracking-wide text-[#6b6a63] mb-2'

function Metric({ label, value, sub }: { label: string; value: string; sub?: string }) {
  return (
    <div>
      <div className="text-[10px] text-[#6b6a63]">{label}</div>
      <div className="text-[19px] font-semibold leading-tight tabular-nums text-[#262625]">
        {value}
      </div>
      {sub ? <div className="text-[9px] text-[#898781]">{sub}</div> : null}
    </div>
  )
}

/** Horizontal stacked bar showing each phase's share of total CAPEX. */
function PhaseBar({ c }: { c: Country }) {
  const total = c.phases.reduce((a, p) => a + p['CAPEX (EUR mm)'], 0) || 1
  return (
    <div>
      <div className="mb-1 flex h-5 w-full overflow-hidden rounded">
        {c.phases.map((p, i) => (
          <div
            key={p.Phase}
            style={{
              width: `${(p['CAPEX (EUR mm)'] / total) * 100}%`,
              background: CATEGORICAL_LIGHT[i % CATEGORICAL_LIGHT.length],
            }}
            className="mr-[2px] last:mr-0"
            title={`${p['Phase name']}: ${eur(p['CAPEX (EUR mm)'])}`}
          />
        ))}
      </div>
      <div className="space-y-[3px]">
        {c.phases.map((p, i) => (
          <div key={p.Phase} className="flex items-center gap-1.5 text-[9px]">
            <span
              style={{ background: CATEGORICAL_LIGHT[i % CATEGORICAL_LIGHT.length] }}
              className="inline-block h-2 w-2 shrink-0 rounded-[1px]"
            />
            <span className="w-[110px] shrink-0 text-[#262625]">
              {p.Phase}. {p['Phase name']}
            </span>
            <span className="tabular-nums text-[#6b6a63]">{eur(p['CAPEX (EUR mm)'])}</span>
            <span className="ml-auto tabular-nums text-[#898781]">
              {p['Design MW'].toFixed(1)} MW
            </span>
          </div>
        ))}
      </div>
    </div>
  )
}

/** Ranked workload classes by CPU share — the composition story in one panel. */
function WorkloadMix({ c }: { c: Country }) {
  const byClass = new Map<string, number>()
  for (const w of c.workloads) {
    const v = Number(w['CPU cores required'])
    byClass.set(w.Class, (byClass.get(w.Class) ?? 0) + (Number.isFinite(v) ? v : 0))
  }
  const total = [...byClass.values()].reduce((a, b) => a + b, 0) || 1
  const rows = [...byClass.entries()].sort((a, b) => b[1] - a[1])

  return (
    <div className="space-y-[3px]">
      {rows.map(([cls, v]) => (
        <div key={cls} className="flex items-center gap-1.5 text-[9px]">
          <span className="w-[104px] shrink-0 truncate text-[#6b6a63]">{cls}</span>
          <span className="h-2 flex-1 bg-[#f0efec]">
            <span
              style={{ width: `${(v / total) * 100}%` }}
              className="block h-2 rounded-r-[2px] bg-[#a8462b]"
            />
          </span>
          <span className="w-8 shrink-0 text-right tabular-nums text-[#898781]">
            {pct(v / total)}
          </span>
        </div>
      ))}
    </div>
  )
}

export function Poster({ bundle }: { bundle: Bundle }) {
  const { iso } = useParams()
  const ref = useRef<HTMLDivElement>(null)

  // Stamp the rendered height so export_artifacts.py can size the capture window.
  // Chrome screenshots the window, not the document, so without this a 2-region
  // country is two-thirds blank and a 5-region one is clipped.
  // Hooks run before the not-found guard below: they must not sit after an early return.
  useEffect(() => {
    if (ref.current) {
      ref.current.setAttribute('data-poster-height', String(Math.ceil(ref.current.scrollHeight)))
    }
  })

  const c = iso ? bundle.countries[iso.toUpperCase()] : undefined
  if (!c) return <NotFound />

  const cap = c.capacity
  const p = c.params
  const phase1 = c.phases[0]
  const flags = [
    c.flags.frontline && 'Frontline',
    c.flags.grid_isolated && 'Grid-isolated',
    c.flags.seismic !== 'low' && `${c.flags.seismic} seismic`,
    c.flags.micro && 'Micro-state',
    c.flags.hyperscaler_regions_live === 0 && 'No in-country cloud region',
  ].filter(Boolean) as string[]

  return (
    // Fixed 1024x1536 so the PNG export is deterministic. Light-only: posters are
    // printed and photocopied, and a dark poster is unusable in both.
    <div
      ref={ref}
      data-poster={c.iso2}
      style={{ width: 1024, colorScheme: 'light' }}
      className="mx-auto bg-[#f5f2e9] p-8 text-[#262625]"
    >
      <header className="mb-4 border-b-2 border-[#a8462b] pb-3">
        <div className="text-[10px] font-semibold uppercase tracking-[0.18em] text-[#a8462b]">
          Sovereign government data centre network — concept study
        </div>
        <h1 className="text-[38px] font-bold leading-none">{c.name}</h1>
        <p className="mt-1 text-[12px] text-[#6b6a63]">
          What a sovereign core would take: capacity, cost, legal posture and a phased migration.
        </p>
      </header>

      {flags.length ? (
        <div className="mb-4 flex flex-wrap gap-1.5">
          {flags.map(f => (
            <span
              key={f}
              className="rounded border border-[#a8462b] px-2 py-[2px] text-[9px] font-semibold uppercase tracking-wide text-[#a8462b]"
            >
              {f}
            </span>
          ))}
        </div>
      ) : null}

      <div className="mb-3 grid grid-cols-4 gap-3">
        <div className={PANEL}>
          <Metric
            label="Facility design load"
            value={mw(cap.design_mw)}
            sub={`PUE ${bundle.assumptions.find(a => a['Assumption'] === 'PUE')?.['Value'] ?? ''}`}
          />
        </div>
        <div className={PANEL}>
          <Metric
            label="Sites"
            value={String(cap.sites)}
            sub={`${cap.avg_mw_per_site.toFixed(2)} MW each`}
          />
        </div>
        <div className={PANEL}>
          <Metric
            label="Servers"
            value={num(cap.total_servers)}
            sub={`~${Math.round(cap.racks)} racks`}
          />
        </div>
        <div className={PANEL}>
          <Metric
            label="CAPEX"
            value={eur(cap.capex_total)}
            sub={`${eur(cap.opex_total)}/yr to run`}
          />
        </div>
      </div>

      <div className="mb-3 grid grid-cols-2 gap-3">
        <section className={PANEL}>
          <h2 className={H}>1 · From workloads to power</h2>
          <div className="space-y-1 text-[10px]">
            {[
              ['CPU servers', num(cap.cpu_servers)],
              ['GPU servers', num(cap.gpu_servers)],
              ['Storage servers', num(cap.storage_servers)],
              ['IT critical load', mw(cap.total_it_mw)],
              ['Facility load', mw(cap.facility_mw)],
              ['Design load (+headroom)', mw(cap.design_mw)],
              ['Annual energy', `${num(cap.annual_mwh)} MWh`],
            ].map(([k, v]) => (
              <div
                key={k}
                className="flex justify-between border-b border-dotted border-[#e3ded0] pb-[2px]"
              >
                <span className="text-[#6b6a63]">{k}</span>
                <span className="font-semibold tabular-nums">{v}</span>
              </div>
            ))}
          </div>
        </section>

        <section className={PANEL}>
          <h2 className={H}>2 · Workload mix (share of CPU demand)</h2>
          <WorkloadMix c={c} />
          <p className="mt-2 text-[9px] italic leading-snug text-[#898781]">
            {c.flags.micro
              ? 'Identity and security floors dominate: both have a minimum viable size regardless of population.'
              : 'Analytics and AI dominate once the identity and security floors are cleared.'}
          </p>
        </section>
      </div>

      <div className="mb-3 grid grid-cols-2 gap-3">
        <section className={PANEL}>
          <h2 className={H}>3 · Proposed geography</h2>
          <div className="space-y-[3px] text-[9px]">
            {c.regions.map(r => (
              <div key={r.Region} className="border-b border-dotted border-[#e3ded0] pb-[3px]">
                <div className="flex justify-between">
                  <span className="font-semibold">{r.Region}</span>
                  <span className="tabular-nums text-[#6b6a63]">
                    {pct(r['Share of design load'])} · {r['Design MW'].toFixed(1)} MW
                  </span>
                </div>
                <div className="text-[#898781]">{r.Role}</div>
              </div>
            ))}
          </div>
          <p className="mt-2 text-[9px] italic leading-snug text-[#898781]">
            First-pass hypotheses encoding only the obvious constraints. Not selected sites.
          </p>
        </section>

        <section className={PANEL}>
          <h2 className={H}>4 · Migration path and cost</h2>
          <PhaseBar c={c} />
          {phase1 ? (
            <p className="mt-2 text-[9px] italic leading-snug text-[#898781]">
              Phase 1 — the floor below which no hybrid arrangement helps — is{' '}
              {eur(phase1['CAPEX (EUR mm)'])}, {phase1['Cumulative CAPEX %'].toFixed(0)}% of total
              CAPEX.
            </p>
          ) : null}
        </section>
      </div>

      <div className="mb-3 grid grid-cols-2 gap-3">
        <section className={PANEL}>
          <h2 className={H}>5 · Legal and regulatory posture</h2>
          <dl className="space-y-1 text-[9px]">
            {[
              ['Governing instrument', p['legal_instrument']],
              ['Certification', p['certification_scheme']],
              ['Classification', p['data_classification']],
              ['Procurement', p['procurement_vehicle']],
            ].map(([k, v]) => (
              <div key={k}>
                <dt className="font-semibold text-[#6b6a63]">{k}</dt>
                <dd className="leading-snug text-[#262625]">{v || '—'}</dd>
              </div>
            ))}
          </dl>
        </section>

        <section className={PANEL}>
          <h2 className={H}>6 · Current state and dependency</h2>
          <dl className="space-y-1 text-[9px]">
            {[
              ['Government cloud', p['sovereign_cloud_initiative']],
              ['Digital identity', p['digital_id']],
              ['Foreign jurisdiction exposure', p['hyperscaler_gov_exposure']],
            ].map(([k, v]) => (
              <div key={k}>
                <dt className="font-semibold text-[#6b6a63]">{k}</dt>
                <dd className="leading-snug text-[#262625]">{v || '—'}</dd>
              </div>
            ))}
          </dl>
        </section>
      </div>

      <section className={`${PANEL} mb-3`}>
        <h2 className={H}>7 · Geography and threat notes</h2>
        <p className="text-[9px] leading-snug text-[#262625]">{p['threat_notes']}</p>
      </section>

      {/* The caveat is ON the poster. An image gets shared without the page around it. */}
      <footer className="border-t border-[#e3ded0] pt-2 text-[8px] leading-snug text-[#898781]">
        <p className="mb-1">
          <strong className="text-[#6b6a63]">Working assumptions, not forecasts.</strong> Capacity
          figures are scaled from a single Dutch reference case, not a survey of this
          country&rsquo;s actual government IT. Legal and regulatory entries were researched in
          September 2026, are{' '}
          <strong className="text-[#6b6a63]">not verified against primary sources</strong>, and will
          date. Maturity, certification-strength and dependency ratings are the author&rsquo;s
          judgements, not official ratings. Nothing here should be relied on for a procurement or
          policy decision.
        </p>
        <p>
          This is an independent concept study. It is not a government document and does not
          represent any member state, institution or programme. No such programme exists in {c.name}
          . Generated {bundle.generated} from the model in this repository — every figure is
          reproducible from it. Corrections welcome. MIT (code) / CC BY 4.0 (data).
        </p>
      </footer>
    </div>
  )
}
