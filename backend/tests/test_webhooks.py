from unittest.mock import patch, MagicMock
from sqlalchemy.orm import Session

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
