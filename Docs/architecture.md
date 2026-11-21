# Architecture

## Current (Phase 0-1)

Client --> Django REST Framework (runserver) --> PostgreSQL

## Target (Phase 4+)

Client --> Nginx --> Gunicorn --> Django REST Framework --+--> PostgreSQL
+--> Redis
