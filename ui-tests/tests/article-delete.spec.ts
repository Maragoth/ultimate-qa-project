import { test, expect } from '@playwright/test';
import { ArticlePage } from '../pages/ArticlePage';
import { createRandomUserViaAPI, createArticleViaAPI } from '../helpers/apiHelpers';
import { setupUserSession } from '../helpers/sessionHelpers';
import { generateArticle } from '../helpers/testData';

test('User can delete an article', async ({ browser }) => {
  const user = await createRandomUserViaAPI();
  const article = generateArticle('Delete', `TestTag-${Math.floor(Math.random() * 1000000)}`);
  const createdArticle = await createArticleViaAPI(user.token, article);

  const context = await browser.newContext();
  const page = await context.newPage();
  const articlePage = new ArticlePage(page);

  await page.goto('http://localhost:4100');
  await setupUserSession(page, user.token, user.username);
  await page.goto(`http://localhost:4100/article/${createdArticle.slug}`);

  await articlePage.deleteArticle();

  await expect(page).toHaveURL('http://localhost:4100/');
  await expect(page.locator(`a:has-text("${article.title}")`)).toHaveCount(0);

  await context.close();
});
