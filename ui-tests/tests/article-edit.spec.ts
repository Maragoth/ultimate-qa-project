import { test, expect } from '@playwright/test';
import { ArticlePage } from '../pages/ArticlePage';
import { generateArticle } from '../helpers/testData';
import { createRandomUserViaAPI, createArticleViaAPI } from '../helpers/apiHelpers';

test('User can edit an existing article', async ({ page }) => {
  const user = await createRandomUserViaAPI();
  const original = generateArticle('Edit-Original', `Tag-${Math.floor(Math.random() * 1000000)}`);
  const updated = generateArticle('Edit-Updated', original.tags[0]);

  const created = await createArticleViaAPI(user.token, original);

  await page.goto('/');
  await page.evaluate((token) => {
    localStorage.setItem('jwt', token);
  }, user.token);
  await page.reload();

  const articlePage = new ArticlePage(page);

  await page.goto(`/article/${created.slug}`);
  await articlePage.clickEditButton();
  await articlePage.editArticle(updated.title, updated.description, updated.body);

  const visibleTitle = await articlePage.getArticleTitle();
  expect(visibleTitle).toBe(updated.title);
});
