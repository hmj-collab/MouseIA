from sqlalchemy import JSON, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database.mixins import TimestampMixin
from app.database.session import Base


class Project(Base, TimestampMixin):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    description = Column(Text, nullable=True)
    tags = Column(JSON, nullable=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=True, index=True)

    organization = relationship("Organization", backref="projects")
