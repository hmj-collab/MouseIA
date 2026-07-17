from fastapi.testclient import TestClient
from app.main import app


def test_reporting_and_dashboard_endpoints() -> None:
    client = TestClient(app)

    # 1. Login
    login_response = client.post(
        "/auth/login",
        json={"username": "admin", "password": "password123"},
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Get Dashboard Metrics
    metrics_resp = client.get("/dashboard/metrics", headers=headers)
    assert metrics_resp.status_code == 200
    metrics = metrics_resp.json()
    assert "projects_count" in metrics
    assert "avg_risk_score" in metrics
    assert "avg_mttr_hours" in metrics
    assert "sla_compliance_pct" in metrics

    # 3. Export Vulnerabilities CSV
    export_resp = client.get("/vulnerabilities/export/csv", headers=headers)
    assert export_resp.status_code == 200
    assert "text/csv" in export_resp.headers["content-type"]
    csv_content = export_resp.text
    assert "ID" in csv_content
    assert "CVE ID" in csv_content
    assert "Titulo" in csv_content
