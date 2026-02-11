"""
Common exception handlers
"""
from fastapi import Request, status
from fastapi.responses import JSONResponse
from app.core.logging import get_logger

logger = get_logger(__name__)


async def validation_exception_handler(request: Request, exc: Exception):
    """Handle validation errors"""
    logger.error(f"Validation error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "message": "Validation error",
            "error": str(exc)
        }
    )


async def generic_exception_handler(request: Request, exc: Exception):
    """Handle generic exceptions"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "message": "Internal server error",
            "error": str(exc) if logger.level == "DEBUG" else "An error occurred"
        }
    )
