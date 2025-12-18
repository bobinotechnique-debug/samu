from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.api.deps import get_current_auth_context
from app.core.security.auth import PrincipalContext

router = APIRouter()


class ProjectSummary(BaseModel):
    id: str
    name: str


@router.get("/", response_model=list[ProjectSummary])
def list_projects(_: PrincipalContext = Depends(get_current_auth_context)) -> list[ProjectSummary]:
    return []
