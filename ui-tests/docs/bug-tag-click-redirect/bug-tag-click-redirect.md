# Bug Report – Tag Click Redirects to Article Instead of Filtering

**Date:** 28.05.2025  
**Test Case:** Clicking a tag below an article filters articles by that tag  
**Severity:** Medium  
**Environment:** http://localhost:4100/

---

### Steps to Reproduce:
1. Log in as any user.
2. Create two articles with the same tag (e.g., `Tag-903884`).
3. Go to "Global Feed".
4. Locate one of the articles and click on its tag (below the article).
5. Observe the behavior.

---

### Expected Result:
User is redirected to a filtered list of articles containing the clicked tag (as in "Popular Tags" section).

---

### Actual Result:
Clicking the tag opens the full article page, just like clicking on the article title or "Read more".

---

###  Additional Notes:
This creates inconsistent UX behavior — clicking tags under articles and tags in the sidebar should behave the same.  
This may confuse users expecting tag-based filtering.

---

### 📎Evidence

- [Error Context](error-context.md)
  
- [Screenshot](test-failed-1.png)

---

**Suggested Fix:**  
Ensure that clicking any tag (sidebar or article preview) filters the global feed by that tag instead of opening the article.
