from __future__ import annotations

from contextlib import AbstractContextManager
from typing import Protocol

from sqlalchemy.orm import Session


class UnitOfWork(Protocol):
    session: Session

    def __enter__(self) -> "UnitOfWork":
        ...

    def __exit__(self, exc_type, exc, traceback) -> None:
        ...

    def commit(self) -> None:
        ...

    def rollback(self) -> None:
        ...


class SqlAlchemyUnitOfWork(AbstractContextManager):
    def __init__(self, session: Session) -> None:
        self.session = session

    def __exit__(self, exc_type, exc, traceback) -> None:  # type: ignore[override]
        if exc:
            self.rollback()
        else:
            self.commit()
        self.session.close()

    def commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()
