from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.core.security import require_role
from app.schemas.finding import FindingCreate, FindingOut
from app.services.finding_service import FindingService

router = APIRouter(prefix="/findings", tags=["findings"])


@router.get("", response_model=list[FindingOut])
def list_findings(db: Session = Depends(get_db), user: dict[str, str] = Depends(require_role("admin", "viewer"))) -> list[FindingOut]:
    return FindingService(db).list_findings()


@router.post("", response_model=FindingOut, status_code=status.HTTP_201_CREATED)
def create_finding(payload: FindingCreate, db: Session = Depends(get_db), user: dict[str, str] = Depends(require_role("admin"))) -> FindingOut:
    return FindingService(db).create_finding(payload)


@router.get("/{finding_id}", response_model=FindingOut)
def get_finding(finding_id: int, db: Session = Depends(get_db), user: dict[str, str] = Depends(require_role("admin", "viewer"))) -> FindingOut:
    finding = FindingService(db).get_finding(finding_id)
    if finding is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Finding not found")
    return finding
