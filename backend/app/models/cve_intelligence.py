from sqlalchemy import Boolean, Column, DateTime, Float, String, Text

from app.database.mixins import TimestampMixin
from app.database.session import Base


class CveIntelligence(Base, TimestampMixin):
    __tablename__ = "cve_intelligence"

    cve_id = Column(String(40), primary_key=True, index=True)
    cvss_score = Column(Float, nullable=True)
    severity = Column(String(40), nullable=True)
    epss_score = Column(Float, nullable=True)
    is_kev = Column(Boolean, nullable=False, default=False)
    description = Column(Text, nullable=True)
    last_fetched_at = Column(DateTime(timezone=True), nullable=False)
