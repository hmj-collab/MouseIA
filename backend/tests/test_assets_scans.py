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

    # 1. Create a project to link the scan to
    project_resp = client.post(
        "/projects",
        json={
            "name": "Scan Target Project",
            "description": "Projeto para testar scan",
            "tags": ["test"],
        },
        headers=headers,
    )
    assert project_resp.status_code == 201
    project_id = project_resp.json()["id"]

    # 1.5 Create a web_application asset for the project
    asset_resp = client.post(
        "/assets",
        json={
            "name": "Scan Target Web Application",
            "asset_type": "web_application",
            "value": "http://non-existent-domain-test.local",
            "description": "Ativo gerado na migração do Site original",
            "is_active": True,
            "project_id": project_id,
        },
        headers=headers,
    )
    assert asset_resp.status_code == 201
    asset_id = asset_resp.json()["id"]

    # 2. Create Scan
    create_resp = client.post(
        "/scans",
        json={
            "scan_type": "wordpress",
            "status": "pending",
            "description": "Varredura WordPress de teste",
            "project_id": project_id,
        },
        headers=headers,
    )
    assert create_resp.status_code == 201
    scan = create_resp.json()
    assert scan["scan_type"] == "wordpress"
    assert scan["status"] == "pending"
    assert scan["project_id"] == project_id
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

    # 6. Verify that Signals were generated for this asset
    signals_resp = client.get("/signals", headers=headers)
    assert signals_resp.status_code == 200
    signals = signals_resp.json()
    # Check that signals exist associated with our asset_id and source scan
    asset_signals = [sig for sig in signals if sig["asset_id"] == asset_id]
    assert len(asset_signals) > 0
    assert any(sig["source"] == "scan-wordpress" for sig in asset_signals)

    # 7. Verify that Findings were generated
    findings_resp = client.get("/findings", headers=headers)
    assert findings_resp.status_code == 200
    findings = findings_resp.json()
    # Check that there are findings linked to the generated signals
    created_sig_ids = {sig["id"] for sig in asset_signals}
    linked_findings = [f for f in findings if f["signal_id"] in created_sig_ids]
    assert len(linked_findings) > 0
    assert any("Detectado" in f["title"] for f in linked_findings)

    # 8. Delete Scan, Asset and Project
    delete_scan_resp = client.delete(f"/scans/{scan_id}", headers=headers)
    assert delete_scan_resp.status_code == 204
    delete_asset_resp = client.delete(f"/assets/{asset_id}", headers=headers)
    assert delete_asset_resp.status_code == 204
    delete_project_resp = client.delete(f"/projects/{project_id}", headers=headers)
    assert delete_project_resp.status_code == 204


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


def test_asset_deletion_cascade(db_session) -> None:
    headers = _admin_headers()

    # 1. Create Asset
    asset_resp = client.post(
        "/assets",
        json={
            "name": "Cascade Target Asset",
            "asset_type": "url",
            "value": "http://wordpress-cascade.local",
            "description": "Asset to test delete cascade",
            "is_active": True,
        },
        headers=headers,
    )
    assert asset_resp.status_code == 201
    asset_id = asset_resp.json()["id"]

    # 2. Create Scan linked to this Asset
    scan_resp = client.post(
        "/scans",
        json={
            "scan_type": "wordpress",
            "status": "pending",
            "description": "Scan to test cascade",
            "asset_id": asset_id,
        },
        headers=headers,
    )
    assert scan_resp.status_code == 201
    scan_id = scan_resp.json()["id"]

    # 3. Launch Scan (creates Signal, Finding, Vulnerability, Recommendation)
    launch_resp = client.post(f"/scans/{scan_id}/launch", headers=headers)
    assert launch_resp.status_code == 200

    # 4. Fetch the Vulnerability and Recommendation to assert they exist
    vulns_resp = client.get("/vulnerabilities", headers=headers)
    vulns = [v for v in vulns_resp.json() if v["asset_id"] == asset_id]
    assert len(vulns) > 0
    vuln_id = vulns[0]["id"]
    finding_id = vulns[0]["finding_id"]

    recs_resp = client.get("/recommendations", headers=headers)
    recs = [r for r in recs_resp.json() if r["vulnerability_id"] == vuln_id]
    assert len(recs) > 0
    rec_id = recs[0]["id"]

    # 5. Retrieve Finding and Signal from DB session
    from app.models.finding import Finding
    from app.models.signal import Signal
    from app.models.task import Task
    from app.models.recommendation import Recommendation
    from app.models.vulnerability import Vulnerability
    from app.models.scan import Scan
    from app.models.asset import Asset

    finding = db_session.query(Finding).filter(Finding.id == finding_id).first()
    assert finding is not None
    signal_id = finding.signal_id
    signal = db_session.query(Signal).filter(Signal.id == signal_id).first()
    assert signal is not None

    # 6. Create a Task linked to the Recommendation
    task = Task(title="Test task for cascade", recommendation_id=rec_id)
    db_session.add(task)
    db_session.commit()
    task_id = task.id

    # Verify Task exists
    assert db_session.query(Task).filter(Task.id == task_id).first() is not None

    # 7. Delete Asset
    delete_resp = client.delete(f"/assets/{asset_id}", headers=headers)
    assert delete_resp.status_code == 204

    # 8. Verify everything is deleted!
    assert db_session.query(Asset).filter(Asset.id == asset_id).first() is None
    assert db_session.query(Scan).filter(Scan.id == scan_id).first() is None
    assert db_session.query(Vulnerability).filter(Vulnerability.id == vuln_id).first() is None
    assert db_session.query(Recommendation).filter(Recommendation.id == rec_id).first() is None
    assert db_session.query(Task).filter(Task.id == task_id).first() is None
    assert db_session.query(Finding).filter(Finding.id == finding_id).first() is None
    assert db_session.query(Signal).filter(Signal.id == signal_id).first() is None

