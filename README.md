# syncd

A mobile app backend built with **FastAPI** and **PostgreSQL**.

## Features

- **JWT authentication** – register, login, and secure all endpoints with Bearer tokens
- **User management** – create, read, update, and delete your account
- **Event / schedule sync** – full CRUD for events with an `is_synced` flag for mobile sync state
- **Auto-generated API docs** – Swagger UI and ReDoc included out of the box

## Tech stack

| Layer | Technology |
|-------|-----------|
| API framework | FastAPI |
| Database | PostgreSQL 16 |
| ORM | SQLAlchemy 2 |
| Auth | JWT (python-jose + passlib/bcrypt) |
| Container | Docker / Docker Compose |

## Quick start (Docker)

```bash
# 1. Copy environment file
cp .env.example .env

# 2. Start services
docker compose up --build
```

The API will be available at <http://localhost:8000>.
Interactive docs: <http://localhost:8000/api/v1/docs>

## Running locally (without Docker)

```bash
cd backend
pip install -r requirements.txt
# set DATABASE_URL and SECRET_KEY in your environment or a .env file
uvicorn app.main:app --reload
```

## API endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Health check |
| `POST` | `/api/v1/users/register` | Register a new user |
| `POST` | `/api/v1/auth/login` | Obtain a JWT access token |
| `GET` | `/api/v1/users/me` | Get current user profile |
| `PUT` | `/api/v1/users/me` | Update current user profile |
| `DELETE` | `/api/v1/users/me` | Delete account |
| `GET` | `/api/v1/events/` | List all events for current user |
| `POST` | `/api/v1/events/` | Create a new event |
| `GET` | `/api/v1/events/{id}` | Get a single event |
| `PUT` | `/api/v1/events/{id}` | Update an event |
| `DELETE` | `/api/v1/events/{id}` | Delete an event |

## Running tests

```bash
cd backend
pip install -r requirements.txt pytest httpx
pytest tests/ -v
```

## Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `POSTGRES_USER` | `postgres` | Database user |
| `POSTGRES_PASSWORD` | `password` | Database password |
| `POSTGRES_DB` | `syncd` | Database name |
| `SECRET_KEY` | `changethissecretkey` | JWT signing secret (change in production!) |
