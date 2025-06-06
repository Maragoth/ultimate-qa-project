# pages/article_page.py

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import logging
import time


class ArticlePage:
    def __init__(self, driver):
        self.driver = driver

    def navigate_to_editor(self, base_url):
        logging.info("Navigating to editor...")
        self.driver.get(base_url)

        # Wait for page to load completely
        WebDriverWait(self.driver, 10).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        logging.info("Page loaded completely")

        # Try different locator strategies
        locators = [
            (AppiumBy.XPATH, '//a[normalize-space()="New Post"]'),
            (AppiumBy.XPATH, '//a[contains(@href, "/editor")]'),
            (AppiumBy.LINK_TEXT, "New Post"),
            (AppiumBy.PARTIAL_LINK_TEXT, "New"),
        ]

        new_post_link = None
        for by, locator in locators:
            try:
                logging.info(f"Trying locator: {by} = {locator}")
                new_post_link = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((by, locator))
                )
                logging.info(f"Found element with locator: {by} = {locator}")
                break
            except TimeoutException:
                logging.info(f"Locator not found: {by} = {locator}")
                continue

        if not new_post_link:
            # Log the page source for debugging
            logging.error("Page source: " + self.driver.page_source)
            raise TimeoutException("Could not find New Post link with any locator")

        # Try to click with multiple strategies
        try:
            logging.info("Attempting JavaScript click")
            self.driver.execute_script("arguments[0].click();", new_post_link)
        except Exception as e:
            logging.info(f"JavaScript click failed: {str(e)}, trying regular click")
            new_post_link.click()

        # Wait for editor form to be visible
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (AppiumBy.XPATH, '//input[@placeholder="Article Title"]')
            )
        )
        logging.info("Successfully navigated to editor")

    def create_article(self, title, description, body, tags):
        # Fill in article form with waits
        title_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (AppiumBy.XPATH, '//input[@placeholder="Article Title"]')
            )
        )
        title_input.send_keys(title)

        desc_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (
                    AppiumBy.XPATH,
                    '//input[contains(@placeholder,"this article about?")]',
                )
            )
        )
        desc_input.send_keys(description)

        body_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (
                    AppiumBy.XPATH,
                    '//textarea[contains(@placeholder,"Write your article")]',
                )
            )
        )
        body_input.send_keys(body)

        for tag in tags:
            tag_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (AppiumBy.XPATH, '//input[@placeholder="Enter tags"]')
                )
            )
            tag_input.send_keys(tag)
            tag_input.send_keys("\n")  # simulate Enter

        publish_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (AppiumBy.XPATH, '//button[normalize-space()="Publish Article"]')
            )
        )
        self.driver.execute_script("arguments[0].click();", publish_button)

        # Wait for article to be published
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((AppiumBy.TAG_NAME, "h1"))
        )

    def get_article_title(self):
        return (
            WebDriverWait(self.driver, 10)
            .until(EC.presence_of_element_located((AppiumBy.TAG_NAME, "h1")))
            .text
        )

    def open_own_article_from_home(self, base_url, title):
        logging.info(f"Opening article with title: {title}")
        # Navigate directly to Global Feed
        self.driver.get(f"{base_url}/?tab=global")

        # Wait for page load and articles to appear
        try:
            # Wait for at least one article to be present
            article_preview = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((AppiumBy.XPATH, "//article-preview"))
            )
            logging.info("Articles loaded in Global Feed")

            # Try to find our specific article
            article_link = WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable(
                    (AppiumBy.XPATH, f'//article-preview//a[contains(., "{title}")]')
                )
            )
            logging.info("Found article link")

            # Scroll the article into view for better click reliability
            self.driver.execute_script(
                "arguments[0].scrollIntoView(true);", article_link
            )
            # Add a small pause to let the scroll complete
            self.driver.execute_script(
                "window.scrollBy(0, -100);"
            )  # Scroll up slightly to ensure element is fully visible

            # Click the article
            self.driver.execute_script("arguments[0].click();", article_link)
            logging.info("Clicked article link")

            # Wait for article page to load
            WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located(
                    (AppiumBy.XPATH, '//a[normalize-space()="Edit Article"]')
                )
            )
            logging.info("Successfully navigated to article page")
        except TimeoutException as e:
            logging.error("Failed to find article or navigate to it")
            logging.error("Page source: " + self.driver.page_source)
            raise

    def click_edit_button(self):
        logging.info("Clicking edit button")
        edit_button = WebDriverWait(self.driver, 3).until(
            EC.element_to_be_clickable(
                (AppiumBy.XPATH, '//a[normalize-space()="Edit Article"]')
            )
        )
        self.driver.execute_script("arguments[0].click();", edit_button)
        logging.info("Clicked edit button")

    def edit_article(self, title, description, body):
        logging.info("Editing article")
        try:
            # Wait for editor form to be ready
            form = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((AppiumBy.XPATH, "//form"))
            )

            # Find all inputs within the form context
            title_input = form.find_element(
                AppiumBy.XPATH, './/input[@placeholder="Article Title"]'
            )
            desc_input = form.find_element(
                AppiumBy.XPATH, './/input[contains(@placeholder,"this article about?")]'
            )
            body_input = form.find_element(
                AppiumBy.XPATH,
                './/textarea[contains(@placeholder,"Write your article")]',
            )

            # Update all fields using send_keys for better reliability
            logging.info("Updating article fields")
            for element, value in [
                (title_input, title),
                (desc_input, description),
                (body_input, body),
            ]:
                element.clear()
                element.send_keys(value)
                # Ensure the value is set
                if element.get_attribute("value") != value:
                    logging.warning(f"Value not set correctly, trying JavaScript")
                    self.driver.execute_script(
                        "arguments[0].value = arguments[1];", element, value
                    )
                    self.driver.execute_script(
                        "arguments[0].dispatchEvent(new Event('input', { bubbles: true }));",
                        element,
                    )

            # Find and click publish button
            publish_button = form.find_element(
                AppiumBy.XPATH, './/button[normalize-space()="Publish Article"]'
            )
            self.driver.execute_script("arguments[0].click();", publish_button)
            logging.info("Clicked publish button")

            # Wait for article to be published and verify the title
            title_element = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((AppiumBy.TAG_NAME, "h1"))
            )
            if title_element.text != title:
                logging.error(
                    f"Title mismatch after publish. Expected: {title}, Got: {title_element.text}"
                )
            logging.info("Article published successfully")

        except Exception as e:
            logging.error(f"Failed to edit article: {str(e)}")
            logging.error("Page source: " + self.driver.page_source)
            raise

    def open_own_article_fallback(self, base_url, title):
        self.driver.get(base_url)
        try:
            element = WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable(
                    (AppiumBy.XPATH, f'//a[normalize-space()="{title}"]')
                )
            )
            self.driver.execute_script("arguments[0].click();", element)
        except:
            # go to profile if not on homepage
            profile_link = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (AppiumBy.XPATH, '//a[contains(@href, "/@")]')
                )
            )
            self.driver.execute_script("arguments[0].click();", profile_link)
            article_link = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (AppiumBy.XPATH, f'//a[normalize-space()="{title}"]')
                )
            )
            self.driver.execute_script("arguments[0].click();", article_link)

    def delete_article(self):
        delete_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (AppiumBy.XPATH, '//button[normalize-space()="Delete Article"]')
            )
        )
        self.driver.execute_script("arguments[0].click();", delete_button)

    def click_read_more_for_article(self, title):
        """Find and click the Read more link for a specific article"""
        logging.info(f"Looking for Read more link for article: {title}")

        # Wait for feed to load and be interactive
        try:
            # Wait for feed toggle
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(
                    (AppiumBy.XPATH, "//div[contains(@class, 'feed-toggle')]")
                )
            )
            logging.info("Feed toggle loaded")

            # Find and click Global Feed if not already active
            global_feed = self.driver.find_element(
                AppiumBy.XPATH, "//a[contains(text(), 'Global Feed')]"
            )

            if "active" not in global_feed.get_attribute("class"):
                global_feed.click()
                logging.info("Switched to Global Feed")
                # Wait a moment for feed to update
                time.sleep(1)

            # Wait for articles to load
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(
                    (AppiumBy.XPATH, "//div[contains(@class, 'article-preview')]")
                )
            )
            logging.info("Articles loaded")

            # Find the article preview containing our title
            article_preview = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(
                    (
                        AppiumBy.XPATH,
                        f"//div[contains(@class, 'article-preview')][.//h1[contains(text(), '{title}')]]",
                    )
                )
            )
            logging.info("Found article preview")

            # Find the Read more... span using the exact XPath structure
            read_more_link = article_preview.find_element(
                AppiumBy.XPATH, ".//a/span[text()='Read more...']"
            )
            logging.info("Found Read more... link")

            # Scroll the link into view and click it
            self.driver.execute_script(
                "arguments[0].scrollIntoView(true);", read_more_link
            )
            self.driver.execute_script(
                "window.scrollBy(0, -100);"
            )  # Scroll up slightly
            logging.info("Scrolled to Read more... link")

            # Try direct click first, fall back to JavaScript click
            try:
                read_more_link.click()
                logging.info("Clicked Read more... link using direct click")
            except:
                logging.info("Direct click failed, trying JavaScript click")
                self.driver.execute_script("arguments[0].click();", read_more_link)
                logging.info("Clicked Read more... link using JavaScript click")

            # Wait for article page to load
            WebDriverWait(self.driver, 5).until(
                EC.text_to_be_present_in_element((AppiumBy.TAG_NAME, "h1"), title)
            )
            logging.info("Article page loaded")

        except TimeoutException as e:
            logging.error("Could not find article or Read more... link")
            logging.error("Current URL: " + self.driver.current_url)
            logging.error("Page source: " + self.driver.page_source)
            raise TimeoutException(
                f"Failed to find or click Read more... for article '{title}'"
            ) from e
