from appium import webdriver
from appium.options.android import UiAutomator2Options
from pathlib import Path
import pytest

@pytest.fixture(scope="function")
def driver():
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.platform_version = "15"
    options.device_name = "Android"
    options.automation_name = "UiAutomator2"
    options.browser_name = "Chrome"
    options.set_capability("autoGrantPermissions", True)
    options.set_capability("disableWindowAnimation", True)
    options.set_capability("uiautomator2ServerInstallTimeout", 60000)
    options.set_capability(
        "chromedriverExecutable",
        str(Path(__file__).parent.parent / "drivers" / "chromedriver.exe")
    )
    
    # Enhanced Chrome options for better performance
    options.set_capability("chromeOptions", {
        "args": [
            "--disable-notifications",
            "--disable-popup-blocking",
            "--disable-infobars",
            "--disable-translate",
            "--disable-extensions",
            "--disable-default-apps",
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--lang=en-US",  # Force English language
            "--disable-features=TranslateUI"  # Disable translation UI
        ]
    })

    # Use the newer client_config approach
    driver = webdriver.Remote(
        command_executor="http://localhost:4723",
        options=options,
        keep_alive=True  # This replaces the deprecated connection pooling
    )
    driver.implicitly_wait(5)  # Reduced from 10 to 5 seconds for faster failure detection
    yield driver
    driver.quit()
