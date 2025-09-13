
# API Tests – Ultimate QA Project

This folder contains automated API tests for the [RealWorld Example App](https://realworld.io/).  
It is part of the larger **Ultimate QA Project**, designed to demonstrate full QA coverage (API, UI, Hybrid, Mobile, CI/CD, Reports).

---

## ✅ Scope & Goals
- User Registration (success & duplicate prevention)
- User Login (success)
- User Login - invalid password (401)
- Full CRUD testing of Articles & Comments
- Profiles (follow/unfollow)
- Tags retrieval
- Favorites (add/remove articles to favorites)
- User Settings update (bio, image)
- Schema validation (JSON Schema)
- Response structure & data validation
- Response time checks (<1000ms)
- Logs for response status, body, time

✅ **Completed Suites**:
- ✅ Expired or malformed JWT returns 401 (`auth suite`)
- ✅ Missing Authorization header returns 401
- ✅ Broken token is rejected
- ✅ Malformed JSON returns 400 (`input validation suite`)
- ✅ Boundary input testing (e.g. long title, short username)
- ✅ Unicode & special characters handling
- ✅ Unsupported HTTP methods return 405
- ✅ Data consistency after creation (immediate GET)
- ✅ Deleting article removes related comments
- ✅ JSON Schema strict match (drift detection)
- ✅ Partial update of user settings (`PUT /user` with only one field)

---

## ✅ Tech Stack
- Python 3.12
- Pytest
- JSON Schema
- RealWorld API (localhost instance)

---

## ✅ Folder Structure
```
api-tests/
├── fixtures/                    # Fixtures for reusable test data (e.g. auth token)
│   └── auth_token.py
├── tests/                            # All API test cases
│   ├── schemas/                       # JSON Schemas for response validation
│   │   ├── article.schema.json
│   │   ├── articles.schema.json
│   │   ├── comment.schema.json
│   │   ├── comments.schema.json
│   │   ├── profile.schema.json
│   │   ├── profiles.schema.json
│   │   └── tags.schema.json
│   ├── test_auth.py                      # Registration, login, auth errors
│   ├── test_articles.py                  # Article CRUD operations
│   ├── test_comments.py                  # Comment create/delete
│   ├── test_profiles.py                  # View/follow/unfollow profiles
│   ├── test_tags.py                      # Get available tags
│   ├── test_favorites.py                 # Favorite/unfavorite articles
│   ├── test_settings.py                  # Update user settings
│   ├── test_schema_validation.py         # Malformed JSON, boundary values, unicode, unsupported method
│   ├── test_data_integrity.py            # Data consistency after POST, delete cascade (article → comments)
│   ├── test_partial_update.py            # Partial update – PUT /user with only bio/image
│   ├── test_auth_invalid.py              # Expired token, missing token, broken token
├── utils/                           # Helper functions for requests, logging, schema validation
│   └── helpers.py
├── conftest.py                 # Global pytest configuration and fixtures
└── README.md                   # How to run API tests
```

---

## ✅ Test Coverage
| Test Area         | Status |
|-------------------|--------|
| User Registration | ✅ Done |
| User Login        | ✅ Done |
| Articles CRUD     | ✅ Done |
| Comments CRUD     | ✅ Done |
| Profiles          | ✅ Done |
| Tags              | ✅ Done |
| Favorites         | ✅ Done |
| User Settings     | ✅ Done |
| Response Schema Validation |✅ Done |
| Performance Check (<1s) |   ✅ Done |
| Extended Auth & Validation |✅ Done |

---

## ⚙️ Prerequisites
- PostgreSQL DB running on `localhost:5432`
- Backend API running on `http://localhost:3000/api`
- Use `npm run reset-db` to clear the database before full test runs (optional)

---

## ✅ Run Tests

Run single test file:
```bash
pytest api-tests/tests/test_articles.py -v -s
```

Run all API tests:
```bash
pytest api-tests/tests -v -s
```

---

## 👤 Author

**Adam Fedorowicz**  
QA Automation Engineer | Full-Stack Tester | DevOps Learner

Passionate about creating real-world automation frameworks that combine UI, API, and CI/CD workflows.  
Experienced in Selenium, Playwright, Pytest, Postman, and Dockerized test environments.  
Focused on practical, scalable, and production-ready QA solutions. 

---

## 📫 Find Me Online
- 🌐 [LinkedIn – Adam Fedorowicz](https://www.linkedin.com/in/adam-fedorowicz-UK)
- 💻 [GitHub – Maragoth](https://github.com/Maragoth)
- 💼 [Upwork – QA Automation Engineer](https://www.upwork.com/freelancers/~018d6c0e188850f30d?mp_source=share)

---

## 🛡️ License

© 2025 Adam Fedorowicz  
Licensed under the [MIT License](https://opensource.org/licenses/MIT).
