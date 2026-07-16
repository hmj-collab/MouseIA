from typing import Optional
from sqlalchemy.orm import Session

from app.models.recommendation import Recommendation
from app.schemas.recommendation import RecommendationCreate, RecommendationUpdate


class RecommendationRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_recommendations(self, vulnerability_id: Optional[int] = None) -> list[Recommendation]:
        query = self.db.query(Recommendation)
        if vulnerability_id is not None:
            query = query.filter(Recommendation.vulnerability_id == vulnerability_id)
        return query.order_by(Recommendation.id.desc()).all()

    def get_by_id(self, recommendation_id: int) -> Optional[Recommendation]:
        return self.db.query(Recommendation).filter(Recommendation.id == recommendation_id).first()

    def create(self, payload: RecommendationCreate) -> Recommendation:
        rec = Recommendation(
            title=payload.title,
            description=payload.description,
            priority=payload.priority,
            status=payload.status,
            vulnerability_id=payload.vulnerability_id,
        )
        self.db.add(rec)
        self.db.commit()
        self.db.refresh(rec)
        return rec

    def update(self, rec: Recommendation, payload: RecommendationUpdate) -> Recommendation:
        if payload.title is not None:
            rec.title = payload.title
        if payload.description is not None:
            rec.description = payload.description
        if payload.priority is not None:
            rec.priority = payload.priority
        if payload.status is not None:
            rec.status = payload.status
        if payload.vulnerability_id is not None:
            rec.vulnerability_id = payload.vulnerability_id

        self.db.commit()
        self.db.refresh(rec)
        return rec

    def delete(self, rec: Recommendation) -> None:
        self.db.delete(rec)
        self.db.commit()
