import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch


# Mock Redis before importing app
mock_redis_instance = MagicMock()
mock_redis_instance.lpush.return_value = True
mock_redis_instance.hset.return_value = True
mock_redis_instance.hget.return_value = b"queued"


@pytest.fixture(autouse=True)
def mock_redis():
    """Mock Redis for all tests."""
    with patch("main.redis.Redis", return_value=mock_redis_instance):
        mock_redis_instance.reset_mock()
        mock_redis_instance.lpush.return_value = True
        mock_redis_instance.hset.return_value = True
        mock_redis_instance.hget.return_value = b"queued"
        yield mock_redis_instance


@pytest.fixture
def client():
    """Create a test client."""
    from main import app
    return TestClient(app)


# Test 1: Create job
def test_create_job(client):
    response = client.post("/jobs")
    assert response.status_code == 200
    data = response.json()
    assert "job_id" in data
    assert len(data["job_id"]) > 0


# Test 2: Get job status
def test_get_job(client):
    response = client.get("/jobs/test-id")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "queued"


# Test 3: Job not found
def test_job_not_found(client):
    mock_redis_instance.hget.return_value = None
    response = client.get("/jobs/unknown-id")
    assert response.status_code == 200
    data = response.json()
    assert data["error"] == "not found"


# Test 4: Health check endpoint
def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
