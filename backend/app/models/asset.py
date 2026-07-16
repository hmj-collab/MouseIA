from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database.mixins import TimestampMixin
from app.database.session import Base


class Asset(Base, TimestampMixin):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    asset_type = Column(String(40), nullable=False)  # ip, domain, host, url, other
    value = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True, index=True)
    site_id = Column(Integer, ForeignKey("sites.id"), nullable=True, index=True)

    company = relationship("Company", backref="assets")
    site = relationship("Site", backref="assets")
