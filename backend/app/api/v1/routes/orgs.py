from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.api.deps import get_current_auth_context
from app.core.security.auth import AuthContext

router = APIRouter()


class OrgSummary(BaseModel):
    id: str
    name: str


@router.get("/", response_model=list[OrgSummary])
def list_orgs(_: AuthContext = Depends(get_current_auth_context)) -> list[OrgSummary]:
    return []
