from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from app.core.errors import AppError


def error_payload_from_exception(exc: AppError) -> dict[str, object]:
    return {
        "error": {
            "code": exc.code,
            "message": exc.message,
            "details": exc.details,
        }
    }


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def handle_app_error(_, exc: AppError):
        return JSONResponse(status_code=exc.status_code, content=error_payload_from_exception(exc))

    @app.exception_handler(HTTPException)
    async def handle_http_error(_, exc: HTTPException):
        payload = {
            "error": {
                "code": "http_error",
                "message": exc.detail,
                "details": {},
            }
        }
        return JSONResponse(status_code=exc.status_code, content=payload)

    @app.exception_handler(Exception)
    async def handle_unexpected(_, exc: Exception):
        payload = {
            "error": {
                "code": "internal_error",
                "message": "Internal server error",
                "details": {},
            }
        }
        return JSONResponse(status_code=500, content=payload)
