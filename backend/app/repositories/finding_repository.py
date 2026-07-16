from typing import Optional

from sqlalchemy.orm import Session

from app.models.finding import Finding
from app.schemas.finding import FindingCreate


class FindingRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_findings(self) -> list[Finding]:
        return self.db.query(Finding).order_by(Finding.id).all()

    def create_finding(self, payload: FindingCreate) -> Finding:
        finding = Finding(
            title=payload.title,
            description=payload.description,
            severity=payload.severity,
            status=payload.status,
            signal_id=payload.signal_id,
        )
        self.db.add(finding)
        self.db.commit()
        self.db.refresh(finding)
        return finding

    def get_finding(self, finding_id: int) -> Optional[Finding]:
        return self.db.query(Finding).filter(Finding.id == finding_id).first()
