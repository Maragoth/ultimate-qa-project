import { test, expect, chromium } from '@playwright/test';
import { createRandomUserViaAPI } from '../helpers/apiHelpers';
import { setupUserSession } from '../helpers/sessionHelpers';

test('Navigation bar reflects login state correctly', async () => {
  const user = await createRandomUserViaAPI();

  const browser = await chromium.launch();
  const context = await browser.newContext();
  const page = await context.newPage();

  // Check navbar when logged out
  await page.goto('http://localhost:4100/');
  await expect(page.locator('a.nav-link:has-text("Home")')).toBeVisible();
  await expect(page.locator('a.nav-link:has-text("Sign in")')).toBeVisible();
  await expect(page.locator('a.nav-link:has-text("Sign up")')).toBeVisible();
  await expect(page.locator('a.nav-link:has-text("New Post")')).toHaveCount(0);
  await expect(page.locator('a.nav-link:has-text("Settings")')).toHaveCount(0);

  // Login via token and check navbar
  await setupUserSession(page, user.token, user.username);
  await page.reload();

  await expect(page.locator('a.nav-link:has-text("Home")')).toBeVisible();
  await expect(page.locator('a.nav-link:has-text("New Post")')).toBeVisible();
  await expect(page.locator('a.nav-link:has-text("Settings")')).toBeVisible();
  await expect(page.locator(`a.nav-link:has-text("${user.username}")`)).toBeVisible();
  await expect(page.locator('a.nav-link:has-text("Sign in")')).toHaveCount(0);
  await expect(page.locator('a.nav-link:has-text("Sign up")')).toHaveCount(0);

  await browser.close();
});
