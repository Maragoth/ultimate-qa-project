import { Page } from '@playwright/test';

export class RegistrationPage {
  readonly page: Page;

  constructor(page: Page) {
    this.page = page;
  }

  async navigate() {
    await this.page.goto('/');
    await this.page.waitForSelector('text=Sign up', { timeout: 3000 });
    await this.page.click('text=Sign up');
    await this.page.waitForSelector('input[placeholder="Username"]', { timeout: 3000 });
  }

  async register(username: string, email: string, password: string) {
  await this.page.fill('input[placeholder="Username"]', username);
  await this.page.fill('input[placeholder="Email"]', email);
  await this.page.fill('input[placeholder="Password"]', password);
  await this.page.waitForSelector('button:has-text("Sign up")', { timeout: 3000 });

  await Promise.all([
    this.page.waitForURL('**/', { timeout: 15000 }),
    this.page.click('button:has-text("Sign up")'),
  ]);
}

  async getErrorMessages(): Promise<string[]> {
    return this.page.locator('.error-messages li').allTextContents();
  }
}
