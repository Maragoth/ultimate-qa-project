import { test, expect } from '@playwright/test';
import { ArticlePage } from '../pages/ArticlePage';
import { createRandomUserViaAPI, createArticleViaAPI } from '../helpers/apiHelpers';
import { generateArticle } from '../helpers/testData';
import { setupUserSession } from '../helpers/sessionHelpers';

test('User can favorite and unfavorite an article from profile', async ({ page }) => {
  const user = await createRandomUserViaAPI();
  const article = generateArticle('Favorite', `Tag-${Math.floor(Math.random() * 1000000)}`);
  const created = await createArticleViaAPI(user.token, article);
  await setupUserSession(page, user.token, user.username);

  const articlePage = new ArticlePage(page);

  await page.goto('/');
  await page.click('text=Global Feed');
  const preview = page.locator(`.article-preview:has(h1:has-text("${article.title}"))`);
  const heart = preview.locator('button:has(.ion-heart)');
  await expect(heart).toBeVisible({ timeout: 5000 });
  await Promise.all([
    page.waitForResponse(resp => resp.url().includes('/favorite') && resp.status() === 200),
    heart.click({ force: true })
  ]);

  await page.goto(`http://localhost:4100/@${user.username}`);
  await expect(page).toHaveURL(new RegExp(`@${user.username}$`), { timeout: 10000 });
  await page.waitForSelector('.article-preview', { timeout: 10000 });

  await page.click('a.nav-link:has-text("Favorited Articles")');
  await expect(page.locator('.article-preview')).toBeVisible({ timeout: 10000 });


  const favorited = page.locator(`.article-preview:has(h1:has-text("${article.title}"))`);
  await expect(favorited).toBeVisible({ timeout: 10000 });

  const unfavHeart = favorited.locator('button:has(.ion-heart)');
  await expect(unfavHeart).toBeVisible({ timeout: 5000 });
  await Promise.all([
    page.waitForResponse(resp => resp.url().includes('/favorite') && resp.status() === 200),
    unfavHeart.click({ force: true })
  ]);
  await page.waitForTimeout(1000);

  await page.goto(`http://localhost:4100/@${user.username}/favorites`);
  await page.waitForLoadState('networkidle');
  const articlePreview = page.locator(`.article-preview:has(h1:has-text("${article.title}"))`);
  await expect(articlePreview).toHaveCount(0, { timeout: 10000 });
});
