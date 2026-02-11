"""
API v1 Router - Combines all v1 endpoints
"""
from fastapi import APIRouter
from app.api.v1.endpoints import health

# Create main API v1 router
api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(health.router)
