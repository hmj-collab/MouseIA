from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class OrganizationCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    domain: Optional[str] = Field(default=None, max_length=255)
    description: Optional[str] = None
    is_active: bool = True


class OrganizationUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=200)
    domain: Optional[str] = Field(default=None, max_length=255)
    description: Optional[str] = None
    is_active: Optional[bool] = None


class OrganizationOut(BaseModel):
    id: int
    name: str
    domain: Optional[str] = None
    description: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
