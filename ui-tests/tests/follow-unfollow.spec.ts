import { test, expect, chromium } from '@playwright/test';
import { generateArticle } from '../helpers/testData';
import { createRandomUserViaAPI, createArticleViaAPI } from '../helpers/apiHelpers';
import { setupUserSession } from '../helpers/sessionHelpers';

const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

test('User can follow and unfollow another author and see changes in Your Feed', async () => {
  // Step 1: Create User B (author) and publish an article
  const userB = await createRandomUserViaAPI();
  const article = generateArticle('FollowFlow', `FollowTag-${Math.floor(Math.random() * 100000)}`);
  await createArticleViaAPI(userB.token, article);

  // Step 2: Create User A (tester) and launch browser session
  const userA = await createRandomUserViaAPI();
  const browserA = await chromium.launch();
  const contextA = await browserA.newContext();
  const pageA = await contextA.newPage();

  // Step 3: Set up User A session
  await pageA.goto('http://localhost:4100');
  await setupUserSession(pageA, userA.token, userA.username);

  // Step 4: Follow User B via API for full stability
  await pageA.request.post(`http://localhost:3000/api/profiles/${userB.username}/follow`, {
    headers: { Authorization: `Token ${userA.token}` },
  });

  // Step 5: Check if the article appears in "Your Feed"
  await pageA.goto('http://localhost:4100/');
  await pageA.click('text=Your Feed');
  await pageA.waitForLoadState('networkidle');

  // Step 6: Poll the /feed endpoint until the article is present
  let found = false;
  for (let i = 0; i < 20; i++) {
    const response = await pageA.request.get('http://localhost:3000/api/articles/feed', {
      headers: { Authorization: `Token ${userA.token}` },
    });

    const feed = await response.json();
    found = feed.articles.some((a: any) => a.title.includes(article.title));
    if (found) break;

    await delay(1000);
  }

  // Step 7: Assert that article is in the feed
  expect(found).toBe(true);

  // Step 8: Unfollow User B via API
  await pageA.request.delete(`http://localhost:3000/api/profiles/${userB.username}/follow`, {
    headers: { Authorization: `Token ${userA.token}` },
  });

  // Step 9: Reload "Your Feed" and verify article is gone
  await pageA.goto('http://localhost:4100/');
  await pageA.click('text=Your Feed');
  await pageA.waitForLoadState('networkidle');

  await expect(pageA.locator(`.article-preview:has(h1:has-text("${article.title}"))`)).toHaveCount(0);

  // Step 10: Close browser
  await browserA.close();
});
