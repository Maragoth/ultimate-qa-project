import pytest
from utils.helpers import (
    create_test_article,
    authorized_get_request,
    log_response,
    validate_schema,
)
import json


@pytest.mark.api
def test_article_response_schema_strict(auth_token, base_url):
    # GIVEN: A test article exists
    article = create_test_article(base_url, auth_token)
    slug = article["slug"]
    url = f"{base_url}/articles/{slug}"

    # WHEN: We fetch the article
    response = authorized_get_request(url, auth_token)
    log_response(response)

    # THEN: Status 200 and fast response
    assert response.status_code == 200
    assert response.elapsed.total_seconds() < 1.0

    # AND: Schema strictly matches response
    from tests.schemas.article_schema_strict import schema as article_schema

    response_json = response.json()
    validate_schema(response_json, article_schema)


@pytest.mark.api
def test_no_unexpected_fields_in_article(auth_token, base_url):
    # GIVEN: A test article exists
    article = create_test_article(base_url, auth_token)
    slug = article["slug"]
    url = f"{base_url}/articles/{slug}"

    # WHEN: We fetch the article
    response = authorized_get_request(url, auth_token)
    log_response(response)
    assert response.status_code == 200
    assert response.elapsed.total_seconds() < 1.0

    # THEN: No unexpected fields in article object
    article_obj = response.json()["article"]
    unexpected = {"debug", "internalId", "__v", "stackTrace", "error", "trace"}
    assert unexpected.isdisjoint(article_obj.keys())
