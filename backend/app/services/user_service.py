from typing import Optional

import bcrypt
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserOut, UserUpdate


def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())


class UserService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def _repo(self) -> UserRepository:
        return UserRepository(self.db)

    def list_users(self) -> list[UserOut]:
        return [self._to_out(u) for u in self._repo().list_users()]

    def get_user(self, user_id: int) -> Optional[UserOut]:
        user = self._repo().get_by_id(user_id)
        return self._to_out(user) if user else None

    def create_user(self, payload: UserCreate) -> UserOut:
        repo = self._repo()
        if repo.get_by_username(payload.username):
            raise ValueError(f"Username '{payload.username}' já está em uso.")
        if repo.get_by_email(payload.email):
            raise ValueError(f"E-mail '{payload.email}' já está em uso.")
        hashed = hash_password(payload.password)
        user = repo.create(
            username=payload.username,
            email=payload.email,
            hashed_password=hashed,
            role=payload.role,
        )
        return self._to_out(user)

    def update_user(self, user_id: int, payload: UserUpdate) -> Optional[UserOut]:
        repo = self._repo()
        user = repo.get_by_id(user_id)
        if user is None:
            return None
        if payload.email and payload.email != user.email:
            if repo.get_by_email(payload.email):
                raise ValueError(f"E-mail '{payload.email}' já está em uso.")
        updated = repo.update(user, payload)
        return self._to_out(updated)

    def delete_user(self, user_id: int) -> bool:
        repo = self._repo()
        user = repo.get_by_id(user_id)
        if user is None:
            return False
        repo.delete(user)
        return True

    def authenticate(self, username: str, password: str) -> Optional[User]:
        user = self._repo().get_by_username(username)
        if user is None or not user.is_active:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def _to_out(self, user: User) -> UserOut:
        return UserOut(
            id=user.id,
            username=user.username,
            email=user.email,
            role=user.role,
            is_active=user.is_active,
        )
