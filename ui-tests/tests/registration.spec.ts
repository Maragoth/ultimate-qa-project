import { test, expect } from '@playwright/test';
import { RegistrationPage } from '../pages/RegistrationPage';
import { generateRandomUser } from '../helpers/testData';

let user = generateRandomUser();

test('User can register successfully', async ({ page }) => {
  const registrationPage = new RegistrationPage(page);
  await registrationPage.navigate();
  await registrationPage.register(user.username, user.email, user.password);
  await expect(page.locator('a.nav-link', { hasText: user.username })).toBeVisible();
});

test('Should show error for invalid email', async ({ page }) => {
  const registrationPage = new RegistrationPage(page);
  await registrationPage.navigate();
  await registrationPage.register(user.username, 'invalidemail.com', user.password);
  const emailInput = page.locator('input[placeholder="Email"]');
  await emailInput.fill('invalidemail.com');
  const isValid = await emailInput.evaluate((el) => (el as HTMLInputElement).checkValidity());
  expect(isValid).toBe(false);
});
