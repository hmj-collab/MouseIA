from fastapi.testclient import TestClient

from app.main import app


def test_signals_crud_flow() -> None:
    client = TestClient(app)

    login_response = client.post(
        "/auth/login",
        json={"username": "admin", "password": "password123"},
    )
    assert login_response.status_code == 200

    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    create_response = client.post(
        "/signals",
        json={
            "source": "scanner",
            "signal_type": "tls",
            "severity": "high",
            "confidence": 90,
            "description": "TLS version is outdated",
            "site_id": 1,
        },
        headers=headers,
    )

    assert create_response.status_code == 201
    created = create_response.json()
    assert created["signal_type"] == "tls"

    list_response = client.get("/signals", headers=headers)
    assert list_response.status_code == 200
    assert any(item["id"] == created["id"] for item in list_response.json())
