from appium.webdriver.common.appiumby import AppiumBy
from helpers.waits import wait_for_element


class HomePage:
    def __init__(self, driver):
        self.driver = driver

    def wait_for_element(self, by, value, timeout=10):
        return wait_for_element(self.driver, (by, value), timeout)

    def click_tag(self, tag):
        tag_element = self.wait_for_element(
            AppiumBy.XPATH,
            f"//section[@id='popular-tags']//a[normalize-space(text())='{tag}']",
        )
        tag_element.click()
