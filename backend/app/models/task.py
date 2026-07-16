from sqlalchemy import Column, Date, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database.mixins import TimestampMixin
from app.database.session import Base


class Task(Base, TimestampMixin):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(300), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(40), nullable=False, default="open")  # open, in_progress, done, cancelled
    assigned_to = Column(String(80), nullable=True)
    due_date = Column(Date, nullable=True)
    recommendation_id = Column(Integer, ForeignKey("recommendations.id"), nullable=True, index=True)

    recommendation = relationship("Recommendation", backref="tasks")
