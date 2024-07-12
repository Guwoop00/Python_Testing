import server
import pytest


@pytest.fixture
def client():
    server.app.config["TESTING"] = True
    with server.app.test_client() as client:
        yield client


@pytest.fixture
def clubs():
    server.clubs = [
        {
            "name": "Test",
            "email": "test@test.com",
            "points": 5
        }
    ]
    yield server.clubs


@pytest.fixture
def competitions():
    server.competitions = [
        {
            "name": "Test Festival 2025",
            "date": "2025-03-27 10:00:00",
            "numberOfPlaces": 25
        },
        {
            "name": "Test Festival 2026",
            "date": "2026-03-27 10:00:00",
            "numberOfPlaces": 25
        }
    ]
    yield server.competitions


def test_clubs_cannot_use_more_points_than_allowed(client, clubs, competitions):
    club = clubs[0]
    competition = competitions[0]

    response = client.post('/purchasePlaces', data={
        'competition': competition['name'],
        'club': club['name'],
        'places': 6
    })
    assert response.status_code == 200
    assert "You do not have enough points" in response.data.decode()
