import pytest
from fixtures.auth_token import auth_token


@pytest.fixture(scope="session")
def base_url():
    return "http://localhost:3000/api"
