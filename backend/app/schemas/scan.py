from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ScanCreate(BaseModel):
    scan_type: str = Field(min_length=1, max_length=80)
    status: str = Field(default="pending", max_length=40)
    description: Optional[str] = None
    asset_id: Optional[int] = None
    site_id: Optional[int] = None


class ScanUpdate(BaseModel):
    scan_type: Optional[str] = Field(default=None, min_length=1, max_length=80)
    status: Optional[str] = Field(default=None, max_length=40)
    description: Optional[str] = None
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    asset_id: Optional[int] = None
    site_id: Optional[int] = None


class ScanOut(BaseModel):
    id: int
    scan_type: str
    status: str
    description: Optional[str] = None
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    asset_id: Optional[int] = None
    site_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
