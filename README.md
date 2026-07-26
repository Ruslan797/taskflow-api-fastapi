# TaskFlow API

TaskFlow API is a REST API for managing tasks and subtasks.

The project is built with FastAPI, PostgreSQL, SQLAlchemy 2.0, Pydantic v2, Alembic, and Docker.

## Features

- Create, read, update, and delete tasks
- Create, read, update, and delete subtasks
- One-to-many relationship between tasks and subtasks
- PostgreSQL database
- Database migrations with Alembic
- Request validation and response serialization with Pydantic
- Service-layer architecture
- Automatic API documentation with Swagger UI

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy 2.0
- Alembic
- Pydantic v2
- Docker

## Project Structure

```text
app/
├── core/
├── database/
├── models/
├── routers/
├── schemas/
├── services/
└── main.py

alembic/
├── versions/
└── env.py
```

## API Endpoints

### Tasks

| Method | Endpoint | Description |
|---|---|---|
| POST | `/tasks` | Create a task |
| GET | `/tasks` | Get all tasks |
| GET | `/tasks/{task_id}` | Get a task |
| PATCH | `/tasks/{task_id}` | Update a task |
| DELETE | `/tasks/{task_id}` | Delete a task |

### Subtasks

| Method | Endpoint | Description |
|---|---|---|
| POST | `/tasks/{task_id}/subtasks` | Create a subtask |
| GET | `/tasks/{task_id}/subtasks` | Get all subtasks for a task |
| GET | `/tasks/{task_id}/subtasks/{subtask_id}` | Get a subtask |
| PATCH | `/tasks/{task_id}/subtasks/{subtask_id}` | Update a subtask |
| DELETE | `/tasks/{task_id}/subtasks/{subtask_id}` | Delete a subtask |

## Local Installation

Clone the repository:

```bash
git clone git@github.com:Ruslan797/taskflow-api-fastapi.git
cd taskflow-api-fastapi
```

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root.

Example:

```env
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/taskflow
```

Do not commit the real `.env` file.

## Database

Start PostgreSQL:

```bash
docker compose up -d
```

Apply database migrations:

```bash
alembic upgrade head
```

## Run the Application

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

## Development Status

The current version includes task and subtask management.

Planned features:

- User authentication
- JWT access tokens
- Projects
- Task ownership
- Filtering and pagination
- Automated tests
- CI/CD
- Production deployment