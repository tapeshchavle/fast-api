"""
Custom exception classes and global exception handlers.

Provides a consistent error response format across the entire API.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

logger = logging.getLogger(__name__)


# ── Error Response Schema ────────────────────────────────────


class ErrorResponse(BaseModel):
    """Standard error response body."""

    detail: str
    status_code: int
    error_type: str


# ── Custom Exceptions ────────────────────────────────────────


class AppException(Exception):
    """Base exception for application-specific errors."""

    def __init__(
        self,
        detail: str = "An unexpected error occurred",
        status_code: int = 500,
        error_type: str = "INTERNAL_ERROR",
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.detail = detail
        self.status_code = status_code
        self.error_type = error_type
        self.headers = headers
        super().__init__(detail)


class NotFoundException(AppException):
    """Resource not found."""

    def __init__(self, detail: str = "Resource not found") -> None:
        super().__init__(detail=detail, status_code=404, error_type="NOT_FOUND")


class BadRequestException(AppException):
    """Invalid request data."""

    def __init__(self, detail: str = "Bad request") -> None:
        super().__init__(detail=detail, status_code=400, error_type="BAD_REQUEST")


class UnauthorizedException(AppException):
    """Authentication required."""

    def __init__(self, detail: str = "Not authenticated") -> None:
        super().__init__(detail=detail, status_code=401, error_type="UNAUTHORIZED")


class ForbiddenException(AppException):
    """Insufficient permissions."""

    def __init__(self, detail: str = "Forbidden") -> None:
        super().__init__(detail=detail, status_code=403, error_type="FORBIDDEN")


# ── Exception Handlers ──────────────────────────────────────


def register_exception_handlers(app: FastAPI) -> None:
    """Register all custom exception handlers on the app."""

    @app.exception_handler(AppException)
    async def app_exception_handler(_request: Request, exc: AppException) -> JSONResponse:
        logger.warning("AppException: %s (status=%d)", exc.detail, exc.status_code)
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(
                detail=exc.detail,
                status_code=exc.status_code,
                error_type=exc.error_type,
            ).model_dump(),
            headers=exc.headers,
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(_request: Request, exc: HTTPException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(
                detail=str(exc.detail),
                status_code=exc.status_code,
                error_type="HTTP_ERROR",
            ).model_dump(),
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(_request: Request, exc: Exception) -> JSONResponse:
        logger.exception("Unhandled exception: %s", exc)
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(
                detail="Internal server error",
                status_code=500,
                error_type="INTERNAL_ERROR",
            ).model_dump(),
        )
