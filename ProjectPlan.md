# 🗂️ Project Plan – Ultimate QA Project

## 🎯 Project Goal & Scope

The goal of this project is to develop a comprehensive QA Automation framework that simulates a real-world enterprise-level testing environment.

It includes fully automated testing across Web UI, API, Mobile, and hybrid layers, integrated with CI/CD pipelines and a locally hosted backend stack.

**Scope includes:**
- Full CRUD API testing with schema validation and response time checks
- End-to-end UI testing with Playwright and Page Object Model across multiple browsers
- Mobile UI testing using Appium on a physical Android device (mobile browser)
- Hybrid tests combining API-based data setup with UI validation
- Continuous integration with GitHub Actions and matrix builds (Node.js, Python, browsers)
- Local environment with PostgreSQL database deployed in a Docker container
- Centralized QA orchestration using n8n to automate environment setup, test execution, and report aggregation



## 🛡️ Test Strategy

### API Testing (Python + Pytest + JSON Schema)
- Authentication & Token handling (valid, expired, missing, malformed tokens)
- CRUD operations for Users, Articles, Comments
- Negative test scenarios (4xx, 5xx responses, malformed JSON, unsupported methods)
- Input validation: boundary values, special characters (e.g. emoji, ł, ç)
- Dependency rules (e.g. deleting article deletes related comments)
- Partial updates (e.g. PATCH-style PUT /user with subset of fields)
- JSON Schema validation of API responses
- Response time assertions (<1000ms)
- Stability checks: schema drift, data consistency


### UI Testing (Playwright)
- Full end-to-end user flows: login, registration, article creation, editing, deletion
- Interaction testing: favoriting, following authors, commenting, tag-based filtering
- Dynamic data verification: updated profiles, images, and navigation based on login state
- Visual and behavioral validation across multiple browsers using Playwright projects
- Page Object Model used for maintainable and scalable test architecture
- Covers both positive scenarios and negative cases (e.g. invalid credentials, missing input)

### Hybrid Testing (UI + API)
- Combines API requests for data setup with UI tests for visual and functional validation
- Enables fast and stable test execution by bypassing repetitive UI steps (e.g., registration, login)
- Uses API to create test data (users, articles, comments) and verifies expected behavior through the UI
- Helps isolate frontend vs backend failures by decoupling test flow between layers

### Mobile Testing (Appium + Physical Android Device)
- Launching mobile Chrome browser and navigating to the web application
- Executing login, registration, and article-related flows on mobile viewport
- Testing UI interactions: creating, editing, deleting articles and comments
- Validating layout responsiveness and element visibility on small screens
- Performing smoke tests of critical user paths on real device
- Ensuring touch interactions, scrolling, and navigation behave as expected


### CI/CD Automation (GitHub Actions)
- Automated test execution on push
- Matrix builds (Node versions, Python versions)
- Allure Reports and HTML reporting
- Dockerized PostgreSQL DB (tests run locally)



## 🧰 Tools & Technologies

| Category           | Tools                                                                      |
|--------------------|----------------------------------------------------------------------------|
| UI Testing         | Playwright (TypeScript) – Chromium, Firefox, WebKit                        |
| API Testing        | Python + Requests + Pytest + JSON Schema                                   |
| Mobile Testing     | Appium + Physical Android Device (Chrome browser in mobile viewport)       |
| CI/CD              | GitHub Actions with matrix builds (Node.js, Python, multi-browser support) |
| Reporting          | Allure + pytest-html (HTML reports with CI publishing)                     |
| Version Control    | Git + GitHub                                                               |
| Test Environment   | API, Frontend, and DB run locally via script-based orchestration           |
| Database Deployment| PostgreSQL containerized via `docker run` (no docker-compose)              |
| Automation         | n8n (automates setup, test sequencing, and report handling)                |



## 📂 Folder Structure

```
ultimate-qa-project/
├── node-express-realworld-example-app/         # Backend (forked from RealWorld project, modified for testing)
├── react-redux-realworld-example-app/          # Frontend (forked from RealWorld project, adapted for UI tests)
├── api-tests/                                  # API Automation Tests (Python + Pytest)
├── ui-tests/                                   # UI Automation Tests (Playwright - desktop)
├── mobile-tests/                               # Mobile Tests (Appium - Android)
├── test-results/                               # Generated test reports (e.g. Allure, HTML)
├── start-project.ps1                           # Starts DB (via docker run), backend, and frontend
├── requirements.txt                            # Python dependencies for API test suite
├── pytest.ini                                  # Pytest configuration (e.g. markers, timeout)
├── README.md                                   # Project documentation
└── ProjectPlan.md                              # QA strategy, roadmap, test checklist

```




## ✅ Test Plan – Detailed Checklist

### API Tests
- [✅] User Registration (200 OK, 400 Errors)
- [✅] User Login (success, failure)
- [✅] CRUD Articles (POST, GET, PUT, DELETE)
- [✅] CRUD Comments management
- [✅] Favorite/Unfavorite Articles
- [✅] Profile Follow/Unfollow
- [✅] Schema validation for API responses
- [✅] Response time <1000ms

📝 Authentication Suite
- [✅] Expired or malformed JWT returns 401
- [✅] Missing Authorization header returns 401
- [✅] Reused or tampered token is rejected

📝 Input Validation Suite
- [✅] Malformed JSON returns 400
- [✅] Boundary input values for title, bio, username
- [✅] Unicode & special characters are processed correctly
- [✅] Unsupported HTTP methods return 405

