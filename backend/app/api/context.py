import contextvars
import uuid
from dataclasses import dataclass, replace
from typing import Optional

from fastapi import Request


@dataclass
class RequestContext:
    request_id: str
    correlation_id: str
    actor_id: Optional[str] = None
    org_id: Optional[str] = None
    token_id: Optional[str] = None


_request_context: contextvars.ContextVar[RequestContext] = contextvars.ContextVar(
    "request_context", default=RequestContext(request_id="unset", correlation_id="unset")
)


def request_context_middleware():
    async def middleware(request: Request, call_next):
        correlation_header = request.headers.get("X-Correlation-ID")
        correlation_id = correlation_header or str(uuid.uuid4())
        context = RequestContext(request_id=str(uuid.uuid4()), correlation_id=correlation_id)
        _request_context.set(context)
        response = await call_next(request)
        response.headers["X-Request-ID"] = context.request_id
        response.headers["X-Correlation-ID"] = context.correlation_id
        return response

    return middleware


def get_request_context() -> RequestContext:
    return _request_context.get()


def attach_principal(request_context: RequestContext, *, actor_id: str | None, org_id: str | None, token_id: str | None) -> None:
    updated = replace(request_context, actor_id=actor_id, org_id=org_id, token_id=token_id)
    _request_context.set(updated)
