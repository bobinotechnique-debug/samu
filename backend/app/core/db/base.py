from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Import models to register metadata for migrations
from app.domain import models as _  # noqa: E402,F401
