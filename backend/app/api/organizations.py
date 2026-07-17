from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.core.security import require_role
from app.schemas.organization import OrganizationCreate, OrganizationOut, OrganizationUpdate
from app.services.organization_service import OrganizationService

router = APIRouter(prefix="/organizations", tags=["organizations"])


@router.get("", response_model=list[OrganizationOut])
def list_organizations(
    db: Session = Depends(get_db),
    user: dict[str, str] = Depends(require_role("admin", "viewer")),
) -> list[OrganizationOut]:
    return OrganizationService(db).list_organizations()


@router.post("", response_model=OrganizationOut, status_code=status.HTTP_201_CREATED)
def create_organization(
    payload: OrganizationCreate,
    db: Session = Depends(get_db),
    user: dict[str, str] = Depends(require_role("admin")),
) -> OrganizationOut:
    return OrganizationService(db).create_organization(payload)


@router.get("/{organization_id}", response_model=OrganizationOut)
def get_organization(
    organization_id: int,
    db: Session = Depends(get_db),
    user: dict[str, str] = Depends(require_role("admin", "viewer")),
) -> OrganizationOut:
    organization = OrganizationService(db).get_organization(organization_id)
    if organization is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organização não encontrada.")
    return organization


@router.put("/{organization_id}", response_model=OrganizationOut)
def update_organization(
    organization_id: int,
    payload: OrganizationUpdate,
    db: Session = Depends(get_db),
    user: dict[str, str] = Depends(require_role("admin")),
) -> OrganizationOut:
    updated = OrganizationService(db).update_organization(organization_id, payload)
    if updated is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organização não encontrada.")
    return updated


@router.delete("/{organization_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_organization(
    organization_id: int,
    db: Session = Depends(get_db),
    user: dict[str, str] = Depends(require_role("admin")),
) -> None:
    deleted = OrganizationService(db).delete_organization(organization_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organização não encontrada.")
