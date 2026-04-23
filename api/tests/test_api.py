import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock

from api.main import app
import api.main

client = TestClient(app)


@pytest.fixture(autouse=True)
def mock_redis(monkeypatch):
    """Mock Redis connection for all tests."""
    mock = MagicMock()
    mock.lpush.return_value = True
    mock.hset.return_value = True
    mock.hget.return_value = b"queued"
    monkeypatch.setattr(api.main, "r", mock)
    return mock


# Test 1: Create a new job
def test_create_job(mock_redis):
    response = client.post("/jobs")
    assert response.status_code == 200
    data = response.json()
    assert "job_id" in data
    assert len(data["job_id"]) > 0


# Test 2: Get job status
def test_get_job_status(mock_redis):
    response = client.get("/jobs/test-id")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "queued"


# Test 3: Job not found returns error
def test_job_not_found(mock_redis):
    mock_redis.hget.return_value = None
    response = client.get("/jobs/nonexistent-id")
    assert response.status_code == 200
    data = response.json()
    assert data["error"] == "not found"


# Test 4: Health check endpoint
def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
