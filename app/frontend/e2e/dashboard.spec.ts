import { test, expect } from '@playwright/test';

test.describe('Dashboard User Journeys', () => {
  test.beforeEach(async ({ page }) => {
    // Intercept API calls to prevent requiring the backend for frontend E2E
    await page.route('**/api/v1/affordability*', async route => {
      const json = {
        meta: {
          basket_id: "protein_v1",
          geography: { id: "BR", name: "Brasil" },
          income_basis: "min",
          methodology_version: "1.0",
          last_updated: new Date().toISOString(),
        },
        data: [
          {
            date: "2024-01-01",
            basket_cost: 100,
            income: 1000,
            income_burden_pct: 10,
            affordability_ratio: 10,
            purchasing_power_index: 100,
            quality_flag: "complete",
            components: { beef: 50, pork: 20, chicken: 20, eggs: 10 }
          }
        ]
      };
      await route.fulfill({ json });
    });

    await page.goto('/');
  });

  test('should load the dashboard and display the App Shell', async ({ page }) => {
    await expect(page.getByRole('heading', { name: 'PoderBR' })).toBeVisible();
    await expect(page.getByRole('heading', { name: 'Dashboard' })).toBeVisible();
    await expect(page.getByText('Welcome to PoderBR')).toBeVisible();
  });

  test('should allow interacting with Geography control', async ({ page }) => {
    const geoSelect = page.getByLabel('Geography');
    await expect(geoSelect).toHaveValue('BR');

    await geoSelect.selectOption('SP');
    await expect(geoSelect).toHaveValue('SP');
  });

  test('should toggle the accessible DataTable alternative for charts', async ({ page }) => {
    // Wait for the data to render
    await expect(page.getByRole('heading', { name: 'Purchasing Power Trend' })).toBeVisible();

    // The chart image role should be visible initially
    await expect(page.getByRole('img', { name: 'Purchasing Power Trend' })).toBeVisible();

    // Click the toggle button for the Trend Chart
    const toggleButton = page.locator('div').filter({ hasText: /^Purchasing Power TrendHistorical trend of the Purchasing Power Index\..*Show Table$/ }).getByRole('button');
    await toggleButton.click();

    // The tabular data should now be visible instead
    await expect(page.getByRole('table').filter({ hasText: 'Purchasing Power Trend data table' })).toBeVisible();

    // The chart image should no longer be visible
    await expect(page.getByRole('img', { name: 'Purchasing Power Trend' })).not.toBeVisible();
  });

  test('should reveal methodology disclosure upon click', async ({ page }) => {
    const disclosureButton = page.getByRole('button', { name: /Data Sources & Methodology/i });

    // Content should be hidden initially
    await expect(page.getByText('Disclaimer: This index measures')).not.toBeVisible();

    // Click to expand
    await disclosureButton.click();

    // Content should now be visible
    await expect(page.getByText('Disclaimer: This index measures')).toBeVisible();
    await expect(page.getByText('Prices: Nominal price data derived')).toBeVisible();
  });
});
