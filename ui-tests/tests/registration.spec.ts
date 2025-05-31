import { test, expect } from '@playwright/test';
import { RegistrationPage } from '../pages/RegistrationPage';
import { generateRandomUser } from '../helpers/testData';

test('User can register via UI', async ({ page }) => {
  const registrationPage = new RegistrationPage(page);
  const user = generateRandomUser();

  await registrationPage.navigate();
  await registrationPage.register(user.username, user.email, user.password);

  await expect(page).toHaveURL('http://localhost:4100/');
  await expect(page.locator('text=Your Feed')).toBeVisible({ timeout: 10000 });
});
