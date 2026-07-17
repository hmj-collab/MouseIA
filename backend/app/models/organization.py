from sqlalchemy import Boolean, Column, Integer, String, Text

from app.database.mixins import TimestampMixin
from app.database.session import Base


class Organization(Base, TimestampMixin):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    domain = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
