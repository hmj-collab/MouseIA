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
    user: dict[str, any] = Depends(require_role("admin", "viewer")),
) -> list[ScanOut]:
    org_id = user.get("organization_id")
    if org_id is not None:
        # Validate requested project/asset scopes
        if project_id is not None:
            from app.models.project import Project
            proj = db.query(Project).filter(Project.id == project_id).first()
            if proj and proj.organization_id != org_id:
                return []
        if asset_id is not None:
            from app.models.asset import Asset
            asset = db.query(Asset).filter(Asset.id == asset_id).first()
            if asset and asset.organization_id != org_id:
                return []
    return ScanService(db).list_scans(project_id=project_id, asset_id=asset_id, organization_id=org_id)


@router.post("", response_model=ScanOut, status_code=status.HTTP_201_CREATED)
def create_scan(
    payload: ScanCreate,
    db: Session = Depends(get_db),
    user: dict[str, any] = Depends(require_role("admin")),
) -> ScanOut:
    try:
        return ScanService(db).create_scan(payload, organization_id=user.get("organization_id"))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/{scan_id}", response_model=ScanOut)
def get_scan(
    scan_id: int,
    db: Session = Depends(get_db),
    user: dict[str, any] = Depends(require_role("admin", "viewer")),
) -> ScanOut:
    scan = ScanService(db).get_scan(scan_id, organization_id=user.get("organization_id"))
    if scan is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Varredura não encontrada.")
    return scan


@router.put("/{scan_id}", response_model=ScanOut)
def update_scan(
    scan_id: int,
    payload: ScanUpdate,
    db: Session = Depends(get_db),
    user: dict[str, any] = Depends(require_role("admin")),
) -> ScanOut:
    try:
        updated = ScanService(db).update_scan(scan_id, payload, organization_id=user.get("organization_id"))
        if updated is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Varredura não encontrada.")
        return updated
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.delete("/{scan_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_scan(
    scan_id: int,
    db: Session = Depends(get_db),
    user: dict[str, any] = Depends(require_role("admin")),
) -> None:
    deleted = ScanService(db).delete_scan(scan_id, organization_id=user.get("organization_id"))
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Varredura não encontrada.")


@router.post("/{scan_id}/launch", response_model=ScanOut)
def launch_scan(
    scan_id: int,
    db: Session = Depends(get_db),
    user: dict[str, any] = Depends(require_role("admin")),
) -> ScanOut:
    scan = ScanService(db).execute_scan(scan_id, organization_id=user.get("organization_id"))
    if scan is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Varredura não encontrada.")
    try:
        from app.models.user import User
        from app.services.audit_service import AuditService
        db_user = db.query(User).filter(User.username == user["username"]).first()
        AuditService(db).log_action(
            user_id=db_user.id if db_user else None,
            action="LAUNCH_SCAN",
            target_type="scan",
            target_id=scan.id,
            details={"scan_type": scan.scan_type, "project_id": scan.project_id}
        )
    except Exception:
        pass
    return scan

