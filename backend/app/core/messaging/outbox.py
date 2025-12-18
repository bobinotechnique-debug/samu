from dataclasses import dataclass
from typing import Any

from app.core.ids import OrgId, ProjectId
from app.core.time import utc_now


@dataclass
class OutboxMessage:
    id: str
    org_id: OrgId
    project_id: ProjectId | None
    topic: str
    payload: dict[str, Any]
    created_at: str = utc_now().isoformat()
