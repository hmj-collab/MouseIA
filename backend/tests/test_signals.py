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

    project_response = client.post(
        "/projects",
        json={
            "name": "Signal Test Project",
            "description": "Projeto para testes de signals",
            "tags": ["test"],
        },
        headers=headers,
    )
    assert project_response.status_code == 201
    project_id = project_response.json()["id"]

    asset_response = client.post(
        "/assets",
        json={
            "name": "Signal Test Asset",
            "asset_type": "url",
            "value": "https://signal-test.local",
            "description": "Ativo para testes de signals",
            "is_active": True,
            "project_id": project_id,
        },
        headers=headers,
    )
    assert asset_response.status_code == 201
    asset_id = asset_response.json()["id"]

    create_response = client.post(
        "/signals",
        json={
            "source": "scanner",
            "signal_type": "tls",
            "severity": "high",
            "confidence": 90,
            "description": "TLS version is outdated",
            "asset_id": asset_id,
        },
        headers=headers,
    )

    assert create_response.status_code == 201
    created = create_response.json()
    assert created["signal_type"] == "tls"
    assert created["asset_id"] == asset_id

    update_response = client.put(
        f"/signals/{created['id']}",
        json={
            "severity": "critical",
            "confidence": 95,
            "description": "Updated signal description",
        },
        headers=headers,
    )
    assert update_response.status_code == 200
    updated = update_response.json()
    assert updated["severity"] == "critical"
    assert updated["confidence"] == 95
    assert updated["description"] == "Updated signal description"

    list_response = client.get(f"/signals?asset_id={asset_id}&min_confidence=90", headers=headers)
    assert list_response.status_code == 200
    assert any(item["id"] == created["id"] for item in list_response.json())

    delete_response = client.delete(f"/signals/{created['id']}", headers=headers)
    assert delete_response.status_code == 204

    get_response = client.get(f"/signals/{created['id']}", headers=headers)
    assert get_response.status_code == 404
