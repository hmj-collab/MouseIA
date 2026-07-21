from typing import Optional
from sqlalchemy.orm import Session

from app.models.webhook import Webhook
from app.schemas.webhook import WebhookCreate, WebhookUpdate


class WebhookRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_all(self) -> list[Webhook]:
        return self.db.query(Webhook).order_by(Webhook.id.desc()).all()

    def get_by_id(self, webhook_id: int) -> Optional[Webhook]:
        return self.db.query(Webhook).filter(Webhook.id == webhook_id).first()

    def create(self, payload: WebhookCreate) -> Webhook:
        webhook = Webhook(
            name=payload.name,
            url=payload.url,
            secret_token=payload.secret_token,
            is_active=payload.is_active,
            trigger_events=payload.trigger_events,
        )
        self.db.add(webhook)
        self.db.commit()
        self.db.refresh(webhook)
        return webhook

    def update(self, webhook: Webhook, payload: WebhookUpdate) -> Webhook:
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(webhook, field, value)
        self.db.commit()
        self.db.refresh(webhook)
        return webhook

    def delete(self, webhook: Webhook) -> None:
        self.db.delete(webhook)
        self.db.commit()
