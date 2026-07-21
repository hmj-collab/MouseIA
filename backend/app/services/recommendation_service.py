from typing import Optional
from sqlalchemy.orm import Session

from app.models.recommendation import Recommendation as RecommendationModel
from app.repositories.recommendation_repository import RecommendationRepository
from app.schemas.recommendation import RecommendationCreate, RecommendationOut, RecommendationUpdate


class RecommendationService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def _repository(self) -> RecommendationRepository:
        return RecommendationRepository(self.db)

    def list_recommendations(self, vulnerability_id: Optional[int] = None, organization_id: Optional[int] = None) -> list[RecommendationOut]:
        recs = self._repository().list_recommendations(vulnerability_id=vulnerability_id, organization_id=organization_id)
        return [self._to_out(r) for r in recs]

    def get_recommendation(self, recommendation_id: int, organization_id: Optional[int] = None) -> Optional[RecommendationOut]:
        rec = self._repository().get_by_id(recommendation_id, organization_id)
        if rec is None:
            return None
        return self._to_out(rec)

    def create_recommendation(self, payload: RecommendationCreate, organization_id: Optional[int] = None) -> RecommendationOut:
        if organization_id is not None and payload.vulnerability_id:
            from app.models.vulnerability import Vulnerability
            from app.models.asset import Asset
            vuln = self.db.query(Vulnerability).filter(Vulnerability.id == payload.vulnerability_id).first()
            if vuln:
                asset = self.db.query(Asset).filter(Asset.id == vuln.asset_id).first()
                if asset and asset.organization_id != organization_id:
                    raise ValueError("A vulnerabilidade informada não pertence à sua organização.")
        rec = self._repository().create(payload)
        return self._to_out(rec)

    def update_recommendation(self, recommendation_id: int, payload: RecommendationUpdate, organization_id: Optional[int] = None) -> Optional[RecommendationOut]:
        rec = self._repository().get_by_id(recommendation_id, organization_id)
        if rec is None:
            return None
        if organization_id is not None and payload.vulnerability_id:
            from app.models.vulnerability import Vulnerability
            from app.models.asset import Asset
            vuln = self.db.query(Vulnerability).filter(Vulnerability.id == payload.vulnerability_id).first()
            if vuln:
                asset = self.db.query(Asset).filter(Asset.id == vuln.asset_id).first()
                if asset and asset.organization_id != organization_id:
                    raise ValueError("A vulnerabilidade informada não pertence à sua organização.")
        updated = self._repository().update(rec, payload)
        return self._to_out(updated)

    def delete_recommendation(self, recommendation_id: int, organization_id: Optional[int] = None) -> bool:
        rec = self._repository().get_by_id(recommendation_id, organization_id)
        if rec is None:
            return False
        self._repository().delete(rec)
        return True

    def _to_out(self, rec: RecommendationModel) -> RecommendationOut:
        return RecommendationOut.model_validate(rec)
