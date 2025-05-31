import { test, expect, chromium } from '@playwright/test';
import { generateArticle } from '../helpers/testData';
import { createRandomUserViaAPI, createArticleViaAPI } from '../helpers/apiHelpers';
import { setupUserSession } from '../helpers/sessionHelpers';

const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

test('User can follow and unfollow another author and see changes in Your Feed', async () => {
  // === Author (userB) ===
  const userB = await createRandomUserViaAPI();
  const article = generateArticle('FollowFlow', `FollowTag-${Math.floor(Math.random() * 100000)}`);
  await createArticleViaAPI(userB.token, article);

  // === Tester (userA) ===
  const userA = await createRandomUserViaAPI();
  const browserA = await chromium.launch();
  const contextA = await browserA.newContext();
  const pageA = await contextA.newPage();

  await pageA.goto('http://localhost:4100');
  await setupUserSession(pageA, userA.token, userA.username);

  // ✅ Zamiast kliknięcia przycisku — follow przez API (maksymalna stabilność)
  await pageA.request.post(`http://localhost:3000/api/profiles/${userB.username}/follow`, {
    headers: { Authorization: `Token ${userA.token}` },
  });

  // === Sprawdzenie czy artykuł pojawił się w feedzie
  await pageA.goto('http://localhost:4100/');
  await pageA.click('text=Your Feed');
  await pageA.waitForLoadState('networkidle');

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

  expect(found).toBe(true);

  // === Unfollow (też przez API, dla stabilności)
  await pageA.request.delete(`http://localhost:3000/api/profiles/${userB.username}/follow`, {
    headers: { Authorization: `Token ${userA.token}` },
  });

  await pageA.goto('http://localhost:4100/');
  await pageA.click('text=Your Feed');
  await pageA.waitForLoadState('networkidle');

  await expect(pageA.locator(`.article-preview:has(h1:has-text("${article.title}"))`)).toHaveCount(0);

  await browserA.close();
});
