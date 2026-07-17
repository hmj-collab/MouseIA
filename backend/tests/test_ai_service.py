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


def test_automated_false_positive_ingestion(db_session) -> None:
    # 1. Create a test asset
    from app.models.asset import Asset
    from app.models.vulnerability import Vulnerability
    from app.services.correlation_service import CorrelationService
    
    asset = Asset(
        name="FP Test Asset",
        asset_type="url",
        value="http://fp-test.local",
        description="Asset for testing false positive reduction",
        is_active=True,
    )
    db_session.add(asset)
    db_session.commit()
    db_session.refresh(asset)

    correlation_svc = CorrelationService(db_session)

    # 2. Process signals designed to trigger false positive (contains 'false_positive')
    signals_batch = [
        {"type": "missing_csp", "severity": "medium", "confidence": 90, "desc": "Simulated false_positive trigger evidence"},
    ]

    findings = correlation_svc.process_new_signals(
        signals_data=signals_batch,
        asset_id=asset.id,
        source="scan-fp"
    )

    assert len(findings) == 1
    finding = findings[0]

    # 3. Retrieve vulnerability and check the effects of false positive detection
    vuln = db_session.query(Vulnerability).filter(Vulnerability.finding_id == finding.id).first()
    assert vuln is not None
    
    # Assert status is automatically set to mitigated
    assert vuln.status == "mitigated"
    
    # Assert description contains the AI Analysis section
    assert "--- ANÁLISE DE IA (MOUSE IA ENGINE) ---" in vuln.description
    assert "AVISO DE FALSO POSITIVO" in vuln.description

    # Assert risk score is reduced by 0.1 multiplier
    assert vuln.risk_score is not None
    assert vuln.risk_score < 1.5

