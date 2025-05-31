import { Page } from '@playwright/test';

export class LoginPage {
  readonly page: Page;

  constructor(page: Page) {
    this.page = page;
  }

  async navigate() {
    await this.page.goto('/');
    await this.page.click('text=Sign in');
  }

  async login(email: string, password: string) {
    await this.page.fill('input[placeholder="Email"]', email);
    await this.page.fill('input[placeholder="Password"]', password);
    await this.page.click('button:has-text("Sign in")');
    await this.page.waitForURL('**/');
  }

  async getErrorMessages(): Promise<string[]> {
    return this.page.locator('.error-messages li').allTextContents();
  }
}
