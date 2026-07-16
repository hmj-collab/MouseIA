from sqlalchemy import JSON, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database.mixins import TimestampMixin
from app.database.session import Base


class Site(Base, TimestampMixin):
    __tablename__ = "sites"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    url = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    tags = Column(JSON, nullable=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True, index=True)

    company = relationship("Company", backref="sites")
