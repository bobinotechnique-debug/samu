import contextvars
import uuid
from dataclasses import dataclass

from fastapi import Request


@dataclass
class RequestContext:
    request_id: str
    correlation_id: str


_request_context: contextvars.ContextVar[RequestContext] = contextvars.ContextVar("request_context")


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
