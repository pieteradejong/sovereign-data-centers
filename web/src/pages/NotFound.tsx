import { Link } from 'react-router-dom'

export function NotFound() {
  return (
    <article>
      <h1 className="mb-2 text-2xl font-semibold">Page not found</h1>
      <p className="text-[var(--color-fg-secondary)]">
        <Link className="underline" to="/">
          Back to the overview
        </Link>
      </p>
    </article>
  )
}
