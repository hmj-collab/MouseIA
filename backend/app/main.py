from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.assets import router as assets_router
from app.api.auth import router as auth_router
from app.api.companies import router as companies_router
from app.api.findings import router as findings_router
from app.api.scans import router as scans_router
from app.api.signals import router as signals_router
from app.api.sites import router as sites_router
from app.api.users import router as users_router
from app.core.security import get_current_user
from app.core.settings import settings
from app.database.session import Base, engine
import app.models  # noqa: F401


def initialize_database() -> None:
    Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_database()
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:3000",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router)
app.include_router(sites_router)
app.include_router(signals_router)
app.include_router(findings_router)
app.include_router(users_router)
app.include_router(companies_router)
app.include_router(assets_router)
app.include_router(scans_router)


@app.get("/health")
def health_check() -> dict[str, object]:
    return {
        "status": "ok",
        "details": {
            "database": "ready",
            "auth": "ready",
        },
    }


@app.get("/protected")
def protected_route(user: dict[str, str] = Depends(get_current_user)) -> dict[str, str]:
    return {"user": user["username"], "role": user["role"], "status": "authorized"}
