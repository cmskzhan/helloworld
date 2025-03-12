import { test, expect } from '@playwright/test';

test('test', async ({ page }) => {
  await page.goto('https://www.vanguardinvestor.co.uk/investments/vanguard-japan-stock-index-fund-gbp-acc/overview');
  await page.getByRole('button', { name: 'Accept all cookies' }).click();
  // Use the provided XPath to locate the element
  const priceElement = page.locator(
    'xpath=/html/body/retail-direct-root/main/ukd-fund-detail/div[2]/ukd-overview/div[1]/ukd-nav-price-card/div/section/strong'
  );

  // Assert that the element is visible
  await expect(priceElement).toBeVisible();

  // Get the text content of the element
  const priceText = await priceElement.textContent();

  // Assert that the text content is as expected
  await expect(priceText?.trim()).toBe('£313.91');
});