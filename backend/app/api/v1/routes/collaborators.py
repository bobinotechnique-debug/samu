from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.api.deps import get_current_auth_context
from app.core.security.auth import PrincipalContext

router = APIRouter()


class CollaboratorSummary(BaseModel):
    id: str
    display_name: str


@router.get("/", response_model=list[CollaboratorSummary])
def list_collaborators(_: PrincipalContext = Depends(get_current_auth_context)) -> list[CollaboratorSummary]:
    return []
