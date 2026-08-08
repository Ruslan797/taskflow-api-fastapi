# TaskFlow API

TaskFlow API is a production-style REST API for task management built with **FastAPI**.

The project is designed as a portfolio backend application demonstrating modern backend development practices, including layered architecture, JWT authentication, authorization, dependency injection, and PostgreSQL integration.

---

# Features

## Authentication

- User registration
- User login
- JWT authentication
- Password hashing with bcrypt
- Protected API endpoints

## Authorization

- Users can access only their own tasks
- Users can access only their own subtasks
- Authorization implemented with reusable FastAPI dependencies

## Tasks

- Create task
- Get all user tasks
- Get task by ID
- Update task
- Delete task

## Subtasks

- Create subtask
- Get all subtasks
- Get subtask by ID
- Update subtask
- Delete subtask

## Database

- PostgreSQL
- SQLAlchemy 2.0 ORM
- Alembic migrations

---

# Tech Stack

- Python 3.13
- FastAPI
- PostgreSQL
- SQLAlchemy 2.0
- Alembic
- Pydantic v2
- JWT
- Passlib (bcrypt)
- Docker
- Uvicorn

---

# Project Structure

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

---

# API Endpoints

## Authentication

| Method | Endpoint |
|--------|----------|
| POST | `/auth/register` |
| POST | `/auth/login` |

---

## Tasks

| Method | Endpoint |
|--------|----------|
| POST | `/tasks` |
| GET | `/tasks` |
| GET | `/tasks/{task_id}` |
| PATCH | `/tasks/{task_id}` |
| DELETE | `/tasks/{task_id}` |

---

## Subtasks

| Method | Endpoint |
|--------|----------|
| POST | `/tasks/{task_id}/subtasks` |
| GET | `/tasks/{task_id}/subtasks` |
| GET | `/tasks/{task_id}/subtasks/{subtask_id}` |
| PATCH | `/tasks/{task_id}/subtasks/{subtask_id}` |
| DELETE | `/tasks/{task_id}/subtasks/{subtask_id}` |

---

# Local Installation

Clone the repository:

```bash
git clone git@github.com:Ruslan797/taskflow-api-fastapi.git
cd taskflow-api-fastapi
```

Create a virtual environment:

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

---

# Environment Variables

Create a `.env` file.

Example:

```env
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/taskflow

SECRET_KEY=your_secret_key

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

# Database

Start PostgreSQL:

```bash
docker compose up -d
```

Run migrations:

```bash
alembic upgrade head
```

---

# Run

```bash
uvicorn app.main:app --reload
```

Application:

```
http://127.0.0.1:8000
```

Swagger:

```
http://127.0.0.1:8000/docs
```

ReDoc:

```
http://127.0.0.1:8000/redoc
```

---

# Architecture

Current architecture:

- Router Layer
- Service Layer
- Dependency Injection
- SQLAlchemy ORM
- JWT Authentication
- Authorization Dependencies

---

# Current Status

Implemented:

- JWT Authentication
- User Registration
- User Login
- Task CRUD
- Subtask CRUD
- Ownership Authorization
- Dependency Injection Refactoring
- Alembic Migrations
- PostgreSQL Integration

---

# Roadmap

Planned improvements:

- Repository Layer
- Generic CRUD Repository
- Pagination
- Filtering
- Sorting
- Projects
- Tags
- Docker Production Setup
- Automated Testing (Pytest)
- GitHub Actions (CI/CD)
- Logging
- Redis
- Background Tasks
- Celery
- API Versioning

---

# License

This project is created for educational and portfolio purposes.
