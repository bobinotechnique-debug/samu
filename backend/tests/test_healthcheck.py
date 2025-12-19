from fastapi.testclient import TestClient


def test_health_probe_returns_live_status(client: TestClient) -> None:
    response = client.get("/health/live")

    assert response.status_code == 200
    assert response.json() == {"status": "live"}
