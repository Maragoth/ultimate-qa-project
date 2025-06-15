import { test, expect } from '@playwright/test';
import { ArticlePage } from '../pages/ArticlePage';
import { generateArticle } from '../helpers/testData';
import { createRandomUserViaAPI } from '../helpers/apiHelpers';
import { setupUserSession } from '../helpers/sessionHelpers';

test('User can create a new article', async ({ page }) => {
  // Step 1: Create a random user via API
  const user = await createRandomUserViaAPI();

  // Step 2: Initialize the ArticlePage object
  const articlePage = new ArticlePage(page);

  // Step 3: Inject auth token into localStorage and reload the page
  await setupUserSession(page, user.token, user.username);

  // Step 4: Generate unique article data
  const article = generateArticle('Create', `TestTag-${Math.floor(Math.random() * 1000000)}`);

  // Step 5: Navigate to the article editor and create the article via UI
  await articlePage.navigateToEditor();
  await articlePage.createArticle(article.title, article.description, article.body, article.tags);

  // Step 6: Verify that the article title matches the expected title
  const actualTitle = await articlePage.getArticleTitle();
  expect(actualTitle).toBe(article.title);
});
