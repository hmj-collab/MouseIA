from typing import Optional

from sqlalchemy.orm import Session

from app.models.finding import Finding
from app.schemas.finding import FindingCreate, FindingUpdate


class FindingRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_findings(
        self,
        title: Optional[str] = None,
        severity: Optional[str] = None,
        status: Optional[str] = None,
        signal_id: Optional[int] = None,
    ) -> list[Finding]:
        query = self.db.query(Finding)

        if title is not None:
            query = query.filter(Finding.title.contains(title))
        if severity is not None:
            query = query.filter(Finding.severity == severity)
        if status is not None:
            query = query.filter(Finding.status == status)
        if signal_id is not None:
            query = query.filter(Finding.signal_id == signal_id)

        return query.order_by(Finding.id).all()

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

    def update_finding(self, finding_id: int, payload: FindingUpdate) -> Optional[Finding]:
        finding = self.get_finding(finding_id)
        if finding is None:
            return None

        if payload.title is not None:
            finding.title = payload.title
        if payload.description is not None:
            finding.description = payload.description
        if payload.severity is not None:
            finding.severity = payload.severity
        if payload.status is not None:
            finding.status = payload.status
        if payload.signal_id is not None:
            finding.signal_id = payload.signal_id

        self.db.commit()
        self.db.refresh(finding)
        return finding

    def delete_finding(self, finding_id: int) -> bool:
        finding = self.get_finding(finding_id)
        if finding is None:
            return False

        self.db.delete(finding)
        self.db.commit()
        return True
