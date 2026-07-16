from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database.mixins import TimestampMixin
from app.database.session import Base


class Recommendation(Base, TimestampMixin):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(300), nullable=False)
    description = Column(Text, nullable=True)
    priority = Column(String(40), nullable=False, default="medium")  # critical, high, medium, low
    status = Column(String(40), nullable=False, default="open")  # open, in_progress, done, dismissed
    vulnerability_id = Column(Integer, ForeignKey("vulnerabilities.id"), nullable=True, index=True)

    vulnerability = relationship("Vulnerability", backref="recommendations")
