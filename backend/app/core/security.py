import os
from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.settings import settings

security = HTTPBearer(auto_error=False)
SECRET_KEY = settings.jwt_secret_key
ALGORITHM = "HS256"

DEFAULT_USERS = {
    "admin": {"password": "password123", "role": "admin"},
    "viewer": {"password": "password123", "role": "viewer"},
}


def create_access_token(username: str, role: str = "viewer", organization_id: Optional[int] = None) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": username,
        "role": role,
        "exp": now + timedelta(hours=1),
        "iat": now,
    }
    if organization_id is not None:
        payload["organization_id"] = organization_id
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def authenticate_user(username: str, password: str) -> Optional[dict[str, str]]:
    if settings.app_environment != "development":
        return None
    user = DEFAULT_USERS.get(username)
    if not user or user["password"] != password:
        return None
    return {"username": username, "role": user["role"]}


def get_current_user(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)) -> dict[str, any]:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.PyJWTError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc

    username = payload.get("sub")
    role = payload.get("role", "viewer")
    org_id = payload.get("organization_id")

    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    if org_id is None:
        try:
            from app.database.session import SessionLocal
            from app.models.user import User
            with SessionLocal() as db:
                db_user = db.query(User).filter(User.username == username).first()
                if db_user:
                    org_id = db_user.organization_id
        except Exception:
            pass

    return {"username": username, "role": role, "organization_id": org_id}


def require_role(*allowed_roles: str):
    def dependency(user: dict[str, any] = Depends(get_current_user)) -> dict[str, any]:
        if user.get("role") not in allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return user

    return dependency
