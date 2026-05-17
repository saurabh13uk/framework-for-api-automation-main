import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest

from api.client import JsonPlaceholderClient
from config.settings import BASE_URL, REQUEST_TIMEOUT


@pytest.fixture(scope="session")
def api_client() -> JsonPlaceholderClient:
    return JsonPlaceholderClient(BASE_URL, REQUEST_TIMEOUT)


@pytest.fixture(scope="session")
def posts_response(api_client):
    return api_client.get_posts_response()


@pytest.fixture(scope="session")
def posts(posts_response):
    posts_response.raise_for_status()
    return posts_response.json()

