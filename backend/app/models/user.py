from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database.mixins import TimestampMixin
from app.database.session import Base


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(80), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(40), nullable=False, default="viewer")
    is_active = Column(Boolean, nullable=False, default=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=True, index=True)

    organization = relationship("Organization", backref="users")
