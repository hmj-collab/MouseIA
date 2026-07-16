from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=300)
    description: Optional[str] = None
    status: str = Field(default="open", max_length=40)
    assigned_to: Optional[str] = Field(default=None, max_length=80)
    due_date: Optional[date] = None
    recommendation_id: Optional[int] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=300)
    description: Optional[str] = None
    status: Optional[str] = Field(default=None, max_length=40)
    assigned_to: Optional[str] = Field(default=None, max_length=80)
    due_date: Optional[date] = None
    recommendation_id: Optional[int] = None


class TaskOut(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: str
    assigned_to: Optional[str] = None
    due_date: Optional[date] = None
    recommendation_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
