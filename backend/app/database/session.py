import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.settings import settings

SQLALCHEMY_DATABASE_URL = settings.database_url

# Ensure parent directory exists for SQLite database
if SQLALCHEMY_DATABASE_URL.startswith("sqlite:///"):
    db_path = SQLALCHEMY_DATABASE_URL.replace("sqlite:///", "")
    if db_path and db_path != ":memory:":
        abs_path = os.path.abspath(db_path)
        dir_path = os.path.dirname(abs_path)
        os.makedirs(dir_path, exist_ok=True)

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=settings.debug)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
