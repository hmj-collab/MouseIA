from fastapi.testclient import TestClient

from app.main import app


def test_viewer_cannot_create_site() -> None:
    client = TestClient(app)

    login_response = client.post(
        "/auth/login",
        json={"username": "viewer", "password": "password123"},
    )
    assert login_response.status_code == 200

    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    create_response = client.post(
        "/sites",
        json={
            "name": "Forbidden Site",
            "url": "https://example.org",
            "description": "Should not be created",
            "tags": ["forbidden"],
        },
        headers=headers,
    )

    assert create_response.status_code == 403
