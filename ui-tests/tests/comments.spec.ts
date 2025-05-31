import { test, expect } from '@playwright/test';
import { createRandomUserViaAPI, createArticleViaAPI } from '../helpers/apiHelpers';
import { setupUserSession } from '../helpers/sessionHelpers';
import { generateArticle } from '../helpers/testData';

test('User can add and delete a comment', async ({ browser }) => {
  const user = await createRandomUserViaAPI();
  const article = generateArticle('Comment article', 'Test comment feature');
  const createdArticle = await createArticleViaAPI(user.token, article);

  const context = await browser.newContext();
  const page = await context.newPage();

  await page.goto('http://localhost:4100');
  await setupUserSession(page, user.token, user.username);

  await page.goto(`http://localhost:4100/article/${createdArticle.slug}`);

  const commentText = `Test comment ${Date.now()}`;
  await page.fill('textarea[placeholder="Write a comment..."]', commentText);
  await page.click('button:has-text("Post Comment")');

  const commentLocator = page.locator('.card-text', { hasText: commentText });
  await expect(commentLocator).toBeVisible();

  const allCards = page.locator('.card');
  const targetCard = allCards.filter({ hasText: commentText });

  const trashIcon = targetCard.locator('.ion-trash-a');
  await trashIcon.evaluate((el: HTMLElement) => el.click());

  await expect(commentLocator).toHaveCount(0);

  await context.close();
});
