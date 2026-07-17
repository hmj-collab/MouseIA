from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.core.security import authenticate_user, create_access_token, require_role
from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.user import UserCreate, UserOut
from app.services.user_service import UserService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    # Tenta autenticar pelo banco primeiro
    db_user = UserService(db).authenticate(payload.username, payload.password)
    if db_user is not None:
        from app.services.audit_service import AuditService
        AuditService(db).log_action(
            user_id=db_user.id,
            action="LOGIN",
            target_type="user",
            target_id=db_user.id,
            details={"username": db_user.username, "role": db_user.role}
        )
        return TokenResponse(access_token=create_access_token(db_user.username, db_user.role))

    # Fallback: usuários hardcodados (transição / testes)
    fallback = authenticate_user(payload.username, payload.password)
    if fallback is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas.")

    from app.models.user import User
    found_user = db.query(User).filter(User.username == fallback["username"]).first()
    found_user_id = found_user.id if found_user else None

    from app.services.audit_service import AuditService
    AuditService(db).log_action(
        user_id=found_user_id,
        action="LOGIN",
        target_type="user",
        target_id=found_user_id,
        details={"username": fallback["username"], "role": fallback["role"], "method": "fallback"}
    )

    return TokenResponse(access_token=create_access_token(fallback["username"], fallback["role"]))



@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(
    payload: UserCreate,
    db: Session = Depends(get_db),
    _: dict[str, str] = Depends(require_role("admin")),
) -> UserOut:
    try:
        return UserService(db).create_user(payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
