from typing import Optional

from sqlalchemy.orm import Session

from app.models.organization import Organization
from app.repositories.organization_repository import OrganizationRepository
from app.schemas.organization import OrganizationCreate, OrganizationOut, OrganizationUpdate


class OrganizationService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def _repo(self) -> OrganizationRepository:
        return OrganizationRepository(self.db)

    def list_organizations(self) -> list[OrganizationOut]:
        return [self._to_out(o) for o in self._repo().list_organizations()]

    def get_organization(self, organization_id: int) -> Optional[OrganizationOut]:
        organization = self._repo().get_by_id(organization_id)
        return self._to_out(organization) if organization else None

    def create_organization(self, payload: OrganizationCreate) -> OrganizationOut:
        organization = self._repo().create(payload)
        return self._to_out(organization)

    def update_organization(self, organization_id: int, payload: OrganizationUpdate) -> Optional[OrganizationOut]:
        organization = self._repo().get_by_id(organization_id)
        if organization is None:
            return None
        updated = self._repo().update(organization, payload)
        return self._to_out(updated)

    def delete_organization(self, organization_id: int) -> bool:
        organization = self._repo().get_by_id(organization_id)
        if organization is None:
            return False
        self._repo().delete(organization)
        return True

    def _to_out(self, organization: Organization) -> OrganizationOut:
        return OrganizationOut.model_validate(organization)
