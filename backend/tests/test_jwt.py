from fastapi.testclient import TestClient

from app.main import app


def test_jwt_login_and_protected_access() -> None:
    client = TestClient(app)

    login_response = client.post(
        "/auth/login",
        json={"username": "admin", "password": "password123"},
    )

    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    protected_response = client.get(
        "/protected",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert protected_response.status_code == 200
    assert protected_response.json()["user"] == "admin"
