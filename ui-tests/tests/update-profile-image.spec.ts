import { test, expect, chromium } from '@playwright/test';
import { createRandomUserViaAPI } from '../helpers/apiHelpers';
import { setupUserSession } from '../helpers/sessionHelpers';

test('User can update profile image URL and see it on profile', async () => {
  const user = await createRandomUserViaAPI();
  const imageUrl = 'https://evek.one/4432-large_default/test.jpg';

  const browser = await chromium.launch();
  const context = await browser.newContext();
  const page = await context.newPage();
  await setupUserSession(page, user.token, user.username);

  // Go to settings and update image URL
  await page.goto('http://localhost:4100/settings');
  await page.locator('input[placeholder="URL of profile picture"]').fill(imageUrl);
  await page.locator('button:has-text("Update Settings")').click();

  // Go to profile page
  await page.goto(`http://localhost:4100/@${user.username}`);

  // Check image is updated
  const profilePic = page.locator(`img.user-img[src="${imageUrl}"]`);
  await expect(profilePic).toBeVisible();

  await browser.close();
});