import pytest
from server import app, loadClubs, loadCompetitions


@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    yield client


@pytest.fixture
def clubs():
    return loadClubs()


@pytest.fixture
def competitions():
    return loadCompetitions()


def test_unknown_email(client):
    response = client.post('/showSummary', data={'email': 'unknown@example.com'})
    assert response.status_code == 302
