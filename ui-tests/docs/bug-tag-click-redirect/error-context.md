# Test info

- Name: Clicking a tag below an article filters articles by that tag
- Location: C:\Users\eplog\ultimate-qa-project\ui-tests\tests\tag-filter-article.spec.ts:5:5

# Error details

```
Error: Timed out 5000ms waiting for expect(locator).toBeVisible()

Locator: locator('.article-preview').locator('text=Tagged-Article-A')
Expected: visible
Received: <element(s) not found>
Call log:
  - expect.toBeVisible with timeout 5000ms
  - waiting for locator('.article-preview').locator('text=Tagged-Article-A')

    at C:\Users\eplog\ultimate-qa-project\ui-tests\tests\tag-filter-article.spec.ts:42:67
```

# Page snapshot

```yaml
- navigation:
  - link "conduit":
    - /url: /
  - list:
    - listitem:
      - link "Home":
        - /url: /
    - listitem:
      - link " New Post":
        - /url: /editor
    - listitem:
      - link " Settings":
        - /url: /settings
    - listitem:
      - link "user1748410139358-39496 user1748410139358-39496":
        - /url: /@user1748410139358-39496
        - img "user1748410139358-39496"
        - text: user1748410139358-39496
- heading "Tagged-Article-A" [level=1]
- link "user1748410139358-39496":
  - /url: /@user1748410139358-39496
  - img "user1748410139358-39496"
- link "user1748410139358-39496":
  - /url: /@user1748410139358-39496
- text: Wed May 28 2025
- link " Edit Article":
  - /url: /editor/Tagged-Article-A-1734
- button " Delete Article"
- paragraph: Body A
- list:
  - listitem: Tag-903884
- separator
- textbox "Write a comment..."
- img "user1748410139358-39496"
- button "Post Comment"
```

# Test source

```ts
   1 | import { test, expect } from '@playwright/test';
   2 | import { createRandomUserViaAPI, createArticleViaAPI } from '../helpers/apiHelpers';
   3 | import { setupUserSession } from '../helpers/sessionHelpers';
   4 |
   5 | test('Clicking a tag below an article filters articles by that tag', async ({ browser }) => {
   6 |   const context = await browser.newContext();
   7 |   const page = await context.newPage();
   8 |
   9 |   const user = await createRandomUserViaAPI();
  10 |   await setupUserSession(page, user.token, user.username);
  11 |
  12 |   const tag = `Tag-${Math.floor(Math.random() * 1000000)}`;
  13 |
  14 |   // Create two articles with the same tag
  15 |   const article1 = await createArticleViaAPI(user.token, {
  16 |     title: 'Tagged-Article-A',
  17 |     description: 'Description A',
  18 |     body: 'Body A',
  19 |     tagList: [tag],
  20 |   });
  21 |
  22 |   const article2 = await createArticleViaAPI(user.token, {
  23 |     title: 'Tagged-Article-B',
  24 |     description: 'Description B',
  25 |     body: 'Body B',
  26 |     tagList: [tag],
  27 |   });
  28 |
  29 |   // Go to Global Feed
  30 |   await page.goto('http://localhost:4100/');
  31 |   await page.getByRole('link', { name: 'Global Feed' }).click();
  32 |
  33 |   // Find article created via API and click its tag
  34 |   const articleLocator = page.locator('.article-preview', { hasText: article1.title });
  35 |   await expect(articleLocator).toBeVisible();
  36 |
  37 |   const tagLocator = articleLocator.locator(`.tag-list >> text=${tag}`);
  38 |   await tagLocator.click();
  39 |
  40 |   // Validate that both tagged articles are shown
  41 |   const articlePreviews = page.locator('.article-preview');
> 42 |   await expect(articlePreviews.locator(`text=${article1.title}`)).toBeVisible();
     |                                                                   ^ Error: Timed out 5000ms waiting for expect(locator).toBeVisible()
  43 |   await expect(articlePreviews.locator(`text=${article2.title}`)).toBeVisible();
  44 |
  45 |   // Optionally check count = 2
  46 |   await expect(articlePreviews).toHaveCount(2);
  47 |
  48 |   await context.close();
  49 | });
  50 |
```