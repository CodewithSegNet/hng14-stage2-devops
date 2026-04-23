# Stage 1: Install dependencies
FROM python:3.11-alpine AS builder

WORKDIR /app

COPY requirements.txt .

# hadolint ignore=DL3013
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-alpine AS runtime

WORKDIR /app

# create non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# copy python deps from builder
COPY --from=builder /install /usr/local

COPY --chown=appuser:appgroup . .

USER appuser

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD pgrep -f worker.py || exit 1

CMD ["python", "worker.py"]