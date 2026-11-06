import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services import task_services


@pytest.fixture
def client():
    task_services.reset_tasks()
    yield TestClient(app)
    task_services.reset_tasks()
