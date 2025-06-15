import { test, expect } from '@playwright/test';
import { RegistrationPage } from '../pages/RegistrationPage';
import { generateRandomUser } from '../helpers/testData';

test('User can register successfully', async ({ page }) => {
  // Step 1: Generate a unique test user
  const user = generateRandomUser();

  // Step 2: Go to registration page and register the user
  const registrationPage = new RegistrationPage(page);
  await registrationPage.navigate();
  await registrationPage.register(user.username, user.email, user.password);

  // Step 3: Verify that username appears in navbar after registration
  await expect(page.locator('a.nav-link', { hasText: user.username })).toBeVisible();
});

test('Should show error for invalid email', async ({ page }) => {
  // Step 1: Generate a test user
  const user = generateRandomUser();

  // Step 2: Go to registration page and attempt registration with invalid email
  const registrationPage = new RegistrationPage(page);
  await registrationPage.navigate();
  await registrationPage.register(user.username, 'invalidemail.com', user.password);

  // Step 3: Verify that email field is invalid
  const emailInput = page.locator('input[placeholder="Email"]');
  await emailInput.fill('invalidemail.com');
  const isValid = await emailInput.evaluate((el) => (el as HTMLInputElement).checkValidity());
  expect(isValid).toBe(false);
});
