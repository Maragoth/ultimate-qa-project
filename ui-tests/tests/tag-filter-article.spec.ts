import { test, expect } from '@playwright/test';
import { createRandomUserViaAPI, createArticleViaAPI } from '../helpers/apiHelpers';
import { setupUserSession } from '../helpers/sessionHelpers';

test('Clicking a tag below an article filters articles by that tag', async ({ browser }) => {
  // Known Issue:
  // - When clicking a tag below an article, it redirects to the article preview
  // - Instead, it should filter articles by that tag (like Popular Tags feature)
  // - Bug documented in docs/bug-tag-click-redirect/
  // - Expected: Tag filter view with all articles having that tag
  // - Actual: Redirects to article preview page
  
  const context = await browser.newContext();
  const page = await context.newPage();

  const user = await createRandomUserViaAPI();
  await setupUserSession(page, user.token, user.username);

  const tag = `Tag-${Math.floor(Math.random() * 1000000)}`;

  // Create two articles with the same tag via API
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

  // Find article and click its tag
  const articleLocator = page.locator('.article-preview', { hasText: article1.title });
  await expect(articleLocator).toBeVisible();

  const tagLocator = articleLocator.locator(`.tag-list >> text=${tag}`);
  await tagLocator.click();

  // Bug verification:
  // 1. Instead of showing tag filter view, we're redirected to article preview
  const articleTitle = page.locator('h1', { hasText: article1.title });
  await expect(articleTitle).toBeVisible();

  // 2. URL should contain /tag/{tag} but contains /article/{slug} instead
  const currentUrl = page.url();
  expect(currentUrl).toContain(`/article/${article1.slug}`);
  expect(currentUrl).not.toContain(`/tag/${tag}`);

  // 3. The other article with the same tag is not visible
  const otherArticle = page.locator('.article-preview', { hasText: article2.title });
  await expect(otherArticle).not.toBeVisible();

  await context.close();
});
