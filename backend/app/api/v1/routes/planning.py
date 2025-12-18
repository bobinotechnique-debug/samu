from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.api.deps import get_current_auth_context
from app.core.security.auth import PrincipalContext

router = APIRouter()


class PlanningSummary(BaseModel):
    status: str


@router.get("/", response_model=PlanningSummary)
def planning_root(_: PrincipalContext = Depends(get_current_auth_context)) -> PlanningSummary:
    return PlanningSummary(status="not_implemented")
