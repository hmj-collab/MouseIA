from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from app.api.dependencies import get_db
from app.core.security import require_role
from app.schemas.asset import AssetCreate, AssetOut, AssetUpdate
from app.services.asset_service import AssetService

router = APIRouter(prefix="/assets", tags=["assets"])


@router.get("", response_model=list[AssetOut])
def list_assets(
    company_id: Optional[int] = None,
    site_id: Optional[int] = None,
    db: Session = Depends(get_db),
    user: dict[str, str] = Depends(require_role("admin", "viewer")),
) -> list[AssetOut]:
    return AssetService(db).list_assets(company_id=company_id, site_id=site_id)


@router.post("", response_model=AssetOut, status_code=status.HTTP_201_CREATED)
def create_asset(
    payload: AssetCreate,
    db: Session = Depends(get_db),
    user: dict[str, str] = Depends(require_role("admin")),
) -> AssetOut:
    return AssetService(db).create_asset(payload)


@router.get("/{asset_id}", response_model=AssetOut)
def get_asset(
    asset_id: int,
    db: Session = Depends(get_db),
    user: dict[str, str] = Depends(require_role("admin", "viewer")),
) -> AssetOut:
    asset = AssetService(db).get_asset(asset_id)
    if asset is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ativo não encontrado.")
    return asset


@router.put("/{asset_id}", response_model=AssetOut)
def update_asset(
    asset_id: int,
    payload: AssetUpdate,
    db: Session = Depends(get_db),
    user: dict[str, str] = Depends(require_role("admin")),
) -> AssetOut:
    updated = AssetService(db).update_asset(asset_id, payload)
    if updated is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ativo não encontrado.")
    return updated


@router.delete("/{asset_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_asset(
    asset_id: int,
    db: Session = Depends(get_db),
    user: dict[str, str] = Depends(require_role("admin")),
) -> None:
    deleted = AssetService(db).delete_asset(asset_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ativo não encontrado.")
