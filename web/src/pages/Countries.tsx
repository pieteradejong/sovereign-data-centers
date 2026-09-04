import { Link } from 'react-router-dom'

import type { Bundle } from '@/data/types'
import { eur, mw, num } from '@/utils/format'

export function Countries({ bundle }: { bundle: Bundle }) {
  const rows = Object.values(bundle.countries).sort(
    (a, b) => b.capacity.design_mw - a.capacity.design_mw,
  )

  return (
    <article>
      <h1 className="mb-1 text-2xl font-semibold">Country briefings</h1>
      <p className="mb-6 max-w-3xl text-[var(--color-fg-secondary)]">
        One strategy per member state: capacity and siting, legal and regulatory posture, provider
        landscape, and a costed migration path.
      </p>

      <div className="scroll-x">
        <table className="w-full border-collapse text-sm">
          <thead>
            <tr className="border-b border-[var(--color-border)] text-left">
              <th scope="col" className="p-2">
                Country
              </th>
              <th scope="col" className="p-2 text-right">
                Design MW
              </th>
              <th scope="col" className="p-2 text-right">
                Sites
              </th>
              <th scope="col" className="p-2 text-right">
                Servers
              </th>
              <th scope="col" className="p-2 text-right">
                CAPEX
              </th>
              <th scope="col" className="p-2">
                Gov cloud
              </th>
            </tr>
          </thead>
          <tbody>
            {rows.map(c => (
              <tr key={c.iso2} className="border-b border-[var(--color-border)]">
                <th scope="row" className="p-2 text-left font-normal">
                  <Link
                    className="text-[var(--color-accent-text)] underline"
                    to={`/country/${c.iso2}`}
                  >
                    {c.name}
                  </Link>
                </th>
                <td className="p-2 text-right tabular-nums">{mw(c.capacity.design_mw)}</td>
                <td className="p-2 text-right tabular-nums">{c.capacity.sites}</td>
                <td className="p-2 text-right tabular-nums">{num(c.capacity.total_servers)}</td>
                <td className="p-2 text-right tabular-nums">{eur(c.capacity.capex_total)}</td>
                <td className="p-2 text-[var(--color-fg-secondary)]">
                  {c.params['gov_cloud_maturity']}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </article>
  )
}
