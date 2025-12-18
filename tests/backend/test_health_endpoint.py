import pathlib
import sys
from fastapi.testclient import TestClient

backend_path = pathlib.Path(__file__).resolve().parents[2] / "backend"
sys.path.append(str(backend_path))

from app.main import app  # type: ignore  # noqa: E402


def test_health_live_endpoint_returns_status() -> None:
    client = TestClient(app)
    response = client.get("/api/v1/health/live")

    assert response.status_code == 200
    assert response.json() == {"status": "live"}
