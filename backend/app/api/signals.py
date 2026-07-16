from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.core.security import require_role
from app.schemas.signal import SignalCreate, SignalOut
from app.services.signal_service import SignalService

router = APIRouter(prefix="/signals", tags=["signals"])


@router.get("", response_model=list[SignalOut])
def list_signals(db: Session = Depends(get_db), user: dict[str, str] = Depends(require_role("admin", "viewer"))) -> list[SignalOut]:
    return SignalService(db).list_signals()


@router.post("", response_model=SignalOut, status_code=status.HTTP_201_CREATED)
def create_signal(payload: SignalCreate, db: Session = Depends(get_db), user: dict[str, str] = Depends(require_role("admin"))) -> SignalOut:
    return SignalService(db).create_signal(payload)


@router.get("/{signal_id}", response_model=SignalOut)
def get_signal(signal_id: int, db: Session = Depends(get_db), user: dict[str, str] = Depends(require_role("admin", "viewer"))) -> SignalOut:
    signal = SignalService(db).get_signal(signal_id)
    if signal is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Signal not found")
    return signal
