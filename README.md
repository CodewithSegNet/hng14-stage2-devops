# DevOps Stage 2 — Job Processing Microservices

A containerized job processing system with three services: a Node.js frontend, a Python/FastAPI API, a Python worker, and Redis for queueing.

## Architecture

```
┌────────────┐     ┌────────────┐     ┌────────────┐
│  Frontend  │────▶│    API     │────▶│   Redis    │
│  (Node.js) │     │  (FastAPI) │     │            │
│  :3000     │     │  :8000     │     │  :6379     │
└────────────┘     └────────────┘     └────────────┘
                                            │
                                      ┌─────┴──────┐
                                      │   Worker    │
                                      │  (Python)   │
                                      └────────────┘
```

- **Frontend** — Web UI where users submit and track jobs
- **API** — Creates jobs, pushes them to Redis, serves status updates
- **Worker** — Polls Redis for jobs, processes them, updates status
- **Redis** — Shared queue and state store

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) (v20.10+)
- [Docker Compose](https://docs.docker.com/compose/install/) (v2.0+)
- Git

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/CodewithSegNet/hng14-stage2-devops.git
cd hng14-stage2-devops
```

### 2. Create environment file

```bash
cp .env.example .env
```

Edit `.env` if you need to customize any values (defaults work out of the box).

### 3. Start the stack

```bash
docker compose up --build -d
```

### 4. Verify all services are running and healthy

```bash
docker compose ps
```

You should see all four services (`redis`, `api`, `worker`, `frontend`) with status `Up (healthy)`.

### 5. Test the application

Check the API health endpoint:

```bash
curl http://localhost:8000/health
# Expected: {"status":"ok"}
```

Submit a job through the frontend:

```bash
curl -X POST http://localhost:3000/submit
# Expected: {"job_id":"<uuid>"}
```

Check job status (replace `<job_id>` with actual ID):

```bash
curl http://localhost:3000/status/<job_id>
# Expected: {"job_id":"<uuid>","status":"completed"} (after ~2 seconds)
```

Open the web dashboard at [http://localhost:3000](http://localhost:3000).

### 6. Stop the stack

```bash
docker compose down -v
```

## What a Successful Startup Looks Like

```
$ docker compose up --build -d
[+] Building 12.3s (25/25) FINISHED
[+] Running 4/4
 ✔ Container redis       Healthy
 ✔ Container api         Healthy
 ✔ Container worker      Healthy
 ✔ Container frontend    Healthy

$ docker compose ps
NAME        SERVICE     STATUS              PORTS
redis       redis       Up (healthy)
api         api         Up (healthy)        0.0.0.0:8000->8000/tcp
worker      worker      Up (healthy)
frontend    frontend    Up (healthy)        0.0.0.0:3000->3000/tcp

$ curl http://localhost:8000/health
{"status":"ok"}
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `REDIS_HOST` | `redis` | Hostname of the Redis instance |
| `REDIS_PORT` | `6379` | Port of the Redis instance |
| `API_URL` | `http://api:8000` | Internal URL for the API service |
| `API_PORT` | `8000` | Host port mapping for the API |
| `FRONTEND_PORT` | `3000` | Host port mapping for the frontend |

## Running Tests

```bash
# Install dependencies
pip install -r api/requirements.txt

# Run tests with coverage
pytest api/tests/ --cov=api -v
```

## CI/CD Pipeline

The GitHub Actions pipeline runs the following stages in order:

1. **Lint** — flake8, eslint, hadolint
2. **Test** — pytest with coverage report
3. **Build** — Docker images tagged with SHA and latest, pushed to local registry
4. **Security** — Trivy vulnerability scanning with SARIF artifact
5. **Integration** — Full stack end-to-end test
6. **Deploy** — Rolling update (main branch only)

## Project Structure

```
├── api/                  # FastAPI backend
│   ├── Dockerfile
│   ├── main.py
│   ├── requirements.txt
│   └── tests/
│       └── test_api.py
├── frontend/             # Node.js/Express frontend
│   ├── Dockerfile
│   ├── app.js
│   ├── package.json
│   └── views/
│       └── index.html
├── worker/               # Python background worker
│   ├── Dockerfile
│   └── worker.py
├── docker-compose.yml
├── integration-test.sh
├── .github/workflows/pipeline.yml
├── FIXES.md
├── .env.example
└── README.md
```