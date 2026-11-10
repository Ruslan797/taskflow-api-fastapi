# TaskFlow API — Python Backend with an AI Agent

Portfolio backend application for task management, built with FastAPI,
PostgreSQL and SQLAlchemy.

The project combines authenticated REST endpoints with a Gemini-powered
AI agent that manages the current user's tasks through backend services.

## Project Status

Active development. The core task-management backend and initial
AI-agent integration are implemented.

This is a portfolio project, not a production-ready service.

## Implemented Features

### Authentication and Authorization

- User registration and login
- JWT access tokens
- Password hashing with pwdlib and Argon2
- Authenticated user profile
- Ownership checks for tasks and subtasks

### Task Management

- Create, list, retrieve, update and delete tasks
- Create, list, retrieve, update and delete subtasks
- User-specific task lists
- PostgreSQL persistence
- Database migrations with Alembic

### AI Agent

- Authenticated chat endpoint: `POST /ai/chat`
- Gemini integration through the Google Gen AI SDK
- Tool calling for listing, creating, updating and deleting tasks
- Reuse of existing backend services
- Ownership checks in task update and delete tools
- Limited in-memory conversation history per user
- Request timeouts and a maximum number of agent steps

The AI integration is still being developed. Conversation history is
not persistent and is not shared between application processes.

#### Token Usage Logging

- Counts conversation tokens before starting the agent loop
- Logs input, output and total token usage for each model response
- Continues processing if the preliminary token count times out
  or encounters a server error

Usage is currently logged per model call. Separate thinking-token
logging and cumulative totals across all agent steps are not yet
implemented.

### Engineering

- Router and service layers
- Repository layer for task persistence
- Dependency injection
- Pydantic request and response schemas
- Database health endpoint
- Initial automated health-check tests

## Technology Stack

- Python
- FastAPI
- Pydantic v2
- PostgreSQL
- SQLAlchemy 2.0
- Alembic
- JWT / python-jose
- pwdlib / Argon2
- Google Gen AI SDK
- Docker Compose for local PostgreSQL
- Pytest

## Architecture

REST requests follow this structure:

`Router → Service → Repository / SQLAlchemy → PostgreSQL`

The task service uses a dedicated repository. User and subtask services
currently access SQLAlchemy directly.

The AI agent calls backend tools that reuse the task service.
The authenticated user's ID is supplied by the backend.

## Project Structure

```text
app/
├── ai_agent/       # Gemini client, agent loop, tools and chat endpoint
├── core/           # Configuration, authentication and dependencies
├── database/       # Database engine and sessions
├── models/         # SQLAlchemy models
├── repositories/   # Task persistence
├── routers/        # REST endpoints
├── schemas/        # Pydantic schemas
├── services/       # Application logic
└── main.py

alembic/            # Database migrations
documentation/     # Additional project documentation
frontend/          # Frontend files
tests/             # Initial health-check tests
docker-compose.yml # Local PostgreSQL service
requirements.txt
```

Project-related models and a migration exist, but project management
is not yet exposed through an implemented API.

## Local Setup

### Prerequisites

- Python with virtual environment support
- Docker with Docker Compose
- A Gemini API key
- An OpenAI API key while the current client initialization requires it

The current agent uses Gemini. An OpenAI client is also initialized
by the application, although it is not used by the agent loop.

### 1. Clone the Repository

```bash
git clone https://github.com/Ruslan797/taskflow-api-fastapi.git
cd taskflow-api-fastapi
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Linux / macOS:

```bash
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

For the current health-check tests, also install:

```bash
python -m pip install pytest httpx
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```dotenv
DATABASE_URL=postgresql+psycopg2://taskflow_user:taskflow_password@localhost:5432/taskflow_db
SECRET_KEY=replace_with_a_long_random_secret
GEMINI_API_KEY=your_gemini_api_key
OPENAI_API_KEY=your_openai_api_key
```

Never commit real credentials or the `.env` file.

The database credentials above match the local development
Docker Compose configuration. Do not use them for production.

The JWT algorithm and token lifetime are currently configured
in `app/core/auth.py`.

### 5. Start PostgreSQL

```bash
docker compose up -d
```

Docker Compose currently starts only PostgreSQL.
The FastAPI application runs separately in the local Python environment.

### 6. Apply Migrations

```bash
alembic upgrade head
```

### 7. Start the API

```bash
uvicorn app.main:app --reload
```

- API: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## API Endpoints

### Authentication

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/auth/register` | Register a user |
| POST | `/auth/login` | Log in and receive an access token |
| GET | `/auth/me` | Retrieve the authenticated user |

Login accepts a JSON body containing `email` and `password`.
Protected endpoints require:

```http
Authorization: Bearer <access_token>
```

### Tasks

| Method | Endpoint |
|--------|----------|
| POST | `/tasks` |
| GET | `/tasks` |
| GET | `/tasks/{task_id}` |
| PATCH | `/tasks/{task_id}` |
| DELETE | `/tasks/{task_id}` |

### Subtasks

| Method | Endpoint |
|--------|----------|
| POST | `/tasks/{task_id}/subtasks` |
| GET | `/tasks/{task_id}/subtasks` |
| GET | `/tasks/{task_id}/subtasks/{subtask_id}` |
| PATCH | `/tasks/{task_id}/subtasks/{subtask_id}` |
| DELETE | `/tasks/{task_id}/subtasks/{subtask_id}` |

### AI and Health

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/ai/chat` | Send a message to the task-management agent |
| GET | `/health` | Check API and database availability |

Example AI request:

```json
{
  "message": "Create a task called Prepare for my technical interview."
}
```

Task data needed for tool calling may be sent to the external
AI provider. Use synthetic data for public demonstrations.

## Testing

With the environment configured and PostgreSQL running:

```bash
python -m pytest tests -v
```

Current automated tests cover:

- Successful database health check
- Database-unavailable response

Authentication, task CRUD, ownership isolation and AI-tool tests
are planned.

## Next Steps

- Make AI configuration optional for non-AI backend usage
- Improve handling of empty model responses and multiple tool calls
- Validate tool arguments and handle tool execution errors
- Add authentication, CRUD and ownership-isolation tests
- Add mocked AI-agent tests
- Add pagination and filtering
- Complete the project-management API
- Containerize the FastAPI application
- Add continuous integration
- Improve deployment configuration and operational logging



## Author

Ruslan Buievskyi

GitHub: https://github.com/Ruslan797