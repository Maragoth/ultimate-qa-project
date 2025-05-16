import pytest
import json
from pathlib import Path
from utils.helpers import (
    authorized_post_request,
    authorized_get_request,
    authorized_delete_request,
    validate_schema,
    log_response,
)

@pytest.mark.comments
def test_full_comment_crud(base_url, auth_token):
    slug = "Try-to-bypass-the-SCSI-sensor-maybe-it-will-generate-the-1080p-card!-1"
    comment_url = f"{base_url}/articles/{slug}/comments"

    # === POST: Add comment ===
    comment_payload = {
        "comment": {
            "body": "This is a test comment created via API."
        }
    }
    response = authorized_post_request(comment_url, auth_token, json_data=comment_payload)
    log_response(response)

    assert response.status_code == 200
    comment_data = response.json()["comment"]

    # Validate schema for single comment
    comment_schema_path = Path(__file__).parent / "schemas" / "comment.schema.json"
    with open(comment_schema_path, "r", encoding="utf-8") as f:
        comment_schema = json.load(f)
    validate_schema(response.json(), comment_schema)

    comment_id = comment_data["id"]

    # === GET: verify comment exists ===
    response = authorized_get_request(comment_url, auth_token)
    log_response(response)

    assert response.status_code == 200

    # Validate schema for comments list
    comments_schema_path = Path(__file__).parent / "schemas" / "comments.schema.json"
    with open(comments_schema_path, "r", encoding="utf-8") as f:
        comments_schema = json.load(f)
    validate_schema(response.json(), comments_schema)

    comments = response.json()["comments"]
    assert any(c["id"] == comment_id for c in comments)

    # === DELETE: delete comment ===
    delete_url = f"{comment_url}/{comment_id}"
    response = authorized_delete_request(delete_url, auth_token)
    log_response(response)

    assert response.status_code == 200
