import { test, expect } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';
import { createRandomUserViaAPI } from '../helpers/apiHelpers';

test('User can login successfully using dynamic user', async ({ page }) => {
  // Step 1: Create a random test user via API
  const user = await createRandomUserViaAPI();

  // Step 2: Initialize login page object and navigate to login page
  const loginPage = new LoginPage(page);
  await loginPage.navigate();

  // Step 3: Perform login using test user's credentials
  await loginPage.login(user.email, user.password);

  // Step 4: Verify successful login by checking "Your Feed" is visible
  await expect(page.locator('text=Your Feed')).toBeVisible({ timeout: 10000 });
});
