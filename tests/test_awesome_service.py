from fastapi.testclient import TestClient

from awesome_playground.awesome_service import app

client = TestClient(app)


def test_root() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Welcome to Awesome Service!"


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_item_valid() -> None:
    response = client.get("/items/1")
    assert response.status_code == 200


def test_item_invalid() -> None:
    response = client.get("/items/0")
    assert response.status_code == 400
