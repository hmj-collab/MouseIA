from typing import Optional

from sqlalchemy.orm import Session

from app.models.organization import Organization
from app.schemas.organization import OrganizationCreate, OrganizationUpdate


class OrganizationRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_organizations(self) -> list[Organization]:
        return self.db.query(Organization).order_by(Organization.id).all()

    def get_by_id(self, organization_id: int) -> Optional[Organization]:
        return self.db.query(Organization).filter(Organization.id == organization_id).first()

    def create(self, payload: OrganizationCreate) -> Organization:
        organization = Organization(
            name=payload.name,
            domain=payload.domain,
            description=payload.description,
            is_active=payload.is_active,
        )
        self.db.add(organization)
        self.db.commit()
        self.db.refresh(organization)
        return organization

    def update(self, organization: Organization, payload: OrganizationUpdate) -> Organization:
        if payload.name is not None:
            organization.name = payload.name
        if payload.domain is not None:
            organization.domain = payload.domain
        if payload.description is not None:
            organization.description = payload.description
        if payload.is_active is not None:
            organization.is_active = payload.is_active
        self.db.commit()
        self.db.refresh(organization)
        return organization

    def delete(self, organization: Organization) -> None:
        self.db.delete(organization)
        self.db.commit()
