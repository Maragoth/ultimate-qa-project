import requests
import jsonschema
from uuid import uuid4


def get_request(url, headers=None, params=None):
    response = requests.get(url, headers=headers, params=params)
    return response


def post_request(url, headers=None, data=None, json_data=None):
    response = requests.post(url, headers=headers, data=data, json=json_data)
    return response


def put_request(url, headers=None, data=None, json_data=None):
    response = requests.put(url, headers=headers, data=data, json=json_data)
    return response


def delete_request(url, headers=None):
    response = requests.delete(url, headers=headers)
    return response


def validate_schema(response_json, schema):
    jsonschema.validate(instance=response_json, schema=schema)


def get_auth_headers(token):
    return {"Authorization": f"Token {token}", "Content-Type": "application/json"}


def authorized_get_request(url, token, params=None):
    headers = get_auth_headers(token)
    response = get_request(url, headers=headers, params=params)
    return response


def authorized_post_request(url, token, data=None, json_data=None):
    headers = get_auth_headers(token)
    response = post_request(url, headers=headers, data=data, json_data=json_data)
    return response


def log_response(response):
    import json

    print(f"Status code: {response.status_code}")
    print(f"Response time: {response.elapsed.total_seconds()}s")

    try:
        response_json = response.json()

        # Trim large fields for readability (body & description)
        if "articles" in response_json and isinstance(response_json["articles"], list):
            for article in response_json["articles"]:
                for field in ["body", "description"]:
                    if field in article and isinstance(article[field], str):
                        article[field] = f"<{len(article[field])} characters>"

        print("Response body:", json.dumps(response_json, indent=2))

    except Exception:
        print("Response body (non-JSON):", response.text)


def authorized_put_request(url, token, data=None, json_data=None):
    headers = get_auth_headers(token)
    return put_request(url, headers=headers, data=data, json_data=json_data)


def authorized_delete_request(url, token):
    headers = get_auth_headers(token)
    return delete_request(url, headers=headers)


def authorized_post_comment(url, token, json_data):
    headers = get_auth_headers(token)
    return post_request(url, headers=headers, json_data=json_data)


def authorized_get_comment(url, token):
    headers = get_auth_headers(token)
    return get_request(url, headers=headers)


def authorized_delete_comment(url, token):
    headers = get_auth_headers(token)
    return delete_request(url, headers=headers)


def simple_get_request(url, headers=None, params=None):
    response = requests.get(url, headers=headers, params=params)
    return response


def create_test_article(base_url, token):
    payload = {
        "article": {
            "title": f"Article-{uuid4()}",
            "description": "test article",
            "body": "test body",
            "tagList": ["test"],
        }
    }
    url = f"{base_url}/articles"
    response = authorized_post_request(url, token, json_data=payload)
    assert response.status_code == 201
    return response.json()["article"]


def create_test_user(base_url):
    from uuid import uuid4

    email = f"test-{uuid4()}@mail.com"
    username = f"user-{uuid4()}"
    password = "Test123!"

    payload = {"user": {"email": email, "username": username, "password": password}}

    register_url = f"{base_url}/users"
    login_url = f"{base_url}/users/login"

    post_request(register_url, json_data=payload)
    response = post_request(
        login_url, json_data={"user": {"email": email, "password": password}}
    )
    assert response.status_code == 200

    token = response.json()["user"]["token"]
    return {"email": email, "username": username, "password": password, "token": token}
