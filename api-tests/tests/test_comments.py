import pytest
import json
from uuid import uuid4
from pathlib import Path
from utils.helpers import (
    authorized_post_request,
    authorized_get_request,
    authorized_delete_request,
    validate_schema,
    log_response,
    create_test_article,
)


@pytest.mark.comments
def test_full_comment_crud(base_url, auth_token):
    # Create article to comment on
    article = create_test_article(base_url, auth_token)
    slug = article["slug"]
    comment_url = f"{base_url}/articles/{slug}/comments"

    # === POST: Add comment ===
    comment_payload = {"comment": {"body": f"This is a test comment {uuid4()}"}}
    response = authorized_post_request(
        comment_url, auth_token, json_data=comment_payload
    )
    log_response(response)
    assert response.status_code == 200
    assert response.elapsed.total_seconds() < 1

    # Validate response schema
    schema_path = Path(__file__).parent / "schemas" / "comment.schema.json"
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)
    validate_schema(response.json(), schema)

    comment_id = response.json()["comment"]["id"]

    # === GET: Retrieve all comments for the article ===
    response = authorized_get_request(comment_url, auth_token)
    log_response(response)
    assert response.status_code == 200
    assert response.elapsed.total_seconds() < 1

    # Validate response schema for multiple comments
    schema_path = Path(__file__).parent / "schemas" / "comments.schema.json"
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)
    validate_schema(response.json(), schema)

    # === DELETE: Delete the comment ===
    delete_url = f"{comment_url}/{comment_id}"
    response = authorized_delete_request(delete_url, auth_token)
    log_response(response)
    assert response.status_code == 200
    assert response.elapsed.total_seconds() < 1
