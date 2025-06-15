# UI Tests – Ultimate QA Project

This folder contains end-to-end UI tests for the [RealWorld Example App](https://realworld.io/) frontend. It is part of the full **Ultimate QA Project**, showcasing modern web automation using Playwright.

## ✅ Scope & Goals
- User authentication (login, registration)
- Full article workflow (create, edit, delete, read)
- Comments (add, delete)
- Profile views (article/comment authors)
- Following authors and filtering feeds
- Favoriting articles and validating visibility
- Settings update (bio, email, password, avatar)
- Profile validation (author view, comment authorship)
- UI error handling (invalid login)

## ✅ Tech Stack
- **Framework**: Playwright
- **Language**: TypeScript
- **Assertion**: Built-in Playwright assertions

## ✅ Folder Structure
```
ui-tests/
├── tests/                                       # All UI test specs
│   ├── login.spec.ts                  ✅100x✅ # user login flow
│   ├── registration.spec.ts           ✅100x✅ # user registration flow
│   ├── article-create.spec.ts         ✅100x✅ # create a new article
│   ├── article-edit.spec.ts           ✅100x✅ # edit an existing article
│   ├── article-readmore.spec.ts       ✅100x✅ # click "Read more" to open full article
│   ├── article-favorite.spec.ts       ✅100x✅ # favorite/unfavorite articles flow
│   ├── comments.spec.ts               ✅100x✅ # add and delete a comment
│   ├── article-delete.spec.ts         ✅100x✅ # delete an article
│   ├── follow-unfollow.spec.ts        ✅100x✅ # follow/unfollow author and verify feed
│   ├── tag-filter-popular.spec.ts     ✅100x✅ # filter articles using "Popular Tags"
│   ├── tag-filter-article.spec.ts    ⚠️BLOCKED⚠️ # known redirect bug (see docs/bug-tag-click-redirect)
│   ├── tag-popularity.spec.ts         ✅100x✅ # tag from new article shows in "Popular Tags"
│   ├── article-author-profile.spec.ts ✅100x✅ # click article author → profile
│   ├── comment-author-profile.spec.ts ✅100x✅ # click comment author → profile
│   ├── update-profile-info.spec.ts    ✅100x✅ # update username, email, bio
│   ├── update-password.spec.ts        ✅100x✅ # update password and login with new password
│   ├── update-profile-image.spec.ts   ✅100x✅ # update profile image URL and verify it
│   ├── navigation.spec.ts             ✅100x✅ # navbar content based on login state
│   └── invalid-login.spec.ts          ✅100x✅ # displays error on invalid credentials
│
├── pages/                         # Page Object classes for form abstraction
│   ├── LoginPage.ts               # reusable login page actions
│   ├── RegistrationPage.ts        # reusable registration page actions
│   └── ArticlePage.ts             # reusable article page interactions
│
├── helpers/                       # Custom helpers & data
│   ├── apiHelpers.ts              # API calls for setup
│   ├── sessionHelpers.ts          # Setup user session via token
│   └── testData.ts                # Generate test users, articles
│
├── docs/                          # Bug documentation with screenshots and notes
│   ├── bug-tag-click-redirect/    # Bug: tags below article don't link to tag page
│   │   ├── bug-tag-click-redirect.md
│   │   ├── error-context.md
│   │   └── test-failed-1.png
│   └── bug-tag-input-missing-hint.md # Bug: no placeholder for tag input when empty
│
├── screenshots/                   # Screenshots from failures (auto-generated)
├── playwright.config.ts           # Playwright test configuration
├── package.json                   # Project dependencies and scripts
├── package-lock.json              # Exact versions of installed dependencies
├── tsconfig.json                  # TypeScript configuration for Playwright
├── TestSummary.md                 # Manual test summary and key notes
└── README.md                      # This documentation
```

## ✅ How to Run

Run all UI tests:
```bash
npx playwright test
```
Run a specific test:
```bash
npx playwright test tests/login.spec.ts
```
Run with debug / trace:
```bash
npx playwright test --debug
```

## ✅ Project Highlights
- Page Object Model used where helpful (Login, Registration, Article)
- Full token-based login simulation using API helpers (instead of UI login)
- High stability (each test passed ✅100x✅)
- Visual assertions and detailed selectors for robust validation
- Detects known UI bugs and validates regression status (blocked test included)
- Bug documentation included (see `docs/` folder)

## 👤 Author

**Adam Fedorowicz**  
QA Automation Engineer | Full-Stack Tester | DevOps Learner

Passionate about creating real-world automation frameworks that combine UI, API, Mobile and CI/CD workflows.  
Experienced in Selenium, Playwright, Pytest, Postman, and Dockerized test environments.  
Focused on practical, scalable, and production-ready QA solutions.

## 📫 Find Me Online

- 🌐 [LinkedIn – Adam Fedorowicz](https://www.linkedin.com/in/adam-fedorowicz-UK)
- 💻 [GitHub – Maragoth](https://github.com/Maragoth)
- 💼 [Upwork – QA Automation Engineer](https://www.upwork.com/freelancers/~018d6c0e188850f30d?mp_source=share)

## 🛡️ License

© 2025 Adam Fedorowicz  
Licensed under the [MIT License](https://opensource.org/licenses/MIT).
