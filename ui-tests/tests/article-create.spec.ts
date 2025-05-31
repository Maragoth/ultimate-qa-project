import { test, expect } from '@playwright/test';
import { ArticlePage } from '../pages/ArticlePage';
import { generateArticle } from '../helpers/testData';
import { createRandomUserViaAPI } from '../helpers/apiHelpers';

test('User can create a new article', async ({ page }) => {
  const user = await createRandomUserViaAPI();
  const articlePage = new ArticlePage(page);

  // Inject token into localStorage and reload
  await page.goto('/');
  await page.evaluate((token) => {
    localStorage.setItem('jwt', token);
  }, user.token);
  await page.reload();

  // Create article via UI
  const article = generateArticle('Create', `TestTag-${Math.floor(Math.random() * 1000000)}`);

  await articlePage.navigateToEditor();
  await articlePage.createArticle(article.title, article.description, article.body, article.tags);

  const actualTitle = await articlePage.getArticleTitle();
  expect(actualTitle).toBe(article.title);
});
