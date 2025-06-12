import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from pages.login_page import LoginPage
from helpers.api_helpers import create_random_user_via_api
from helpers.config import BASE_URL
from helpers.assertions import verify_logged_in


@pytest.mark.mobile
def test_user_can_login_successfully_using_dynamic_user(driver):
    """Test that a user can successfully log in with valid credentials"""

    # Create user first to minimize delay between creation and usage
    user = create_random_user_via_api()

    # Navigate directly to the login page and perform login
    login_page = LoginPage(driver)
    login_page.navigate(BASE_URL)
    login_page.login(user["email"], user["password"])

    # Verify successful login
    verify_logged_in(driver)
