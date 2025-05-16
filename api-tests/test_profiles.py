import pytest
import json
from pathlib import Path
from utils.helpers import authorized_get_request, authorized_post_request, authorized_delete_request, validate_schema, log_response


@pytest.mark.profiles
def test_get_profile(base_url, auth_token):
    username = "qa-tester"
    url = f"{base_url}/profiles/{username}"

    response = authorized_get_request(url, auth_token)
    log_response(response)

    assert response.status_code == 200
    assert response.elapsed.total_seconds() < 1

    # validate schema
    schema_path = Path(__file__).parent / "schemas" / "profile.schema.json"
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)
    validate_schema(response.json(), schema)

    profile_data = response.json()["profile"]
    assert profile_data["username"] == username


@pytest.mark.profiles
def test_follow_unfollow_profile(base_url, auth_token):
    username_to_follow = "qa-tester"
    follow_url = f"{base_url}/profiles/{username_to_follow}/follow"

    # Follow user
    response = authorized_post_request(follow_url, auth_token)
    log_response(response)

    assert response.status_code == 200
    assert response.json()["profile"]["following"] is True

    # Unfollow user
    response = authorized_delete_request(follow_url, auth_token)
    log_response(response)

    assert response.status_code == 200
    assert response.json()["profile"]["following"] is False
