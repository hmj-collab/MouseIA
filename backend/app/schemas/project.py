from typing import Optional

from pydantic import BaseModel, Field


class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    description: Optional[str] = None
    tags: list[str] = Field(default_factory=list)
    organization_id: Optional[int] = None


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=120)
    description: Optional[str] = None
    tags: Optional[list[str]] = None
    organization_id: Optional[int] = None


class ProjectOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    tags: list[str] = Field(default_factory=list)
    organization_id: Optional[int] = None

    model_config = {"from_attributes": True}
