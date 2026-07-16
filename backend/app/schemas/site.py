from typing import Optional

from pydantic import BaseModel, Field, HttpUrl


class SiteCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    url: HttpUrl
    description: Optional[str] = None
    tags: list[str] = Field(default_factory=list)


class SiteUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=120)
    url: Optional[HttpUrl] = None
    description: Optional[str] = None
    tags: Optional[list[str]] = None


class SiteOut(BaseModel):
    id: int
    name: str
    url: str
    description: Optional[str] = None
    tags: list[str] = Field(default_factory=list)
