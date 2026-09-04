/**
 * Shown on every page, not buried in the methodology.
 *
 * The capacity figures are scaled placeholders and the legal entries are unverified
 * research. A reader who lands on a country page from a search result must see that
 * before they see a number, or the site misrepresents its own confidence.
 */
export function ProvenanceBanner({ generated }: { generated: string }) {
  return (
    <p className="border-b border-[var(--color-border)] bg-[var(--color-bg-emphasis)] px-4 py-2 text-xs text-[var(--color-fg-secondary)]">
      <strong className="text-[var(--color-fg-primary)]">
        Working assumptions, not forecasts.
      </strong>{' '}
      Capacity figures are scaled from a single Dutch reference case. Legal and regulatory entries
      were researched in September 2026, are not yet verified against primary sources, and will
      date. Generated {generated}.{' '}
      <a className="underline" href="/methodology">
        How this was built
      </a>
      .
    </p>
  )
}