📝 Data Integrity Suite
- [✅] Freshly created resource is immediately consistent
- [✅] Deleting parent (article) removes related comments

📝 Schema & Response Suite
- [✅] JSON Schema strictly matches response body
- [✅] No unexpected fields in production responses

📝 Partial Update Suite
- [✅] PUT /user with partial fields updates only what's provided


### 🖥️📱 UI Tests (Desktop + Mobile)
- [✅] User login flow: Verify successful login with valid credentials.
- [✅] User registration flow: Test the registration process with valid and invalid data inputs.
- [✅] Create a new article: Ensure that users can create articles and they appear in the feed.
- [✅] Edit an existing article: Verify that users can edit articles and changes are saved correctly.
- [✅] Click "Read more" to open full article: Test the functionality of expanding articles to read the full content.
- [✅] Favorite/unfavorite articles flow: Test the ability to favorite and unfavorite articles, ensuring the UI updates accordingly.
- [✅] Add and delete a comment: Verify that users can add comments to articles and delete them.
- [✅] Delete an article: Confirm that users can delete articles and they are removed from the feed.
- [✅] Follow/unfollow author and verify feed: Ensure users can follow and unfollow authors, with the feed updating to reflect these changes.
- [✅] Filter articles using "Popular Tags": Test filtering functionality using popular tags to ensure correct articles are displayed.
- [✅] Filter by clicking tags below an article: Verify that clicking on tags below an article filters the feed accordingly.
- [✅] Tag from new article shows in "Popular Tags": Ensure that tags from newly created articles appear in the "Popular Tags" section.
- [✅] Click article author: Verify that clicking on an article author's name navigates to their profile page.
- [✅] Click comment author: Ensure that clicking on a comment author's name navigates to their profile page.
- [✅] Update username, email, bio: Test updating user profile information and verify changes are saved.
- [✅] Update password and login with new password: Verify that users can update their password and log in with the new credentials.
- [✅] Update profile image URL and verify it: Ensure users can update their profile image and the change is reflected in the UI.
- [✅] Navbar content based on login state: Verify that the navigation bar displays appropriate options based on the user's login state.
- [✅] Displays error on invalid credentials: Confirm that the application shows an error message when login attempts are made with invalid credentials.

### 🔁 Hybrid Tests - API helpers for UI testing
- [✅] Create random user via API – Generates a test user with a guaranteed unique username to avoid conflicts across test runs.
- [✅] Login via API – Logs in via backend to skip UI login flow and speed up tests execution.
- [✅] Create article via API – Creates an article with a unique title specific to the current test case.
- [✅] Create comment via API – Adds a predefined comment via API to save time during UI validation steps.

### CI/CD & Reporting
- [✅] Automated API tests (GitHub Actions)
- [✅] Automated Desktop UI tests (GitHub Actions)
- [📝] Matrix builds – planned for future
- [✅] HTML test reports via pytest-html (downloadable from CI artifacts)



## 🗓️ Roadmap & Milestones

| 🧩 Stage | Description                          | ⏱️ Estimated Time | ⏳ Status        |
|---------|--------------------------------------|-------------------|------------------|
| Stage 0 | Project setup, clone, env, docker    | 1h                | ✅ Complete       |
| Stage 1 | API Testing (CRUD, Auth, Schema)     | 6–8h              | ✅ Complete       |
| Stage 2 | UI Testing (Playwright + POM)        | 8–10h             | ✅ Complete       |
| Stage 3 | Hybrid UI+API tests                  | 4h                | ✅ Complete       |
| Stage 4 | Mobile Testing (Appium)              | 6–8h              | ✅ Complete       |
| Stage 5 | CI/CD & Matrix Builds                | 6h                | ✅ Complete       |



## 🚀 Future Enhancements

- Integrate n8n as the central automation orchestrator for the entire QA pipeline
- Automated setup of backend, frontend, DB, and mobile environment
- Sequential execution of API, UI, and Mobile test suites
- Centralized generation and export of test reports to a unified dashboard or directory


## 📈 Expected Outcome

The outcome of this project is a complete, production-grade Quality Assurance framework designed to simulate a real-world enterprise testing workflow.

- Full-stack QA coverage – Includes automated API, UI (desktop & mobile), hybrid, and smoke tests across multiple platforms and technologies.
- Modular architecture – All tests follow the Page Object Model and API helper abstraction for maintainability and reuse.
- Cross-browser and cross-platform validation – Test execution across Chromium, Firefox, WebKit, and physical Android device ensures compatibility and consistency.
- CI/CD integration – GitHub Actions with matrix builds and auto-triggered workflows for every commit, including reporting and badge generation.
- Advanced reporting – Allure and HTML reports auto-published to GitHub Pages, enabling transparent and sharable test results.
- Local test environment – API backend, frontend application, and PostgreSQL database run locally via Docker or manual scripts, ensuring fast, stable, and isolated test execution without external dependencies.
- Portfolio-grade delivery – The project is packaged with full documentation (README, Test Plan, Test Summary) and published as a GitHub repository suitable for job applications or freelance proposals.
- Unified automation layer using n8n to sequentially start environment components (DB, API, UI, Appium), run tests (API → UI → Mobile), and consolidate reports into a single location

This project is designed to serve as a reference-level QA Automation framework, demonstrating the author’s ability to plan, implement, and scale complex testing solutions in a modern DevOps ecosystem.