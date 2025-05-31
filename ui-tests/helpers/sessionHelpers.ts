import { Page } from '@playwright/test';

export async function setupUserSession(page: Page, token: string, username: string) {
  await page.goto('/');
  await page.evaluate((jwt) => {
    localStorage.setItem('jwt', jwt);
  }, token);

  await page.reload();

  // Trigger the frontend to recognize the logged-in user
  await page.request.get('http://localhost:3000/api/user', {
    headers: { Authorization: `Token ${token}` }
  });

  // Wait until the username appears in the navbar
  await page.waitForSelector(`a.nav-link[href="/@${username}"]`, { timeout: 5000 });
}
