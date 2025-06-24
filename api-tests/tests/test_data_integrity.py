import pytest
from uuid import uuid4
from utils.helpers import (
    post_request,
    get_request,
    delete_request,
    log_response,
    authorized_post_comment,
    authorized_get_comment,
    create_test_article,
)


@pytest.mark.api
def test_created_article_is_immediately_accessible(auth_token, base_url):
    # GIVEN: A new, unique article payload
    unique = uuid4().hex[:5]
    url = f"{base_url}/articles"
    headers = {
        "Authorization": f"Token {auth_token}",
        "Content-Type": "application/json",
    }
    payload = {
        "article": {
            "title": f"InstantTest-{unique}",
            "description": "Should be instantly visible",
            "body": "Integrity test body",
            "tagList": ["integrity"],
        }
    }

    # WHEN: Creating article
    create_response = post_request(url, headers=headers, json_data=payload)
    log_response(create_response)
    assert create_response.status_code == 201
    assert create_response.elapsed.total_seconds() < 1.0

    slug = create_response.json()["article"]["slug"]

    # THEN: Immediately fetch the article via GET
    get_url = f"{base_url}/articles/{slug}"
    get_response = get_request(get_url, headers=headers)
    log_response(get_response)
    assert get_response.status_code == 200
    assert get_response.elapsed.total_seconds() < 1.0


@pytest.mark.api
def test_deleting_article_removes_comments(auth_token, base_url):
    # GIVEN: An article with a comment
    article = create_test_article(base_url, auth_token)
    slug = article["slug"]

    comment_url = f"{base_url}/articles/{slug}/comments"
    comment_payload = {"comment": {"body": "Comment to be deleted"}}

    # WHEN: Post comment
    comment_response = authorized_post_comment(comment_url, auth_token, comment_payload)
    log_response(comment_response)
    assert comment_response.status_code in [200, 201]
    assert comment_response.elapsed.total_seconds() < 1.0

    comment_id = comment_response.json()["comment"]["id"]

    # AND: Delete the article
    article_url = f"{base_url}/articles/{slug}"
    delete_response = delete_request(
        article_url, headers={"Authorization": f"Token {auth_token}"}
    )
    log_response(delete_response)
    assert delete_response.status_code == 204

    # THEN: Verify that the comment is gone
    get_comment_url = f"{base_url}/articles/{slug}/comments"
    comment_get_response = authorized_get_comment(get_comment_url, auth_token)
    log_response(comment_get_response)
    assert comment_get_response.status_code == 200
    assert all(
        c["id"] != comment_id for c in comment_get_response.json().get("comments", [])
    )
