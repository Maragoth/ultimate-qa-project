import pytest
import json
from pathlib import Path
from utils.helpers import (
    create_test_user,
    authorized_post_request,
    authorized_get_request,
    authorized_delete_request,
    validate_schema,
    log_response,
)


@pytest.mark.profiles
def test_follow_unfollow_user(base_url, auth_token):
    # Create a second user to follow
    target_user = create_test_user(base_url)
    username = target_user["username"]

    follow_url = f"{base_url}/profiles/{username}/follow"
    profile_url = f"{base_url}/profiles/{username}"

    # === POST: Follow the user ===
    response = authorized_post_request(follow_url, auth_token)
    log_response(response)
    assert response.status_code == 200
    assert response.elapsed.total_seconds() < 1
    assert response.json()["profile"]["following"] is True

    # === GET: Get followed profile ===
    response = authorized_get_request(profile_url, auth_token)
    log_response(response)
    assert response.status_code == 200
    assert response.elapsed.total_seconds() < 1
    assert response.json()["profile"]["following"] is True

    # Validate schema
    schema_path = Path(__file__).parent / "schemas" / "profile.schema.json"
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)
    validate_schema(response.json(), schema)

    # === DELETE: Unfollow the user ===
    response = authorized_delete_request(follow_url, auth_token)
    log_response(response)
    assert response.status_code == 200
    assert response.elapsed.total_seconds() < 1
    assert response.json()["profile"]["following"] is False
