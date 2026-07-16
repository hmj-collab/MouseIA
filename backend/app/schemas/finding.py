from typing import Optional

from pydantic import BaseModel, Field


class FindingCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = None
    severity: str = Field(min_length=1, max_length=40)
    status: str = Field(default="open", min_length=1, max_length=40)
    signal_id: Optional[int] = None


class FindingOut(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    severity: str
    status: str
    signal_id: Optional[int] = None


class FindingUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = None
    severity: Optional[str] = Field(default=None, min_length=1, max_length=40)
    status: Optional[str] = Field(default=None, min_length=1, max_length=40)
    signal_id: Optional[int] = None
