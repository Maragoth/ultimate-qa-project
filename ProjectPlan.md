# 🗂️ Project Plan – Ultimate QA Project

## 🎯 Project Goal & Scope

The goal of this project is to build a comprehensive QA Automation framework simulating a real-world enterprise testing environment.  
It covers Web UI, API, Mobile, Hybrid testing and CI/CD automation with Dockerized database.

**Scope includes:**
- Full CRUD API Testing with schema validation
- UI End-to-End Testing with Playwright and Page Object Model
- Mobile smoke testing with Appium
- Hybrid tests combining UI flows with API validations
- CI/CD pipeline with GitHub Actions and matrix builds
- PostgreSQL database integration via Docker

---

## 🛡️ Test Strategy

### API Testing (Python + Pytest + JSON Schema)
- Authentication & Token handling
- CRUD operations for Users, Articles, Comments
- Negative test scenarios (4xx, 5xx responses)
- JSON Schema validation of API responses
- Response time assertions (<1000ms)

### UI Testing (Playwright)
- User login & registration workflows
- CRUD UI operations (Create, Edit, Delete articles)
- Visual regression snapshots
- Page Object Model structure
- Negative UI tests (invalid forms, error handling)

### Hybrid Testing (UI + API)
- Validate UI actions with API responses
- Create data via API → verify via UI
- Token-based UI tests bypassing manual login

### Mobile Testing (Appium + Android Emulator)
- Application launch & smoke tests
- UI form interactions (login, navigation)
- Basic compatibility checks

### CI/CD Automation (GitHub Actions)
- Automated test execution on push
- Matrix builds (Node versions, Python versions)
- Allure Reports and HTML reporting
- Dockerized PostgreSQL DB (tests run locally)

---

## 🧰 Tools & Technologies

| Category         | Tools                                    |
| ---------------- | ---------------------------------------- |
| UI Testing       | Playwright (TypeScript)                  |
| API Testing      | Python + Requests + Pytest + JSON Schema |
| Mobile Testing   | Appium + Android Emulator                |
| CI/CD            | GitHub Actions (Matrix Builds)           |
| Containerization | Docker (PostgreSQL DB only)              |
| Reporting        | Allure / pytest-html                     |
| Version Control  | Git + GitHub                             |


---

## 📂 Folder Structure

```
ultimate-qa-project/
├── node-express-realworld-example-app/  # Backend
├── react-redux-realworld-example-app/  # Frontend
├── api-tests/                          # API Automation Tests
├── ui-tests/                           # UI Automation Tests
├── mobile-tests/                       # Mobile Tests
├── docker-compose.yml                  # DB setup (if needed later)
├── start-project.ps1                   # Start script
├── stop-project.ps1                    # Stop script
├── restart-project.ps1                 # Restart script
├── README.md                           # Documentation
└── ProjectPlan.md                      # Roadmap & Strategy
```


---

## ✅ Test Plan – Detailed Checklist

### API Tests
- [ ] User Registration (200 OK, 400 Errors)
- [ ] User Login (success, failure)
- [ ] CRUD Articles (POST, GET, PUT, DELETE)
- [ ] CRUD Comments management
- [ ] Favorite/Unfavorite Articles
- [ ] Profile Follow/Unfollow
- [ ] Schema validation for API responses
- [ ] Response time <1000ms

### UI Tests
- [ ] Successful Login flow
- [ ] Negative Login (invalid data)
- [ ] Article creation & editing
- [ ] Article deletion
- [ ] Tag-based filtering
- [ ] Follow/Unfollow authors
- [ ] Like/Unlike articles
- [ ] Comment addition & deletion
- [ ] Visual snapshot tests
- [ ] UI error handling (404, 500 pages)

### Hybrid Tests
- [ ] Create article via API → Validate in UI
- [ ] Add comment via API → Verify in UI
- [ ] Favorite article in UI → Validate API count
- [ ] Follow user via UI → Confirm via API

### Mobile Tests
- [ ] App launch verification
- [ ] Login form interactions (mobile viewport)
- [ ] Article feed scrolling & interactions
- [ ] Responsive layout checks

### CI/CD & Reporting
- [ ] Automated API tests (GitHub Actions)
- [ ] Automated UI tests (GitHub Actions)
- [ ] Matrix builds (Node 20/22, Python 3.10/3.12, Chromium/Firefox/WebKit)
- [ ] Allure report generation
- [ ] Report publishing to GitHub Pages

---

## 🗓️ Roadmap & Milestones

| Stage   | Description                          | Estimated Time |
| ------- | ------------------------------------ | -------------- |
| Stage 0 | Project setup, clone, env, docker    | 1h             |
| Stage 1 | API Testing (CRUD, Auth, Schema)     | 6-8h           |
| Stage 2 | UI Testing (Playwright + POM)        | 8-10h          |
| Stage 3 | Hybrid UI+API tests                  | 4h             |
| Stage 4 | Mobile Testing (Appium)              | 6-8h           |
| Stage 5 | CI/CD & Matrix Builds                | 6h             |
| Stage 6 | Docker Optimization (optional later) | 3h             |

---

## 📈 Expected Outcome
- Fully automated QA framework simulating real client projects
- Modular and scalable test structure
- CI/CD pipeline integration with reporting
- Ready-to-present portfolio project demonstrating full-stack QA expertise