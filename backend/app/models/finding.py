from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database.mixins import TimestampMixin
from app.database.session import Base


class Finding(Base, TimestampMixin):
    __tablename__ = "findings"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    severity = Column(String(40), nullable=False)
    status = Column(String(40), nullable=False, default="open")
    signal_id = Column(Integer, ForeignKey("signals.id"), nullable=True)

    signal = relationship("Signal", backref="findings")
