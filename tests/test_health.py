from unittest.mock import patch

from app.main import app

from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError


client = TestClient(app)


def test_health_check() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "api": "ok",
        "database": "ok",
    }


def test_health_check_database_unavailable() -> None:
    with patch(
        "app.routers.health.engine.connect",
        side_effect=SQLAlchemyError("Database connection failed"),
    ):
        response = client.get("/health")

    assert response.status_code == 503
    assert response.json() == {
        "detail": "Database is unavailable",
    }