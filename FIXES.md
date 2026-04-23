# FIXES.md — Bugs Found and Fixed

## Fix 1: Redis connection hardcoded to localhost in API

- **File:** `api/main.py`
- **Line:** 9–11
- **Problem:** Redis host was hardcoded to `"localhost"`, which fails inside containers where Redis runs as a separate service on the Docker network.
- **Fix:** Changed to use environment variables with fallback defaults:
  ```python
  r = redis.Redis(
      host=os.getenv("REDIS_HOST", "redis"),
      port=int(os.getenv("REDIS_PORT", 6379))
  )
  ```

## Fix 2: Redis connection hardcoded to localhost in Worker

- **File:** `worker/worker.py`
- **Line:** 5–9
- **Problem:** Same as Fix 1 — Redis host was hardcoded to `"localhost"`, failing in containers.
- **Fix:** Changed to use environment variables with fallback defaults:
  ```python
  r = redis.Redis(
      host=os.getenv("REDIS_HOST", "redis"),
      port=int(os.getenv("REDIS_PORT", 6379))
  )
  ```

## Fix 3: Frontend API URL hardcoded

- **File:** `frontend/app.js`
- **Line:** 6
- **Problem:** The API URL was hardcoded to `"http://localhost:8000"`, which fails in containers where the API runs as a separate service.
- **Fix:** Changed to use environment variable with fallback:
  ```javascript
  const API_URL = process.env.API_URL || "http://localhost:8000";
  ```

## Fix 4: Frontend package.json has `"type": "module"` but code uses CommonJS

- **File:** `frontend/package.json`
- **Line:** 5
- **Problem:** `"type": "module"` was set, which tells Node.js to treat all `.js` files as ES modules. However, `app.js` uses CommonJS syntax (`require()`, not `import`). This causes `ReferenceError: require is not defined` at runtime.
- **Fix:** Removed `"type": "module"` from `package.json` so Node.js treats `.js` files as CommonJS (the default).

## Fix 5: `api/.env` committed to git with plaintext secrets

- **File:** `api/.env`
- **Line:** 1
- **Problem:** The file `api/.env` containing `REDIS_PASSWORD=supersecretpassword123` was committed to the repository. Secrets must never be in version control.
- **Fix:** Removed `api/.env` from git tracking with `git rm --cached api/.env`. Added `.env` and `*.env` patterns to `.gitignore` (while keeping `.env.example`).

## Fix 6: No `.dockerignore` files — secrets could be copied into images

- **Files:** `api/`, `frontend/`, `worker/` (all missing `.dockerignore`)
- **Problem:** Without `.dockerignore` files, `COPY . .` in Dockerfiles would copy `.env` files, test directories, `__pycache__`, and other unnecessary files into production images.
- **Fix:** Created `.dockerignore` files for all three services to exclude `.env`, `*.env`, `venv/`, `__pycache__/`, `tests/`, and other dev artifacts.

## Fix 7: Frontend Dockerfile was not multi-stage

- **File:** `frontend/Dockerfile`
- **Lines:** 1–17
- **Problem:** The frontend Dockerfile used a single stage, meaning `npm install` build artifacts and dev tools remained in the final image, increasing image size.
- **Fix:** Converted to a multi-stage build: Stage 1 (`builder`) installs dependencies with `npm ci --omit=dev`, Stage 2 (`runtime`) copies only `node_modules` from the builder.

## Fix 8: API Dockerfile used `useradd` instead of Alpine-compatible `adduser`

- **File:** `api/Dockerfile`
- **Line:** 19
- **Problem:** The API Dockerfile used `useradd -m appuser`, which is a Debian command. Since the image is Alpine-based, the correct command is `addgroup`/`adduser`.
- **Fix:** Changed to `addgroup -S appgroup && adduser -S appuser -G appgroup`.

## Fix 9: docker-compose frontend depends_on used `service_started` instead of `service_healthy`

- **File:** `docker-compose.yml`
- **Line:** 44
- **Problem:** The frontend service used `condition: service_started` for the API dependency. This means the frontend could start before the API is actually ready to serve requests.
- **Fix:** Changed to `condition: service_healthy` so the frontend waits until the API's health check passes.

## Fix 10: docker-compose had no resource limits

- **File:** `docker-compose.yml`
- **Problem:** No CPU or memory limits were set on any service, which could allow a single service to consume all host resources.
- **Fix:** Added `deploy.resources.limits` for all services (0.5 CPU, 256M memory each).

## Fix 11: docker-compose had no restart policies

- **File:** `docker-compose.yml`
- **Problem:** No restart policies were configured, meaning containers would not restart after crashes.
- **Fix:** Added `restart: unless-stopped` to all services.

## Fix 12: docker-compose had hardcoded configuration values

- **File:** `docker-compose.yml`
- **Lines:** 17–18, 30–31, 41
- **Problem:** Environment variable values like `redis`, `6379`, and `http://api:8000` were hardcoded directly in the Compose file.
- **Fix:** Changed all values to use environment variable interpolation with defaults: `${REDIS_HOST:-redis}`, `${REDIS_PORT:-6379}`, `${API_URL:-http://api:8000}`.

## Fix 13: Worker Dockerfile was not multi-stage

- **File:** `worker/Dockerfile`
- **Lines:** 1–23
- **Problem:** Single-stage build with build tools remaining in the final image.
- **Fix:** Converted to a multi-stage build: Stage 1 installs Python dependencies with `--prefix=/install`, Stage 2 copies only the installed packages.