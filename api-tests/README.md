# API Tests – Ultimate QA Project

This folder contains automated API tests for the [RealWorld Example App](https://realworld.io/). It is part of the larger **Ultimate QA Project**, designed to demonstrate full QA coverage (API, UI, Hybrid, Mobile, CI/CD, Reports).

## ✅ Scope & Goals
- User Registration (success & duplicate prevention)
- Full CRUD testing of Articles & Comments
- Profiles (follow/unfollow)
- Tags retrieval
- Favorites (add/remove articles to favorites)
- User Settings update (bio, image)
- Schema validation (JSON Schema)
- Response structure & data validation
- Response time checks (<1000ms)
- Logs for response status, body, time

## ✅ Tech Stack
- Python 3.12
- Pytest
- JSON Schema
- RealWorld API (localhost instance)

## ✅ Folder Structure
```
api-tests/
├── schemas/
│ ├── article.schema.json
│ ├── articles.schema.json
│ ├── comment.schema.json
│ ├── comments.schema.json
│ ├── profile.schema.json
│ ├── profiles.schema.json
│ └── tags.schema.json
├── test_auth.py
├── test_articles.py
├── test_comments.py
├── test_profiles.py
├── test_tags.py
├── test_favorites.py
├── test_settings.py
└── utils/
└── helpers.py
```


## ✅ Test Coverage
| Test Area     | Status |
|---------------|--------|
| User Registration | ✅ Done |
| Articles CRUD | ✅ Done |
| Comments CRUD | ✅ Done |
| Profiles      | ✅ Done |
| Tags          | ✅ Done |
| Favorites     | ✅ Done |
| User Settings | ✅ Done |
| Response Schema Validation | ✅ Done |
| Performance Check (<1s) | ✅ Done |

## ✅ Run Tests
Single test file:
```bash
pytest api-tests/test_articles.py -v -s
```

All API tests:
```bash
pytest api-tests/ -v -s
```
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
