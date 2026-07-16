from fastapi.testclient import TestClient

from app.main import app


def test_auth_flow() -> None:
    client = TestClient(app)

    response = client.post(
        "/auth/login",
        json={"username": "admin", "password": "password123"},
    )

    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert response.json()["access_token"]
