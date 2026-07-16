from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.core.security import require_role
from app.schemas.finding import FindingCreate, FindingOut, FindingUpdate
from app.services.finding_service import FindingService

router = APIRouter(prefix="/findings", tags=["findings"])


@router.get("", response_model=list[FindingOut])
def list_findings(
    title: Optional[str] = None,
    severity: Optional[str] = None,
    status: Optional[str] = None,
    signal_id: Optional[int] = None,
    db: Session = Depends(get_db),
    user: dict[str, str] = Depends(require_role("admin", "viewer")),
) -> list[FindingOut]:
    return FindingService(db).list_findings(
        title=title,
        severity=severity,
        status=status,
        signal_id=signal_id,
    )


@router.post("", response_model=FindingOut, status_code=status.HTTP_201_CREATED)
def create_finding(payload: FindingCreate, db: Session = Depends(get_db), user: dict[str, str] = Depends(require_role("admin"))) -> FindingOut:
    return FindingService(db).create_finding(payload)


@router.get("/{finding_id}", response_model=FindingOut)
def get_finding(finding_id: int, db: Session = Depends(get_db), user: dict[str, str] = Depends(require_role("admin", "viewer"))) -> FindingOut:
    finding = FindingService(db).get_finding(finding_id)
    if finding is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Finding not found")
    return finding


@router.put("/{finding_id}", response_model=FindingOut)
def update_finding(finding_id: int, payload: FindingUpdate, db: Session = Depends(get_db), user: dict[str, str] = Depends(require_role("admin"))) -> FindingOut:
    finding = FindingService(db).update_finding(finding_id, payload)
    if finding is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Finding not found")
    return finding


@router.delete("/{finding_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_finding(finding_id: int, db: Session = Depends(get_db), user: dict[str, str] = Depends(require_role("admin"))) -> None:
    deleted = FindingService(db).delete_finding(finding_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Finding not found")
