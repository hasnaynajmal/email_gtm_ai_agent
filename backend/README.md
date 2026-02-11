# AI Email GTM Agent - Backend API

An AI-powered B2B outreach system that automates company discovery, research, contact finding, and personalized email generation using AI agents.

## 🚀 Features

- **Automated Company Discovery**: Find target companies using Exa search based on industry, size, and criteria
- **Deep Company Research**: AI-powered intelligence gathering for personalization
- **Contact Finding**: Discover decision makers and their contact information
- **Personalized Email Generation**: Create engaging, conversational cold emails
- **Campaign Orchestration**: Complete workflow automation from discovery to email
- **Real-time Streaming**: Progress updates during campaign execution
- **REST API**: Clean, well-documented API endpoints
- **Docker Support**: Containerized deployment ready

## 🏗️ Architecture

### Core Services

1. **AgentService** - Manages AI agents (Agno + OpenAI)
2. **CompanyDiscoveryService** - Finds target companies via Exa
3. **CompanyResearchService** - Gathers company intelligence
4. **ContactFinderService** - Discovers decision makers
5. **EmailGenerationService** - Creates personalized emails
6. **WorkflowOrchestrationService** - Coordinates full campaign

## 📁 Project Structure

```
backend/
├── app/
│   ├── main.py                 # FastAPI application factory
│   ├── api/v1/
│   │   ├── router.py           # API router
│   │   └── endpoints/
│   │       ├── health.py       # Health check
│   │       ├── campaign.py     # Campaign configuration
│   │       └── execution.py    # Campaign execution
│   ├── core/
│   │   ├── config.py           # Settings & environment
│   │   ├── constants.py        # Templates & constants
│   │   ├── exceptions.py       # Custom exceptions
│   │   └── logging.py          # Logging setup
│   ├── schemas/
│   │   ├── outreach.py         # Pydantic models
│   │   └── health.py           # Health schemas
│   ├── services/
│   │   ├── agent_service.py    # AI agent management
│   │   ├── company_service.py  # Company discovery
│   │   ├── research_service.py # Company research
│   │   ├── contact_service.py  # Contact finding
│   │   ├── email_service.py    # Email generation
│   │   └── workflow_service.py # Campaign orchestration
│   ├── models/                 # Database models (optional)
│   ├── middleware/             # Custom middleware
│   └── utils/                  # Utilities
├── requirements.txt            # Python dependencies
├── .env.example                # Environment template
├── Dockerfile                  # Docker image
└── docker-compose.yml          # Docker Compose config
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

   # Edit .env and add your API keys
   # Required:
   EXA_API_KEY=your_exa_api_key_here
   OPENAI_API_KEY=your_openai_api_key_here
   ```

