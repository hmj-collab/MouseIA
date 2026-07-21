from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class WebhookCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    url: str = Field(min_length=1, max_length=500)
    secret_token: Optional[str] = Field(default=None, max_length=255)
    is_active: bool = True
    trigger_events: str = "scan_completed,critical_vuln_found"


class WebhookUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    url: Optional[str] = Field(default=None, min_length=1, max_length=500)
    secret_token: Optional[str] = Field(default=None, max_length=255)
    is_active: Optional[bool] = None
    trigger_events: Optional[str] = None


class WebhookOut(BaseModel):
    id: int
    name: str
    url: str
    secret_token: Optional[str] = None
    is_active: bool
    trigger_events: str
    created_at: datetime

    model_config = {"from_attributes": True}
