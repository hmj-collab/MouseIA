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

    def list_assets(self, company_id: Optional[int] = None, site_id: Optional[int] = None) -> list[AssetOut]:
        assets = self._repository().list_assets(company_id=company_id, site_id=site_id)
        return [self._to_out(asset) for asset in assets]

    def get_asset(self, asset_id: int) -> Optional[AssetOut]:
        asset = self._repository().get_by_id(asset_id)
        if asset is None:
            return None
        return self._to_out(asset)

    def create_asset(self, payload: AssetCreate) -> AssetOut:
        asset = self._repository().create(payload)
        return self._to_out(asset)

    def update_asset(self, asset_id: int, payload: AssetUpdate) -> Optional[AssetOut]:
        asset = self._repository().get_by_id(asset_id)
        if asset is None:
            return None
        updated = self._repository().update(asset, payload)
        return self._to_out(updated)

    def delete_asset(self, asset_id: int) -> bool:
        asset = self._repository().get_by_id(asset_id)
        if asset is None:
            return False
        self._repository().delete(asset)
        return True

    def _to_out(self, asset: AssetModel) -> AssetOut:
        return AssetOut.model_validate(asset)
