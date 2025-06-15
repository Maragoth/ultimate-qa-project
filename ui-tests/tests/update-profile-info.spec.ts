import { test, expect, chromium } from '@playwright/test';
import { createRandomUserViaAPI } from '../helpers/apiHelpers';
import { setupUserSession } from '../helpers/sessionHelpers';

test('User can update profile info: username, bio, and email', async () => {
  // Step 1: Create new user via API
  const user = await createRandomUserViaAPI();

  // Step 2: Launch browser and authenticate session
  const browser = await chromium.launch();
  const context = await browser.newContext();
  const page = await context.newPage();
  await setupUserSession(page, user.token, user.username);

  // Step 3: Go to settings page
  await page.goto('http://localhost:4100/settings');

  // Step 4: Define new profile data
  const newUsername = user.username + '_updated';
  const newEmail = 'updated_' + user.email;
  const newBio = 'Short bio for test';

  // Step 5: Fill in updated profile fields
  await page.locator('input[placeholder="Username"]').fill(newUsername);
  await page.locator('input[placeholder="Email"]').fill(newEmail);
  await page.locator('textarea[placeholder="Short bio about you"]').fill(newBio);

  // Step 6: Submit the form
  await page.locator('button:has-text("Update Settings")').click();

  // Step 7: Revisit settings to verify changes were saved
  await page.goto('http://localhost:4100/settings');
  await expect(page.locator('input[placeholder="Username"]')).toHaveValue(newUsername);
  await expect(page.locator('input[placeholder="Email"]')).toHaveValue(newEmail);
  await expect(page.locator('textarea[placeholder="Short bio about you"]')).toHaveValue(newBio);

  // Step 8: Cleanup
  await browser.close();
});
