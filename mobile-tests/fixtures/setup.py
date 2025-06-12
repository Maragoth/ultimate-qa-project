from appium import webdriver
from appium.options.android import UiAutomator2Options
from pathlib import Path
import pytest


@pytest.fixture(scope="function")
def driver():
    options = UiAutomator2Options()

    # Basic platform settings
    options.platform_name = "Android"
    options.platform_version = "15"
    options.device_name = "Android"
    options.automation_name = "UiAutomator2"
    options.browser_name = "Chrome"

    # Basic Appium settings
    options.set_capability("autoGrantPermissions", True)
    options.set_capability("disableWindowAnimation", True)
    options.set_capability("uiautomator2ServerInstallTimeout", 60000)
    options.set_capability(
        "chromedriverExecutable",
        str(Path(__file__).parent.parent / "drivers" / "chromedriver.exe"),
    )

    # Chrome-specific mobile settings
    chrome_options = {
        "args": [
            "--disable-notifications",
            "--disable-popup-blocking",
            "--disable-infobars",
            "--disable-translate",
            "--disable-extensions",
            "--disable-default-apps",
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--lang=en-US",
            "--disable-features=TranslateUI",
            "--disable-blink-features=AutomationControlled",
            "--disable-web-security",
            "--disable-site-isolation-trials",
            "--enable-automation",
            "--enable-features=NetworkService,NetworkServiceInProcess",
        ]
    }
    options.set_capability("goog:chromeOptions", chrome_options)

    # Additional mobile settings
    options.set_capability("nativeWebScreenshot", True)
    options.set_capability("autoAcceptAlerts", True)
    options.set_capability("autoDismissAlerts", True)
    options.set_capability("newCommandTimeout", 300)
    options.set_capability("chromedriverDisableBuildCheck", True)
    options.set_capability("ensureWebviewsHavePages", True)
    options.set_capability("webviewDevtoolsPort", 9222)

    # Initialize the driver with options
    driver = webdriver.Remote(command_executor="http://localhost:4723", options=options)
    driver.implicitly_wait(3)  # Keep reasonable implicit wait for element location

    # Set window size for mobile view
    driver.set_window_size(390, 844)  # iPhone 12 Pro dimensions

    yield driver
    driver.quit()