5. **Run the application**

   ```bash
   # Using Python directly
   python run.py

   # Or using uvicorn
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

6. **Access the API**
   - API: http://localhost:8000
   - Swagger Docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## 🔑 API Keys Required

### Exa API Key

- **Purpose**: Company discovery and web research
- **Get it from**: https://exa.ai
- **Used for**: Finding target companies, gathering company intelligence

### OpenAI API Key

- **Purpose**: AI-powered email generation and analysis
- **Get it from**: https://platform.openai.com
- **Used for**: Running AI agents, generating personalized emails

## 📚 API Endpoints

### Campaign Configuration

#### `GET /api/v1/campaign/options`

Get all available campaign configuration options.

**Response:**

```json
{
  "company_categories": {
    "SaaS/Technology Companies": {
      "description": "Software, cloud services, and tech platforms",
      "typical_roles": ["CTO", "Head of Engineering", ...]
    },
    ...
  },
  "service_types": ["Software Solution", "Consulting Services", ...],
  "company_sizes": ["Startup (1-50)", "SMB (51-500)", ...],
  "personalization_levels": ["Basic", "Medium", "Deep"],
  "target_departments": ["GTM (Sales & Marketing)", "HR", ...]
}
```

#### `POST /api/v1/campaign/configure`

Validate campaign configuration before execution.

**Request:**

```json
{
  "outreach_config": {
    "company_category": "SaaS/Technology Companies",
    "target_departments": ["GTM (Sales & Marketing)"],
    "service_type": "Software Solution",
    "company_size_preference": "SMB (51-500)",
    "personalization_level": "Deep"
  },
  "sender_details": {
    "name": "John Doe",
    "email": "john@company.com",
    "organization": "Acme Corp",
    "service_offered": "We help build data products",
    "calendar_link": "https://calendly.com/john"
  },
  "num_companies": 5
}
```

**Response:**

```json
{
  "valid": true,
  "errors": [],
  "warnings": ["Calendar link not provided - emails will lack booking link"],
  "config_summary": { ... }
}
```

### Campaign Execution

#### `POST /api/v1/execute/campaign`

Execute a complete automated outreach campaign (synchronous).

**Request:** Same as `/campaign/configure`

**Response:**

```json
{
  "campaign_id": null,
  "results": [
    {
      "company_info": {
        "company_name": "Example Corp",
        "website_url": "https://example.com",
        "industry": "SaaS",
        "recent_news": [...],
        "challenges": [...],
        ...
      },
      "contacts": [
        {
          "name": "Jane Smith",
          "title": "VP of Marketing",
          "email": "jane@example.com",
          "linkedin": "https://linkedin.com/in/jane",
          ...
        }
      ],
      "generated_emails": [
        {
          "subject": "Quick question about Example Corp's growth",
          "body": "Hey Jane,\n\nI noticed Example Corp's...",
          "personalization_notes": "Referenced recent company news..."
        }
      ],
      "research_summary": "Company: Example Corp..."
    }
  ],
  "total_companies": 5,
  "total_contacts": 8,
  "total_emails": 8,
  "execution_time": 120.5
}
```

#### `POST /api/v1/execute/campaign/stream`

Execute campaign with real-time progress updates (Server-Sent Events).

Returns NDJSON stream with progress updates:

```json
{"status": "discovering", "message": "Discovering target companies...", "progress": 0.1}
{"status": "discovered", "message": "Found 5 companies", "progress": 0.2, "companies_found": 5}
{"status": "processing", "message": "Researching Example Corp...", "progress": 0.3, ...}
{"status": "completed", "message": "Campaign completed", "progress": 1.0, "results": [...]}
```

#### `POST /api/v1/execute/companies/discover`

Discover companies only (without full campaign).

**Request:**

```json
{
  "company_category": "SaaS/Technology Companies",
  "target_departments": ["GTM (Sales & Marketing)"],
  "service_type": "Software Solution",
  "company_size_preference": "All Sizes",
  "personalization_level": "Deep"
}
```

**Query Params:** `num_companies` (default: 5, max: 20)

**Response:**

```json
{
  "status": "success",
  "companies_found": 5,
  "companies": [
    {
      "company_name": "Example Corp",
      "website_url": "https://example.com",
      "industry": "SaaS",
      "description": "Leading SaaS platform for...",
      "company_size": "51-500",
      "location": "San Francisco, CA"
    }
  ]
}
```

#### `POST /api/v1/execute/email/generate`

Generate a single personalized email.

**Request:**

```json
{
  "company_info": {
    "company_name": "Example Corp",
    "website_url": "https://example.com",
    "industry": "SaaS",
    ...
  },
  "contact_info": {
    "name": "Jane Smith",
    "title": "VP of Marketing",
    "company": "Example Corp",
    ...
  },
  "sender_details": { ... },
  "outreach_config": { ... }
}
```

**Response:**

```json
{
  "email": {
    "subject": "Quick question about Example Corp",
    "body": "Hey Jane,\n\n...",
    "personalization_notes": "Referenced recent news..."
  },
  "company_info": { ... },
  "contact_info": { ... }
}
```

### Health & Status

#### `GET /api/v1/health`

Basic health check.

#### `GET /api/v1/execute/health`

Check campaign execution service health (validates AI agents).

**Response:**

```json
{
  "status": "healthy",
  "agents_configured": true,
  "exa_api_configured": true,
  "openai_api_configured": true,
  "openai_model": "gpt-4"
}
```

## 🧪 Example Usage

### Using cURL

```bash
# Get campaign options
curl http://localhost:8000/api/v1/campaign/options

# Discover companies
curl -X POST http://localhost:8000/api/v1/execute/companies/discover?num_companies=3 \
  -H "Content-Type: application/json" \
  -d '{
    "company_category": "SaaS/Technology Companies",
    "target_departments": ["GTM (Sales & Marketing)"],
    "service_type": "Software Solution",
    "company_size_preference": "All Sizes",
    "personalization_level": "Deep"
  }'

# Execute full campaign
curl -X POST http://localhost:8000/api/v1/execute/campaign \
  -H "Content-Type: application/json" \
  -d @campaign_config.json
```

### Using Python

````python
import requests

# Get options
response = requests.get("http://localhost:8000/api/v1/campaign/options")
options = response.json()

# Execute campaign
campaign_config = {
    "outreach_config": {
        "company_category": "SaaS/Technology Companies",
        "target_departments": ["GTM (Sales & Marketing)"],
        "service_type": "Software Solution",
        "company_size_preference": "SMB (51-500)",
        "personalization_level": "Deep"
    },
    "sender_details": {
        "name": "John Doe",
        "email": "john@company.com",
        "organization": "Acme Corp",
        "service_offered": "We build data products",
        "calendar_link": "https://calendly.com/john"
    },
    "num_companies": 5
}

response = requests.post(
    "http://localhost:8000/api/v1/execute/campaign",
    json=campaign_config
)
results = response.json()
print(f"Generated {results['total_emails']} emails for {results['total_companies']} companies")
```   # Edit .env with your configuration
````

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
