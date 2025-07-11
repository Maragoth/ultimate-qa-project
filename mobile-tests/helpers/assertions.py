from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def verify_logged_in(driver, timeout=5):
    """Verify that user is logged in by checking for Your Feed link

    Args:
        driver: The WebDriver instance
        timeout: Maximum time to wait for element (default 5 seconds)
    """
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.XPATH, '//a[normalize-space()="Your Feed"]'))
    )


def verify_article_created(driver, expected_title, timeout=5):
    """Verify that an article was created successfully

    Args:
        driver: The WebDriver instance
        expected_title: The expected article title
        timeout: Maximum time to wait for element (default 5 seconds)
    """
    actual_title = (
        WebDriverWait(driver, timeout)
        .until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
        .text
    )
    assert (
        actual_title == expected_title
    ), f"Expected title '{expected_title}' but got '{actual_title}'"


def verify_error_message(error_messages, expected_message):
    """Verify that an error message is present in the list of errors

    Args:
        error_messages: List of error message strings
        expected_message: The expected error message
    """
    assert (
        expected_message in error_messages
    ), f"Expected error message '{expected_message}' not found in {error_messages}"


def assert_element_present(driver, by, locator, timeout=10):
    """Assert that an element is present and visible on the page

    Args:
        driver: The WebDriver instance
        by: The locator strategy (e.g., AppiumBy.XPATH)
        locator: The locator string
        timeout: Maximum time to wait for element (default 10 seconds)
    """
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, locator))
        )
    except:
        raise AssertionError(f"Element not found with locator: {locator}")


def assert_element_not_present(driver, by, locator, timeout=10):
    """Assert that an element is not present on the page

    Args:
        driver: The WebDriver instance
        by: The locator strategy (e.g., AppiumBy.XPATH)
        locator: The locator string
        timeout: Maximum time to wait for element (default 10 seconds)
    """
    try:
        WebDriverWait(driver, timeout).until_not(
            EC.presence_of_element_located((by, locator))
        )
    except:
        raise AssertionError(
            f"Element was found but should not be present with locator: {locator}"
        )


def assert_element_count(driver, by, locator, expected_count, timeout=10):
    """Assert that a specific number of elements are present on the page

    Args:
        driver: The WebDriver instance
        by: The locator strategy (e.g., AppiumBy.XPATH)
        locator: The locator string
        expected_count: The expected number of elements
        timeout: Maximum time to wait for elements (default 10 seconds)
    """
    elements = WebDriverWait(driver, timeout).until(
        lambda d: d.find_elements(by, locator)
    )
    actual_count = len(elements)
    assert (
        actual_count == expected_count
    ), f"Expected {expected_count} elements, but found {actual_count}."
