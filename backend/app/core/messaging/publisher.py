from typing import Protocol

from app.core.messaging.outbox import OutboxMessage


class MessagePublisher(Protocol):
    def publish(self, message: OutboxMessage) -> None:
        ...
