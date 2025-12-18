import os
from importlib import reload

TEST_DATABASE_URL = "sqlite+pysqlite:///:memory:"
TEST_REDIS_URL = "redis://localhost:6379/0"

os.environ.setdefault("SAMU_DATABASE_URL", TEST_DATABASE_URL)
os.environ.setdefault("SAMU_REDIS_URL", TEST_REDIS_URL)
os.environ.setdefault("SAMU_TESTING", "true")
os.environ.setdefault("SAMU_ENVIRONMENT", "ci")

from fastapi.testclient import TestClient

import app.core.config as config
from app.main import create_app


def make_client() -> TestClient:
    os.environ["SAMU_DATABASE_URL"] = TEST_DATABASE_URL
    os.environ["SAMU_REDIS_URL"] = TEST_REDIS_URL
    os.environ["SAMU_TESTING"] = "true"
    os.environ["SAMU_ENVIRONMENT"] = "ci"
    config.get_settings.cache_clear()
    reload(config)
    app = create_app()
    return TestClient(app)


def test_app_starts():
    client = make_client()
    response = client.get("/api/v1/health/live")
    assert response.status_code == 200


def test_health_live():
    client = make_client()
    response = client.get("/api/v1/health/live")
    assert response.status_code == 200
    assert response.json() == {"status": "live"}


def test_health_ready_db():
    client = make_client()
    response = client.get("/api/v1/health/ready")
    assert response.status_code == 200
    assert response.json()["status"] == "ready"


def test_error_model_shape():
    client = make_client()
    response = client.get("/api/v1/orgs/")
    assert response.status_code == 401
    payload = response.json()
    assert payload["error"]["code"] == "http_error"
    assert "message" in payload["error"]
    assert "details" in payload["error"]
