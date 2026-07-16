from fastapi.testclient import TestClient

from app.main import app


def test_sites_crud_flow() -> None:
    client = TestClient(app)

    create_response = client.post(
        "/sites",
        json={
            "name": "Example Site",
            "url": "https://example.com",
            "description": "Public demo site",
            "tags": ["public", "demo"],
        },
    )

    assert create_response.status_code == 201
    created = create_response.json()
    site_id = created["id"]

    list_response = client.get("/sites")
    assert list_response.status_code == 200
    assert any(item["id"] == site_id for item in list_response.json())

    update_response = client.put(
        f"/sites/{site_id}",
        json={
            "name": "Updated Example Site",
            "url": "https://example.com",
            "description": "Updated description",
            "tags": ["public", "demo", "updated"],
        },
    )
    assert update_response.status_code == 200
    assert update_response.json()["name"] == "Updated Example Site"

    delete_response = client.delete(f"/sites/{site_id}")
    assert delete_response.status_code == 204

    get_response = client.get(f"/sites/{site_id}")
    assert get_response.status_code == 404
