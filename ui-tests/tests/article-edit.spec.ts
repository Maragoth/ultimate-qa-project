import { test, expect } from '@playwright/test';
import { ArticlePage } from '../pages/ArticlePage';
import { generateArticle } from '../helpers/testData';
import { createRandomUserViaAPI, createArticleViaAPI } from '../helpers/apiHelpers';
import { setupUserSession } from '../helpers/sessionHelpers';

test('User can edit an existing article', async ({ page }) => {
  // Step 1: Create a test user via API
  const user = await createRandomUserViaAPI();

  // Step 2: Generate original and updated article data
  const original = generateArticle('Edit-Original', `Tag-${Math.floor(Math.random() * 1000000)}`);
  const updated = generateArticle('Edit-Updated', original.tags[0]);

  // Step 3: Create the article via API as the test user
  const created = await createArticleViaAPI(user.token, original);

  // Step 4: Set up user session in browser
  await setupUserSession(page, user.token, user.username);

  // Step 5: Navigate to the article page
  await page.goto(`/article/${created.slug}`);

  // Step 6: Click the edit button to open the editor
  const articlePage = new ArticlePage(page);
  await articlePage.clickEditButton();

  // Step 7: Fill in the updated article data and submit
  await articlePage.editArticle(updated.title, updated.description, updated.body);

  // Step 8: Verify that the article title was updated successfully
  const visibleTitle = await articlePage.getArticleTitle();
  expect(visibleTitle).toBe(updated.title);
});
