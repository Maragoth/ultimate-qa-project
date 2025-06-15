import { test, expect, chromium } from '@playwright/test';
import { createRandomUserViaAPI } from '../helpers/apiHelpers';
import { setupUserSession } from '../helpers/sessionHelpers';

test('Navigation bar reflects login state correctly', async () => {
  // Step 1: Create a test user
  const user = await createRandomUserViaAPI();

  // Step 2: Launch a new browser context
  const browser = await chromium.launch();
  const context = await browser.newContext();
  const page = await context.newPage();

  // Step 3: Visit homepage while logged out and check navbar elements
  await page.goto('http://localhost:4100/');
  await expect(page.locator('a.nav-link:has-text("Home")')).toBeVisible();
  await expect(page.locator('a.nav-link:has-text("Sign in")')).toBeVisible();
  await expect(page.locator('a.nav-link:has-text("Sign up")')).toBeVisible();
  await expect(page.locator('a.nav-link:has-text("New Post")')).toHaveCount(0);
  await expect(page.locator('a.nav-link:has-text("Settings")')).toHaveCount(0);

  // Step 4: Log in using token injection and reload the page
  await setupUserSession(page, user.token, user.username);
  await page.reload();

  // Step 5: Verify navbar reflects logged-in state
  await expect(page.locator('a.nav-link:has-text("Home")')).toBeVisible();
  await expect(page.locator('a.nav-link:has-text("New Post")')).toBeVisible();
  await expect(page.locator('a.nav-link:has-text("Settings")')).toBeVisible();
  await expect(page.locator(`a.nav-link:has-text("${user.username}")`)).toBeVisible();
  await expect(page.locator('a.nav-link:has-text("Sign in")')).toHaveCount(0);
  await expect(page.locator('a.nav-link:has-text("Sign up")')).toHaveCount(0);

  // Step 6: Close browser
  await browser.close();
});
