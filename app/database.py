from __future__ import annotations

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

_DB_HOST = os.environ.get("DB_HOST", "")
_DB_PORT = os.environ.get("DB_PORT", "5432")
_DB_NAME = os.environ.get("DB_NAME", "")
_DB_USER = os.environ.get("DB_USER", "")
_DB_PASSWORD = os.environ.get("DB_PASSWORD", "")

_missing = [name for name, val in {
    "DB_HOST": _DB_HOST,
    "DB_NAME": _DB_NAME,
    "DB_USER": _DB_USER,
    "DB_PASSWORD": _DB_PASSWORD,
}.items() if not val]

if _missing:
    raise RuntimeError(
        f"Missing required database environment variable(s): {', '.join(_missing)}. "
        "Set DB_HOST, DB_PORT (default 5432), DB_NAME, DB_USER, and DB_PASSWORD."
    )

DATABASE_URL = (
    f"postgresql://{_DB_USER}:{_DB_PASSWORD}@{_DB_HOST}:{_DB_PORT}/{_DB_NAME}"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,      # drops stale connections automatically
    pool_size=5,
    max_overflow=10,
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


def create_tables() -> None:
    """Create all tables that do not yet exist. Safe to call on every startup."""
    from .models import AppUserModel, ScanModel, ScheduleModel, TeamModel  # noqa: F401
    Base.metadata.create_all(engine)
