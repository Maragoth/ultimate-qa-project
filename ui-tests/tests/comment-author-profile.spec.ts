import { test, expect, chromium } from '@playwright/test';
import { createRandomUserViaAPI, createArticleViaAPI, addCommentViaAPI } from '../helpers/apiHelpers';
import { setupUserSession } from '../helpers/sessionHelpers';

test('Clicking comment author opens their profile with their own articles only', async () => {
  const userB = await createRandomUserViaAPI(); // comment author
  const userA = await createRandomUserViaAPI(); // article author

  const articleA = await createArticleViaAPI(userA.token, {
    title: 'Article-By-UserA',
    description: 'desc A',
    body: 'body A',
    tagList: ['comment'],
  });

  await addCommentViaAPI(userB.token, articleA.slug, {
    body: 'Nice post!',
  });

  const articleB = await createArticleViaAPI(userB.token, {
    title: 'Article-By-UserB',
    description: 'desc B',
    body: 'body B',
    tagList: ['own'],
  });

  const browserB = await chromium.launch();
  const contextB = await browserB.newContext();
  const pageB = await contextB.newPage();
  await setupUserSession(pageB, userB.token, userB.username);

  await pageB.goto(`http://localhost:4100/article/${articleA.slug}`);

  // Wait for the comment to be visible using best selector
  const commentCard = pageB.locator('.card:has(p.card-text:has-text("Nice post!"))');
  await expect(commentCard).toHaveCount(1, { timeout: 10000 });

  const commentText = commentCard.locator('p.card-text');
  await expect(commentText).toContainText('Nice post!');

  // Click the author's name under the comment and wait for navigation
  const authorLink = commentCard.locator('a.comment-author:has-text("' + userB.username + '")');
  await authorLink.scrollIntoViewIfNeeded();
  await Promise.all([
    pageB.waitForNavigation({ timeout: 10000 }),
    authorLink.click(),
  ]);

  // Validate redirected to userB's profile page
  await expect(pageB).toHaveURL(new RegExp(`/@${userB.username}$`));

  // Validate active tab is "My Articles"
  const activeTab = pageB.locator('.articles-toggle .nav-link.active');
  await expect(activeTab).toHaveText('My Articles');

  // Validate that only User B's article is shown
  const previews = pageB.locator('.article-preview');
  await expect(previews).toHaveCount(1);
  await expect(previews.first()).toContainText(articleB.title);
  await expect(previews.first()).not.toContainText(articleA.title);

  await browserB.close();
});
