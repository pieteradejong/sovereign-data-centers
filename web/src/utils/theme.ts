import { useEffect, useState } from 'react'

import type { Mode } from './palette'

const KEY = 'eu27-theme'

/**
 * Theme is *selected*, not inferred: an explicit choice stamps data-theme on <html>
 * and wins over the OS in both directions. Chart palettes have separately validated
 * dark steps, so this must be readable synchronously by chart code.
 */
export function useTheme(): [Mode, (m: Mode) => void] {
  const [mode, setMode] = useState<Mode>(() => {
    try {
      const stored = localStorage.getItem(KEY)
      if (stored === 'light' || stored === 'dark') return stored
    } catch {
      // Private browsing and blocked site-data both throw; fall through to the OS.
    }
    return window.matchMedia?.('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
  })

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', mode)
    try {
      localStorage.setItem(KEY, mode)
    } catch {
      // Non-fatal: the theme still applies for this page view.
    }
  }, [mode])

  return [mode, setMode]
}
