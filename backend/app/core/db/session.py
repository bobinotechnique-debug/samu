from contextlib import contextmanager
import functools

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import get_settings


@functools.lru_cache(maxsize=1)
def _engine_from_url(database_url: str):
    is_sqlite_memory = database_url.startswith("sqlite") and ":memory:" in database_url
    connect_args = {"check_same_thread": False} if database_url.startswith("sqlite") else {}
    pool_class = StaticPool if is_sqlite_memory else None
    return create_engine(
        database_url,
        future=True,
        pool_pre_ping=True,
        connect_args=connect_args,
        poolclass=pool_class,
    )


def reset_engine_cache() -> None:
    _engine_from_url.cache_clear()


def get_engine():
    settings = get_settings()
    return _engine_from_url(settings.database_url)


def get_session_factory() -> sessionmaker[Session]:
    return sessionmaker(bind=get_engine(), autocommit=False, autoflush=False, future=True)


@contextmanager
def db_session():
    session_factory = get_session_factory()
    session = session_factory()
    try:
        yield session
    finally:
        session.close()


def check_database() -> bool:
    engine = get_engine()
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    return True
