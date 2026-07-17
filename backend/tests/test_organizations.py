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


def test_organizations_crud_flow() -> None:
    headers = _admin_headers()

    # Criar organizacao
    create_resp = client.post(
        "/organizations",
        json={
            "name": "Test Organization",
            "domain": "testorganization.com",
            "description": "Uma organizacao de teste",
            "is_active": True,
        },
        headers=headers,
    )
    assert create_resp.status_code == 201
    created = create_resp.json()
    assert created["name"] == "Test Organization"
    assert created["domain"] == "testorganization.com"
    assert created["description"] == "Uma organizacao de teste"
    assert created["is_active"] is True
    organization_id = created["id"]

    # Listar organizacoes
    list_resp = client.get("/organizations", headers=headers)
    assert list_resp.status_code == 200
    assert any(o["id"] == organization_id for o in list_resp.json())

    # Buscar por ID
    get_resp = client.get(f"/organizations/{organization_id}", headers=headers)
    assert get_resp.status_code == 200
    assert get_resp.json()["name"] == "Test Organization"

    # Atualizar organizacao
    update_resp = client.put(
        f"/organizations/{organization_id}",
        json={
            "name": "Test Organization Updated",
            "domain": "updated.com",
        },
        headers=headers,
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["name"] == "Test Organization Updated"
    assert update_resp.json()["domain"] == "updated.com"

    # Deletar organizacao
    delete_resp = client.delete(f"/organizations/{organization_id}", headers=headers)
    assert delete_resp.status_code == 204

    # Confirmar deletado
    get_after_delete = client.get(f"/organizations/{organization_id}", headers=headers)
    assert get_after_delete.status_code == 404


def test_viewer_cannot_mutate_organizations() -> None:
    viewer_headers = _viewer_headers()

    # Viewer can read list
    list_resp = client.get("/organizations", headers=viewer_headers)
    assert list_resp.status_code == 200

    # Viewer cannot create
    create_resp = client.post(
        "/organizations",
        json={
            "name": "Unauthorized Organization",
        },
        headers=viewer_headers,
    )
    assert create_resp.status_code == 403

    # Viewer cannot delete
    delete_resp = client.delete("/organizations/1", headers=viewer_headers)
    assert delete_resp.status_code == 403
