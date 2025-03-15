import pytest

from fastapi.testclient import TestClient
from api.todo import app


@pytest.fixture
def client():
    return TestClient(app=app)