from typing import Optional

from sqlalchemy.orm import Session

from app.models.signal import Signal as SignalModel
from app.repositories.signal_repository import SignalRepository
from app.schemas.signal import SignalCreate, SignalOut


class SignalService:
    def __init__(self, db: Optional[Session] = None) -> None:
        self.db = db

    def _repository(self) -> SignalRepository:
        return SignalRepository(self.db)

    def list_signals(self) -> list[SignalOut]:
        signals = self._repository().list_signals()
        return [self._to_out(signal) for signal in signals]

    def create_signal(self, payload: SignalCreate) -> SignalOut:
        signal = self._repository().create_signal(payload)
        return self._to_out(signal)

    def get_signal(self, signal_id: int) -> Optional[SignalOut]:
        signal = self._repository().get_signal(signal_id)
        if signal is None:
            return None
        return self._to_out(signal)

    def _to_out(self, signal: SignalModel) -> SignalOut:
        return SignalOut(
            id=signal.id,
            source=signal.source,
            signal_type=signal.signal_type,
            severity=signal.severity,
            confidence=signal.confidence,
            description=signal.description,
            site_id=signal.site_id,
        )
