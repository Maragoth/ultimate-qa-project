# Bug Report – Missing Hint for Tag Input

**Date:** 28.05.2025  
**Test Case:** Creating article with tags  
**Severity:** Low-Medium  
**Environment:** http://localhost:4100/editor

---

### Steps to Reproduce:
1. Log in as any user.
2. Go to "New Post" page.
3. Type a tag in the "Enter tags" input, but **do not** press Enter.
4. Click "Publish Article".

---

### Expected Result:
- Either:
  - A visual hint like "Press Enter to add tag" is displayed, **or**
  - The tag is automatically added upon typing or publishing.

---

### Actual Result:
- The tag is **not** added unless the user presses Enter.
- There is **no indication** that pressing Enter is required.
- As a result, the article is published **without any tags**, and user input is silently lost.

---

### Impact:
- Users unintentionally publish articles without tags.
- This affects tag-based filtering and popular tags logic.
- It's a small but frustrating UX issue.

---

### Suggested Fix:
- Add a visible hint below the tag input: _"Press Enter to add tag"_
- Or consider auto-adding tags on blur or submit action.
