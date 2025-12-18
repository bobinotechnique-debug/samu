from typing import Protocol

from app.audit.model import AuditEvent


class AuditSink(Protocol):
    def write(self, event: AuditEvent) -> None:
        ...
