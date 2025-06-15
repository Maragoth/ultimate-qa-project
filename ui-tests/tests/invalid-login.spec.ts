import { test, expect, chromium } from '@playwright/test';

// Invalid login attempt should show error message

test('Invalid login displays error message', async () => {
  // Step 1: Launch a new browser context
  const browser = await chromium.launch();
  const context = await browser.newContext();
  const page = await context.newPage();

  // Step 2: Navigate to login page
  await page.goto('http://localhost:4100/login');

  // Step 3: Enter invalid credentials
  await page.locator('input[placeholder="Email"]').fill('wrong@email.com');
  await page.locator('input[placeholder="Password"]').fill('wrongpass');

  // Step 4: Click the "Sign in" button
  await page.locator('button:has-text("Sign in")').click();

  // Step 5: Assert that the error message is displayed
  await expect(page.locator('.error-messages')).toContainText('email or password is invalid');

  // Step 6: Close browser
  await browser.close();
});
