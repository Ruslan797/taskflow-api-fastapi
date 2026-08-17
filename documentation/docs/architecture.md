# Architecture

TaskFlow API follows a layered architecture designed to separate HTTP handling, business logic, and database access.

## Request Flow

A typical request passes through the following layers:

```text
Client
  ↓
HTTP Request
  ↓
FastAPI Router
  ↓
Dependencies
  ↓
Service Layer
  ↓
Repository Layer
  ↓
SQLAlchemy Session
  ↓
PostgreSQL
```