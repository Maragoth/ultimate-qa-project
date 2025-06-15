import { test, expect } from '@playwright/test';
import { createRandomUserViaAPI, createArticleViaAPI } from '../helpers/apiHelpers';
import { generateArticle } from '../helpers/testData';
import { setupUserSession } from '../helpers/sessionHelpers';

test('User can favorite and unfavorite an article from profile', async ({ page }) => {
  // Step 1: Create test user and article via API
  const user = await createRandomUserViaAPI();
  const article = generateArticle('Favorite', `Tag-${Math.floor(Math.random() * 1000000)}`);
  await createArticleViaAPI(user.token, article);

  // Step 2: Setup user session in browser
  await setupUserSession(page, user.token, user.username);

  // Step 3: Navigate to homepage and locate article preview
  await page.goto('/');
  await page.click('text=Global Feed');

  const preview = page.locator(`.article-preview:has(h1:has-text("${article.title}"))`);
  const heart = preview.locator('button:has(.ion-heart)');
  await expect(heart).toBeVisible({ timeout: 5000 });

  // Step 4: Favorite the article (wait for /favorite response)
  await Promise.all([
    page.waitForResponse(resp => resp.url().includes('/favorite') && resp.status() === 200),
    heart.click({ force: true })
  ]);

  // Step 5: Navigate to user's profile page
  await page.goto(`http://localhost:4100/@${user.username}`);
  await expect(page).toHaveURL(new RegExp(`@${user.username}$`), { timeout: 10000 });
  await page.waitForSelector('.article-preview', { timeout: 10000 });

  // Step 6: Open the "Favorited Articles" tab
  await page.click('a.nav-link:has-text("Favorited Articles")');
  await expect(page.locator('.article-preview')).toBeVisible({ timeout: 10000 });

  // Step 7: Locate favorited article and unfavorite it
  const favorited = page.locator(`.article-preview:has(h1:has-text("${article.title}"))`);
  await expect(favorited).toBeVisible({ timeout: 10000 });

  const unfavHeart = favorited.locator('button:has(.ion-heart)');
  await expect(unfavHeart).toBeVisible({ timeout: 5000 });

  await Promise.all([
    page.waitForResponse(resp => resp.url().includes('/favorite') && resp.status() === 200),
    unfavHeart.click({ force: true })
  ]);

  // Step 8: Verify that article is no longer listed in favorites
  await page.waitForTimeout(1000);
  await page.goto(`http://localhost:4100/@${user.username}/favorites`);
  await page.waitForLoadState('networkidle');

  const articlePreview = page.locator(`.article-preview:has(h1:has-text("${article.title}"))`);
  await expect(articlePreview).toHaveCount(0, { timeout: 10000 });
});
