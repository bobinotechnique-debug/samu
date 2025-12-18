from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.api.deps import get_current_auth_context
from app.core.security.auth import PrincipalContext

router = APIRouter()


class FinanceSummary(BaseModel):
    status: str


@router.get("/", response_model=FinanceSummary)
def finance_root(_: PrincipalContext = Depends(get_current_auth_context)) -> FinanceSummary:
    return FinanceSummary(status="not_implemented")
