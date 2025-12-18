from contextlib import contextmanager
from typing import Iterator


@contextmanager
def traced_span(name: str) -> Iterator[None]:
    yield
