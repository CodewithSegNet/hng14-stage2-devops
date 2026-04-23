FROM python:3.11-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m appuser

USER appuser

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

ENV PATH=/home/appuser/.local/bin:$PATH

COPY . .

HEALTHCHECK CMD pgrep -f worker.py || exit 1

CMD ["python", "worker.py"]