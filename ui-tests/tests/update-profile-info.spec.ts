import { test, expect, chromium } from '@playwright/test';
import { createRandomUserViaAPI } from '../helpers/apiHelpers';
import { setupUserSession } from '../helpers/sessionHelpers';

test('User can update profile info: username, bio, and email', async () => {
  const user = await createRandomUserViaAPI();

  const browser = await chromium.launch();
  const context = await browser.newContext();
  const page = await context.newPage();
  await setupUserSession(page, user.token, user.username);

  await page.goto('http://localhost:4100/settings');

  // Fill in new data
  const newUsername = user.username + '_updated';
  const newEmail = 'updated_' + user.email;
  const newBio = 'Short bio for test';

  await page.locator('input[placeholder="Username"]').fill(newUsername);
  await page.locator('input[placeholder="Email"]').fill(newEmail);
  await page.locator('textarea[placeholder="Short bio about you"]')
    .fill(newBio);

  // Click Update Settings
  await page.locator('button:has-text("Update Settings")').click();

  // Navigate again to settings to verify changes
  await page.goto('http://localhost:4100/settings');

  await expect(page.locator('input[placeholder="Username"]')).toHaveValue(newUsername);
  await expect(page.locator('input[placeholder="Email"]')).toHaveValue(newEmail);
  await expect(page.locator('textarea[placeholder="Short bio about you"]'))
    .toHaveValue(newBio);

  await browser.close();
});
