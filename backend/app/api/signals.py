from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.core.security import require_role
from app.schemas.signal import SignalCreate, SignalOut, SignalUpdate
from app.services.signal_service import SignalService

router = APIRouter(prefix="/signals", tags=["signals"])


@router.get("", response_model=list[SignalOut])
def list_signals(
    source: Optional[str] = None,
    signal_type: Optional[str] = None,
    severity: Optional[str] = None,
    site_id: Optional[int] = None,
    min_confidence: Optional[int] = None,
    max_confidence: Optional[int] = None,
    db: Session = Depends(get_db),
    user: dict[str, str] = Depends(require_role("admin", "viewer")),
) -> list[SignalOut]:
    return SignalService(db).list_signals(
        source=source,
        signal_type=signal_type,
        severity=severity,
        site_id=site_id,
        min_confidence=min_confidence,
        max_confidence=max_confidence,
    )


@router.post("", response_model=SignalOut, status_code=status.HTTP_201_CREATED)
def create_signal(payload: SignalCreate, db: Session = Depends(get_db), user: dict[str, str] = Depends(require_role("admin"))) -> SignalOut:
    return SignalService(db).create_signal(payload)


@router.get("/{signal_id}", response_model=SignalOut)
def get_signal(signal_id: int, db: Session = Depends(get_db), user: dict[str, str] = Depends(require_role("admin", "viewer"))) -> SignalOut:
    signal = SignalService(db).get_signal(signal_id)
    if signal is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Signal not found")
    return signal


@router.put("/{signal_id}", response_model=SignalOut)
def update_signal(signal_id: int, payload: SignalUpdate, db: Session = Depends(get_db), user: dict[str, str] = Depends(require_role("admin"))) -> SignalOut:
    signal = SignalService(db).update_signal(signal_id, payload)
    if signal is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Signal not found")
    return signal


@router.delete("/{signal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_signal(signal_id: int, db: Session = Depends(get_db), user: dict[str, str] = Depends(require_role("admin"))) -> None:
    deleted = SignalService(db).delete_signal(signal_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Signal not found")
