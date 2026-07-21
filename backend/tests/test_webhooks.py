from unittest.mock import patch, MagicMock
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient

from app.main import app
from app.models.webhook import Webhook
from app.services.webhook_service import WebhookService


def test_webhook_dispatch_flow(db_session: Session) -> None:
    # 1. Create a test active webhook
    hook = Webhook(
        name="Test Slack Channel",
        url="http://mock-webhook.local/slack",
        secret_token="secret_key_123",
        is_active=True,
        trigger_events="scan_completed,critical_vuln_found"
    )
    db_session.add(hook)
    db_session.commit()
    db_session.refresh(hook)

    # 2. Trigger webhook dispatch and verify signature calculation
    with patch("httpx.Client.post") as mock_post:
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_post.return_value = mock_resp

        svc = WebhookService(db_session)
        svc.dispatch_event("scan_completed", {"scan_id": 999, "status": "completed"})

        # Assert HTTP POST was called once
        assert mock_post.called
        args, kwargs = mock_post.call_args
        
        # Verify target URL and headers
        assert args[0] == "http://mock-webhook.local/slack"
        assert "X-MouseIA-Signature" in kwargs["headers"]
        
        # Verify payload contents
        import json
        payload = json.loads(kwargs["content"].decode("utf-8"))
        assert payload["event"] == "scan_completed"
        assert payload["data"]["scan_id"] == 999


def test_webhooks_api_crud(db_session: Session) -> None:
    client = TestClient(app)
    # Login as admin
    login_resp = client.post("/auth/login", json={"username": "admin", "password": "password123"})
    assert login_resp.status_code == 200
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 1. Create a Webhook
    create_resp = client.post(
        "/webhooks",
        json={
            "name": "API Webhook Test",
            "url": "http://example.com/webhook",
            "secret_token": "token123",
            "is_active": True,
            "trigger_events": "scan_completed"
        },
        headers=headers
    )
    assert create_resp.status_code == 201
    webhook_id = create_resp.json()["id"]
    assert create_resp.json()["name"] == "API Webhook Test"

    # 2. Get the Webhook
    get_resp = client.get(f"/webhooks/{webhook_id}", headers=headers)
    assert get_resp.status_code == 200
    assert get_resp.json()["url"] == "http://example.com/webhook"

    # 3. Update the Webhook
    put_resp = client.put(
        f"/webhooks/{webhook_id}",
        json={"name": "API Webhook Test Updated", "is_active": False},
        headers=headers
    )
    assert put_resp.status_code == 200
    assert put_resp.json()["name"] == "API Webhook Test Updated"
    assert put_resp.json()["is_active"] is False

    # 4. List Webhooks
    list_resp = client.get("/webhooks", headers=headers)
    assert list_resp.status_code == 200
    assert any(w["id"] == webhook_id for w in list_resp.json())

    # 5. Delete the Webhook
    del_resp = client.delete(f"/webhooks/{webhook_id}", headers=headers)
    assert del_resp.status_code == 204

    # 6. Verify Deleted
    get_del = client.get(f"/webhooks/{webhook_id}", headers=headers)
    assert get_del.status_code == 404

    # 7. Verify viewer is forbidden
    viewer_login = client.post("/auth/login", json={"username": "viewer", "password": "password123"})
    assert viewer_login.status_code == 200
    viewer_token = viewer_login.json()["access_token"]
    viewer_headers = {"Authorization": f"Bearer {viewer_token}"}
    
    assert client.get("/webhooks", headers=viewer_headers).status_code == 403
    assert client.post("/webhooks", json={"name": "x", "url": "http://x"}, headers=viewer_headers).status_code == 403
