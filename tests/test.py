import pytest
from api.main import app


@pytest.fixture
def client():
  app.testing = True
  with app.test_client() as client:
    yield client


def test_index(client):
  response = client.get('/')
  assert response.status_code == 200
  assert response.data.decode('utf-8') == 'Hello from Flask!'
