# FastAPI Template - Project Structure

This document provides a detailed explanation of the project structure.

## 📁 Complete Directory Structure

```
backend/
│
├── app/                              # Main application package
│   ├── __init__.py                   # Package initialization
│   ├── main.py                       # FastAPI application factory & configuration
│   │
│   ├── api/                          # API routes and endpoints
│   │   ├── __init__.py
│   │   └── v1/                       # API version 1
│   │       ├── __init__.py
│   │       ├── router.py             # Main router combining all v1 endpoints
│   │       └── endpoints/            # Individual endpoint modules
│   │           ├── __init__.py
│   │           ├── health.py         # Health check endpoint
│   │           └── users.py          # User CRUD endpoints
│   │
│   ├── core/                         # Core functionality and configuration
│   │   ├── __init__.py
│   │   ├── config.py                 # Application settings using Pydantic
│   │   ├── security.py               # Security utilities (JWT, password hashing)
│   │   ├── logging.py                # Logging configuration
│   │   └── exceptions.py             # Custom exception handlers
│   │
│   ├── db/                           # Database configuration and utilities
│   │   ├── __init__.py
│   │   ├── session.py                # Database session management
│   │   └── init_db.py                # Database initialization script
│   │
│   ├── models/                       # SQLAlchemy database models
│   │   ├── __init__.py
│   │   └── user.py                   # User model
│   │
│   ├── schemas/                      # Pydantic schemas for validation
│   │   ├── __init__.py
│   │   ├── common.py                 # Common response schemas
│   │   ├── health.py                 # Health check schemas
│   │   └── user.py                   # User request/response schemas
│   │
│   ├── services/                     # Business logic layer
│   │   ├── __init__.py
│   │   └── user.py                   # User service with CRUD operations
│   │
│   ├── middleware/                   # Custom middleware
│   │   ├── __init__.py
│   │   └── logging.py                # Request logging middleware
│   │
│   └── utils/                        # Utility functions and helpers
│       ├── __init__.py
│       └── strings.py                # String manipulation utilities
│
├── run.py                            # Uvicorn server runner
├── requirements.txt                  # Production dependencies
├── requirements-dev.txt              # Development dependencies
│
├── .env.example                      # Example environment variables
├── .gitignore                        # Git ignore rules
│
├── Dockerfile                        # Docker image definition
├── docker-compose.yml                # Docker Compose configuration
├── .dockerignore                     # Docker ignore rules
│
├── Makefile                          # Development and deployment commands
├── quickstart.bat                    # Windows quick start script
├── quickstart.sh                     # Linux/Mac quick start script
│
└── README.md                         # Comprehensive documentation
```

## 📚 Component Descriptions

### Core Components

#### `app/main.py`

- Application factory pattern
- FastAPI instance creation
- Middleware configuration
- Router inclusion
- CORS setup
- Database initialization on startup

#### `app/core/`

- **config.py**: Environment-based configuration using Pydantic Settings
- **security.py**: JWT token creation/validation, password hashing
- **logging.py**: Centralized logging configuration
- **exceptions.py**: Global exception handlers

### API Layer

#### `app/api/v1/`

