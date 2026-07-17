from typing import Optional

from sqlalchemy.orm import Session

from app.models.signal import Signal
from app.schemas.signal import SignalCreate, SignalUpdate


class SignalRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_signals(
        self,
        source: Optional[str] = None,
        signal_type: Optional[str] = None,
        severity: Optional[str] = None,
        asset_id: Optional[int] = None,
        min_confidence: Optional[int] = None,
        max_confidence: Optional[int] = None,
    ) -> list[Signal]:
        query = self.db.query(Signal)

        if source is not None:
            query = query.filter(Signal.source == source)
        if signal_type is not None:
            query = query.filter(Signal.signal_type == signal_type)
        if severity is not None:
            query = query.filter(Signal.severity == severity)
        if asset_id is not None:
            query = query.filter(Signal.asset_id == asset_id)
        if min_confidence is not None:
            query = query.filter(Signal.confidence >= min_confidence)
        if max_confidence is not None:
            query = query.filter(Signal.confidence <= max_confidence)

        return query.order_by(Signal.id).all()

    def create_signal(self, payload: SignalCreate) -> Signal:
        signal = Signal(
            source=payload.source,
            signal_type=payload.signal_type,
            severity=payload.severity,
            confidence=payload.confidence,
            description=payload.description,
            asset_id=payload.asset_id,
            finding_id=payload.finding_id,
        )
        self.db.add(signal)
        self.db.commit()
        self.db.refresh(signal)
        return signal

    def get_signal(self, signal_id: int) -> Optional[Signal]:
        return self.db.query(Signal).filter(Signal.id == signal_id).first()

    def update_signal(self, signal_id: int, payload: SignalUpdate) -> Optional[Signal]:
        signal = self.get_signal(signal_id)
        if signal is None:
            return None

        if payload.source is not None:
            signal.source = payload.source
        if payload.signal_type is not None:
            signal.signal_type = payload.signal_type
        if payload.severity is not None:
            signal.severity = payload.severity
        if payload.confidence is not None:
            signal.confidence = payload.confidence
        if payload.description is not None:
            signal.description = payload.description
        if payload.asset_id is not None:
            signal.asset_id = payload.asset_id
        if payload.finding_id is not None:
            signal.finding_id = payload.finding_id


        self.db.commit()
        self.db.refresh(signal)
        return signal

    def delete_signal(self, signal_id: int) -> bool:
        signal = self.get_signal(signal_id)
        if signal is None:
            return False

        self.db.delete(signal)
        self.db.commit()
        return True
