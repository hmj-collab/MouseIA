from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


ASSET_TYPES = {"ip", "domain", "host", "url", "other"}


class AssetCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    asset_type: str = Field(min_length=1, max_length=40)
    value: str = Field(min_length=1, max_length=500)
    description: Optional[str] = None
    is_active: bool = True
    organization_id: Optional[int] = None
    project_id: Optional[int] = None


class AssetUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=200)
    asset_type: Optional[str] = Field(default=None, min_length=1, max_length=40)
    value: Optional[str] = Field(default=None, min_length=1, max_length=500)
    description: Optional[str] = None
    is_active: Optional[bool] = None
    organization_id: Optional[int] = None
    project_id: Optional[int] = None


class AssetOut(BaseModel):
    id: int
    name: str
    asset_type: str
    value: str
    description: Optional[str] = None
    is_active: bool
    organization_id: Optional[int] = None
    project_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
