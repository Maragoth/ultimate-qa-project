import pytest
from utils.helpers import post_request


@pytest.fixture(scope="session")
def auth_token(base_url):
    register_url = f"{base_url}/users"
    login_url = f"{base_url}/users/login"

    user_data = {
        "email": "qa@tester.com",
        "username": "qa_tester",
        "password": "Test123!",
    }

    # Register (ignore 422 error)
    post_request(register_url, json_data={"user": user_data})

    # Login
    response = post_request(
        login_url,
        json_data={
            "user": {"email": user_data["email"], "password": user_data["password"]}
        },
    )
    assert response.status_code == 200
    return response.json()["user"]["token"]
