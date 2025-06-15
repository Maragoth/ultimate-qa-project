import { test, expect } from '@playwright/test';
import { ArticlePage } from '../pages/ArticlePage';
import { createRandomUserViaAPI, createArticleViaAPI } from '../helpers/apiHelpers';
import { setupUserSession } from '../helpers/sessionHelpers';
import { generateArticle } from '../helpers/testData';

test('User can delete an article', async ({ browser }) => {
  // Step 1: Create a random test user via API
  const user = await createRandomUserViaAPI();

  // Step 2: Generate article data
  const article = generateArticle('Delete', `TestTag-${Math.floor(Math.random() * 1000000)}`);

  // Step 3: Create the article via API using the test user
  const createdArticle = await createArticleViaAPI(user.token, article);

  // Step 4: Launch a new browser context and page
  const context = await browser.newContext();
  const page = await context.newPage();
  const articlePage = new ArticlePage(page);

  // Step 5: Open the homepage and inject user session
  await page.goto('http://localhost:4100');
  await setupUserSession(page, user.token, user.username);

  // Step 6: Navigate directly to the article page
  await page.goto(`http://localhost:4100/article/${createdArticle.slug}`);

  // Step 7: Delete the article via UI
  await articlePage.deleteArticle();

  // Step 8: Verify that we are redirected to the homepage
  await expect(page).toHaveURL('http://localhost:4100/');

  // Step 9: Verify that the deleted article is no longer listed
  await expect(page.locator(`a:has-text("${article.title}")`)).toHaveCount(0);

  // Step 10: Close the browser context
  await context.close();
});
