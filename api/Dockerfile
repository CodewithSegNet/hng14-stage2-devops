# stage 1 - build
FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt .

# install to custom user base (clean + portable)
ENV PYTHONUSERBASE=/install
RUN pip install --no-cache-dir --user -r requirements.txt


# stage 2 - runtime
FROM python:3.11-slim

WORKDIR /app

# install system deps FIRST (as root)
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# create non-root user
RUN useradd -m appuser

# copy dependencies
COPY --from=builder /install /home/appuser/.local
ENV PATH=/home/appuser/.local/bin:$PATH

# switch user AFTER installs
USER appuser

COPY . .

# healthcheck should hit real endpoint (NOT /docs in production)
HEALTHCHECK --interval=30s --timeout=5s CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]