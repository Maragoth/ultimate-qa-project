// ui-tests/tests/tag-filter-popular.spec.ts

import { test, expect } from '@playwright/test';
import { createRandomUserViaAPI, createArticleViaAPI } from '../helpers/apiHelpers';
import { setupUserSession } from '../helpers/sessionHelpers';
import { generateArticle } from '../helpers/testData';

test('Click tag in sidebar and verify articles contain that tag', async ({ browser }) => {
  // Step 1: Start new browser context and create user
  const context = await browser.newContext();
  const page = await context.newPage();
  const user = await createRandomUserViaAPI();
  await setupUserSession(page, user.token, user.username);

  // Step 2: Generate article with unique tag and create it via API
  const article = generateArticle('SidebarTag', `Tag-${Math.floor(Math.random() * 1000000)}`);
  const tag = article.tags[0];
  await createArticleViaAPI(user.token, article);

  // Step 3: Visit homepage and wait for tag to appear
  await page.goto('http://localhost:4100/');
  await expect(page.locator(`.tag-list >> text=${tag}`)).toBeVisible({ timeout: 5000 });

  // Step 4: Click on tag in sidebar
  await page.locator(`.tag-list >> text=${tag}`).click();

  // Step 5: Verify selected tag is active in feed toggle
  await expect(page.locator('.feed-toggle')).toContainText(tag);

  // Step 6: Verify articles contain the selected tag
  const articles = page.locator('.article-preview');
  const count = await articles.count();
  expect(count).toBeGreaterThan(0);

  for (let i = 0; i < count; i++) {
    const tags = await articles.nth(i).locator('ul.tag-list li').allTextContents();
    const cleanedTags = tags.map(t => t.trim());
    expect(cleanedTags.includes(tag)).toBe(true);
  }

  // Step 7: Cleanup
  await context.close();
});
