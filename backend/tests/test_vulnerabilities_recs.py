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


def test_vulnerabilities_and_recommendations_flow() -> None:
    admin_headers = _admin_headers()
    viewer_headers = _viewer_headers()

    # 1. Create a project to run scans against
    project_resp = client.post(
        "/projects",
        json={
            "name": "Correlated Vulnerability Project Target",
            "description": "Projeto para testar motor de correlacao",
            "tags": ["test", "wp"],
        },
        headers=admin_headers,
    )
    assert project_resp.status_code == 201
    project_id = project_resp.json()["id"]

    # 1.5 Create a web_application asset for the project
    asset_resp = client.post(
        "/assets",
        json={
            "name": "Correlated Vulnerability Asset Target",
            "asset_type": "web_application",
            "value": "http://wordpress-test-correlation.local",
            "description": "Ativo para testar correlacao",
            "is_active": True,
            "project_id": project_id,
        },
        headers=admin_headers,
    )
    assert asset_resp.status_code == 201
    asset_id = asset_resp.json()["id"]

    # 2. Create Scan linked to the project
    scan_resp = client.post(
        "/scans",
        json={
            "scan_type": "wordpress",
            "status": "pending",
            "description": "Varredura para teste de correlacao",
            "project_id": project_id,
        },
        headers=admin_headers,
    )
    assert scan_resp.status_code == 201
    scan_id = scan_resp.json()["id"]

    # 3. Launch scan - this triggers execute_scan, creating signals, findings,
    # and then correlating them to Vulnerabilities & Recommendations automatically!
    launch_resp = client.post(f"/scans/{scan_id}/launch", headers=admin_headers)
    assert launch_resp.status_code == 200

    # 4. List vulnerabilities and verify automated creation
    vulns_resp = client.get("/vulnerabilities", headers=admin_headers)
    assert vulns_resp.status_code == 200
    vulns = vulns_resp.json()
    assert len(vulns) > 0

    # Locate the wordpress vulnerability
    wp_vuln = next((v for v in vulns if "WordPress" in v["title"]), None)
    assert wp_vuln is not None
    assert wp_vuln["cve_id"] == "CVE-2023-32243"
    assert wp_vuln["cvss_score"] == 8.8
    assert wp_vuln["severity"] == "critical"
    assert wp_vuln["status"] == "open"
    vuln_id = wp_vuln["id"]

    # 5. List recommendations and verify automated creation
    recs_resp = client.get("/recommendations", headers=admin_headers)
    assert recs_resp.status_code == 200
    recs = recs_resp.json()
    assert len(recs) > 0

    # Verify recommendation linked to our vulnerability
    linked_rec = next((r for r in recs if r["vulnerability_id"] == vuln_id), None)
    assert linked_rec is not None
    assert "functions.php" in linked_rec["description"]
    assert linked_rec["priority"] == "high"
    assert linked_rec["status"] == "open"
    rec_id = linked_rec["id"]

    # 6. Test RBAC: Viewers can read, but cannot update/delete
    # Read lists as viewer
    assert client.get("/vulnerabilities", headers=viewer_headers).status_code == 200
    assert client.get(f"/vulnerabilities/{vuln_id}", headers=viewer_headers).status_code == 200
    assert client.get("/recommendations", headers=viewer_headers).status_code == 200
    assert client.get(f"/recommendations/{rec_id}", headers=viewer_headers).status_code == 200

    # Viewers cannot update vulnerability status
    assert client.put(f"/vulnerabilities/{vuln_id}", json={"status": "resolved"}, headers=viewer_headers).status_code == 403
    # Viewers cannot update recommendation status
    assert client.put(f"/recommendations/{rec_id}", json={"status": "done"}, headers=viewer_headers).status_code == 403
    # Viewers cannot delete
    assert client.delete(f"/vulnerabilities/{vuln_id}", headers=viewer_headers).status_code == 403
    assert client.delete(f"/recommendations/{rec_id}", headers=viewer_headers).status_code == 403

    # 7. Admin can update status (mitigate, resolve, accept)
    # Update vulnerability status to mitigated
    update_vuln_resp = client.put(f"/vulnerabilities/{vuln_id}", json={"status": "mitigated"}, headers=admin_headers)
    assert update_vuln_resp.status_code == 200
    assert update_vuln_resp.json()["status"] == "mitigated"

    # Update recommendation status to done
    update_rec_resp = client.put(f"/recommendations/{rec_id}", json={"status": "done"}, headers=admin_headers)
    assert update_rec_resp.status_code == 200
    assert update_rec_resp.json()["status"] == "done"

    # 8. Clean up
    assert client.delete(f"/recommendations/{rec_id}", headers=admin_headers).status_code == 204
    assert client.delete(f"/vulnerabilities/{vuln_id}", headers=admin_headers).status_code == 204
    assert client.delete(f"/scans/{scan_id}", headers=admin_headers).status_code == 204
    assert client.delete(f"/assets/{asset_id}", headers=admin_headers).status_code == 204
    assert client.delete(f"/projects/{project_id}", headers=admin_headers).status_code == 204
