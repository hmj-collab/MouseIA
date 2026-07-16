from typing import Optional

from pydantic import BaseModel, Field


class SignalCreate(BaseModel):
    source: str = Field(min_length=1, max_length=80)
    signal_type: str = Field(min_length=1, max_length=80)
    severity: str = Field(min_length=1, max_length=40)
    confidence: int = Field(default=0, ge=0, le=100)
    description: Optional[str] = None
    site_id: Optional[int] = None


class SignalOut(BaseModel):
    id: int
    source: str
    signal_type: str
    severity: str
    confidence: int
    description: Optional[str] = None
    site_id: Optional[int] = None


class SignalUpdate(BaseModel):
    source: Optional[str] = Field(default=None, min_length=1, max_length=80)
    signal_type: Optional[str] = Field(default=None, min_length=1, max_length=80)
    severity: Optional[str] = Field(default=None, min_length=1, max_length=40)
    confidence: Optional[int] = Field(default=None, ge=0, le=100)
    description: Optional[str] = None
    site_id: Optional[int] = None
