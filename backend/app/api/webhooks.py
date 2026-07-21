from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from app.api.dependencies import get_db
from app.core.security import require_role
from app.schemas.webhook import WebhookCreate, WebhookOut, WebhookUpdate
from app.services.webhook_service import WebhookService

router = APIRouter(prefix="/webhooks", tags=["webhooks"])


@router.get("", response_model=list[WebhookOut])
def list_webhooks(
    db: Session = Depends(get_db),
    user: dict[str, any] = Depends(require_role("admin"))
) -> list[WebhookOut]:
    return WebhookService(db).list_webhooks()


@router.post("", response_model=WebhookOut, status_code=status.HTTP_201_CREATED)
def create_webhook(
    payload: WebhookCreate,
    db: Session = Depends(get_db),
    user: dict[str, any] = Depends(require_role("admin"))
) -> WebhookOut:
    return WebhookService(db).create_webhook(payload)


@router.get("/{webhook_id}", response_model=WebhookOut)
def get_webhook(
    webhook_id: int,
    db: Session = Depends(get_db),
    user: dict[str, any] = Depends(require_role("admin"))
) -> WebhookOut:
    webhook = WebhookService(db).get_webhook(webhook_id)
    if webhook is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Webhook não encontrado.")
    return webhook


@router.put("/{webhook_id}", response_model=WebhookOut)
def update_webhook(
    webhook_id: int,
    payload: WebhookUpdate,
    db: Session = Depends(get_db),
    user: dict[str, any] = Depends(require_role("admin"))
) -> WebhookOut:
    updated = WebhookService(db).update_webhook(webhook_id, payload)
    if updated is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Webhook não encontrado.")
    return updated


@router.delete("/{webhook_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_webhook(
    webhook_id: int,
    db: Session = Depends(get_db),
    user: dict[str, any] = Depends(require_role("admin"))
) -> None:
    deleted = WebhookService(db).delete_webhook(webhook_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Webhook não encontrado.")
