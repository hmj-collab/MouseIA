from sqlalchemy.orm import Session
from typing import Any, Dict
import hashlib
import hmac
import httpx
import logging
import json

from app.models.webhook import Webhook

logger = logging.getLogger(__name__)


class WebhookService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_active_webhooks(self) -> list[Webhook]:
        return self.db.query(Webhook).filter(Webhook.is_active == True).all()

    def dispatch_event(self, event_name: str, payload: Dict[str, Any]) -> None:
        active_hooks = self.list_active_webhooks()
        
        for hook in active_hooks:
            triggers = [t.strip() for t in hook.trigger_events.split(",") if t.strip()]
            if event_name not in triggers:
                continue
                
            payload_data = {
                "event": event_name,
                "webhook_name": hook.name,
                "data": payload
            }
            payload_bytes = json.dumps(payload_data, default=str).encode("utf-8")
            
            headers = {"Content-Type": "application/json"}
            if hook.secret_token:
                signature = hmac.new(
                    hook.secret_token.encode("utf-8"),
                    payload_bytes,
                    hashlib.sha256
                ).hexdigest()
                headers["X-MouseIA-Signature"] = signature
                
            try:
                # Use a low timeout to prevent blocking application flow
                with httpx.Client(timeout=2.0) as client:
                    logger.info(f"Disparando webhook '{hook.name}' para a URL {hook.url}...")
                    client.post(hook.url, content=payload_bytes, headers=headers)
            except Exception as e:
                logger.error(f"Erro ao disparar webhook '{hook.name}': {str(e)}")
