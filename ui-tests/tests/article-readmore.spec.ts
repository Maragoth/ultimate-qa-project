import { test, expect } from '@playwright/test';
import { generateArticle } from '../helpers/testData';
import { ArticlePage } from '../pages/ArticlePage';
import { createRandomUserViaAPI } from '../helpers/apiHelpers';
import { setupUserSession } from '../helpers/sessionHelpers';

test('User can open correct article using "Read more" link', async ({ page }) => {
  // Step 1: Create a test user via API
  const user = await createRandomUserViaAPI();

  // Step 2: Initialize ArticlePage POM
  const articlePage = new ArticlePage(page);

  // Step 3: Set up user session in browser
  await setupUserSession(page, user.token, user.username);

  // Step 4: Generate article data
  const tag = `TestTag-${Math.floor(Math.random() * 1000000)}`;
  const article = generateArticle('ReadMore', tag);

  // Step 5: Create the article via UI
  await articlePage.navigateToEditor();
  await articlePage.createArticle(article.title, article.description, article.body, article.tags);

  // Step 6: Try to locate the article preview on homepage
  const articlePreview = page.locator(`.article-preview:has(h1:has-text("${article.title}"))`);
  const isVisible = await articlePreview.first().isVisible({ timeout: 3000 }).catch(() => false);

  // Step 7: If article not visible, go to user profile to find it
  if (!isVisible) {
    await page.click("a.nav-link[href*='/@']");
    await page.waitForURL('**/@**');
  }

  // Step 8: Click on "Read more" link in the article preview
  const correctPreview = page.locator(`.article-preview:has(h1:has-text("${article.title}"))`);
  const readMoreLink = correctPreview.locator("a:has-text('Read more')");
  await readMoreLink.click();

  // Step 9: Verify that article detail page is opened and title is correct
  await expect(page).toHaveURL(/.*\/article\//);
  await expect(page.locator('h1')).toHaveText(article.title);
});
