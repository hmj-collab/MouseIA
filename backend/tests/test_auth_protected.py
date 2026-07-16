from fastapi.testclient import TestClient

from app.main import app


def test_protected_route_requires_token() -> None:
    client = TestClient(app)

    response = client.get("/protected")

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"
