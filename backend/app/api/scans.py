from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from app.api.dependencies import get_db
from app.core.security import require_role
from app.schemas.scan import ScanCreate, ScanOut, ScanUpdate
from app.services.scan_service import ScanService

router = APIRouter(prefix="/scans", tags=["scans"])


@router.get("", response_model=list[ScanOut])
def list_scans(
    project_id: Optional[int] = None,
    asset_id: Optional[int] = None,
    db: Session = Depends(get_db),
    user: dict[str, str] = Depends(require_role("admin", "viewer")),
) -> list[ScanOut]:
    return ScanService(db).list_scans(project_id=project_id, asset_id=asset_id)


@router.post("", response_model=ScanOut, status_code=status.HTTP_201_CREATED)
def create_scan(
    payload: ScanCreate,
    db: Session = Depends(get_db),
    user: dict[str, str] = Depends(require_role("admin")),
) -> ScanOut:
    return ScanService(db).create_scan(payload)


@router.get("/{scan_id}", response_model=ScanOut)
def get_scan(
    scan_id: int,
    db: Session = Depends(get_db),
    user: dict[str, str] = Depends(require_role("admin", "viewer")),
) -> ScanOut:
    scan = ScanService(db).get_scan(scan_id)
    if scan is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Varredura não encontrada.")
    return scan


@router.put("/{scan_id}", response_model=ScanOut)
def update_scan(
    scan_id: int,
    payload: ScanUpdate,
    db: Session = Depends(get_db),
    user: dict[str, str] = Depends(require_role("admin")),
) -> ScanOut:
    updated = ScanService(db).update_scan(scan_id, payload)
    if updated is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Varredura não encontrada.")
    return updated


@router.delete("/{scan_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_scan(
    scan_id: int,
    db: Session = Depends(get_db),
    user: dict[str, str] = Depends(require_role("admin")),
) -> None:
    deleted = ScanService(db).delete_scan(scan_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Varredura não encontrada.")


@router.post("/{scan_id}/launch", response_model=ScanOut)
def launch_scan(
    scan_id: int,
    db: Session = Depends(get_db),
    user: dict[str, str] = Depends(require_role("admin")),
) -> ScanOut:
    scan = ScanService(db).execute_scan(scan_id)
    if scan is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Varredura não encontrada.")
    return scan
