from typing import Optional

from sqlalchemy.orm import Session

from app.models.finding import Finding as FindingModel
from app.repositories.finding_repository import FindingRepository
from app.schemas.finding import FindingCreate, FindingOut, FindingUpdate


class FindingService:
    def __init__(self, db: Optional[Session] = None) -> None:
        self.db = db

    def _repository(self) -> FindingRepository:
        return FindingRepository(self.db)

    def list_findings(
        self,
        title: Optional[str] = None,
        severity: Optional[str] = None,
        status: Optional[str] = None,
        signal_id: Optional[int] = None,
    ) -> list[FindingOut]:
        findings = self._repository().list_findings(
            title=title,
            severity=severity,
            status=status,
            signal_id=signal_id,
        )
        return [self._to_out(finding) for finding in findings]

    def create_finding(self, payload: FindingCreate) -> FindingOut:
        finding = self._repository().create_finding(payload)
        return self._to_out(finding)

    def get_finding(self, finding_id: int) -> Optional[FindingOut]:
        finding = self._repository().get_finding(finding_id)
        if finding is None:
            return None
        return self._to_out(finding)

    def update_finding(self, finding_id: int, payload: FindingUpdate) -> Optional[FindingOut]:
        finding = self._repository().update_finding(finding_id, payload)
        if finding is None:
            return None
        return self._to_out(finding)

    def delete_finding(self, finding_id: int) -> bool:
        return self._repository().delete_finding(finding_id)

    def _to_out(self, finding: FindingModel) -> FindingOut:
        return FindingOut(
            id=finding.id,
            title=finding.title,
            description=finding.description,
            severity=finding.severity,
            status=finding.status,
            signal_id=finding.signal_id,
        )
