# CloudCRUD

**An end-to-end backend engineering and DevOps project: from a Django REST API to a monitored, automated deployment on Google Cloud.**

CloudCRUD is a deliberately simple Product Management REST API. The application itself is not the point. The goal is to practice and document the **complete lifecycle of a backend service**: developing, containerizing, automating, deploying, monitoring, securing, and maintaining it.

> **Status:** Phase 0 (project setup) and Phase 1 (backend API) are complete. Later phases are planned. See the [Roadmap](#roadmap).

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Configuration](#configuration)
- [API Reference](#api-reference)
- [Testing](#testing)
- [Roadmap](#roadmap)
- [Design Decisions](#design-decisions)
- [Learning Approach](#learning-approach)
- [Author](#author)

---

## Features

**Implemented**

- RESTful CRUD API for products built with Django REST Framework and function-based views
- PostgreSQL persistence with Django ORM and versioned migrations
- UUID primary keys and `Decimal`-based pricing
- Request validation at the field and model level
- Consistent JSON error format across all failure types
- Paginated list endpoint
- Liveness and readiness health endpoints
- Structured (JSON) logging to stdout
- Interactive OpenAPI documentation (Swagger UI) via drf-spectacular
- Environment-based configuration (no secrets in code)
- Automated unit and integration tests with pytest

**Planned:** Redis caching, Gunicorn and Nginx, Docker and Docker Compose, CI/CD with GitHub Actions, Kubernetes and Helm, Terraform on GCP, Prometheus, Grafana, OpenTelemetry, and security hardening.

---

## Tech Stack

| Category | Technology | Status |
|---|---|---|
| Language | Python | Active |
| Framework | Django, Django REST Framework | Active |
| Database | PostgreSQL | Active |
| API Docs | drf-spectacular (OpenAPI 3) | Active |
| Testing | pytest, pytest-django | Active |
| Cache | Redis | Planned |
| App Server / Proxy | Gunicorn, Nginx | Planned |
| Containers | Docker, Docker Compose | Planned |
| CI/CD | GitHub Actions, Google Artifact Registry | Planned |
| Orchestration | Kubernetes, Helm | Planned |
| Infrastructure as Code | Terraform | Planned |
| Cloud | Google Cloud Platform (GKE, optional Cloud SQL) | Planned |
| Monitoring | Prometheus, Grafana, OpenTelemetry | Planned |

---

## Architecture

**Current (Phases 0-1)**

```text
Client ──> Django REST Framework (runserver) ──> PostgreSQL
```

**Target (Phase 4 onward)**

```text
Client
  │
  ▼
Nginx (reverse proxy)
  │
  ▼
Gunicorn
  │
  ▼
Django REST Framework ──┬──> PostgreSQL
                        └──> Redis
```

More detail lives in [`docs/architecture.md`](docs/architecture.md).

---

## Project Structure

```text
CloudCRUD/
├── config/              # Django project: settings, root URLs, health views, error handler, logging
├── products/            # Products app: model, serializer, views, URLs
├── tests/               # pytest test suite
├── docs/                # Project documentation
├── docker/              # Docker assets (planned)
├── nginx/               # Nginx configuration (planned)
├── kubernetes/          # Kubernetes manifests (planned)
├── helm/                # Helm chart (planned)
├── terraform/           # Infrastructure as Code (planned)
├── monitoring/          # Prometheus and Grafana configuration (planned)
├── .github/             # GitHub Actions workflows (planned)
├── manage.py
├── pytest.ini
├── requirements.txt         # Runtime dependencies
├── requirements-dev.txt     # Development and test dependencies
├── .env.example
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.12 or newer
- PostgreSQL 14 or newer
- Git

### 1. Clone and create a virtual environment

```bash
git clone https://github.com/<your-username>/CloudCRUD.git
cd CloudCRUD

python -m venv .venv
source .venv/bin/activate          # Windows PowerShell: .venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```bash
pip install -r requirements-dev.txt
```

### 3. Set up PostgreSQL

Connect with `psql` as a superuser and run:

```sql
CREATE USER cloudcrud WITH PASSWORD 'cloudcrud';
CREATE DATABASE cloudcrud OWNER cloudcrud;
ALTER USER cloudcrud CREATEDB;   -- required so pytest can create its test database
```

> These credentials are for local development only. Use strong, unique credentials anywhere else.

### 4. Configure the environment

```bash
cp .env.example .env
```

Edit `.env` and set a real `SECRET_KEY`. To generate one:

```bash
python -c "from django.core.management.utils import get_random_secret_key as k; print(k())"
```

### 5. Migrate and run

```bash
python manage.py migrate
python manage.py runserver
```

The API is now available at `http://localhost:8000`. Open **`http://localhost:8000/api/docs/`** for the interactive Swagger UI.

Optional: create an admin user with `python manage.py createsuperuser` and visit `/admin/`.

---

## Configuration

All configuration is read from environment variables (or a local `.env` file). Never commit `.env`.

| Variable | Description | Example |
|---|---|---|
| `SECRET_KEY` | Django secret key (required) | `<long random string>` |
| `DEBUG` | Enable debug mode. Must be `False` in production | `True` |
| `ALLOWED_HOSTS` | Comma-separated list of allowed hosts | `localhost,127.0.0.1` |
| `DB_NAME` | PostgreSQL database name | `cloudcrud` |
| `DB_USER` | PostgreSQL user | `cloudcrud` |
| `DB_PASSWORD` | PostgreSQL password | `cloudcrud` |
| `DB_HOST` | PostgreSQL host | `localhost` |
| `DB_PORT` | PostgreSQL port | `5432` |

---

## API Reference

Interactive documentation: `/api/docs/` (Swagger UI) and `/api/schema/` (raw OpenAPI schema).

### Product

| Field | Type | Notes |
|---|---|---|
| `id` | UUID | Read-only, generated by the server |
| `name` | string | Required, at least 3 characters |
| `description` | text | Optional |
| `price` | decimal | Required, must be `>= 0`, up to 2 decimal places |
| `stock` | integer | Must be `>= 0`, defaults to `0` |
| `created_at` | datetime | Read-only |
| `updated_at` | datetime | Read-only |

### Endpoints

| Method | Endpoint | Description | Success |
|---|---|---|---|
| `GET` | `/api/products/` | List products (paginated, `?page=N`) | `200` |
| `POST` | `/api/products/` | Create a product | `201` |
| `GET` | `/api/products/{id}/` | Retrieve a product | `200` |
| `PUT` | `/api/products/{id}/` | Replace a product (all fields required) | `200` |
| `DELETE` | `/api/products/{id}/` | Delete a product | `204` |
| `GET` | `/health/` | General health | `200` |
| `GET` | `/health/live/` | Liveness: the process is running | `200` |
| `GET` | `/health/ready/` | Readiness: dependencies are reachable | `200` / `503` |

### Example

```bash
curl -X POST http://localhost:8000/api/products/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Mechanical Keyboard", "description": "Hot-swappable", "price": "49.90", "stock": 10}'
```

```json
{
  "id": "3f6c7c3e-8b5a-4f0e-9d1a-2b7e6c1a9f10",
  "name": "Mechanical Keyboard",
  "description": "Hot-swappable",
  "price": "49.90",
  "stock": 10,
  "created_at": "2026-11-21T10:15:30.123456Z",
  "updated_at": "2026-11-21T10:15:30.123456Z"
}
```

### Paginated list format

```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [ { "id": "...", "name": "..." } ]
}
```

### Error format

Every error returned by the API uses the same structure:

```json
{
  "error": {
    "code": "validation_error",
    "message": "Invalid request data.",
    "details": {
      "price": ["Ensure this value is greater than or equal to 0.00."]
    }
  }
}
```

| HTTP status | `code` |
|---|---|
| 400 | `validation_error` |
| 404 | `not_found` |
| 405 | `method_not_allowed` |
| 500 | `server_error` (details are logged, never exposed) |

---

## Testing

```bash
pytest -v
```

The suite covers every CRUD endpoint, validation failures, 404 handling, error response format, and the health endpoints. Tests run against a temporary PostgreSQL database that is created and destroyed automatically.

---

## Roadmap

| Phase | Focus | Status |
|---|---|---|
| 0 | Project initialization and planning | Done |
| 1 | Backend API development (Django REST Framework, PostgreSQL, tests) | Done |
| 2 | Docker and containerization | Planned |
| 3 | Docker Compose, PostgreSQL, and Redis caching | Planned |
| 4 | Gunicorn and Nginx reverse proxy | Planned |
| 5 | CI pipeline with GitHub Actions | Planned |
| 6 | Kubernetes fundamentals and local deployment | Planned |
| 7 | Helm | Planned |
| 8 | Infrastructure as Code with Terraform | Planned |
| 9 | Google Cloud Platform deployment | Planned |
| 10 | Continuous deployment (CD) | Planned |
| 11 | Monitoring and observability | Planned |
| 12 | Security and production hardening | Planned |
| 13 | Final documentation and portfolio | Planned |

---

## Design Decisions

- **Function-based views over `ModelViewSet`.** Each request flow is explicit and easy to trace, which suits a learning project. Refactoring to viewsets and routers is a possible later exercise.
- **`Decimal` for money.** Floating-point rounding errors are unacceptable for prices.
- **UUID primary keys.** Identifiers are not guessable or sequential.
- **Uniform error envelope.** Clients handle a single error structure, and unexpected exceptions never leak internals.
- **Separate liveness and readiness endpoints.** They map directly onto Kubernetes probes in Phase 6.
- **JSON logs on stdout.** This is the standard contract for containerized applications and centralized log collection.
- **Configuration through environment variables.** The same codebase runs locally, in containers, and in the cloud.

---

## Learning Approach

Each phase follows the same workflow: **learn first**, **implement independently**, then **verify** before moving on. Problems encountered and lessons learned are documented along the way in [`docs/`](docs/).

---

## Author

**Haikal Fikri**, Software Engineer based in Batam, Indonesia.

GitHub: [`<your-username>`](https://github.com/<your-username>)
