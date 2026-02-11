"""
Common response schemas
"""
from typing import Optional, Any
from pydantic import BaseModel


class SuccessResponse(BaseModel):
    """Standard success response"""
    success: bool = True
    message: str
    data: Optional[Any] = None


class ErrorResponse(BaseModel):
    """Standard error response"""
    success: bool = False
    message: str
    error: Optional[str] = None
