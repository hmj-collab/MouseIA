from typing import Optional

from sqlalchemy.orm import Session

from app.models.signal import Signal
from app.schemas.signal import SignalCreate


class SignalRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_signals(self) -> list[Signal]:
        return self.db.query(Signal).order_by(Signal.id).all()

    def create_signal(self, payload: SignalCreate) -> Signal:
        signal = Signal(
            source=payload.source,
            signal_type=payload.signal_type,
            severity=payload.severity,
            confidence=payload.confidence,
            description=payload.description,
            site_id=payload.site_id,
        )
        self.db.add(signal)
        self.db.commit()
        self.db.refresh(signal)
        return signal

    def get_signal(self, signal_id: int) -> Optional[Signal]:
        return self.db.query(Signal).filter(Signal.id == signal_id).first()
