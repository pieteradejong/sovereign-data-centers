import { useEffect, useState } from 'react'
import { Route, Routes } from 'react-router-dom'

import { Layout } from './components/Layout'
import { loadBundle } from './data/load'
import type { Bundle } from './data/types'
import { Countries } from './pages/Countries'
import { Country } from './pages/Country'
import { Matrix } from './pages/Matrix'
import { Methodology } from './pages/Methodology'
import { NotFound } from './pages/NotFound'
import { Overview } from './pages/Overview'
import { Scenario } from './pages/Scenario'
import { Workloads } from './pages/Workloads'
import { useTheme } from './utils/theme'

export function App() {
  const [bundle, setBundle] = useState<Bundle | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [mode] = useTheme()

  useEffect(() => {
    loadBundle().then(setBundle, e => setError(String(e)))
  }, [])

  if (error) {
    return (
      <main className="mx-auto max-w-2xl p-6">
        <h1 className="mb-2 text-xl font-semibold">Could not load the data</h1>
        <p className="text-[var(--color-fg-secondary)]">{error}</p>
        <p className="mt-2 text-sm text-[var(--color-fg-muted)]">
          Run <code>python3 model/export_json.py</code> to regenerate the bundle.
        </p>
      </main>
    )
  }

  // Deliberately a plain message rather than a spinner: headless Chrome prints these
  // routes to PDF, and a spinner is what a broken export looks like.
  if (!bundle) {
    return (
      <main className="mx-auto max-w-2xl p-6 text-[var(--color-fg-secondary)]">
        Loading the EU-27 dataset…
      </main>
    )
  }

  return (
    <Routes>
      <Route element={<Layout generated={bundle.generated} />}>
        <Route index element={<Overview bundle={bundle} />} />
        <Route path="matrix" element={<Matrix bundle={bundle} mode={mode} />} />
        <Route path="workloads" element={<Workloads bundle={bundle} mode={mode} />} />
        <Route path="scenario" element={<Scenario bundle={bundle} />} />
        <Route path="countries" element={<Countries bundle={bundle} />} />
        <Route path="country/:iso" element={<Country bundle={bundle} />} />
        <Route path="methodology" element={<Methodology bundle={bundle} />} />
        <Route path="*" element={<NotFound />} />
      </Route>
    </Routes>
  )
}
