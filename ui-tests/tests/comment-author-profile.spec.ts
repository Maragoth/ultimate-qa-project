import { test, expect, chromium } from '@playwright/test';
import { createRandomUserViaAPI, createArticleViaAPI, addCommentViaAPI } from '../helpers/apiHelpers';
import { setupUserSession } from '../helpers/sessionHelpers';

test('Clicking comment author opens their profile with their own articles only', async () => {
  // Step 1: Create two users – one to write article, one to comment
  const userB = await createRandomUserViaAPI(); // comment author
  const userA = await createRandomUserViaAPI(); // article author

  // Step 2: User A creates an article
  const articleA = await createArticleViaAPI(userA.token, {
    title: 'Article-By-UserA',
    description: 'desc A',
    body: 'body A',
    tagList: ['comment'],
  });

  // Step 3: User B adds a comment to User A's article
  await addCommentViaAPI(userB.token, articleA.slug, {
    body: 'Nice post!',
  });

  // Step 4: User B creates their own article
  const articleB = await createArticleViaAPI(userB.token, {
    title: 'Article-By-UserB',
    description: 'desc B',
    body: 'body B',
    tagList: ['own'],
  });

  // Step 5: Start a new browser as User B and go to article A's page
  const browserB = await chromium.launch();
  const contextB = await browserB.newContext();
  const pageB = await contextB.newPage();
  await setupUserSession(pageB, userB.token, userB.username);
  await pageB.goto(`http://localhost:4100/article/${articleA.slug}`);

  // Step 6: Wait for comment to appear
  const commentCard = pageB.locator('.card:has(p.card-text:has-text("Nice post!"))');
  await expect(commentCard).toHaveCount(1, { timeout: 10000 });

  const commentText = commentCard.locator('p.card-text');
  await expect(commentText).toContainText('Nice post!');

  // Step 7: Click the author's name under the comment and wait for navigation
  const authorLink = commentCard.locator('a.comment-author:has-text("' + userB.username + '")');
  await authorLink.scrollIntoViewIfNeeded();
  await Promise.all([
    pageB.waitForNavigation({ timeout: 10000 }),
    authorLink.click(),
  ]);

  // Step 8: Verify redirected to user B's profile
  await expect(pageB).toHaveURL(new RegExp(`/@${userB.username}$`));

  // Step 9: Verify "My Articles" tab is active
  const activeTab = pageB.locator('.articles-toggle .nav-link.active');
  await expect(activeTab).toHaveText('My Articles');

  // Step 10: Verify only User B's article is listed
  const previews = pageB.locator('.article-preview');
  await expect(previews).toHaveCount(1);
  await expect(previews.first()).toContainText(articleB.title);
  await expect(previews.first()).not.toContainText(articleA.title);

  // Step 11: Clean up
  await browserB.close();
});
