# OCR Benchmark & Document Intelligence Lab (OCRDIL)

A production-grade OCR benchmarking platform for researchers, enterprises, and the open-source community.

**Current version:** v0.2 — Core OCR Pipeline

## Stack

| Layer      | Technology              |
|------------|-------------------------|
| API        | FastAPI (Python 3.11+)  |
| Database   | PostgreSQL 16           |
| Task queue | Celery + Redis           |
| Frontend   | React + Vite (v1.1)     |
| Infra      | Docker Compose          |

## Project structure

```
OCR/
├── backend/     FastAPI application
├── frontend/    Web UI (v1.1)
├── infra/       Deployment configs
├── docs/        Documentation
└── docker-compose.yml
```

## Getting started

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and Docker Compose
- (Optional) Python 3.11+ for local development without Docker

### Quick start (Docker)

1. Clone the repository and enter the project directory:

   ```bash
   git clone <repository-url>
   cd OCR
   ```

2. Copy the environment template:

   ```bash
   cp .env.example .env
   ```

3. Start all services:

   ```bash
   docker compose up --build
   ```

4. Verify the API is healthy:

   ```bash
   curl http://localhost:8000/health
   ```

   Expected response:

   ```json
   {
     "status": "healthy",
     "service": "OCRDIL",
     "version": "0.1.0",
     "timestamp": "2026-06-27T12:00:00+00:00"
   }
   ```

Services will be available at:

| Service  | URL                        |
|----------|----------------------------|
| API      | http://localhost:8000      |
| API docs | http://localhost:8000/docs |
| Postgres | localhost:5432             |
| Redis    | localhost:6379             |

### Local development (without Docker)

```bash
cd backend
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

pip install -e ".[dev]"
uvicorn app.main:app --reload
```

Run tests:

```bash
cd backend
pytest -v
```

Run linters:

```bash
cd backend
ruff check .
black --check .
mypy app
```

### Pre-commit hooks

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

## API

### `GET /health`

Returns service health status, version, and timestamp.

### `POST /api/v1/documents/upload`

Upload a document (PDF, PNG, JPEG, TIFF) for OCR processing. Returns `202 Accepted` and queues a Celery job that runs **Tesseract**, **EasyOCR**, and **PaddleOCR** in parallel.

```bash
curl -X POST http://localhost:8000/api/v1/documents/upload \
  -F "file=@scan.pdf"
```

### `GET /api/v1/documents/{id}`

Get document status and OCR results from all engines.

### `GET /api/v1/documents`

List uploaded documents.

## Roadmap

| Phase | Versions | Focus                                      |
|-------|----------|--------------------------------------------|
| 1     | v0.1–v0.3 | Foundation: OCR pipeline + evaluation     |
| 2     | v1.0–v1.3 | Platform: auth, UI, engines, post-processing |
| 3     | v2.0–v2.3 | Intelligence: metrics, annotation, datasets |
| 4     | v3.0–v3.4 | Scale: K8s, observability, multi-tenancy  |
| 5     | v4.0–v5.0 | Ecosystem: fine-tuning, SDK, GA release    |

See [plan.md](plan.md) for the full project plan.

## License

TBD
