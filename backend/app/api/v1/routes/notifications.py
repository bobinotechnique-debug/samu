from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.api.deps import get_current_auth_context
from app.core.security.auth import AuthContext

router = APIRouter()


class NotificationSummary(BaseModel):
    status: str


@router.get("/", response_model=NotificationSummary)
def notifications_root(_: AuthContext = Depends(get_current_auth_context)) -> NotificationSummary:
    return NotificationSummary(status="not_implemented")
