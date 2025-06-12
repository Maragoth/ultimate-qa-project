import pytest
import json
from uuid import uuid4
from pathlib import Path
from utils.helpers import (
    authorized_post_request,
    authorized_get_request,
    authorized_put_request,
    authorized_delete_request,
    validate_schema,
    log_response,
)


@pytest.mark.articles
def test_full_article_crud(base_url, auth_token):
    # === POST: create article ===
    url = f"{base_url}/articles"
    payload = {
        "article": {
            "title": f"QA Test Article {uuid4()}",
            "description": "Initial description",
            "body": "This is the initial body of the test article.",
            "tagList": ["qa", "test", "automation"],
        }
    }

    response = authorized_post_request(url, auth_token, json_data=payload)
    log_response(response)

    assert response.status_code == 201
    assert response.elapsed.total_seconds() < 1

    slug = response.json()["article"]["slug"]

    # === GET: verify article exists ===
    get_url = f"{base_url}/articles/{slug}"
    response = authorized_get_request(get_url, auth_token)
    log_response(response)

    assert response.status_code == 200
    assert response.elapsed.total_seconds() < 1

    article_data = response.json()["article"]
    assert article_data["title"] == payload["article"]["title"]
    assert article_data["description"] == payload["article"]["description"]

    # === Validate response schema ===
    schema_path = Path(__file__).parent / "schemas" / "article.schema.json"
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    validate_schema(response.json(), schema)

    # === PUT: update article ===
    update_payload = {
        "article": {
            "title": f"{payload['article']['title']} Updated",
            "description": "Updated description",
            "body": "Updated body content.",
            "tagList": ["qa", "test", "updated"],
        }
    }

    response = authorized_put_request(get_url, auth_token, json_data=update_payload)
    log_response(response)

    assert response.status_code == 200
    assert response.elapsed.total_seconds() < 1

    updated_article = response.json()["article"]
    assert updated_article["title"] == update_payload["article"]["title"]
    assert updated_article["description"] == update_payload["article"]["description"]

    # Update slug after PUT
    slug = updated_article["slug"]
    get_url = f"{base_url}/articles/{slug}"

    # === DELETE: cleanup ===
    response = authorized_delete_request(get_url, auth_token)
    log_response(response)

    assert response.status_code == 204

    # === GET: verify deletion ===
    response = authorized_get_request(get_url, auth_token)
    log_response(response)

    assert response.status_code == 404
    assert response.elapsed.total_seconds() < 1
