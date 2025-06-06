# pages/article_page.py

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ArticlePage:
    def __init__(self, driver):
        self.driver = driver

    def navigate_to_editor(self, base_url):
        self.driver.get(base_url)
        self.driver.find_element(AppiumBy.XPATH, '//a[normalize-space()="New Post"]').click()

    def create_article(self, title, description, body, tags):
        self.driver.find_element(AppiumBy.XPATH, '//input[@placeholder="Article Title"]').send_keys(title)
        self.driver.find_element(AppiumBy.XPATH, '//input[contains(@placeholder,"this article about?")]').send_keys(description)
        self.driver.find_element(AppiumBy.XPATH, '//textarea[contains(@placeholder,"Write your article")]').send_keys(body)
        for tag in tags:
            tag_input = self.driver.find_element(AppiumBy.XPATH, '//input[@placeholder="Enter tags"]')
            tag_input.send_keys(tag)
            tag_input.send_keys('\n')  # simulate Enter
        self.driver.find_element(AppiumBy.XPATH, '//button[normalize-space()="Publish Article"]').click()

    def get_article_title(self):
        return self.driver.find_element(AppiumBy.TAG_NAME, 'h1').text

    def open_own_article_from_home(self, base_url, title):
        self.driver.get(base_url)
        self.driver.find_element(AppiumBy.XPATH, f'//a[normalize-space()="{title}"]').click()

    def click_edit_button(self):
        self.driver.find_element(AppiumBy.XPATH, '//a[normalize-space()="Edit Article"]').click()

    def edit_article(self, title, description, body):
        self.driver.find_element(AppiumBy.XPATH, '//input[@placeholder="Article Title"]').clear()
        self.driver.find_element(AppiumBy.XPATH, '//input[@placeholder="Article Title"]').send_keys(title)

        self.driver.find_element(AppiumBy.XPATH, '//input[contains(@placeholder,"this article about?")]').clear()
        self.driver.find_element(AppiumBy.XPATH, '//input[contains(@placeholder,"this article about?")]').send_keys(description)

        self.driver.find_element(AppiumBy.XPATH, '//textarea[contains(@placeholder,"Write your article")]').clear()
        self.driver.find_element(AppiumBy.XPATH, '//textarea[contains(@placeholder,"Write your article")]').send_keys(body)

        self.driver.find_element(AppiumBy.XPATH, '//button[normalize-space()="Publish Article"]').click()

    def open_own_article_fallback(self, base_url, title):
        self.driver.get(base_url)
        try:
            element = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((AppiumBy.XPATH, f'//a[normalize-space()="{title}"]'))
            )
            element.click()
        except:
            # go to profile if not on homepage
            self.driver.find_element(AppiumBy.XPATH, '//a[contains(@href, "/@")]').click()
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, f'//a[normalize-space()="{title}"]'))
            ).click()

    def delete_article(self):
        self.driver.find_element(AppiumBy.XPATH, '//button[normalize-space()="Delete Article"]').click()
