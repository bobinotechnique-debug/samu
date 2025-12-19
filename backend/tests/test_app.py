from fastapi.testclient import TestClient


def test_app_starts(client: TestClient):
    response = client.get("/health/live")
    assert response.status_code == 200


def test_health_live(client: TestClient):
    response = client.get("/health/live")
    assert response.status_code == 200
    assert response.json() == {"status": "live"}


def test_health_ready_db(client: TestClient):
    response = client.get("/health/ready")
    assert response.status_code == 200
    assert response.json()["status"] == "ready"


def test_health_ready_alias(client: TestClient):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ready"}


def test_request_and_correlation_headers(client: TestClient):
    correlation_id = "corr-123"
    response = client.get("/health/live", headers={"X-Correlation-ID": correlation_id})
    assert response.status_code == 200
    assert response.headers.get("X-Request-ID")
    assert response.headers.get("X-Correlation-ID") == correlation_id
