import { test, expect, chromium } from '@playwright/test';
import { createRandomUserViaAPI } from '../helpers/apiHelpers';
import { setupUserSession } from '../helpers/sessionHelpers';

const NEW_PASSWORD = 'NewPass123!';

test('User can update password and log in with new password', async () => {
  // Step 1: Create new user via API
  const user = await createRandomUserViaAPI();

  // Step 2: Launch browser and authenticate session
  const browser = await chromium.launch();
  const context = await browser.newContext();
  const page = await context.newPage();
  await setupUserSession(page, user.token, user.username);

  // Step 3: Navigate to settings page and update password
  await page.goto('http://localhost:4100/settings');
  await page.locator('input[placeholder="New Password"]').fill(NEW_PASSWORD);

  await Promise.all([
    page.waitForURL('http://localhost:4100/', { timeout: 10000 }),
    page.locator('button:has-text("Update Settings")').click(),
  ]);

  // Step 4: Go back to settings and log out
  await page.goto('http://localhost:4100/settings');
  await page.locator('button.btn-outline-danger:has-text("Or click here to logout.")').click();

  // Step 5: Log in using new password
  await page.goto('http://localhost:4100/login');
  await page.locator('input[placeholder="Email"]').fill(user.email);
  await page.locator('input[placeholder="Password"]').fill(NEW_PASSWORD);

  await Promise.all([
    page.waitForNavigation({ url: 'http://localhost:4100/', timeout: 10000 }),
    page.locator('button:has-text("Sign in")').click()
  ]);

  // Step 6: Verify user is logged in by checking nav link with username
  await expect(page.locator(`a.nav-link:has-text("${user.username}")`)).toBeVisible();

  // Step 7: Cleanup
  await browser.close();
});
