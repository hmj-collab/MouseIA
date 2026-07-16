from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.core.security import require_role
from app.schemas.company import CompanyCreate, CompanyOut, CompanyUpdate
from app.services.company_service import CompanyService

router = APIRouter(prefix="/companies", tags=["companies"])


@router.get("", response_model=list[CompanyOut])
def list_companies(
    db: Session = Depends(get_db),
    user: dict[str, str] = Depends(require_role("admin", "viewer")),
) -> list[CompanyOut]:
    return CompanyService(db).list_companies()


@router.post("", response_model=CompanyOut, status_code=status.HTTP_201_CREATED)
def create_company(
    payload: CompanyCreate,
    db: Session = Depends(get_db),
    user: dict[str, str] = Depends(require_role("admin")),
) -> CompanyOut:
    return CompanyService(db).create_company(payload)


@router.get("/{company_id}", response_model=CompanyOut)
def get_company(
    company_id: int,
    db: Session = Depends(get_db),
    user: dict[str, str] = Depends(require_role("admin", "viewer")),
) -> CompanyOut:
    company = CompanyService(db).get_company(company_id)
    if company is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Empresa não encontrada.")
    return company


@router.put("/{company_id}", response_model=CompanyOut)
def update_company(
    company_id: int,
    payload: CompanyUpdate,
    db: Session = Depends(get_db),
    user: dict[str, str] = Depends(require_role("admin")),
) -> CompanyOut:
    updated = CompanyService(db).update_company(company_id, payload)
    if updated is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Empresa não encontrada.")
    return updated


@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_company(
    company_id: int,
    db: Session = Depends(get_db),
    user: dict[str, str] = Depends(require_role("admin")),
) -> None:
    deleted = CompanyService(db).delete_company(company_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Empresa não encontrada.")
