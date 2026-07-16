from datetime import datetime, timezone

from sqlalchemy import Column, DateTime
from sqlalchemy.orm import declarative_mixin


def _utcnow():
    return datetime.now(timezone.utc)


@declarative_mixin
class TimestampMixin:
    created_at = Column(DateTime(timezone=True), nullable=False, default=_utcnow)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=_utcnow, onupdate=_utcnow)
