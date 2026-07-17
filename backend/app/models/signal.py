from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database.mixins import TimestampMixin
from app.database.session import Base


class Signal(Base, TimestampMixin):
    __tablename__ = "signals"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String(80), nullable=False)
    signal_type = Column(String(80), nullable=False)
    severity = Column(String(40), nullable=False)
    confidence = Column(Integer, nullable=False, default=0)
    description = Column(Text, nullable=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=True, index=True)
    finding_id = Column(Integer, ForeignKey("findings.id"), nullable=True, index=True)

    asset = relationship("Asset", backref="signals")
    finding = relationship("Finding", foreign_keys=[finding_id], backref="signals")

