# stage 1 - build
FROM python:3.11-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# stage 2 - runtime
FROM python:3.11-slim

WORKDIR /app

# stage 3 - create non-root user
RUN useradd -m appuser
USER appuser

# copy dependencies
COPY --from=builder /root/.local /home/appuser/.local
ENV PATH=/home/appuser/.local/bin:$PATH

COPY . .

RUN apt-get update && apt-get install -y curl

# HEALTHCHECK
HEALTHCHECK CMD curl -f http://localhost:8000/docs || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]