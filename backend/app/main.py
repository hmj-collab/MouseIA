from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.sites import router as sites_router
from app.core.settings import settings
from app.database.session import Base, engine
from app.models.site import Site  # noqa: F401

app = FastAPI(title=settings.app_name)
app.include_router(auth_router)
app.include_router(sites_router)


def initialize_database() -> None:
    Base.metadata.create_all(bind=engine)


initialize_database()


@app.on_event("startup")
def startup() -> None:
    initialize_database()


@app.get("/health")
def health_check() -> dict[str, object]:
    return {
        "status": "ok",
        "details": {
            "database": "ready",
            "auth": "ready",
        },
    }
