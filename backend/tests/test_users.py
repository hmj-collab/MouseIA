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


def test_users_crud_flow() -> None:
    headers = _admin_headers()

    # Criar usuário
    create_resp = client.post(
        "/users",
        json={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "securepass123",
            "role": "viewer",
        },
        headers=headers,
    )
    assert create_resp.status_code == 201
    created = create_resp.json()
    assert created["username"] == "testuser"
    assert created["email"] == "testuser@example.com"
    assert created["role"] == "viewer"
    assert created["is_active"] is True
    assert "hashed_password" not in created
    user_id = created["id"]

    # Listar usuários
    list_resp = client.get("/users", headers=headers)
    assert list_resp.status_code == 200
    assert any(u["id"] == user_id for u in list_resp.json())

    # Buscar por ID
    get_resp = client.get(f"/users/{user_id}", headers=headers)
    assert get_resp.status_code == 200
    assert get_resp.json()["username"] == "testuser"

    # Atualizar role
    update_resp = client.put(
        f"/users/{user_id}",
        json={"role": "admin"},
        headers=headers,
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["role"] == "admin"

    # Desativar usuário
    deactivate_resp = client.put(
        f"/users/{user_id}",
        json={"is_active": False},
        headers=headers,
    )
    assert deactivate_resp.status_code == 200
    assert deactivate_resp.json()["is_active"] is False

    # Deletar usuário
    delete_resp = client.delete(f"/users/{user_id}", headers=headers)
    assert delete_resp.status_code == 204

    # Confirmar que foi deletado
    get_after_delete = client.get(f"/users/{user_id}", headers=headers)
    assert get_after_delete.status_code == 404


def test_duplicate_username_returns_409() -> None:
    headers = _admin_headers()

    payload = {
        "username": "dupuser",
        "email": "dup1@example.com",
        "password": "securepass123",
        "role": "viewer",
    }
    r1 = client.post("/users", json=payload, headers=headers)
    assert r1.status_code == 201

    r2 = client.post("/users", json={**payload, "email": "dup2@example.com"}, headers=headers)
    assert r2.status_code == 409

    # Limpar
    client.delete(f"/users/{r1.json()['id']}", headers=headers)


def test_duplicate_email_returns_409() -> None:
    headers = _admin_headers()

    payload = {
        "username": "emailuser1",
        "email": "shared@example.com",
        "password": "securepass123",
        "role": "viewer",
    }
    r1 = client.post("/users", json=payload, headers=headers)
    assert r1.status_code == 201

    r2 = client.post("/users", json={**payload, "username": "emailuser2"}, headers=headers)
    assert r2.status_code == 409

    # Limpar
    client.delete(f"/users/{r1.json()['id']}", headers=headers)


def test_viewer_cannot_access_users() -> None:
    headers = _viewer_headers()

    assert client.get("/users", headers=headers).status_code == 403
    assert client.post("/users", json={}, headers=headers).status_code == 403


def test_login_with_db_user() -> None:
    headers = _admin_headers()

    # Criar usuário no banco
    create_resp = client.post(
        "/users",
        json={
            "username": "dbloginuser",
            "email": "dblogin@example.com",
            "password": "mypassword99",
            "role": "viewer",
        },
        headers=headers,
    )
    assert create_resp.status_code == 201
    user_id = create_resp.json()["id"]

    # Login usando o usuário do banco
    login_resp = client.post(
        "/auth/login",
        json={"username": "dbloginuser", "password": "mypassword99"},
    )
    assert login_resp.status_code == 200
    assert "access_token" in login_resp.json()

    # Login com senha errada
    bad_resp = client.post(
        "/auth/login",
        json={"username": "dbloginuser", "password": "wrongpassword"},
    )
    assert bad_resp.status_code == 401

    # Limpar
    client.delete(f"/users/{user_id}", headers=headers)


def test_register_endpoint() -> None:
    headers = _admin_headers()

    resp = client.post(
        "/auth/register",
        json={
            "username": "reguser",
            "email": "reg@example.com",
            "password": "regpassword1",
            "role": "viewer",
        },
        headers=headers,
    )
    assert resp.status_code == 201
    assert resp.json()["username"] == "reguser"

    # Limpar
    client.delete(f"/users/{resp.json()['id']}", headers=headers)
