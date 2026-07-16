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
    site_id = Column(Integer, ForeignKey("sites.id"), nullable=True)

    site = relationship("Site", backref="signals")
