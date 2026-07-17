from fastapi.testclient import TestClient

from app.main import app


def test_projects_crud_flow() -> None:
    client = TestClient(app)

    login_response = client.post(
        "/auth/login",
        json={"username": "admin", "password": "password123"},
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    create_response = client.post(
        "/projects",
        json={
            "name": "Example Project",
            "description": "Public demo project",
            "tags": ["public", "demo"],
        },
        headers=headers,
    )

    assert create_response.status_code == 201
    created = create_response.json()
    project_id = created["id"]

    list_response = client.get("/projects", headers=headers)
    assert list_response.status_code == 200
    assert any(item["id"] == project_id for item in list_response.json())

    update_response = client.put(
        f"/projects/{project_id}",
        json={
            "name": "Updated Example Project",
            "description": "Updated description",
            "tags": ["public", "demo", "updated"],
        },
        headers=headers,
    )
    assert update_response.status_code == 200
    assert update_response.json()["name"] == "Updated Example Project"

    delete_response = client.delete(f"/projects/{project_id}", headers=headers)
    assert delete_response.status_code == 204

    get_response = client.get(f"/projects/{project_id}", headers=headers)
    assert get_response.status_code == 404
