"""
FastAPI Application Factory
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.core.logging import setup_logging
from app.api.v1.router import api_router
from app.db.session import engine, Base
from app.middleware.logging import RequestLoggingMiddleware


def create_application() -> FastAPI:
    """
    Create and configure FastAPI application
    """
    # Setup logging
    setup_logging()
    
    # Create FastAPI app
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description=settings.APP_DESCRIPTION,
        debug=settings.DEBUG,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json"
    )
    
    # CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
        allow_methods=settings.CORS_ALLOW_METHODS,
        allow_headers=settings.CORS_ALLOW_HEADERS,
    )
    
    # Request logging middleware
    app.add_middleware(RequestLoggingMiddleware)
    
    # Include API routers
    app.include_router(api_router, prefix=settings.API_V1_PREFIX)
    
    # Root endpoint
    @app.get("/")
    async def root():
        return JSONResponse(
            content={
                "message": f"Welcome to {settings.APP_NAME}",
                "version": settings.APP_VERSION,
                "docs": "/docs"
            }
        )
    
    # Create database tables
    @app.on_event("startup")
    async def startup_event():
        """Initialize database on startup"""
        Base.metadata.create_all(bind=engine)
    
    return app


# Create app instance
app = create_application()
