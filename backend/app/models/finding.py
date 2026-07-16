from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.database.session import Base


class Finding(Base):
    __tablename__ = "findings"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    severity = Column(String(40), nullable=False)
    status = Column(String(40), nullable=False, default="open")
    signal_id = Column(Integer, ForeignKey("signals.id"), nullable=True)

    signal = relationship("Signal", backref="findings")
