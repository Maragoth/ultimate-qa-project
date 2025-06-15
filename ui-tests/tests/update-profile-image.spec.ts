import { test, expect, chromium } from '@playwright/test';
import { createRandomUserViaAPI } from '../helpers/apiHelpers';
import { setupUserSession } from '../helpers/sessionHelpers';

test('User can update profile image URL and see it on profile', async () => {
  // Step 1: Create new user via API
  const user = await createRandomUserViaAPI();
  const imageUrl = 'https://evek.one/4432-large_default/test.jpg';

  // Step 2: Launch browser and authenticate session
  const browser = await chromium.launch();
  const context = await browser.newContext();
  const page = await context.newPage();
  await setupUserSession(page, user.token, user.username);

  // Step 3: Go to settings and update profile image URL
  await page.goto('http://localhost:4100/settings');
  await page.locator('input[placeholder="URL of profile picture"]').fill(imageUrl);
  await page.locator('button:has-text("Update Settings")').click();

  // Step 4: Navigate to user profile page
  await page.goto(`http://localhost:4100/@${user.username}`);

  // Step 5: Verify updated image is visible on profile
  const profilePic = page.locator(`img.user-img[src="${imageUrl}"]`);
  await expect(profilePic).toBeVisible();

  // Step 6: Cleanup
  await browser.close();
});
