import { test, expect, chromium } from '@playwright/test';

// Invalid login attempt should show error message

test('Invalid login displays error message', async () => {
  const browser = await chromium.launch();
  const context = await browser.newContext();
  const page = await context.newPage();

  await page.goto('http://localhost:4100/login');
  await page.locator('input[placeholder="Email"]').fill('wrong@email.com');
  await page.locator('input[placeholder="Password"]').fill('wrongpass');
  await page.locator('button:has-text("Sign in")').click();

  await expect(page.locator('.error-messages')).toContainText('email or password is invalid');

  await browser.close();
});
