# 📱 Mobile Tests – Ultimate QA Project

This folder contains mobile automation tests using **Appium** on a **real Android device**.
It simulates a real user interacting with the **mobile version of the RealWorld app UI** opened in a browser.

---

## 🎯 Scope

* Connect your Android device via USB (enable USB debugging)
* Open mobile browser (e.g., Chrome) with `http://<your-computer-ip>:4100` (e.g., `http://192.168.1.191:4100`)
* Make sure your phone and computer are on the same WiFi network
* Perform basic smoke tests using Appium:

  * Login form interactions
  * Article navigation
  * Basic visual checks

---

## 🔧 Tech Stack

| Tool             | Purpose                              |
| ---------------- | ------------------------------------ |
| Appium           | Mobile automation driver             |
| Appium Inspector | Inspect mobile elements              |
| Android Device   | Physical Android phone/tablet        |
| Node.js          | Required for Appium server           |
| Python           | Automation language for test scripts |
| pytest           | Test runner                          |
| Java SDK         | Needed by Android tools             |

---

## 🧱 Prerequisites

Install the following tools:

* [Node.js](https://nodejs.org/) (v18+)

* [Python 3.10+](https://www.python.org/)

* [Java SDK 11+](https://adoptium.net/)

* [Appium](https://appium.io/):

  ```bash
  npm install -g appium
  ```
  - Install Android driver for Appium:

  ```bash
  appium driver install uiautomator2
  ```

* [Appium Inspector](https://github.com/appium/appium-inspector/releases)

---

## 📦 Python Dependencies

Install required packages:

```bash
pip install -r requirements.txt
```

Content of `requirements.txt`:

```
pytest
Appium-Python-Client
```

---

## 📲 Android Device Setup

1. Enable Developer Options:
   * Go to Settings > About Phone
   * Tap "Build Number" 7 times to enable Developer Options

2. Enable USB Debugging:
   * Go to Settings > Developer Options
   * Enable "USB debugging"

3. Connect your device:
   * Connect your Android device to your computer via USB
   * Accept the USB debugging prompt on your device
   * Verify connection by running:
     ```bash
     adb devices
     ```
   * Your device should be listed as "device" (not "unauthorized")

4. Install Chrome browser on your device if not already installed

---

## 🌐 Accessing RealWorld App in Browser

1. Start full stack (DB + Backend + Frontend):

   ```bash
   ./start-project.ps1
   ```

2. Make sure your phone and computer are on the same WiFi network

3. Find your computer's IP address:
   ```bash
   ipconfig
   ```
   Look for IPv4 Address under your WiFi adapter (e.g., 192.168.1.191)

4. On your Android device, open **Chrome** and go to:
   ```
   http://<your-computer-ip>:4100
   ```

For example:
http://192.168.1.191:4100

---

## 🚀 Running Tests

1. Start the Appium server:
   ```bash
   appium
   ```

2. Configure your host settings:
   * Open `mobile-tests/env.py`
   * Update the `HOST_CONFIG` dictionary with your computer's IP address:
     ```python
     HOST_CONFIG = {
         "API_HOST": "192.168.1.191",     # Replace with your IP
         "FRONTEND_HOST": "192.168.1.191", # Replace with your IP
         "API_PORT": "3000",
         "FRONTEND_PORT": "4100"
     }
     ```

3. Run the tests from root project folder:
   ```bash
   pytest mobile-tests/
   ```

---

## 📂 Folder Structure

```
mobile-tests/
├── tests/
│   ├── test_login.py                       ✅10x✅# user login flow
│   ├── test_invalid_login.py               ✅10x✅# invalid login (error message)
│   ├── test_registration.py                ✅10x✅# user registration flow
│   ├── test_article_create.py              ✅10x✅# create a new article
│   ├── test_article_edit.py                ✅10x✅# edit article content
│   ├── test_article_readmore.py            ✅10x✅# open full article from preview
│   ├── test_article_favorite.py            ✅10x✅# favorite/unfavorite articles
│   ├── test_comments.py                    ✅10x✅# add and delete comment
│   ├── test_article_delete.py              ✅10x✅# delete article
│   ├── test_follow_unfollow.py             ✅10x✅# follow/unfollow author and verify feed
│   ├── test_tag_filter_popular.py          ✅10x✅# filter by "Popular Tags"
│   ├── test_tag_filter_article.py          ✅10x✅#⚠️ BLOCKED – tag click redirect issue
│   ├── test_tag_popularity.py              ✅10x✅# new tag appears in Popular Tags
│   ├── test_article_author_profile.py      ✅10x✅# click article author → profile
│   ├── test_comment_author_profile.py      ✅10x✅# click comment author → profile
│   ├── test_update_profile_info.py         ✅10x✅# update username, email, bio
│   ├── test_update_password.py             ✅10x✅# update password and re-login
│   ├── test_update_profile_image.py        ✅10x✅# update profile image and verify
│   └── test_navigation.py                  ✅10x✅# navbar behavior based on login state
├── pages/
│   ├── __init__.py
│   ├── article_page.py                     # Article creation, editing, and interactions
│   ├── login_page.py                       # Login form and authentication
│   └── registration_page.py                # User registration and signup
├── fixtures/
│   └── setup.py
├── helpers/
│   ├── __init__.py
│   ├── api_helpers.py                      # API interaction utilities
│   ├── assertions.py                       # Custom test assertions
│   ├── auth.py                            # Authentication helper functions
│   ├── config.py                          # Test configuration and settings
│   ├── popup_handlers.py                  # Handle browser popups and alerts
│   ├── session.py                         # Browser session management
│   ├── test_data.py                       # Test data generation and constants
│   └── waits.py                           # Custom wait conditions
├── requirements.txt
└── README.md
```

---

## 👤 Author

**Adam Fedorowicz**
QA Automation Engineer | Full-Stack Tester | DevOps Learner

* 🌐 [LinkedIn – Adam Fedorowicz](https://www.linkedin.com/in/adam-fedorowicz-UK)
* 💻 [GitHub – Maragoth](https://github.com/Maragoth)
* 💼 [Upwork – QA Automation Engineer](https://www.upwork.com/freelancers/~018d6c0e188850f30d?mp_source=share)

---

## 🛡️ License

© 2025 Adam Fedorowicz
Licensed under the [MIT License](https://opensource.org/licenses/MIT)