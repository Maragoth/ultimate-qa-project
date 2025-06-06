from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def dismiss_translation_popup(driver):
    """Dismiss the Chrome translation popup by selecting 'Never translate pages in English'"""
    try:
        # Wait for the translation popup to appear
        popup = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located(
                (By.XPATH, '//div[contains(text(), "Przetłumaczyć")]')
            )
        )

        # Click the gear icon
        gear_icon = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    '//div[contains(text(), "Przetłumaczyć")]/ancestor::div[@role="dialog"]//button[@aria-label="Więcej opcji tłumaczenia"]',
                )
            )
        )
        driver.execute_script("arguments[0].click();", gear_icon)

        # Click "Never translate pages in English"
        never_translate = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    '//div[text()="Nigdy nie tłumacz stron, których językiem jest angielski"]',
                )
            )
        )
        driver.execute_script("arguments[0].click();", never_translate)

        # Verify the popup is gone
        WebDriverWait(driver, 3).until_not(
            EC.presence_of_element_located(
                (By.XPATH, '//div[contains(text(), "Przetłumaczyć")]')
            )
        )
        print("Translation popup successfully dismissed")
    except Exception as e:
        print(f"Translation popup not found or already dismissed: {str(e)}")


def dismiss_cookie_popup(driver):
    """Dismiss the cookie consent popup"""
    try:
        # Try to find and click "Odrzuć wszystko" button
        button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//button[normalize-space()="Odrzuć wszystko"]')
            )
        )
        driver.execute_script("arguments[0].click();", button)
    except Exception as e:
        print(f"Cookie popup not found or already dismissed: {str(e)}")


def handle_popups(driver):
    """Handle all known popups that might appear"""
    try:
        # Check for translation popup
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located(
                (By.XPATH, '//div[contains(text(), "Przetłumaczyć")]')
            )
        )
        dismiss_translation_popup(driver)
    except:
        print("No translation popup on frontend")

    try:
        # Check for cookie popup
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located(
                (By.XPATH, '//button[normalize-space()="Odrzuć wszystko"]')
            )
        )
        dismiss_cookie_popup(driver)
    except:
        print("No cookie popup on frontend")
