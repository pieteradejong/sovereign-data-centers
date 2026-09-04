import { useParams } from 'react-router-dom'

import type { Bundle } from '@/data/types'
import { eur, mw, num, pct } from '@/utils/format'
import { NotFound } from './NotFound'

function Section({ n, title, children }: { n: number; title: string; children: React.ReactNode }) {
  return (
    <section className="mb-8">
      <h2 className="mb-2 text-lg font-semibold">
        <span className="mr-2 text-[var(--color-fg-muted)]">{n}</span>
        {title}
      </h2>
      {children}
    </section>
  )
}

function Facts({ rows }: { rows: [string, string][] }) {
  return (
    <dl className="grid gap-x-4 gap-y-1 text-sm sm:grid-cols-[max-content_1fr]">
      {rows.map(([k, v]) => (
        <div key={k} className="contents">
          <dt className="text-[var(--color-fg-secondary)]">{k}</dt>
          <dd className="mb-1 sm:mb-0">{v}</dd>
        </div>
      ))}
    </dl>
  )
}

export function Country({ bundle }: { bundle: Bundle }) {
  const { iso } = useParams()
  const c = iso ? bundle.countries[iso.toUpperCase()] : undefined
  if (!c) return <NotFound />

  const p = c.params
  const cap = c.capacity
  const phase1 = c.phases[0]

  return (
    <article>
      <h1 className="mb-1 text-2xl font-semibold">{c.name}</h1>
      <p className="mb-6 max-w-3xl text-[var(--color-fg-secondary)]">
        Sovereign government data centre network — capacity, legal posture, provider landscape and
        migration path.
      </p>

      <Section n={1} title="Starting point">
        <Facts
          rows={[
            ['Population', `${c.scale.population_m.toFixed(2)} m`],
            ['GDP', `EUR ${num(c.scale.gdp_eur_bn)} bn`],
            ['Public administration (NACE O)', `${num(c.scale.gov_employment_k)} k`],
            ['Electricity price', `${c.scale.elec_price_eur_mwh.toFixed(1)} EUR/MWh`],
            ['Renewables', `${c.scale.renewables_pct.toFixed(1)}%`],
            ['Live hyperscaler regions', String(c.flags.hyperscaler_regions_live)],
          ]}
        />
      </Section>

      <Section n={2} title="What is structurally different">
        <ul className="list-disc space-y-2 pl-5 text-sm text-[var(--color-fg-secondary)]">
          {c.structural_differences.map((d, i) => (
            <li key={i}>{d.replace(/\*\*/g, '')}</li>
          ))}
        </ul>
      </Section>

      <Section n={3} title="Capacity">
        <Facts
          rows={[
            [
              'Servers',
              `${num(cap.total_servers)} (CPU ${num(cap.cpu_servers)} / GPU ${num(cap.gpu_servers)} / storage ${num(cap.storage_servers)})`,
            ],
            ['IT critical load', mw(cap.total_it_mw)],
            ['Facility design load', mw(cap.design_mw)],
            ['Sites', `${cap.sites} (by capacity ${cap.sites_by_mw}, floor ${c.flags.min_sites})`],
            ['Average per site', mw(cap.avg_mw_per_site)],
            [
              'Site count set by',
              cap.binding_constraint === 'min_sites'
                ? 'the minimum-sites floor, not capacity'
                : 'capacity',
            ],
            ['CAPEX', eur(cap.capex_total)],
            ['OPEX', `${eur(cap.opex_total)} / yr`],
          ]}
        />
      </Section>

      <Section n={4} title="Proposed geography">
        <div className="scroll-x">
          <table className="w-full border-collapse text-xs">
            <thead>
              <tr className="border-b border-[var(--color-border)] text-left">
                <th scope="col" className="p-1">
                  Region
                </th>
                <th scope="col" className="p-1">
                  Role
                </th>
                <th scope="col" className="p-1 text-right">
                  Share
                </th>
                <th scope="col" className="p-1 text-right">
                  MW
                </th>
                <th scope="col" className="p-1">
                  Notes
                </th>
              </tr>
            </thead>
            <tbody>
              {c.regions.map(r => (
                <tr key={r.Region} className="border-b border-[var(--color-border)]">
                  <th scope="row" className="p-1 text-left font-normal">
                    {r.Region}
                  </th>
                  <td className="p-1 text-[var(--color-fg-secondary)]">{r.Role}</td>
                  <td className="p-1 text-right tabular-nums">{pct(r['Share of design load'])}</td>
                  <td className="p-1 text-right tabular-nums">{r['Design MW'].toFixed(1)}</td>
                  <td className="p-1 text-[var(--color-fg-muted)]">{r.Notes}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <p className="mt-2 text-xs italic text-[var(--color-fg-secondary)]">
          First-pass geographic hypotheses encoding only the obvious constraints, to be replaced by
          scored site selection.
        </p>
      </Section>

      <Section n={5} title="Legal and regulatory posture">
        <Facts
          rows={[
            ['Governing instrument', p['legal_instrument'] ?? '—'],
            ['Cloud certification', p['certification_scheme'] ?? '—'],
            ['Data classification', p['data_classification'] ?? '—'],
            ['Procurement route', p['procurement_vehicle'] ?? '—'],
          ]}
        />
        <p className="mt-3 text-sm text-[var(--color-fg-secondary)]">
          <strong className="text-[var(--color-fg-primary)]">Foreign jurisdiction exposure.</strong>{' '}
          {p['hyperscaler_gov_exposure']}
        </p>
        <p className="mt-2 text-sm text-[var(--color-fg-muted)]">
          Under the US CLOUD Act and FISA 702 a provider subject to US jurisdiction can face a
          lawful order for data it holds regardless of where that data sits. Residency is necessary
          but not sufficient; what matters is who holds the keys and who can be compelled.
        </p>
      </Section>

      <Section n={6} title="Current state and provider landscape">
        <Facts
          rows={[
            ['Government cloud', p['sovereign_cloud_initiative'] ?? '—'],
            ['Maturity', p['gov_cloud_maturity'] ?? '—'],
            ['Digital identity', p['digital_id'] ?? '—'],
            ['Interconnection', p['ixp'] ?? '—'],
          ]}
        />
      </Section>

      <Section n={7} title="Migration path and cost">
        <div className="scroll-x">
          <table className="w-full border-collapse text-xs">
            <thead>
              <tr className="border-b border-[var(--color-border)] text-left">
                <th scope="col" className="p-1">
                  Phase
                </th>
                <th scope="col" className="p-1">
                  Scope
                </th>
                <th scope="col" className="p-1 text-right">
                  MW
                </th>
                <th scope="col" className="p-1 text-right">
                  CAPEX
                </th>
                <th scope="col" className="p-1 text-right">
                  Cumulative
                </th>
                <th scope="col" className="p-1">
                  Hybrid
                </th>
              </tr>
            </thead>
            <tbody>
              {c.phases.map(ph => (
                <tr key={ph.Phase} className="border-b border-[var(--color-border)]">
                  <th scope="row" className="p-1 text-left font-normal">
                    {ph.Phase}
                  </th>
                  <td className="p-1">{ph['Phase name']}</td>
                  <td className="p-1 text-right tabular-nums">{ph['Design MW'].toFixed(1)}</td>
                  <td className="p-1 text-right tabular-nums">{eur(ph['CAPEX (EUR mm)'])}</td>
                  <td className="p-1 text-right tabular-nums">
                    {ph['Cumulative CAPEX %'].toFixed(0)}%
                  </td>
                  <td className="p-1 text-[var(--color-fg-secondary)]">{ph['Hybrid eligible']}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        {phase1 ? (
          <p className="mt-3 text-sm text-[var(--color-fg-secondary)]">
            Phase 1 is the number that matters: <strong>{eur(phase1['CAPEX (EUR mm)'])}</strong> for{' '}
            {phase1['Design MW'].toFixed(1)} MW, {phase1['Cumulative CAPEX %'].toFixed(0)}% of total
            CAPEX. That is the floor below which no hybrid arrangement helps — and it is a small
            fraction of the full build.
          </p>
        ) : null}
      </Section>

      <Section n={8} title="Geography and threat notes">
        <p className="text-sm text-[var(--color-fg-secondary)]">{p['threat_notes']}</p>
      </Section>
    </article>
  )
}
