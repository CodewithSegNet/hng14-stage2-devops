#!/bin/bash
set -e

TIMEOUT=60
INTERVAL=3
ELAPSED=0

echo "=== Integration Test ==="

# Start the stack
echo "Starting services..."
docker compose up -d --build

# Wait for services to be healthy
echo "Waiting for services to become healthy..."
until curl -sf http://localhost:8000/health > /dev/null 2>&1; do
  sleep "$INTERVAL"
  ELAPSED=$((ELAPSED + INTERVAL))
  if [ "$ELAPSED" -ge "$TIMEOUT" ]; then
    echo "FAIL: Services did not become healthy within ${TIMEOUT}s"
    docker compose down -v
    exit 1
  fi
  echo "  Waiting... (${ELAPSED}s / ${TIMEOUT}s)"
done

echo "API is healthy."

# Wait for frontend
until curl -sf http://localhost:3000/ > /dev/null 2>&1; do
  sleep "$INTERVAL"
  ELAPSED=$((ELAPSED + INTERVAL))
  if [ "$ELAPSED" -ge "$TIMEOUT" ]; then
    echo "FAIL: Frontend did not become healthy within ${TIMEOUT}s"
    docker compose down -v
    exit 1
  fi
done

echo "Frontend is healthy."

# Submit a job through the frontend
echo "Submitting a job..."
RESPONSE=$(curl -sf -X POST http://localhost:3000/submit)
JOB_ID=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['job_id'])")

if [ -z "$JOB_ID" ]; then
  echo "FAIL: Could not submit job"
  docker compose down -v
  exit 1
fi

echo "Job submitted: $JOB_ID"

# Poll until completed or timeout
POLL_ELAPSED=0
POLL_TIMEOUT=30
STATUS=""

while [ "$POLL_ELAPSED" -lt "$POLL_TIMEOUT" ]; do
  STATUS_RESPONSE=$(curl -sf "http://localhost:3000/status/$JOB_ID")
  STATUS=$(echo "$STATUS_RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('status',''))")

  echo "  Job status: $STATUS (${POLL_ELAPSED}s / ${POLL_TIMEOUT}s)"

  if [ "$STATUS" = "completed" ]; then
    break
  fi

  sleep "$INTERVAL"
  POLL_ELAPSED=$((POLL_ELAPSED + INTERVAL))
done

# Assert final status
if [ "$STATUS" = "completed" ]; then
  echo "PASS: Job completed successfully!"
  EXIT_CODE=0
else
  echo "FAIL: Job did not complete. Final status: $STATUS"
  EXIT_CODE=1
fi

# Always tear down
echo "Tearing down..."
docker compose down -v

exit $EXIT_CODE
