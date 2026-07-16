import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def _admin_headers() -> dict[str, str]:
    resp = client.post("/auth/login", json={"username": "admin", "password": "password123"})
    assert resp.status_code == 200
    return {"Authorization": f"Bearer {resp.json()['access_token']}"}


def _viewer_headers() -> dict[str, str]:
    resp = client.post("/auth/login", json={"username": "viewer", "password": "password123"})
    assert resp.status_code == 200
    return {"Authorization": f"Bearer {resp.json()['access_token']}"}


def test_companies_crud_flow() -> None:
    headers = _admin_headers()

    # Criar empresa
    create_resp = client.post(
        "/companies",
        json={
            "name": "Test Company",
            "domain": "testcompany.com",
            "description": "Uma empresa de teste",
            "is_active": True,
        },
        headers=headers,
    )
    assert create_resp.status_code == 201
    created = create_resp.json()
    assert created["name"] == "Test Company"
    assert created["domain"] == "testcompany.com"
    assert created["description"] == "Uma empresa de teste"
    assert created["is_active"] is True
    company_id = created["id"]

    # Listar empresas
    list_resp = client.get("/companies", headers=headers)
    assert list_resp.status_code == 200
    assert any(c["id"] == company_id for c in list_resp.json())

    # Buscar por ID
    get_resp = client.get(f"/companies/{company_id}", headers=headers)
    assert get_resp.status_code == 200
    assert get_resp.json()["name"] == "Test Company"

    # Atualizar empresa
    update_resp = client.put(
        f"/companies/{company_id}",
        json={
            "name": "Test Company Updated",
            "domain": "updated.com",
        },
        headers=headers,
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["name"] == "Test Company Updated"
    assert update_resp.json()["domain"] == "updated.com"

    # Deletar empresa
    delete_resp = client.delete(f"/companies/{company_id}", headers=headers)
    assert delete_resp.status_code == 204

    # Confirmar deletado
    get_after_delete = client.get(f"/companies/{company_id}", headers=headers)
    assert get_after_delete.status_code == 404


def test_viewer_cannot_mutate_companies() -> None:
    viewer_headers = _viewer_headers()

    # Viewer can read list
    list_resp = client.get("/companies", headers=viewer_headers)
    assert list_resp.status_code == 200

    # Viewer cannot create
    create_resp = client.post(
        "/companies",
        json={
            "name": "Unauthorized Company",
        },
        headers=viewer_headers,
    )
    assert create_resp.status_code == 403

    # Viewer cannot delete
    delete_resp = client.delete("/companies/1", headers=viewer_headers)
    assert delete_resp.status_code == 403
