# AI Email GTM Reachout Agent - Full Stack Application

> **Intelligent AI-Powered Email Outreach Automation Platform**  
> Transform your Go-To-Market strategy with automated company discovery, intelligent research, and personalized email generation.

[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-14+-black.svg)](https://nextjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5+-blue.svg)](https://www.typescriptlang.org/)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Frontend Guide](#frontend-guide)
- [Configuration](#configuration)
- [Development](#development)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Overview

The **AI Email GTM Reachout Agent** is a comprehensive full-stack application that automates the entire outreach workflow:

1. **Company Discovery** - Find relevant companies using AI-powered search (Exa API)
2. **Deep Research** - Gather comprehensive intelligence about each company
3. **Contact Finding** - Identify key decision-makers and their contact information
4. **Email Generation** - Create hyper-personalized outreach emails
5. **Campaign Management** - Track, manage, and analyze all campaigns

**Perfect for:**

- Sales teams targeting specific industries
- Marketing agencies running outbound campaigns
- Startups building their customer pipeline
- Business development professionals

---

## Features

### AI-Powered Automation

- **Smart Company Discovery**: Uses Exa API to find companies matching your criteria
- **Intelligent Research**: Multi-agent system gathers comprehensive company insights
- **Context-Aware Emails**: Personalized content based on company data and recent news
- **Adaptive Learning**: Improves recommendations based on campaign results

### Campaign Management

- **Multi-Step Configuration**: Easy-to-use wizard for campaign setup
- **Real-Time Execution**: Live progress tracking with Server-Sent Events (SSE)
- **Campaign History**: Complete archive with search and filtering
- **Detailed Analytics**: Track performance metrics and insights

### Modern User Experience

- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **Real-Time Updates**: Live progress bars and status notifications
- **Interactive Results**: Expandable cards, copy functionality, export options
- **Toast Notifications**: User-friendly feedback for all actions

### Developer-Friendly

- **Clean Architecture**: Separation of concerns, modular design
- **Type Safety**: Full TypeScript coverage with strict typing
- **API-First Design**: RESTful endpoints with comprehensive documentation
- **Easy Deployment**: Docker support, environment-based configuration

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend (Next.js)                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Campaign    │  │   Campaign   │  │   Campaign   │      │
│  │  Config UI   │  │  Execution   │  │   History    │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
│         │                  │                  │               │
│         └──────────────────┼──────────────────┘               │
│                            │                                  │
│                    ┌───────▼────────┐                        │
│                    │   API Client   │                        │
│                    │    (Axios)     │                        │
│                    └───────┬────────┘                        │
└────────────────────────────┼─────────────────────────────────┘
                             │ HTTP/SSE
┌────────────────────────────▼─────────────────────────────────┐
│                     Backend (FastAPI)                         │
│  ┌──────────────────────────────────────────────────────┐   │
│  │               API Endpoints (v1)                      │   │
│  │  • Campaign Configuration  • Execution  • History     │   │
│  └────────┬──────────────────────────────────────────────┘   │
│           │                                                   │
│  ┌────────▼──────────────────────────────────────────────┐   │
│  │                Service Layer                           │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌────────────┐  │   │
│  │  │   Workflow   │  │   Company    │  │  Contact   │  │   │
│  │  │ Orchestrator │  │  Discovery   │  │   Finder   │  │   │
│  │  └──────┬───────┘  └──────┬───────┘  └─────┬──────┘  │   │
│  │         │                  │                │         │   │
│  │  ┌──────▼───────┐  ┌──────▼───────┐  ┌─────▼──────┐  │   │
│  │  │   Research   │  │    Email     │  │   Storage  │  │   │
│  │  │   Service    │  │  Generation  │  │  (JSON)    │  │   │
│  │  └──────────────┘  └──────────────┘  └────────────┘  │   │
│  └───────────────────────────────────────────────────────┘   │
│                            │                                  │
│  ┌─────────────────────────▼──────────────────────────┐     │
│  │                AI Agent Layer (Agno)                │     │
│  │  • Company Finder  • Researcher  • Contact Finder   │     │
│  │  • Email Generator                                  │     │
│  └─────────────────────────────────────────────────────┘     │
└────────────────────────────┬──────────────────────────────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
         ┌────▼────┐   ┌────▼────┐   ┌────▼────┐
         │ OpenAI  │   │ Exa API │   │  Local  │
         │   API   │   │         │   │ Storage │
         └─────────┘   └─────────┘   └─────────┘
```

### Data Flow

1. **User configures campaign** → Frontend validation → Backend API
2. **Backend orchestrates workflow** → AI agents execute tasks in sequence
3. **Real-time updates** → SSE streams progress to frontend
4. **Results stored** → JSON files in `backend/data/campaigns/`
5. **User views results** → Frontend fetches and displays data

---

## Tech Stack

### Backend

| Technology   | Version | Purpose                                  |
| ------------ | ------- | ---------------------------------------- |
| **FastAPI**  | 0.109+  | High-performance async web framework     |
| **Pydantic** | 2.5+    | Data validation and settings management  |
| **Agno**     | 2.0+    | AI agent orchestration framework         |
| **OpenAI**   | 1.0+    | GPT-4 for intelligent content generation |
| **Exa API**  | Latest  | Neural search for company discovery      |
| **Uvicorn**  | Latest  | ASGI server with auto-reload             |

### Frontend

| Technology          | Version | Purpose                         |
| ------------------- | ------- | ------------------------------- |
| **Next.js**         | 14+     | React framework with App Router |
| **TypeScript**      | 5+      | Type-safe JavaScript            |
| **Tailwind CSS**    | 3+      | Utility-first CSS framework     |
| **Axios**           | Latest  | HTTP client with interceptors   |
| **React Hot Toast** | Latest  | Beautiful notifications         |
| **Lucide React**    | Latest  | Icon library                    |

### Development Tools

- **ESLint** - Code linting
- **Prettier** - Code formatting
- **Git** - Version control

---

## Getting Started

### Prerequisites

```bash
# Required
- Python 3.11+
- Node.js 18+
- npm or yarn
- Git

# API Keys (Required)
- OpenAI API key
- Exa API key
```

### Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/hasnaynajmal/email_gtm_ai_agent.git
cd email_gtm_ai_agent
```

#### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env and add your API keys:
# OPENAI_API_KEY=your_openai_key_here
# EXA_API_KEY=your_exa_key_here
# CORS_ORIGINS=["http://localhost:3000","http://localhost:8000"]
```

#### 3. Frontend Setup

```bash
# Open new terminal and navigate to frontend
cd frontend

# Install dependencies
npm install

# Create .env.local file
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
```

#### 4. Start Development Servers

**Terminal 1 - Backend:**

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**

```bash
cd frontend
npm run dev
```

#### 5. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## Project Structure

```
email_gtm_ai_agent/
├── backend/                      # FastAPI backend
│   ├── app/
│   │   ├── api/                  # API endpoints
│   │   │   └── v1/
│   │   │       ├── endpoints/    # Route handlers
│   │   │       │   ├── campaign.py
│   │   │       │   ├── execution.py
│   │   │       │   ├── health.py
│   │   │       │   └── history.py
│   │   │       └── router.py
│   │   ├── core/                 # Core configuration
│   │   │   ├── config.py         # Settings
│   │   │   ├── exceptions.py     # Custom exceptions
│   │   │   ├── logging.py        # Logging config
│   │   │   └── security.py       # Security utilities
│   │   ├── db/                   # Database layer
│   │   │   ├── init_db.py
│   │   │   └── session.py
│   │   ├── middleware/           # Custom middleware
│   │   │   └── logging.py
│   │   ├── models/               # Data models
│   │   ├── schemas/              # Pydantic schemas
│   │   │   ├── common.py
│   │   │   ├── health.py
│   │   │   └── outreach.py
│   │   ├── services/             # Business logic
│   │   │   ├── company_service.py
│   │   │   ├── contact_service.py
│   │   │   ├── email_service.py
│   │   │   ├── research_service.py
│   │   │   └── workflow_service.py
│   │   ├── utils/                # Utilities
│   │   └── main.py               # Application entry
│   ├── data/                     # Data storage
│   │   └── campaigns/            # Campaign JSON files
│   ├── .env                      # Environment variables
│   ├── requirements.txt          # Python dependencies
│   └── README.md
│
├── frontend/                     # Next.js frontend
│   ├── app/                      # App Router pages
│   │   ├── campaign/
│   │   │   ├── new/              # Campaign configuration
│   │   │   │   └── page.tsx
│   │   │   └── execute/          # Campaign execution
│   │   │       └── page.tsx
│   │   ├── campaigns/
│   │   │   └── [id]/             # Campaign details
│   │   │       └── page.tsx
│   │   ├── history/              # Campaign history
│   │   │   └── page.tsx
│   │   ├── layout.tsx            # Root layout
│   │   ├── page.tsx              # Landing page
│   │   └── globals.css           # Global styles
│   ├── components/               # React components
│   │   ├── campaign/             # Campaign-specific
│   │   │   ├── CampaignHistoryList.tsx
│   │   │   ├── CompanyCard.tsx
│   │   │   ├── ConfigForm.tsx
│   │   │   ├── EmailCard.tsx
│   │   │   ├── ExecutionProgress.tsx
│   │   │   ├── ResultsDisplay.tsx
│   │   │   ├── SenderForm.tsx
│   │   │   ├── StatisticsCards.tsx
│   │   │   └── StepIndicator.tsx
│   │   ├── layout/               # Layout components
│   │   │   └── Header.tsx
│   │   └── ui/                   # Reusable UI
│   │       ├── Badge.tsx
│   │       ├── Button.tsx
│   │       ├── Card.tsx
│   │       ├── Input.tsx
│   │       ├── Loading.tsx
│   │       └── Select.tsx
│   ├── lib/                      # Utilities
│   │   ├── api.ts                # API client
│   │   ├── types.ts              # TypeScript types
│   │   └── utils.ts              # Helper functions
│   ├── .env.local                # Environment variables
│   ├── package.json              # Node dependencies
│   ├── tsconfig.json             # TypeScript config
│   ├── tailwind.config.ts        # Tailwind config
│   └── README.md
│
└── README.md                     # This file
```

---

## API Documentation

### Base URL

```
http://localhost:8000/api/v1
```

### Authentication

Currently no authentication required (add OAuth2/JWT in production)

### Key Endpoints

#### Campaign Configuration

```http
GET /campaign/options
Returns available configuration options

POST /campaign/configure
Body: CampaignConfig
Returns: ValidationResult
```

#### Campaign Execution

```http
POST /execute/campaign
Body: CampaignConfig
Returns: CampaignExecutionResponse

GET /execute/campaign/stream
Query: CampaignConfig (JSON)
Returns: Server-Sent Events stream
```

#### Campaign History

```http
GET /campaigns/history?limit=10&offset=0
Returns: List of campaign summaries

GET /campaigns/{campaign_id}
Returns: Complete campaign details

DELETE /campaigns/{campaign_id}
Deletes a campaign

GET /campaigns/stats/summary
Returns: Aggregate statistics
```

### Request/Response Examples

**POST /campaign/configure**

```json
{
  "category": "AI & ML Solutions",
  "departments": ["Engineering", "Data Science"],
  "service_type": "API Integration",
  "company_size": "Series B",
  "personalization_level": "high",
  "num_companies": 5,
  "sender_name": "John Doe",
  "sender_email": "john@company.com",
  "sender_organization": "TechCorp",
  "service_offering": "AI infrastructure solutions"
}
```

**Response:**

```json
{
  "is_valid": true,
  "message": "Campaign configuration validated successfully",
  "config_summary": {...}
}
```

---

## Frontend Guide

### Pages

#### 1. Landing Page (`/`)

- Hero section with CTA
- Feature highlights
- Quick start button

#### 2. Campaign Configuration (`/campaign/new`)

- **Step 1**: Outreach configuration (category, departments, etc.)
- **Step 2**: Sender details (name, email, organization)
- Form validation and API integration

#### 3. Campaign Execution (`/campaign/execute`)

- Real-time progress tracking
- Live statistics (companies, contacts, emails)
- Results display with company/email cards
- Export functionality

#### 4. Campaign History (`/history`)

- Statistics dashboard
- Filterable campaign list
- Quick actions (view, delete)

#### 5. Campaign Details (`/campaigns/[id]`)

- Full configuration details
- Complete results with all emails
- Export options

### Components

#### UI Components (`components/ui/`)

- **Button**: 5 variants (primary, secondary, outline, ghost, danger)
- **Card**: Composable card with header/content/footer
- **Input/Textarea**: Form inputs with validation states
- **Select/MultiSelect**: Dropdown selectors
- **Badge**: Status indicators
- **Loading**: Spinner component

#### Campaign Components (`components/campaign/`)

- **StepIndicator**: Multi-step form progress
- **ConfigForm**: Campaign configuration form
- **SenderForm**: Sender details form
- **ExecutionProgress**: Real-time progress bar
- **ResultsDisplay**: Campaign results viewer
- **CompanyCard**: Company information display
- **EmailCard**: Generated email display with actions
- **CampaignHistoryList**: Campaign list with filters
- **StatisticsCards**: Metrics dashboard

### Styling

- Tailwind CSS utility-first approach
- Custom color palette (blue primary, gray neutrals)
- Responsive breakpoints (sm, md, lg, xl)
- Dark mode ready (not implemented yet)

---

## Configuration

### Backend Environment Variables

```bash
# .env file in backend/

# API Keys (Required)
OPENAI_API_KEY=sk-your-openai-key
EXA_API_KEY=your-exa-api-key

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True
LOG_LEVEL=INFO

# CORS Settings (JSON array format)
CORS_ORIGINS=["http://localhost:3000","http://localhost:8000"]

# Storage
DATA_DIR=data/campaigns

# AI Model Configuration
OPENAI_MODEL=gpt-4
TEMPERATURE=0.7
MAX_TOKENS=2000
```

### Frontend Environment Variables

```bash
# .env.local file in frontend/

# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000

# Optional: Analytics, Error Tracking
# NEXT_PUBLIC_GA_ID=your-ga-id
# NEXT_PUBLIC_SENTRY_DSN=your-sentry-dsn
```

---

## Development

### Backend Development

```bash
# Run with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run tests (if implemented)
pytest

# Format code
black app/
isort app/

# Type checking
mypy app/
```

### Frontend Development

```bash
# Development server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Lint code
npm run lint

# Format code
npm run format
```

### Adding New Features

#### Backend: Add New Endpoint

1. Create route handler in `app/api/v1/endpoints/`
2. Add Pydantic schemas in `app/schemas/`
3. Implement business logic in `app/services/`
4. Register route in `app/api/v1/router.py`

#### Frontend: Add New Page

1. Create page component in `app/[route]/page.tsx`
2. Add API function in `lib/api.ts`
3. Define TypeScript types in `lib/types.ts`
4. Create reusable components in `components/`

---

## Deployment

### Docker Deployment (Recommended)

**Backend Dockerfile:**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Frontend Dockerfile:**

```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

CMD ["npm", "start"]
```

**docker-compose.yml:**

```yaml
version: "3.8"

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - EXA_API_KEY=${EXA_API_KEY}
    volumes:
      - ./backend/data:/app/data

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://backend:8000
    depends_on:
      - backend
```

### Cloud Deployment

#### Vercel (Frontend)

```bash
cd frontend
vercel deploy --prod
```

#### Railway/Render (Backend)

- Connect GitHub repository
- Set environment variables
- Deploy with automatic builds

#### AWS/GCP/Azure

- Use Docker containers
- Set up load balancers
- Configure environment variables
- Enable auto-scaling

---

## Troubleshooting

### Common Issues

#### CORS Errors

```
Error: CORS policy blocked
```

**Solution**: Ensure `CORS_ORIGINS` in backend `.env` includes frontend URL in JSON array format:

```bash
CORS_ORIGINS=["http://localhost:3000","http://localhost:8000"]
```

#### API Connection Failed

```
Error: Network Error / ECONNREFUSED
```

**Solution**:

1. Verify backend is running on port 8000
2. Check `NEXT_PUBLIC_API_URL` in frontend `.env.local`
3. Ensure no firewall blocking ports

#### Company Parsing Issues

```
WARNING: Parsed 0 companies from response
```

**Solution**:

- AI agent response format changed - check `company_service.py` parsing logic
- Verify OpenAI API key is valid
- Check Exa API quota

#### SSE Stream Not Working

```
EventSource failed / Stream disconnected
```

**Solution**:

1. Check network tab for errors
2. Verify backend `/execute/campaign/stream` endpoint
3. Increase request timeout in API client

#### Type Errors in Frontend

```
Type 'any' is not assignable
```

**Solution**: Run `npm run lint` and fix TypeScript errors with proper types

### Logs

**Backend logs:**

```bash
# In backend terminal - INFO/WARNING/ERROR messages
# Check for API call traces, agent execution, parsing issues
```

**Frontend logs:**

```bash
# Browser console - Network tab for API calls
# Check for failed requests, CORS issues, SSE streams
```

---

## License

This project is private and proprietary.

---

## Author

**Hasnay Najmal**

- GitHub: [@hasnaynajmal](https://github.com/hasnaynajmal)
- Repository: [email_gtm_ai_agent](https://github.com/hasnaynajmal/email_gtm_ai_agent)

---

## Acknowledgments

- **FastAPI** for the amazing web framework
- **Next.js** team for the React framework
- **OpenAI** for GPT-4 API
- **Exa** for neural search capabilities
- **Agno** for AI agent orchestration

---

## Roadmap

### Phase 1: Core Features

- [x] Company discovery
- [x] Research automation
- [x] Contact finding
- [x] Email generation
- [x] Campaign management

### Phase 2: Enhancements

- [ ] Email sending integration (SendGrid/AWS SES)
- [ ] A/B testing for email variations
- [ ] Response tracking and analytics
- [ ] CRM integration (Salesforce, HubSpot)
- [ ] Team collaboration features

### Phase 3: Advanced Features

- [ ] Machine learning for email optimization
- [ ] Multi-language support
- [ ] Custom AI model fine-tuning
- [ ] Webhook integrations
- [ ] Mobile app

---

## Support

For issues, questions, or contributions:

1. Check [Troubleshooting](#troubleshooting) section
2. Review [API Documentation](#api-documentation)
3. Open an issue on GitHub
4. Contact: hasnay@example.com

---

**Made with AI-powered automation**
