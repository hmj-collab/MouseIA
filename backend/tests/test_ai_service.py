from fastapi.testclient import TestClient
from app.main import app


def test_ai_analysis_endpoint() -> None:
    client = TestClient(app)

    # 1. Login
    login_response = client.post(
        "/auth/login",
        json={"username": "admin", "password": "password123"},
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Create Project
    project_resp = client.post(
        "/projects",
        json={
            "name": "AI Test Project",
            "description": "Projeto de teste de IA",
            "tags": ["test"],
        },
        headers=headers,
    )
    assert project_resp.status_code == 201
    project_id = project_resp.json()["id"]

    # 3. Create Asset
    asset_resp = client.post(
        "/assets",
        json={
            "name": "AI Test Asset",
            "asset_type": "url",
            "value": "http://ai-test.local",
            "description": "Ativo para teste de IA",
            "is_active": True,
            "project_id": project_id,
        },
        headers=headers,
    )
    assert asset_resp.status_code == 201
    asset_id = asset_resp.json()["id"]

    # 4. Create Vulnerability
    vuln_resp = client.post(
        "/vulnerabilities",
        json={
            "title": "WordPress site vulnerability",
            "description": "A WordPress core vulnerability detected",
            "severity": "critical",
            "status": "open",
            "asset_id": asset_id,
        },
        headers=headers,
    )
    assert vuln_resp.status_code == 201
    vuln_id = vuln_resp.json()["id"]

    # 5. Call AI Analysis endpoint
    ai_resp = client.post(f"/vulnerabilities/{vuln_id}/ai-analysis", headers=headers)
    assert ai_resp.status_code == 200
    ai_data = ai_resp.json()

    # Verify structured attributes returned by Gemini wrapper fallback
    assert "explanation" in ai_data
    assert "business_impact" in ai_data
    assert "remediation_steps" in ai_data
    assert ai_data["confidence_score"] > 0
    assert "is_false_positive" in ai_data
