from typing import Optional

from sqlalchemy.orm import Session

from app.models.asset import Asset
from app.schemas.asset import AssetCreate, AssetUpdate


class AssetRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_assets(self, organization_id: Optional[int] = None, project_id: Optional[int] = None) -> list[Asset]:
        q = self.db.query(Asset)
        if organization_id is not None:
            q = q.filter(Asset.organization_id == organization_id)
        if project_id is not None:
            q = q.filter(Asset.project_id == project_id)
        return q.order_by(Asset.id).all()

    def get_by_id(self, asset_id: int) -> Optional[Asset]:
        return self.db.query(Asset).filter(Asset.id == asset_id).first()

    def create(self, payload: AssetCreate) -> Asset:
        asset = Asset(**payload.model_dump())
        self.db.add(asset)
        self.db.commit()
        self.db.refresh(asset)
        return asset

    def update(self, asset: Asset, payload: AssetUpdate) -> Asset:
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(asset, field, value)
        self.db.commit()
        self.db.refresh(asset)
        return asset

    def delete(self, asset: Asset) -> None:
        self.db.delete(asset)
        self.db.commit()
