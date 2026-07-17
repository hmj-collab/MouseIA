from fastapi.testclient import TestClient

from app.main import app


def test_findings_crud_flow() -> None:
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
            "name": "Finding Test Project",
            "description": "Projeto para testes de findings",
            "tags": ["test"],
        },
        headers=headers,
    )
    assert project_response.status_code == 201
    project_id = project_response.json()["id"]

    asset_response = client.post(
        "/assets",
        json={
            "name": "Finding Test Asset",
            "asset_type": "url",
            "value": "https://finding-test.local",
            "description": "Ativo para testes de findings",
            "is_active": True,
            "project_id": project_id,
        },
        headers=headers,
    )
    assert asset_response.status_code == 201
    asset_id = asset_response.json()["id"]

    signal_response = client.post(
        "/signals",
        json={
            "source": "scanner",
            "signal_type": "http",
            "severity": "medium",
            "confidence": 60,
            "description": "HTTP discrepancy detected",
            "asset_id": asset_id,
        },
        headers=headers,
    )
    assert signal_response.status_code == 201
    signal_id = signal_response.json()["id"]

    create_response = client.post(
        "/findings",
        json={
            "title": "Outdated TLS configuration",
            "description": "The site is exposing an outdated TLS version.",
            "severity": "high",
            "status": "open",
            "signal_id": signal_id,
        },
        headers=headers,
    )

    assert create_response.status_code == 201
    created = create_response.json()
    assert created["title"] == "Outdated TLS configuration"
    assert created["signal_id"] == signal_id

    update_response = client.put(
        f"/findings/{created['id']}",
        json={
            "status": "closed",
            "severity": "critical",
        },
        headers=headers,
    )
    assert update_response.status_code == 200
    updated = update_response.json()
    assert updated["status"] == "closed"
    assert updated["severity"] == "critical"

    list_response = client.get(f"/findings?status=closed&signal_id={signal_id}", headers=headers)
    assert list_response.status_code == 200
    assert any(item["id"] == created["id"] for item in list_response.json())

    delete_response = client.delete(f"/findings/{created['id']}", headers=headers)
    assert delete_response.status_code == 204

    get_response = client.get(f"/findings/{created['id']}", headers=headers)
    assert get_response.status_code == 404
