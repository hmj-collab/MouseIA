from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from app.api.dependencies import get_db
from app.core.security import require_role
from app.schemas.recommendation import RecommendationCreate, RecommendationOut, RecommendationUpdate
from app.services.recommendation_service import RecommendationService

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.get("", response_model=list[RecommendationOut])
def list_recommendations(
    vulnerability_id: Optional[int] = None,
    db: Session = Depends(get_db),
    user: dict[str, any] = Depends(require_role("admin", "viewer"))
) -> list[RecommendationOut]:
    org_id = user.get("organization_id")
    if org_id is not None and vulnerability_id is not None:
        from app.models.vulnerability import Vulnerability
        from app.models.asset import Asset
        vuln = db.query(Vulnerability).filter(Vulnerability.id == vulnerability_id).first()
        if vuln:
            asset = db.query(Asset).filter(Asset.id == vuln.asset_id).first()
            if asset and asset.organization_id != org_id:
                return []
    return RecommendationService(db).list_recommendations(vulnerability_id=vulnerability_id, organization_id=org_id)


@router.post("", response_model=RecommendationOut, status_code=status.HTTP_201_CREATED)
def create_recommendation(
    payload: RecommendationCreate,
    db: Session = Depends(get_db),
    user: dict[str, any] = Depends(require_role("admin"))
) -> RecommendationOut:
    try:
        return RecommendationService(db).create_recommendation(payload, organization_id=user.get("organization_id"))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/{recommendation_id}", response_model=RecommendationOut)
def get_recommendation(
    recommendation_id: int,
    db: Session = Depends(get_db),
    user: dict[str, any] = Depends(require_role("admin", "viewer"))
) -> RecommendationOut:
    rec = RecommendationService(db).get_recommendation(recommendation_id, organization_id=user.get("organization_id"))
    if rec is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recomendação não encontrada")
    return rec


@router.put("/{recommendation_id}", response_model=RecommendationOut)
def update_recommendation(
    recommendation_id: int,
    payload: RecommendationUpdate,
    db: Session = Depends(get_db),
    user: dict[str, any] = Depends(require_role("admin"))
) -> RecommendationOut:
    try:
        rec = RecommendationService(db).update_recommendation(recommendation_id, payload, organization_id=user.get("organization_id"))
        if rec is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recomendação não encontrada")
        return rec
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.delete("/{recommendation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recommendation(
    recommendation_id: int,
    db: Session = Depends(get_db),
    user: dict[str, any] = Depends(require_role("admin"))
) -> None:
    deleted = RecommendationService(db).delete_recommendation(recommendation_id, organization_id=user.get("organization_id"))
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recomendação não encontrada")
