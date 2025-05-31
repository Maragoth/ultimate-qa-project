import { test, expect, chromium } from '@playwright/test';
import { createRandomUserViaAPI } from '../helpers/apiHelpers';
import { setupUserSession } from '../helpers/sessionHelpers';

const NEW_PASSWORD = 'NewPass123!';

test('User can update password and log in with new password', async () => {
  const user = await createRandomUserViaAPI();

  const browser = await chromium.launch();
  const context = await browser.newContext();
  const page = await context.newPage();
  await setupUserSession(page, user.token, user.username);

  // Go to settings and update password
  await page.goto('http://localhost:4100/settings');
  await page.locator('input[placeholder="New Password"]').fill(NEW_PASSWORD);

  await Promise.all([
    page.waitForURL('http://localhost:4100/', { timeout: 10000 }),
    page.locator('button:has-text("Update Settings")').click(),
  ]);

  // Navigate back to settings and logout
  await page.goto('http://localhost:4100/settings');
  await page.locator('button.btn-outline-danger:has-text("Or click here to logout.")').click();

  // Login with new password
  await page.goto('http://localhost:4100/login');
  await page.locator('input[placeholder="Email"]').fill(user.email);
  await page.locator('input[placeholder="Password"]').fill(NEW_PASSWORD);

  await Promise.all([
    page.waitForNavigation({ url: 'http://localhost:4100/', timeout: 10000 }),
    page.locator('button:has-text("Sign in")').click()
  ]);

  await expect(page.locator(`a.nav-link:has-text("${user.username}")`)).toBeVisible();

  await browser.close();
});
