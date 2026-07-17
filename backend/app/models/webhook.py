import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime

from app.database.session import Base


class Webhook(Base):
    __tablename__ = "webhooks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    url = Column(String(500), nullable=False)
    secret_token = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    trigger_events = Column(String(255), default="scan_completed,critical_vuln_found", nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.datetime.now(datetime.timezone.utc), nullable=False)
