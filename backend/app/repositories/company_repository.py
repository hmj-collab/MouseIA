from typing import Optional

from sqlalchemy.orm import Session

from app.models.company import Company
from app.schemas.company import CompanyCreate, CompanyUpdate


class CompanyRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_companies(self) -> list[Company]:
        return self.db.query(Company).order_by(Company.id).all()

    def get_by_id(self, company_id: int) -> Optional[Company]:
        return self.db.query(Company).filter(Company.id == company_id).first()

    def create(self, payload: CompanyCreate) -> Company:
        company = Company(
            name=payload.name,
            domain=payload.domain,
            description=payload.description,
            is_active=payload.is_active,
        )
        self.db.add(company)
        self.db.commit()
        self.db.refresh(company)
        return company

    def update(self, company: Company, payload: CompanyUpdate) -> Company:
        if payload.name is not None:
            company.name = payload.name
        if payload.domain is not None:
            company.domain = payload.domain
        if payload.description is not None:
            company.description = payload.description
        if payload.is_active is not None:
            company.is_active = payload.is_active
        self.db.commit()
        self.db.refresh(company)
        return company

    def delete(self, company: Company) -> None:
        self.db.delete(company)
        self.db.commit()
