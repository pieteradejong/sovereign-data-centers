import type { Bundle } from '@/data/types'

export function Methodology({ bundle }: { bundle: Bundle }) {
  return (
    <article className="max-w-3xl">
      <h1 className="mb-1 text-2xl font-semibold">Methodology</h1>
      <p className="mb-6 text-[var(--color-fg-secondary)]">{bundle.provenance}</p>

      <h2 className="mb-2 text-lg font-semibold">What this is</h2>
      <p className="mb-4 text-sm text-[var(--color-fg-secondary)]">
        A capacity model for a national sovereign government cloud, built for the Netherlands and
        scaled to the other 26 member states by population, public-administration employment and
        GDP. It sizes a destination, not a journey, and every number is a working assumption rather
        than a sourced forecast.
      </p>

      <h2 className="mb-2 text-lg font-semibold">What it is not</h2>
      <ul className="mb-6 list-disc space-y-1 pl-5 text-sm text-[var(--color-fg-secondary)]">
        <li>Not a procurement estimate. Facility CAPEX is a flat EUR/MW planning figure.</li>
        <li>
          Not a survey of real government IT inventories. Workload demand is scaled from one
          country&rsquo;s hand-built table.
        </li>
        <li>
          Not verified law. The legal and regulatory entries are one researcher&rsquo;s reading of
          public policy documents, and have not yet been checked against primary sources.
        </li>
        <li>Not a ranking. The sovereignty dimensions are shown separately and never summed.</li>
      </ul>

      <h2 className="mb-2 text-lg font-semibold">Shared assumptions</h2>
      <div className="scroll-x">
        <table className="w-full border-collapse text-xs">
          <thead>
            <tr className="border-b border-[var(--color-border)] text-left">
              <th scope="col" className="p-1">
                Assumption
              </th>
              <th scope="col" className="p-1 text-right">
                Value
              </th>
              <th scope="col" className="p-1">
                Unit
              </th>
              <th scope="col" className="p-1">
                Status
              </th>
            </tr>
          </thead>
          <tbody>
            {bundle.assumptions.map((a, i) => (
              <tr key={i} className="border-b border-[var(--color-border)]">
                <th scope="row" className="p-1 text-left font-normal">
                  {a['Assumption']}
                </th>
                <td className="p-1 text-right tabular-nums">{a['Value']}</td>
                <td className="p-1 text-[var(--color-fg-secondary)]">{a['Unit']}</td>
                <td className="p-1 text-[var(--color-fg-muted)]">{a['Source / Status']}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </article>
  )
}
