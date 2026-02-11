# Backend - AI Email GTM Reachout Agent

FastAPI-based backend for automated email outreach campaigns.

## Architecture

### Service Layer

- **WorkflowService**: Orchestrates the entire campaign workflow
- **CompanyService**: Company discovery using Exa API
- **ResearchService**: Deep research on discovered companies
- **ContactService**: Finding key decision-makers
- **EmailService**: Personalized email generation

### AI Agents (Agno Framework)

- **Company Finder Agent**: Neural search for relevant companies
- **Research Agent**: Comprehensive company intelligence gathering
- **Contact Finder Agent**: Decision-maker identification
- **Email Generator Agent**: Personalized email composition

## Setup

### 1. Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Create `.env` file:

```bash
# API Keys
OPENAI_API_KEY=sk-your-key-here
EXA_API_KEY=your-exa-key-here

# CORS (JSON array format - IMPORTANT!)
CORS_ORIGINS=["http://localhost:3000","http://localhost:8000"]

# Server
HOST=0.0.0.0
PORT=8000
DEBUG=True
LOG_LEVEL=INFO
```

### 4. Run Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### Health

- `GET /health` - Health check
- `GET /` - Root redirect to docs

### Campaign Configuration

- `GET /api/v1/campaign/options` - Get available options
- `POST /api/v1/campaign/configure` - Validate configuration

### Campaign Execution

- `POST /api/v1/execute/campaign` - Execute campaign (JSON)
- `GET /api/v1/execute/campaign/stream` - Execute with SSE streaming
- `POST /api/v1/execute/companies/discover` - Discover companies only

### Campaign History

- `GET /api/v1/campaigns/history` - List all campaigns
- `GET /api/v1/campaigns/{id}` - Get campaign details
- `DELETE /api/v1/campaigns/{id}` - Delete campaign
- `GET /api/v1/campaigns/stats/summary` - Get statistics

## Key Files

```
backend/
├── app/
│   ├── main.py              # FastAPI application
│   ├── api/v1/
│   │   ├── router.py        # API router
│   │   └── endpoints/       # Route handlers
│   ├── services/            # Business logic
│   │   ├── workflow_service.py
│   │   ├── company_service.py
│   │   ├── research_service.py
│   │   ├── contact_service.py
│   │   └── email_service.py
│   ├── schemas/             # Pydantic models
│   └── core/                # Configuration
├── data/campaigns/          # JSON storage
└── requirements.txt         # Dependencies
```

## Testing

```bash
# Run tests (when implemented)
pytest

# With coverage
pytest --cov=app

# Format code
black app/
isort app/
```

## Adding New Endpoints

1. Create handler in `app/api/v1/endpoints/your_endpoint.py`
2. Define schemas in `app/schemas/`
3. Implement logic in `app/services/`
4. Register in `app/api/v1/router.py`

Example:

```python
# endpoints/your_endpoint.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/your-route")
async def your_handler():
    return {"message": "Success"}

# router.py
from app.api.v1.endpoints import your_endpoint
api_router.include_router(your_endpoint.router, prefix="/your-prefix", tags=["Your Tag"])
```

## Deployment

### Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Production Settings

- Set `DEBUG=False`
- Use proper secret keys
- Enable HTTPS
- Configure rate limiting
- Add authentication (OAuth2/JWT)

## Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json
