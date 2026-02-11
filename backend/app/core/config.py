"""
Application configuration and settings
"""
import os
from typing import Optional
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings with environment variable support
    """
    
    # App Info
    APP_NAME: str = "AI Email GTM Agent"
    APP_VERSION: str = "0.1.0"
    APP_DESCRIPTION: str = "AI-powered B2B outreach agent for personalized email campaigns"
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # API Settings
    API_V1_PREFIX: str = "/api/v1"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = True
    
    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list[str] = ["*"]
    CORS_ALLOW_HEADERS: list[str] = ["*"]
    
    # Database
    DATABASE_URL: Optional[str] = "sqlite:///./app.db"
    
    # Security
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    # AI Agent API Keys
    EXA_API_KEY: str = ""
    OPENAI_API_KEY: str = ""
    
    # OpenAI Configuration
    OPENAI_MODEL: str = "gpt-4"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


# Global settings instance
settings = Settings()
