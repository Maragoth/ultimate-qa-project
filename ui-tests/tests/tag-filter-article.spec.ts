import { test, expect } from '@playwright/test';
import { createRandomUserViaAPI, createArticleViaAPI } from '../helpers/apiHelpers';
import { setupUserSession } from '../helpers/sessionHelpers';

test('Clicking a tag below an article filters articles by that tag', async ({ browser }) => {
  const context = await browser.newContext();
  const page = await context.newPage();

  const user = await createRandomUserViaAPI();
  await setupUserSession(page, user.token, user.username);

  const tag = `Tag-${Math.floor(Math.random() * 1000000)}`;

  // Create two articles with the same tag
  const article1 = await createArticleViaAPI(user.token, {
    title: 'Tagged-Article-A',
    description: 'Description A',
    body: 'Body A',
    tagList: [tag],
  });

  const article2 = await createArticleViaAPI(user.token, {
    title: 'Tagged-Article-B',
    description: 'Description B',
    body: 'Body B',
    tagList: [tag],
  });

  // Go to Global Feed
  await page.goto('http://localhost:4100/');
  await page.getByRole('link', { name: 'Global Feed' }).click();

  // Find article created via API and click its tag
  const articleLocator = page.locator('.article-preview', { hasText: article1.title });
  await expect(articleLocator).toBeVisible();

  const tagLocator = articleLocator.locator(`.tag-list >> text=${tag}`);
  await tagLocator.click();

  // Validate that both tagged articles are shown
  const articlePreviews = page.locator('.article-preview');
  await expect(articlePreviews.locator(`text=${article1.title}`)).toBeVisible();
  await expect(articlePreviews.locator(`text=${article2.title}`)).toBeVisible();

  // Optionally check count = 2
  await expect(articlePreviews).toHaveCount(2);

  await context.close();
});
