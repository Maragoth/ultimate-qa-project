import { test, expect } from '@playwright/test';
import { generateArticle } from '../helpers/testData';
import { ArticlePage } from '../pages/ArticlePage';
import { createRandomUserViaAPI } from '../helpers/apiHelpers';

test('User can open correct article using "Read more" link', async ({ page }) => {
  const user = await createRandomUserViaAPI();
  const articlePage = new ArticlePage(page);

  await page.goto('/');
  await page.evaluate((token) => {
    localStorage.setItem('jwt', token);
  }, user.token);
  await page.reload();

  const tag = `TestTag-${Math.floor(Math.random() * 1000000)}`;
  const article = generateArticle('ReadMore', tag);

  await articlePage.navigateToEditor();
  await articlePage.createArticle(article.title, article.description, article.body, article.tags);

  const articlePreview = page.locator(`.article-preview:has(h1:has-text("${article.title}"))`);
  const isVisible = await articlePreview.first().isVisible({ timeout: 3000 }).catch(() => false);

  if (!isVisible) {
    await page.click("a.nav-link[href*='/@']");
    await page.waitForURL('**/@**');
  }

  const correctPreview = page.locator(`.article-preview:has(h1:has-text("${article.title}"))`);
  const readMoreLink = correctPreview.locator("a:has-text('Read more')");
  await readMoreLink.click();

  await expect(page).toHaveURL(/.*\/article\//);
  await expect(page.locator('h1')).toHaveText(article.title);
});
