from typing import Optional
from sqlalchemy.orm import Session
from app.models.asset import Asset as AssetModel
from app.repositories.asset_repository import AssetRepository
from app.schemas.asset import AssetCreate, AssetOut, AssetUpdate


class AssetService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def _repository(self) -> AssetRepository:
        return AssetRepository(self.db)

    def list_assets(self, organization_id: Optional[int] = None, project_id: Optional[int] = None) -> list[AssetOut]:
        assets = self._repository().list_assets(organization_id=organization_id, project_id=project_id)
        return [self._to_out(asset) for asset in assets]

    def get_asset(self, asset_id: int, organization_id: Optional[int] = None) -> Optional[AssetOut]:
        asset = self._repository().get_by_id(asset_id, organization_id)
        if asset is None:
            return None
        return self._to_out(asset)

    def create_asset(self, payload: AssetCreate, organization_id: Optional[int] = None) -> AssetOut:
        if organization_id is not None:
            payload.organization_id = organization_id
        if payload.project_id:
            from app.models.project import Project
            proj = self.db.query(Project).filter(Project.id == payload.project_id).first()
            if proj and organization_id is not None and proj.organization_id != organization_id:
                raise ValueError("O projeto informado não pertence à sua organização.")
        asset = self._repository().create(payload)
        return self._to_out(asset)

    def update_asset(self, asset_id: int, payload: AssetUpdate, organization_id: Optional[int] = None) -> Optional[AssetOut]:
        asset = self._repository().get_by_id(asset_id, organization_id)
        if asset is None:
            return None
        updated = self._repository().update(asset, payload)
        return self._to_out(updated)

    def delete_asset(self, asset_id: int, organization_id: Optional[int] = None) -> bool:
        asset = self._repository().get_by_id(asset_id, organization_id)
        if asset is None:
            return False

        # 1. Delete all Scans associated with the Asset
        from app.models.scan import Scan
        scans = self.db.query(Scan).filter(Scan.asset_id == asset_id).all()
        for scan in scans:
            self.db.delete(scan)

        # 1.5 Delete all Signals associated with the Asset
        from app.models.signal import Signal
        signals = self.db.query(Signal).filter(Signal.asset_id == asset_id).all()
        for sig in signals:
            self.db.delete(sig)

        # 2. Delete all Vulnerabilities, Recommendations, Tasks, Findings
        from app.models.vulnerability import Vulnerability
        from app.models.recommendation import Recommendation
        from app.models.task import Task
        from app.models.finding import Finding

        vulns = self.db.query(Vulnerability).filter(Vulnerability.asset_id == asset_id).all()
        for vuln in vulns:
            # Delete Tasks linked to Recommendations of this Vulnerability
            recs = self.db.query(Recommendation).filter(Recommendation.vulnerability_id == vuln.id).all()
            for rec in recs:
                tasks = self.db.query(Task).filter(Task.recommendation_id == rec.id).all()
                for task in tasks:
                    self.db.delete(task)
                self.db.delete(rec)

            finding_id = vuln.finding_id
            self.db.delete(vuln)

            if finding_id:
                finding = self.db.query(Finding).filter(Finding.id == finding_id).first()
                if finding:
                    signal_id = finding.signal_id
                    self.db.delete(finding)
                    if signal_id:
                        signal = self.db.query(Signal).filter(Signal.id == signal_id).first()
                        if signal:
                            self.db.delete(signal)

        # 3. Delete the Asset itself
        self._repository().delete(asset)
        return True

    def _to_out(self, asset: AssetModel) -> AssetOut:
        return AssetOut.model_validate(asset)
