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


def test_assets_crud_flow() -> None:
    headers = _admin_headers()

    # 1. Create Asset
    create_resp = client.post(
        "/assets",
        json={
            "name": "Public API",
            "asset_type": "url",
            "value": "http://example.com/api",
            "description": "API pública de testes",
            "is_active": True,
        },
        headers=headers,
    )
    assert create_resp.status_code == 201
    created = create_resp.json()
    assert created["name"] == "Public API"
    assert created["asset_type"] == "url"
    assert created["value"] == "http://example.com/api"
    assert created["description"] == "API pública de testes"
    assert created["is_active"] is True
    asset_id = created["id"]

    # 2. List Assets
    list_resp = client.get("/assets", headers=headers)
    assert list_resp.status_code == 200
    assert any(a["id"] == asset_id for a in list_resp.json())

    # 3. Get Asset by ID
    get_resp = client.get(f"/assets/{asset_id}", headers=headers)
    assert get_resp.status_code == 200
    assert get_resp.json()["name"] == "Public API"

    # 4. Update Asset
    update_resp = client.put(
        f"/assets/{asset_id}",
        json={
            "name": "Public API Updated",
            "value": "https://example.com/api-v2",
        },
        headers=headers,
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["name"] == "Public API Updated"
    assert update_resp.json()["value"] == "https://example.com/api-v2"

    # 5. Delete Asset
    delete_resp = client.delete(f"/assets/{asset_id}", headers=headers)
    assert delete_resp.status_code == 204

    # 6. Confirm Deleted
    get_after_delete = client.get(f"/assets/{asset_id}", headers=headers)
    assert get_after_delete.status_code == 404


def test_scans_crud_flow_and_execution() -> None:
    headers = _admin_headers()

    # 1. Create a site to link the scan to
    site_resp = client.post(
        "/sites",
        json={
            "name": "Scan Target Site",
            "url": "http://non-existent-domain-test.local",
            "description": "Site para testar scan",
            "tags": ["test"],
        },
        headers=headers,
    )
    assert site_resp.status_code == 201
    site_id = site_resp.json()["id"]

    # 2. Create Scan
    create_resp = client.post(
        "/scans",
        json={
            "scan_type": "wordpress",
            "status": "pending",
            "description": "Varredura WordPress de teste",
            "site_id": site_id,
        },
        headers=headers,
    )
    assert create_resp.status_code == 201
    scan = create_resp.json()
    assert scan["scan_type"] == "wordpress"
    assert scan["status"] == "pending"
    assert scan["site_id"] == site_id
    scan_id = scan["id"]

    # 3. List Scans
    list_resp = client.get("/scans", headers=headers)
    assert list_resp.status_code == 200
    assert any(s["id"] == scan_id for s in list_resp.json())

    # 4. Update Scan
    update_resp = client.put(
        f"/scans/{scan_id}",
        json={"description": "Nova descrição do scan"},
        headers=headers,
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["description"] == "Nova descrição do scan"

    # 5. Launch scan and trigger analysis
    launch_resp = client.post(f"/scans/{scan_id}/launch", headers=headers)
    assert launch_resp.status_code == 200
    launched = launch_resp.json()
    assert launched["status"] == "completed"
    assert launched["started_at"] is not None
    assert launched["finished_at"] is not None

    # 6. Verify that Signals were generated for this site
    signals_resp = client.get("/signals", headers=headers)
    assert signals_resp.status_code == 200
    signals = signals_resp.json()
    # Check that signals exist associated with our site_id and source scan
    site_signals = [sig for sig in signals if sig["site_id"] == site_id]
    assert len(site_signals) > 0
    assert any(sig["source"] == "scan-wordpress" for sig in site_signals)

    # 7. Verify that Findings were generated
    findings_resp = client.get("/findings", headers=headers)
    assert findings_resp.status_code == 200
    findings = findings_resp.json()
    # Check that there are findings linked to the generated signals
    created_sig_ids = {sig["id"] for sig in site_signals}
    linked_findings = [f for f in findings if f["signal_id"] in created_sig_ids]
    assert len(linked_findings) > 0
    assert any("Detectado" in f["title"] for f in linked_findings)

    # 8. Delete Scan and Site
    delete_scan_resp = client.delete(f"/scans/{scan_id}", headers=headers)
    assert delete_scan_resp.status_code == 204
    delete_site_resp = client.delete(f"/sites/{site_id}", headers=headers)
    assert delete_site_resp.status_code == 204


def test_viewer_permissions_on_assets_and_scans() -> None:
    viewer_headers = _viewer_headers()

    # Viewers can read lists
    assert client.get("/assets", headers=viewer_headers).status_code == 200
    assert client.get("/scans", headers=viewer_headers).status_code == 200

    # Viewers cannot create or modify assets
    assert client.post("/assets", json={"name": "No"}, headers=viewer_headers).status_code == 403
    assert client.put("/assets/1", json={"name": "No"}, headers=viewer_headers).status_code == 403
    assert client.delete("/assets/1", headers=viewer_headers).status_code == 403

    # Viewers cannot create, modify, or launch scans
    assert client.post("/scans", json={"scan_type": "wordpress"}, headers=viewer_headers).status_code == 403
    assert client.put("/scans/1", json={"scan_type": "wordpress"}, headers=viewer_headers).status_code == 403
    assert client.delete("/scans/1", headers=viewer_headers).status_code == 403
    assert client.post("/scans/1/launch", headers=viewer_headers).status_code == 403
