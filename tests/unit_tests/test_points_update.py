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
            "points": 13
        }
    ]
    yield server.clubs


@pytest.fixture
def competitions():
    server.competitions = [
        {
            "name": "Test Festival 2025",
            "date": "2025-03-27 10:00:00",
            "numberOfPlaces": 23
        },
        {
            "name": "Test Festival 2026",
            "date": "2026-03-27 10:00:00",
            "numberOfPlaces": 25
        }
    ]
    yield server.competitions


def test_point_updates_are_reflected(client, clubs, competitions):
    club = clubs[0]
    competition = competitions[0]

    initial_points = club['points']
    initial_places = competition['numberOfPlaces']
    booked = 3

    response = client.post('/purchasePlaces', data={
        'competition': competition['name'],
        'club': club['name'],
        'places': booked
    }, follow_redirects=True)

    assert response.status_code == 200
    assert "Great-booking complete!" in response.data.decode()
    assert f"Points available: {initial_points - booked}" in response.data.decode()
    assert f"Number of Places: {initial_places - booked}" in response.data.decode()
