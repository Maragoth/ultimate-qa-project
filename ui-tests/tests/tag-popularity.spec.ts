import { test, expect } from '@playwright/test';
import { createRandomUserViaAPI, createArticleViaAPI } from '../helpers/apiHelpers';
import { setupUserSession } from '../helpers/sessionHelpers';

test('Tag from new articles appears in "Popular Tags"', async ({ browser }) => {
  // Step 1: Start new browser context and create user
  const context = await browser.newContext();
  const page = await context.newPage();
  const user = await createRandomUserViaAPI();
  await setupUserSession(page, user.token, user.username);

  // Step 2: Generate unique tag
  const tag = `TestTag-${Math.floor(Math.random() * 1000000)}`;

  // Step 3: Create two articles using the same tag
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

  // Step 4: Go to homepage and check if tag appears in "Popular Tags"
  await page.goto('http://localhost:4100/');

  // Step 5: Retry up to 5 times to allow tag cache/index to update
  let popularTags: string[] = [];
  for (let i = 0; i < 5; i++) {
    await page.waitForTimeout(1000);
    await page.reload();
    popularTags = await page.locator('.tag-list a').allTextContents();
    if (popularTags.map(t => t.trim()).includes(tag)) break;
  }

  // Step 6: Assert that generated tag is visible in sidebar
  expect(popularTags.map(t => t.trim())).toContain(tag);

  // Step 7: Cleanup
  await context.close();
});
