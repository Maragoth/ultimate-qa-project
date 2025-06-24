import sys
import os

# Add parent directory to sys.path for proper module resolution
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from pages.login_page import LoginPage
from helpers.api_helpers import create_random_user_via_api
from helpers.config import BASE_URL
from helpers.assertions import verify_logged_in


@pytest.mark.mobile
def test_user_can_login_successfully_using_dynamic_user(driver):
    """Test that a user can successfully log in with valid credentials"""

    # Step 1: Create a new user via API to ensure credentials are valid
    user = create_random_user_via_api()

    # Step 2: Navigate to the login page and log in using created credentials
    login_page = LoginPage(driver)
    login_page.navigate(BASE_URL)
    login_page.login(user["email"], user["password"])

    # Step 3: Verify that the user is successfully logged in (UI check)
    verify_logged_in(driver)
