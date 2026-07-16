from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=80)
    email: EmailStr
    password: str = Field(min_length=8)
    role: str = Field(default="viewer", pattern="^(admin|viewer)$")


class UserOut(BaseModel):
    id: int
    username: str
    email: str
    role: str
    is_active: bool

    model_config = {"from_attributes": True}


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    role: Optional[str] = Field(default=None, pattern="^(admin|viewer)$")
    is_active: Optional[bool] = None
