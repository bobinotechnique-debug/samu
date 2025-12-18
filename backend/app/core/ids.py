import uuid
from typing import NewType

OrgId = NewType("OrgId", uuid.UUID)
ProjectId = NewType("ProjectId", uuid.UUID)
UserId = NewType("UserId", uuid.UUID)


def parse_uuid(value: str) -> uuid.UUID:
    return uuid.UUID(value)
