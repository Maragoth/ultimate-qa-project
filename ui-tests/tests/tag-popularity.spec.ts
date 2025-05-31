import { test, expect } from '@playwright/test';
import { createRandomUserViaAPI, createArticleViaAPI } from '../helpers/apiHelpers';
import { setupUserSession } from '../helpers/sessionHelpers';

test('Tag from new articles appears in "Popular Tags"', async ({ browser }) => {
  const context = await browser.newContext();
  const page = await context.newPage();

  const user = await createRandomUserViaAPI();
  await setupUserSession(page, user.token, user.username);

  const tag = `TestTag-${Math.floor(Math.random() * 1000000)}`;

  // Create two articles with the same tag
  await createArticleViaAPI(user.token, {
    title: 'Popular-A',
    description: 'Desc A',
    body: 'Body A',
    tagList: [tag],
  });

  await createArticleViaAPI(user.token, {
    title: 'Popular-B',
    description: 'Desc B',
    body: 'Body B',
    tagList: [tag],
  });

  // Go to homepage and check Popular Tags
  await page.goto('http://localhost:4100/');

  let popularTags: string[] = [];
  for (let i = 0; i < 5; i++) {
    await page.waitForTimeout(1000);
    await page.reload();
    popularTags = await page.locator('.tag-list a').allTextContents();
    if (popularTags.map(t => t.trim()).includes(tag)) break;
  }

  expect(popularTags.map(t => t.trim())).toContain(tag);

  await context.close();
});
