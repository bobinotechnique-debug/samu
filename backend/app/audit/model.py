from dataclasses import dataclass
from typing import Any

from app.core.ids import OrgId, ProjectId, UserId
from app.core.time import utc_now


@dataclass
class AuditEvent:
    id: str
    org_id: OrgId
    project_id: ProjectId | None
    actor_id: UserId | None
    action: str
    payload: dict[str, Any]
    created_at: str = utc_now().isoformat()
