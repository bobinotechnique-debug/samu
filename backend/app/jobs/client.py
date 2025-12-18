from typing import Protocol


class JobClient(Protocol):
    def enqueue(self, queue: str, payload: dict) -> str:
        ...
