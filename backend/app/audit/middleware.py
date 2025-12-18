from typing import Callable

from fastapi import Request, Response


async def audit_middleware(request: Request, call_next: Callable[[Request], Response]) -> Response:
    response = await call_next(request)
    return response
