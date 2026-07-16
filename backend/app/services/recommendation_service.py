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

    def list_recommendations(self, vulnerability_id: Optional[int] = None) -> list[RecommendationOut]:
        recs = self._repository().list_recommendations(vulnerability_id=vulnerability_id)
        return [self._to_out(r) for r in recs]

    def get_recommendation(self, recommendation_id: int) -> Optional[RecommendationOut]:
        rec = self._repository().get_by_id(recommendation_id)
        if rec is None:
            return None
        return self._to_out(rec)

    def create_recommendation(self, payload: RecommendationCreate) -> RecommendationOut:
        rec = self._repository().create(payload)
        return self._to_out(rec)

    def update_recommendation(self, recommendation_id: int, payload: RecommendationUpdate) -> Optional[RecommendationOut]:
        rec = self._repository().get_by_id(recommendation_id)
        if rec is None:
            return None
        updated = self._repository().update(rec, payload)
        return self._to_out(updated)

    def delete_recommendation(self, recommendation_id: int) -> bool:
        rec = self._repository().get_by_id(recommendation_id)
        if rec is None:
            return False
        self._repository().delete(rec)
        return True

    def _to_out(self, rec: RecommendationModel) -> RecommendationOut:
        return RecommendationOut.model_validate(rec)
