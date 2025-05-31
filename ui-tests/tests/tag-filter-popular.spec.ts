// ui-tests/tests/tag-filter-popular.spec.ts

import { test, expect } from '@playwright/test';
import { createRandomUserViaAPI } from '../helpers/apiHelpers';
import { setupUserSession } from '../helpers/sessionHelpers';

test('Click tag in sidebar and verify articles contain that tag', async ({ page, browser }) => {
  const context = await browser.newContext();
  const newPage = await context.newPage();

  const user = await createRandomUserViaAPI();
  await createRandomUserViaAPI();
  await setupUserSession(page, user.token, user.username);


  await newPage.goto('http://localhost:4100/');

  const popularTag = newPage.locator('.tag-list a').first();
  const tagName = (await popularTag.textContent())?.trim();
  await popularTag.click();

  await expect(newPage.locator('.feed-toggle')).toContainText(tagName!);

  const articles = newPage.locator('.article-preview');
  const count = await articles.count();
  expect(count).toBeGreaterThan(0);

  for (let i = 0; i < count; i++) {
    const tags = await articles.nth(i).locator('ul.tag-list li').allTextContents();
    const cleanedTags = tags.map(t => t.trim());
    expect(cleanedTags.includes(tagName)).toBe(true);
  }

  await context.close();
});
