from typing import Optional

from sqlalchemy.orm import Session

from app.models.company import Company
from app.repositories.company_repository import CompanyRepository
from app.schemas.company import CompanyCreate, CompanyOut, CompanyUpdate


class CompanyService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def _repo(self) -> CompanyRepository:
        return CompanyRepository(self.db)

    def list_companies(self) -> list[CompanyOut]:
        return [self._to_out(c) for c in self._repo().list_companies()]

    def get_company(self, company_id: int) -> Optional[CompanyOut]:
        company = self._repo().get_by_id(company_id)
        return self._to_out(company) if company else None

    def create_company(self, payload: CompanyCreate) -> CompanyOut:
        company = self._repo().create(payload)
        return self._to_out(company)

    def update_company(self, company_id: int, payload: CompanyUpdate) -> Optional[CompanyOut]:
        company = self._repo().get_by_id(company_id)
        if company is None:
            return None
        updated = self._repo().update(company, payload)
        return self._to_out(updated)

    def delete_company(self, company_id: int) -> bool:
        company = self._repo().get_by_id(company_id)
        if company is None:
            return False
        self._repo().delete(company)
        return True

    def _to_out(self, company: Company) -> CompanyOut:
        return CompanyOut.model_validate(company)
