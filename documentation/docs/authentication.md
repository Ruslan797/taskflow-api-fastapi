# Authentication

TaskFlow API uses JWT-based authentication to identify users and protect private resources.

## Authentication Flow

```text
Client
  ↓
POST /auth/login
  ↓
User credentials
  ↓
Password verification
  ↓
JWT access token
  ↓
Client stores token
  ↓
Authorization: Bearer <token>
  ↓
Protected endpoint
  ↓
get_current_user
  ↓
JWT validation
  ↓
Current User
```

## Registration

A new user can create an account using the registration endpoint.

```http
POST /auth/register
```

The password is never stored in the database as plain text. Before the user is saved, the password is hashed.

## Login

The client sends user credentials to:

```http
POST /auth/login
```

After successful authentication, the API returns a JWT access token.

## Bearer Token

Protected requests include the access token in the HTTP `Authorization` header:

```http
Authorization: Bearer <access_token>
```

FastAPI extracts the token using the authentication dependency.

## Current User

Protected endpoints use the `get_current_user` dependency.

Conceptually:

```text
HTTP Request
    ↓
Authorization header
    ↓
OAuth2 dependency
    ↓
JWT token
    ↓
JWT validation
    ↓
user_id
    ↓
Database
    ↓
User ORM object
    ↓
current_user
```

This allows route handlers to work with an authenticated `User` object instead of manually parsing and validating the JWT token.

## Authorization

Authentication answers:

> Who is the user?

Authorization answers:

> Is this user allowed to access this resource?

TaskFlow restricts tasks and subtasks to their owners.

For example, a user cannot access a task owned by another user.

Resource ownership checks are implemented using reusable FastAPI dependencies.