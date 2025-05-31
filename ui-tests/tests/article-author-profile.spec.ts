import { test, expect } from '@playwright/test';
import { createRandomUserViaAPI, createArticleViaAPI } from '../helpers/apiHelpers';
import { setupUserSession } from '../helpers/sessionHelpers';

test('Clicking author name under article opens profile with user articles', async ({ browser }) => {
  const context = await browser.newContext();
  const page = await context.newPage();

  const user = await createRandomUserViaAPI();
  await setupUserSession(page, user.token, user.username);

  const article = await createArticleViaAPI(user.token, {
    title: 'Profile-Article',
    description: 'Desc',
    body: 'Body',
    tagList: ['test'],
  });

  // Go to Global Feed
  await page.goto('http://localhost:4100/');
  await page.getByRole('link', { name: 'Global Feed' }).click();

  // Find the article and click on the author's name
  const articleLocator = page.locator('.article-preview', { hasText: article.title });
  await expect(articleLocator).toBeVisible();

  const authorLink = articleLocator.locator('a.author');
  await authorLink.click();

  // Expect to land on the profile page with "My Articles" tab
  await expect(page).toHaveURL(new RegExp(`/@${user.username}$`));
  await expect(page.locator('.articles-toggle .nav-link.active')).toHaveText('My Articles');


  // Expect the article to be listed
  const articles = page.locator('.article-preview');
  await expect(articles).toHaveCount(1);
  await expect(articles.first()).toContainText(article.title);

  await context.close();
});
