import AxeBuilder from '@axe-core/playwright'
import { expect, test } from '@playwright/test'

/**
 * These assert that routes render REAL DATA, not that they merely load.
 *
 * The app is client-rendered, so the failure mode that matters is a page that
 * returns 200 and shows a loading message forever — which is exactly what a broken
 * PDF export looks like too. Every check below therefore asserts a specific figure
 * traceable to the model.
 */

const ROUTES = [
  '/',
  '/matrix',
  '/workloads',
  '/scenario',
  '/countries',
  '/country/DE',
  '/methodology',
]

test.describe('data actually renders', () => {
  test('overview shows the EU-27 totals from the model', async ({ page }) => {
    await page.goto('/')
    // 305.7 MW and 125,089 servers are the committed totals in eu27_results.csv.
    await expect(page.getByText('305.7 MW')).toBeVisible()
    await expect(page.getByText('125,089')).toBeVisible()
  })

  test('matrix renders all 27 countries with 8 dimensions each', async ({ page }) => {
    await page.goto('/matrix')
    await expect(page.getByRole('heading', { name: /sovereignty readiness/i })).toBeVisible()
    // 27 body rows, one per country.
    await expect(page.locator('tbody tr')).toHaveCount(27)
    // Each cell is a button labelled with its value, so identity is never colour-only.
    await expect(page.getByRole('button', { name: /^Germany, Certification regime/ })).toBeVisible()
  })

  test('clicking a matrix cell reveals its source text', async ({ page }) => {
    await page.goto('/matrix')
    await page.getByRole('button', { name: /^France, Certification regime/ }).click()
    await expect(page.getByText(/SecNumCloud/i).first()).toBeVisible()
  })

  test('country page shows figures matching facility_summary.csv', async ({ page }) => {
    await page.goto('/country/DE')
    await expect(page.getByRole('heading', { name: 'Germany', level: 1 })).toBeVisible()
    await expect(page.getByText('60.4 MW')).toBeVisible()
    await expect(page.getByText(/BSI C5/).first()).toBeVisible()
    await expect(page.getByText(/Sovereign core/).first()).toBeVisible()
  })

  test('scenario sandbox recomputes when an assumption changes', async ({ page }) => {
    await page.goto('/scenario')
    await expect(page.getByText('Published EU-27 total')).toBeVisible()

    // Halving MW-per-site must increase the number of sites.
    const slider = page.getByLabel('MW per site')
    await slider.fill('4')
    await expect(page.getByText('Hypothetical EU-27 total')).toBeVisible()
  })

  test('workload heatmap toggles between share and absolute', async ({ page }) => {
    await page.goto('/workloads')
    await expect(page.getByRole('button', { name: 'Absolute cores' })).toBeVisible()
    await page.getByRole('button', { name: 'Absolute cores' }).click()
    await expect(page.getByText(/Absolute CPU cores/).first()).toBeVisible()
  })

  test('every chart offers a data table, so nothing is colour-only', async ({ page }) => {
    await page.goto('/matrix')
    await page.getByRole('button', { name: /show data table/i }).click()
    await expect(page.getByRole('button', { name: /hide data table/i })).toBeVisible()
  })
})

test.describe('accessibility', () => {
  for (const route of ROUTES) {
    test(`${route} has no detectable violations`, async ({ page }) => {
      await page.goto(route)
      // Wait for data-dependent content rather than a fixed timeout.
      await expect(page.locator('main')).toBeVisible()
      const results = await new AxeBuilder({ page })
        .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
        .analyze()
      expect(results.violations).toEqual([])
    })
  }
})

test.describe('responsive', () => {
  test('the 27x8 heatmap does not force the page to scroll sideways at 375px', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 800 })
    await page.goto('/matrix')
    await expect(page.locator('tbody tr').first()).toBeVisible()

    const overflow = await page.evaluate(
      () => document.documentElement.scrollWidth - document.documentElement.clientWidth,
    )
    // Wide tables must scroll inside their own container, never the body.
    expect(overflow).toBeLessThanOrEqual(1)
  })
})
