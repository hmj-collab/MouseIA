from fastapi.testclient import TestClient

from app.main import app


def test_sites_require_authentication() -> None:
    client = TestClient(app)

    response = client.get("/sites")

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"
