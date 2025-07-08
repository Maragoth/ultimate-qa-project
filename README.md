# 🛡️ Ultimate QA Project – Full-Stack Automation Framework

A comprehensive QA Automation project simulating real-world enterprise testing environments.  
It combines multiple QA disciplines in a unified framework:

- ✅ Web UI Testing (Playwright)
- ✅ API Testing (Python + Pytest + JSON Schema)
- ✅ Mobile Testing (Appium + Android physical device)
- ✅ Hybrid UI + API Tests
- ✅ CI/CD Automation (GitHub Actions, matrix builds)
- ✅ Dockerized Database (PostgreSQL)
- ✅ Local Frontend & Backend for testing

---

## 📦 Project Structure

```
ultimate-qa-project/
├── node-express-realworld-example-app/ # Backend API (Node.js)
├── react-redux-realworld-example-app/ # Frontend UI (React)
├── api-tests/ # API Automation Tests (Pytest)
├── ui-tests/ # UI Automation Tests (Playwright)
├── mobile-tests/ # Mobile Tests (Appium)
├── start-project.ps1 # Start DB, Backend, Frontend (Windows script)
└── README.md # Documentation
└── ProjectPlan.md # Goals, Roadmap, strategy, technology
```


---

## 🎯 Project Goals

- Master modern QA tools and best practices
- Simulate real company workflows and automation tasks
- Automate UI, API, Mobile and Hybrid test scenarios
- Implement CI/CD pipelines with matrix builds and reports
- Run tests in Docker containers for consistency (DB only)

---

## 🔧 Tools & Technologies

- **UI Testing**: Playwright (JavaScript/TypeScript)
- **API Testing**: Python + Requests + Pytest + JSON Schema
- **Mobile Testing**: Appium + Android physical device
- **CI/CD**: GitHub Actions (matrix builds, reports)
- **Docker**: Docker (PostgreSQL DB)
- **Reports**: Allure, pytest-html
- **Version Control**: Git + GitHub

---

## 🛠️ Setup Instructions

### 1️⃣ Clone Repositories

```bash
git clone https://github.com/Maragoth/ultimate-qa-project.git
cd ultimate-qa-project

git clone https://github.com/Maragoth/node-express-realworld-example-app.git
git clone https://github.com/Maragoth/react-redux-realworld-example-app.git
```

### 2️⃣ Setup Virtual Environment (Windows)

```bash
python -m venv venv
.\venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
npm install --prefix node-express-realworld-example-app
npm install --prefix react-redux-realworld-example-app
npm install --prefix ui-tests
pip install -r requirements.txt
```

### 4️⃣ Environment Variables

In `node-express-realworld-example-app/`, create a file named `.env` with the following content:

```
DATABASE_URL="postgresql://postgres:postgres@localhost:5432/conduit?schema=public"
JWT_SECRET="super-secret"
NODE_ENV=development
```

### 5️⃣ Start Database
```bash
docker run --name conduit-db -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres
```
### 6️⃣ Generate Prisma Client & Apply Migrations
```bash
cd node-express-realworld-example-app
npx prisma generate
npx prisma migrate deploy
```
### 7️⃣ Start Backend API (New Terminal)
```bash
cd node-express-realworld-example-app
npx nx serve api
```
### 8️⃣ Start Frontend (New Terminal)
```bash
cd react-redux-realworld-example-app
npm start
```
### ✅ Alternative: Automatic Script (Windows)
Use this only **after completing database migrations** (Step 6).  
This script starts PostgreSQL (Docker), Backend (Node), and Frontend (React) in one go.

```bash
.\start-project.ps1
```
## 🛑 Stopping Services
To stop Frontend and Backend, simply close their terminal windows.

To stop PostgreSQL database, you have two options:

### 1️⃣ Docker CLI:
```bash
docker stop conduit-db
```
### 2️⃣ Docker Desktop:
- Open Docker Desktop

- Go to Containers tab

- Click Stop next to conduit-db

### ♻️ Resetting the Database (optional)
To wipe all articles, comments, tags, and users (clean state for API tests):

From the backend folder:
```bash
cd node-express-realworld-example-app
npm run reset-db
```
### 🌐 Access via Browser (Desktop)

Frontend: http://localhost:4100/

Backend API: http://localhost:3000/api

## 🚀 Running Tests

### API Tests
```
pytest api-tests/tests
```
### UI Tests (Playwright)
```
npx playwright test ui-tests/tests
```
### Mobile Tests (Appium)
```
pytest mobile-tests/tests
```

## 🚧 CI/CD & Automation (Planned)
- GitHub Actions workflows for automated tests

- Matrix builds for environment coverage

- Allure / pytest-html reports integration

- Dockerized testing (API tests)
  
## 👤 Author

**Adam Fedorowicz**  
QA Automation Engineer | Full-Stack Tester | DevOps Learner

Passionate about creating real-world automation frameworks that combine UI, API, and CI/CD workflows.  
Experienced in Selenium, Playwright, Pytest, Postman, and Dockerized test environments.  
Focused on practical, scalable, and production-ready QA solutions.  

## 📫 Find Me Online

- 🌐 [LinkedIn – Adam Fedorowicz](https://www.linkedin.com/in/adam-fedorowicz-UK)
- 💻 [GitHub – Maragoth](https://github.com/Maragoth)
- 💼 [Upwork – QA Automation Engineer](https://www.upwork.com/freelancers/~018d6c0e188850f30d?mp_source=share)
  
## 🛡️ License

© 2025 Adam Fedorowicz  
Licensed under the [MIT License](https://opensource.org/licenses/MIT).

Manual CI Trigger