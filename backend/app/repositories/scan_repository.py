from typing import Optional
from sqlalchemy.orm import Session
from app.models.scan import Scan
from app.schemas.scan import ScanCreate, ScanUpdate


class ScanRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_scans(self, project_id: Optional[int] = None, asset_id: Optional[int] = None) -> list[Scan]:
        q = self.db.query(Scan)
        if project_id is not None:
            q = q.filter(Scan.project_id == project_id)
        if asset_id is not None:
            q = q.filter(Scan.asset_id == asset_id)
        return q.order_by(Scan.id.desc()).all()

    def get_by_id(self, scan_id: int) -> Optional[Scan]:
        return self.db.query(Scan).filter(Scan.id == scan_id).first()

    def create(self, payload: ScanCreate) -> Scan:
        scan = Scan(
            scan_type=payload.scan_type,
            status=payload.status,
            description=payload.description,
            asset_id=payload.asset_id,
            project_id=payload.project_id,
        )
        self.db.add(scan)
        self.db.commit()
        self.db.refresh(scan)
        return scan

    def update(self, scan: Scan, payload: ScanUpdate) -> Scan:
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(scan, field, value)
        self.db.commit()
        self.db.refresh(scan)
        return scan

    def delete(self, scan: Scan) -> None:
        self.db.delete(scan)
        self.db.commit()