- **router.py**: Combines all v1 endpoints into a single router
- **endpoints/**: Individual endpoint files for different resources
  - Each endpoint file contains related route handlers
  - Uses dependency injection for database sessions
  - Follows RESTful conventions

### Database Layer

#### `app/db/`

- **session.py**: SQLAlchemy engine, session factory, and base class
- **init_db.py**: Script to initialize database tables

#### `app/models/`

- SQLAlchemy ORM models
- Database table definitions
- Relationships between tables

### Data Validation Layer

#### `app/schemas/`

- Pydantic models for request/response validation
- Data serialization/deserialization
- Type checking and validation rules

### Business Logic Layer

#### `app/services/`

- Business logic and CRUD operations
- Separated from route handlers for better testability
- Uses dependency injection for database access

### Middleware Layer

#### `app/middleware/`

- Custom middleware for cross-cutting concerns
- Request/response logging
- Can be extended for authentication, rate limiting, etc.

### Utilities

#### `app/utils/`

- Helper functions and utilities
- Reusable code across the application

## 🔄 Request Flow

```
Client Request
    ↓
FastAPI Application (main.py)
    ↓
Middleware (logging, CORS)
    ↓
API Router (v1/router.py)
    ↓
Endpoint Handler (v1/endpoints/*.py)
    ↓
Service Layer (services/*.py)
    ↓
Database Model (models/*.py)
    ↓
Database
```

## 🎯 Design Patterns

### 1. **Separation of Concerns**

- API routes → Business logic → Data access
- Each layer has a specific responsibility

### 2. **Dependency Injection**

```python
def get_endpoint(db: Session = Depends(get_db)):
    # db is injected automatically
```

### 3. **Repository Pattern (Services)**

- Services encapsulate data access logic
- Makes testing easier with mock services

### 4. **Factory Pattern**

- `create_application()` function creates and configures the app
- Enables different configurations for testing/production

### 5. **API Versioning**

- URL-based versioning: `/api/v1/`, `/api/v2/`
- Easy to maintain multiple versions simultaneously

## 📝 Naming Conventions

### Files

- Lowercase with underscores: `user_service.py`
- Descriptive names: `health.py`, `config.py`

### Classes

- PascalCase: `UserService`, `UserCreate`
- Descriptive: Model name + purpose

### Functions

- snake_case: `get_user()`, `create_user()`
- Verb-based for actions

### Variables

- snake_case: `user_id`, `db_session`
- Descriptive and meaningful

## 🔐 Security Best Practices

1. **Environment Variables**: Sensitive data in `.env` file
2. **Password Hashing**: bcrypt for password storage
3. **JWT Tokens**: Secure authentication (ready to implement)
4. **CORS**: Configurable CORS settings
5. **Input Validation**: Pydantic schemas validate all inputs
6. **SQL Injection**: SQLAlchemy ORM prevents SQL injection

## 🚀 Adding New Features

### Adding a New Resource (e.g., "Posts")

1. **Create Model** (`app/models/post.py`):

```python
from app.db.session import Base

class Post(Base):
    __tablename__ = "posts"
    # Define columns
```

2. **Create Schemas** (`app/schemas/post.py`):

```python
from pydantic import BaseModel

class PostCreate(BaseModel):
    title: str
    content: str
```

3. **Create Service** (`app/services/post.py`):

```python
class PostService:
    def __init__(self, db: Session):
        self.db = db
```

4. **Create Endpoints** (`app/api/v1/endpoints/posts.py`):

```python
router = APIRouter(prefix="/posts", tags=["Posts"])

@router.post("")
async def create_post(...):
    pass
```

5. **Register Router** (in `app/api/v1/router.py`):

```python
from app.api.v1.endpoints import posts

api_router.include_router(posts.router)
```

## 📊 Database Migration

For production use, consider adding Alembic for database migrations:

```bash
pip install alembic
alembic init alembic
```

## 🧪 Testing Structure

Recommended testing structure:

```
tests/
├── __init__.py
├── conftest.py              # Pytest fixtures
├── test_api/
│   ├── test_health.py
│   └── test_users.py
├── test_services/
│   └── test_user_service.py
└── test_models/
    └── test_user_model.py
```

## 📦 Extending the Template

### Add PostgreSQL Database

1. Update `requirements.txt`: add `psycopg2-binary`
2. Update `.env`: `DATABASE_URL=postgresql://user:pass@localhost/db`
3. Uncomment PostgreSQL in `docker-compose.yml`

### Add Redis Cache

1. Update `requirements.txt`: add `redis`
2. Create `app/core/cache.py` for Redis client
3. Uncomment Redis in `docker-compose.yml`

### Add Authentication

1. Create `app/api/v1/endpoints/auth.py`
2. Add login/register endpoints
3. Create authentication dependencies
4. Protect routes with `Depends(get_current_user)`

## 📖 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Uvicorn Documentation](https://www.uvicorn.org/)

---

This structure follows industry best practices and is designed to be scalable, maintainable, and easy to understand.
