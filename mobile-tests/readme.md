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
│   ├── login.spec.py                       # 🕒 user login flow
│   ├── invalid-login.spec.py               # 🕒 invalid login (error message)
│   ├── registration.spec.py                # 🕒 user registration flow
│   ├── article-create.spec.py              # 🕒 create a new article
│   ├── article-edit.spec.py                # 🕒 edit article content
│   ├── article-readmore.spec.py            # 🕒 open full article from preview
│   ├── article-favorite.spec.py            # 🕒 favorite/unfavorite articles
│   ├── comments.spec.py                    # 🕒 add and delete comment
│   ├── article-delete.spec.py              # 🕒 delete article
│   ├── follow-unfollow.spec.py             # 🕒 follow/unfollow author and verify feed
│   ├── tag-filter-popular.spec.py          # 🕒 filter by "Popular Tags"
│   ├── tag-filter-article.spec.py          # ⚠️ BLOCKED – tag click redirect issue
│   ├── tag-popularity.spec.py              # 🕒 new tag appears in Popular Tags
│   ├── article-author-profile.spec.py      # 🕒 click article author → profile
│   ├── comment-author-profile.spec.py      # 🕒 click comment author → profile
│   ├── update-profile-info.spec.py         # 🕒 update username, email, bio, avatar
│   ├── update-password.spec.py             # 🕒 update password and re-login
│   ├── update-profile-image.spec.py        # 🕒 update profile image and verify
│   └── navigation.spec.py                  # 🕒 navbar behavior based on login state
├── fixtures/
│   └── setup.py
├── helpers/
│   └── session.py
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