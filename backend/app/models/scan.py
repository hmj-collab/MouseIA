from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database.mixins import TimestampMixin
from app.database.session import Base


class Scan(Base, TimestampMixin):
    __tablename__ = "scans"

    id = Column(Integer, primary_key=True, index=True)
    scan_type = Column(String(80), nullable=False)
    status = Column(String(40), nullable=False, default="pending")  # pending, running, completed, failed
    description = Column(Text, nullable=True)
    started_at = Column(DateTime(timezone=True), nullable=True)
    finished_at = Column(DateTime(timezone=True), nullable=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True, index=True)

    asset = relationship("Asset", backref="scans")
    project = relationship("Project", backref="scans")
