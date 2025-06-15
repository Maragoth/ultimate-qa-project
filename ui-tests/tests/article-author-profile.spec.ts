import { test, expect } from '@playwright/test';
import { createRandomUserViaAPI, createArticleViaAPI } from '../helpers/apiHelpers';
import { setupUserSession } from '../helpers/sessionHelpers';

test('Clicking author name under article opens profile with user articles', async ({ browser }) => {
  // Step 1: Create isolated browser context and page
  const context = await browser.newContext();
  const page = await context.newPage();

  // Step 2: Create a random user via API
  const user = await createRandomUserViaAPI();

  // Step 3: Set up user session using token and username
  await setupUserSession(page, user.token, user.username);

  // Step 4: Create an article via API using the test user
  const article = await createArticleViaAPI(user.token, {
    title: 'Profile-Article',
    description: 'Desc',
    body: 'Body',
    tagList: ['test'],
  });

  // Step 5: Go to Global Feed
  await page.goto('http://localhost:4100/');
  await page.getByRole('link', { name: 'Global Feed' }).click();

  // Step 6: Locate the article and click on the author's name
  const articleLocator = page.locator('.article-preview', { hasText: article.title });
  await expect(articleLocator).toBeVisible();

  const authorLink = articleLocator.locator('a.author');
  await authorLink.click();

  // Step 7: Verify that we are on the author's profile page with the "My Articles" tab active
  await expect(page).toHaveURL(new RegExp(`/@${user.username}$`));
  await expect(page.locator('.articles-toggle .nav-link.active')).toHaveText('My Articles');

  // Step 8: Verify that the article is listed in the author's profile
  const articles = page.locator('.article-preview');
  await expect(articles).toHaveCount(1);
  await expect(articles.first()).toContainText(article.title);

  // Step 9: Close browser context
  await context.close();
});
