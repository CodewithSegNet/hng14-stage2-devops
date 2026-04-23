import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock

from api.main import app

client = TestClient(app)


# Mock Redis globally
@pytest.fixture(autouse=True)
def mock_redis(monkeypatch):
    mock = MagicMock()

    # mock behavior
    mock.lpush.return_value = True
    mock.hset.return_value = True
    mock.hget.return_value = b"queued"

    monkeypatch.setattr("api.main.r", mock)


# ✅ Test 1: Create job
def test_create_job():
    response = client.post("/jobs")
    assert response.status_code == 200
    assert "job_id" in response.json()


# ✅ Test 2: Get job
def test_get_job():
    response = client.get("/jobs/test-id")
    assert response.status_code == 200
    assert response.json()["status"] == "queued"


# ✅ Test 3: Job not found
def test_job_not_found(monkeypatch):
    from api import main

    mock = MagicMock()
    mock.hget.return_value = None
    monkeypatch.setattr(main, "r", mock)

    response = client.get("/jobs/unknown")
    assert response.status_code == 200
    assert response.json()["error"] == "not found"