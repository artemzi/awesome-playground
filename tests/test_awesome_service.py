import logging
from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient

from awesome_playground.awesome_service import app, create_app

client = TestClient(app)


def test_root() -> None:
    response = client.get("/")
    assert response.status_code == HTTPStatus.OK
    assert response.json()["message"] == "Welcome to Awesome Service!"


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == HTTPStatus.OK
    assert response.json()["status"] == "healthy"


def test_item_valid() -> None:
    response = client.get("/items/1")
    assert response.status_code == HTTPStatus.OK


def test_item_invalid() -> None:
    response = client.get("/items/0")
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_lifespan_logging(caplog: pytest.LogCaptureFixture) -> None:
    caplog.set_level(logging.INFO)
    application = create_app()
    with TestClient(application) as lifespan_client:
        response = lifespan_client.get("/health")
        assert response.status_code == HTTPStatus.OK
    lifespan_messages = [r.message for r in caplog.records]
    assert any("starting service" in msg for msg in lifespan_messages)
    assert any("stopping service" in msg for msg in lifespan_messages)
