import pytest
from starlette.testclient import TestClient

from web.main import create_app


class InMemoryUserWebClient:
    _base_url = "/users"

    def __init__(self):
        self._client = TestClient(create_app(users={}))

    def create(self, payload: dict):
        return self._client.post(url=self._base_url, json=payload)

    def get_all(self):
        return self._client.get(url=self._base_url)

    def remove(self, email: str):
        return self._client.delete(url=f"{self._base_url}/{email}")


@pytest.fixture
def web_client():
    return InMemoryUserWebClient
