import pytest
import sys
from utils.helpers import post_request

@pytest.fixture(scope="session")
def base_url():
    return "http://localhost:3000/api"

@pytest.fixture(scope="session")
def auth_token(base_url):
    url = f"{base_url}/users/login"
    payload = {
        "user": {
            "email": "qa@tester.com",
            "password": "Test123!"
        }
    }
    response = post_request(url, json_data=payload)
    assert response.status_code == 200
    token = response.json()["user"]["token"]
    print(f"\nAuth Token: {token}\n", file=sys.stdout)
    return token
