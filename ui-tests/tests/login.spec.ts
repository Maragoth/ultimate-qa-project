import { test, expect } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';
import { createRandomUserViaAPI } from '../helpers/apiHelpers';

test('User can login successfully using dynamic user', async ({ page }) => {
  const user = await createRandomUserViaAPI();

  const loginPage = new LoginPage(page);
  await loginPage.navigate();
  await loginPage.login(user.email, user.password);

  await expect(page.locator('text=Your Feed')).toBeVisible({ timeout: 10000 });
});
