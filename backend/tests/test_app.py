from fastapi.testclient import TestClient


def test_app_starts(client: TestClient):
    response = client.get("/api/v1/health/live")
    assert response.status_code == 200


def test_health_live(client: TestClient):
    response = client.get("/api/v1/health/live")
    assert response.status_code == 200
    assert response.json() == {"status": "live"}


def test_health_ready_db(client: TestClient):
    response = client.get("/api/v1/health/ready")
    assert response.status_code == 200
    assert response.json()["status"] == "ready"
