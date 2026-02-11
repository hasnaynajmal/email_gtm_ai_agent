# FastAPI Template

A professional FastAPI boilerplate with best practices, proper folder structure, and optional Docker support.

## 🚀 Features

- **Clean Architecture**: Well-organized folder structure separating concerns
- **API Versioning**: Built-in support for API versions (v1, v2, etc.)
- **Database Integration**: SQLAlchemy ORM with example models
- **Request Validation**: Pydantic schemas for request/response validation
- **Security**: JWT authentication, password hashing with bcrypt
- **Configuration Management**: Environment-based configuration with Pydantic Settings
- **Middleware**: Request logging and CORS support
- **Docker Support**: Optional containerization with Docker and Docker Compose
- **Auto Documentation**: Swagger UI and ReDoc
- **Health Check**: Built-in health check endpoint

## 📁 Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application factory
│   ├── api/                    # API routes
│   │   ├── __init__.py
│   │   └── v1/                 # API version 1
│   │       ├── __init__.py
│   │       ├── router.py       # Combined router for all v1 endpoints
│   │       └── endpoints/      # Individual endpoint files
│   │           ├── __init__.py
│   │           ├── health.py   # Health check endpoint
│   │           └── users.py    # User management endpoints
│   ├── core/                   # Core functionality
│   │   ├── __init__.py
│   │   ├── config.py           # Application settings
│   │   ├── security.py         # Security utilities
│   │   └── logging.py          # Logging configuration
│   ├── db/                     # Database
│   │   ├── __init__.py
│   │   └── session.py          # Database session management
│   ├── models/                 # SQLAlchemy models
│   │   ├── __init__.py
│   │   └── user.py             # User model
│   ├── schemas/                # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── health.py           # Health check schema
│   │   └── user.py             # User schemas
│   ├── services/               # Business logic
│   │   ├── __init__.py
│   │   └── user.py             # User service
│   ├── middleware/             # Custom middleware
│   │   ├── __init__.py
│   │   └── logging.py          # Request logging
│   └── utils/                  # Utility functions
│       ├── __init__.py
│       └── strings.py          # String utilities
├── run.py                      # Uvicorn runner
├── requirements.txt            # Python dependencies
├── .env.example                # Example environment variables
├── .gitignore                  # Git ignore file
├── Dockerfile                  # Docker image definition
├── docker-compose.yml          # Docker Compose configuration
└── .dockerignore               # Docker ignore file
```

## 🛠️ Setup

### Option 1: Local Development (Without Docker)

1. **Clone the repository**

   ```bash
   cd backend
   ```

2. **Create virtual environment**

   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**

   ```bash
   # Copy example env file
   cp .env.example .env

   # Edit .env with your configuration
   ```

5. **Run the application**

   ```bash
   python run.py
   ```

   The API will be available at:
   - API: http://localhost:8000
   - Swagger Docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Option 2: Docker Development

1. **Build and run with Docker Compose**

   ```bash
   docker-compose up --build
   ```

2. **Run in detached mode**

   ```bash
   docker-compose up -d
   ```

3. **Stop containers**

   ```bash
   docker-compose down
   ```

4. **View logs**
   ```bash
   docker-compose logs -f
   ```

## 📝 Usage

### Health Check

```bash
curl http://localhost:8000/api/v1/health
```

Response:

```json
{
  "status": "healthy",
  "message": "API is running successfully"
}
```

### Create User

```bash
curl -X POST http://localhost:8000/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "johndoe",
    "password": "SecurePassword123",
    "full_name": "John Doe"
  }'
```

### Get All Users

```bash
curl http://localhost:8000/api/v1/users
```

### Get User by ID

```bash
curl http://localhost:8000/api/v1/users/1
```

### Update User

```bash
curl -X PUT http://localhost:8000/api/v1/users/1 \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "John Updated"
  }'
```

### Delete User

```bash
curl -X DELETE http://localhost:8000/api/v1/users/1
```

## 🔧 Configuration

Environment variables can be configured in `.env` file:

| Variable       | Description                          | Default                |
| -------------- | ------------------------------------ | ---------------------- |
| `APP_NAME`     | Application name                     | FastAPI Template       |
| `ENVIRONMENT`  | Environment (development/production) | development            |
| `DEBUG`        | Debug mode                           | True                   |
| `HOST`         | Server host                          | 0.0.0.0                |
| `PORT`         | Server port                          | 8000                   |
| `DATABASE_URL` | Database connection string           | sqlite:///./app.db     |
| `SECRET_KEY`   | Secret key for JWT                   | (change in production) |
| `LOG_LEVEL`    | Logging level                        | INFO                   |

## 🎯 API Versioning

To add a new API version:

1. Create new version folder: `app/api/v2/`
2. Create endpoints in `app/api/v2/endpoints/`
3. Create router in `app/api/v2/router.py`
4. Include router in `app/main.py`:
   ```python
   from app.api.v2.router import api_router as api_v2_router
   app.include_router(api_v2_router, prefix="/api/v2")
   ```

## 📦 Adding New Features

### Add New Endpoint

1. Create endpoint file in `app/api/v1/endpoints/new_endpoint.py`
2. Define your routes
3. Add to router in `app/api/v1/router.py`:
   ```python
   from app.api.v1.endpoints import new_endpoint
   api_router.include_router(new_endpoint.router)
   ```

### Add New Model

1. Create model in `app/models/new_model.py`
2. Create schemas in `app/schemas/new_model.py`
3. Create service in `app/services/new_model.py`
4. Create endpoints using the service

## 🔒 Security

- Passwords are hashed using bcrypt
- JWT tokens for authentication (configured but not enforced)
- CORS enabled (configure in `app/core/config.py`)
- Change `SECRET_KEY` in production!

## 🧪 Testing

To add tests, create a `tests/` directory and use pytest:

```bash
pip install pytest pytest-asyncio httpx
pytest
```

## 📚 Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI JSON: http://localhost:8000/openapi.json

## 🚢 Deployment

### Production Settings

1. Set environment variables:

   ```
   ENVIRONMENT=production
   DEBUG=False
   SECRET_KEY=your-strong-secret-key
   DATABASE_URL=your-production-database-url
   ```

2. Use proper database (PostgreSQL/MySQL instead of SQLite)

3. Run with production server:
   ```bash
   gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

### Docker Production

Build and deploy production image:

```bash
docker build -t fastapi-app:latest .
docker run -p 8000:8000 --env-file .env fastapi-app:latest
```

## 📄 License

This is a template project for educational and commercial use.

## 🤝 Contributing

Feel free to fork and customize for your needs!

## 📞 Support

For issues or questions, please create an issue in the repository.
