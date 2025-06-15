import { test, expect } from '@playwright/test';
import { createRandomUserViaAPI, createArticleViaAPI } from '../helpers/apiHelpers';
import { setupUserSession } from '../helpers/sessionHelpers';
import { generateArticle } from '../helpers/testData';

test('User can add and delete a comment', async ({ browser }) => {
  // Step 1: Create test user and article via API
  const user = await createRandomUserViaAPI();
  const article = generateArticle('Comment article', 'Test comment feature');
  const createdArticle = await createArticleViaAPI(user.token, article);

  // Step 2: Start new browser context and set user session
  const context = await browser.newContext();
  const page = await context.newPage();

  await page.goto('http://localhost:4100');
  await setupUserSession(page, user.token, user.username);

  // Step 3: Open the article page
  await page.goto(`http://localhost:4100/article/${createdArticle.slug}`);

  // Step 4: Add a new comment via UI
  const commentText = `Test comment ${Date.now()}`;
  await page.fill('textarea[placeholder="Write a comment..."]', commentText);
  await page.click('button:has-text("Post Comment")');

  // Step 5: Verify that the comment was added
  const commentLocator = page.locator('.card-text', { hasText: commentText });
  await expect(commentLocator).toBeVisible();

  // Step 6: Find the comment container and delete the comment
  const allCards = page.locator('.card');
  const targetCard = allCards.filter({ hasText: commentText });

  const trashIcon = targetCard.locator('.ion-trash-a');
  await trashIcon.evaluate((el: HTMLElement) => el.click());

  // Step 7: Verify that the comment was deleted
  await expect(commentLocator).toHaveCount(0);

  // Step 8: Close browser context
  await context.close();
});
