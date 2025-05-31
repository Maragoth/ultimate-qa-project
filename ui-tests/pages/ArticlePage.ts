import { Page, expect } from '@playwright/test';

export class ArticlePage {
  readonly page: Page;

  constructor(page: Page) {
    this.page = page;
  }

  async navigateToEditor() {
    await this.page.goto('/');
    await this.page.click('a.nav-link:has-text("New Post")');
    await this.page.waitForURL('**/editor');
  }

  async createArticle(title: string, description: string, body: string, tags: string[]) {
    await this.page.fill('input[placeholder="Article Title"]', title);
    await this.page.fill('input[placeholder*="this article about?"]', description);
    await this.page.fill('textarea[placeholder*="Write your article"]', body);
    for (const tag of tags) {
      await this.page.fill('input[placeholder="Enter tags"]', tag);
      await this.page.keyboard.press('Enter');
    }
    await this.page.click('button:has-text("Publish Article")');
    await this.page.waitForURL('**/article/**');
  }

  async getArticleTitle(): Promise<string> {
    return this.page.locator('h1').innerText();
  }

  async openOwnArticleFromHome(title: string) {
    await this.page.goto('/');
    await this.page.click(`a:has-text("${title}")`);
    await this.page.waitForURL('**/article/**');
  }

  async clickEditButton() {
    await this.page.click('a:has-text("Edit Article")');
    await this.page.waitForURL('**/editor/**');
  }

    async editArticle(title: string, description: string, body: string) {
    await this.page.fill('input[placeholder="Article Title"]', title);
    await this.page.fill('input[placeholder*="this article about?"]', description);
    await this.page.fill('textarea[placeholder*="Write your article"]', body);
    await Promise.all([
      this.page.waitForURL('**/article/**', { timeout: 10000 }),
      this.page.click('button:has-text("Publish Article")')
    ]);
  }


async openOwnArticleFallback(title: string) {
  await this.page.goto('/');

  // Try to find the article on the homepage (Your Feed or Global Feed)
  const articleOnHome = this.page.locator(`a:has-text("${title}")`).first();
  const isVisible = await articleOnHome.isVisible({ timeout: 3000 }).catch(() => false);

  if (isVisible) {
    await expect(articleOnHome).toBeVisible();
    await articleOnHome.click();
    await this.page.waitForURL('**/article/**');
    return;
  }

  // If not found, navigate to profile and try there
  await this.page.click('a.nav-link[href*="/@"]');
  await this.page.waitForURL('**/@**');

  const articleInProfile = this.page.locator(`a:has-text("${title}")`).first();
  await expect(articleInProfile).toBeVisible();
  await articleInProfile.click();
  await this.page.waitForURL('**/article/**');
}


  async deleteArticle() {
    await this.page.click('button:has-text("Delete Article")');
    await this.page.waitForURL('**/');
  }


  
}

