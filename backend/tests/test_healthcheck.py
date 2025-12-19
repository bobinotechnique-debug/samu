from datetime import datetime

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.routes.health import get_readiness_checker


@pytest.fixture
def readiness_override(app: FastAPI):
    def _override(checks: dict[str, str]):
        def _checker() -> dict[str, str]:
            return checks

        app.dependency_overrides[get_readiness_checker] = lambda: _checker

    yield _override
    app.dependency_overrides.pop(get_readiness_checker, None)


def _assert_timestamp_isoformat(timestamp: str) -> None:
    parsed = datetime.fromisoformat(timestamp)
    assert parsed.isoformat() == timestamp


def test_health_live_returns_ok_status(client: TestClient) -> None:
    response = client.get("/health/live")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    _assert_timestamp_isoformat(payload["timestamp"])
    assert payload["checks"] == {}


def test_health_ready_includes_checks(client: TestClient, readiness_override) -> None:
    readiness_override({"db": "ok"})

    response = client.get("/health/ready")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["checks"] == {"db": "ok"}
    _assert_timestamp_isoformat(payload["timestamp"])


def test_health_ready_returns_error_status_on_failure(
    client: TestClient, readiness_override
) -> None:
    readiness_override({"db": "error"})

    response = client.get("/health/ready")

    assert response.status_code == 503
    payload = response.json()
    assert payload["status"] == "error"
    assert payload["checks"] == {"db": "error"}
    _assert_timestamp_isoformat(payload["timestamp"])


def test_health_readiness_alias_matches_payload(client: TestClient, readiness_override) -> None:
    readiness_override({"db": "ok"})

    response = client.get("/api/v1/health")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["checks"] == {"db": "ok"}
    _assert_timestamp_isoformat(payload["timestamp"])
