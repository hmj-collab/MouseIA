from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.models.audit_log import AuditLog


def test_audit_logging_flow(db_session: Session) -> None:
    client = TestClient(app)

    # 1. Perform login
    login_response = client.post(
        "/auth/login",
        json={"username": "admin", "password": "password123"},
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Check if a LOGIN audit log exists
    login_audit = db_session.query(AuditLog).filter(AuditLog.action == "LOGIN").first()
    assert login_audit is not None
    assert login_audit.target_type == "user"

    # 3. Create a project to test action logging
    proj_resp = client.post(
        "/projects",
        json={
            "name": "Audit Test Project",
            "description": "Validating audit trail",
            "tags": ["audit", "test"],
            "url": "http://audit-test.local"
        },
        headers=headers
    )
    assert proj_resp.status_code == 201
    project_id = proj_resp.json()["id"]

    # 4. Check if a CREATE_PROJECT audit log exists
    project_audit = db_session.query(AuditLog).filter(
        AuditLog.action == "CREATE_PROJECT",
        AuditLog.target_id == project_id
    ).first()
    assert project_audit is not None
    assert project_audit.target_type == "project"
    assert "Audit Test Project" in project_audit.details
