import pytest
from utils.helpers import get_request, get_auth_headers, log_response
from time import time


@pytest.mark.api
def test_malformed_token_returns_401(base_url):
    # GIVEN: A malformed JWT
    url = f"{base_url}/user"
    headers = {
        "Authorization": "Token malformed.token.value",
        "Content-Type": "application/json",
    }

    # WHEN: Sending GET /user with malformed token
    response = get_request(url, headers=headers)

    # THEN: Should return 401 Unauthorized and respond within 1s
    log_response(response)
    assert response.status_code == 401
    assert response.elapsed.total_seconds() < 1.0


@pytest.mark.api
def test_missing_token_returns_401(base_url):
    # GIVEN: No Authorization header
    url = f"{base_url}/user"
    headers = {"Content-Type": "application/json"}

    # WHEN: Sending GET /user without token
    response = get_request(url, headers=headers)

    # THEN: Should return 401 Unauthorized and respond within 1s
    log_response(response)
    assert response.status_code == 401
    assert response.elapsed.total_seconds() < 1.0


@pytest.mark.api
def test_tampered_token_returns_401(auth_token, base_url):
    # GIVEN: A valid token modified (tampered)
    tampered_token = auth_token[:-5] + "abcde"
    headers = {
        "Authorization": f"Token {tampered_token}",
        "Content-Type": "application/json",
    }
    url = f"{base_url}/user"

    # WHEN: Sending GET /user with tampered token
    response = get_request(url, headers=headers)

    # THEN: Should return 401 Unauthorized and respond within 1s
    log_response(response)
    assert response.status_code == 401
    assert response.elapsed.total_seconds() < 1.0
