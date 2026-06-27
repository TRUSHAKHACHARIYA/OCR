from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check_returns_healthy() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "OCRDIL"
    assert data["version"] == "0.2.0"
    assert "timestamp" in data
