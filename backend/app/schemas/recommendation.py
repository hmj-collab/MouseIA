from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class RecommendationCreate(BaseModel):
    title: str = Field(min_length=1, max_length=300)
    description: Optional[str] = None
    priority: str = Field(default="medium", max_length=40)
    status: str = Field(default="open", max_length=40)
    vulnerability_id: Optional[int] = None


class RecommendationUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=300)
    description: Optional[str] = None
    priority: Optional[str] = Field(default=None, max_length=40)
    status: Optional[str] = Field(default=None, max_length=40)
    vulnerability_id: Optional[int] = None


class RecommendationOut(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    priority: str
    status: str
    vulnerability_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
