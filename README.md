# Flask + PostgreSQL with Docker Compose


This is a small Flask API and PostgreSQL database together with one command. The API reports service health and lets you create and list notes. Compose waits for the database health check before starting the API, and a named volume keeps database files across container restarts.

## Stack

- Python 3.12 and Flask
- PostgreSQL 16
- Docker Compose with service health checks and dependency ordering
- Environment-based configuration and persistent database volume

## Start

Install Docker Desktop (or Docker Engine with the Compose plugin), then run from this directory:

```bash
docker compose up --build
```

The API is available at `http://localhost:8000`. To stop the services, press `Ctrl+C`, then run `docker compose down`. Data remains in the named volume. To remove the volume and its data too, run `docker compose down -v`.

## Try the API

```bash
curl http://localhost:8000/health
curl http://localhost:8000/notes
curl -X POST http://localhost:8000/notes \
  -H 'Content-Type: application/json' \
  -d '{"text":"My first Compose note"}'
```

`GET /health` returns an application status and database connectivity. `GET /notes` lists saved notes. `POST /notes` creates one; send JSON with a non-empty `text` field (up to 500 characters).

## Configuration

Copy `.env.example` to `.env` to customize local credentials and the published port. Defaults are for local demonstration only; replace them before using this setup in a real deployment. `.env` is ignored by Git.

## Project layout

```text
.
├── app.py
├── compose.yaml
├── Dockerfile
├── requirements.txt
└── .env.example
```

## What this demonstrates

- Building an application image from a Dockerfile
- Connecting application and database services on a Compose network
- Waiting for a database health check before starting the application
- Keeping database data in a named volume
- Reading configuration from environment variables
- Checking application health through an HTTP endpoint

This sample is intentionally small and is not hardened for production. A production deployment should use managed secrets, TLS, backup and restore procedures, migration tooling, and appropriate network and access controls.
