import pytest
import server


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
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": 25
        },
        {
            "name": "Test Festival 2026",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": 25
        }
    ]
    yield server.competitions


def test_booking_places_in_past_competitions(client, clubs, competitions):
    club = clubs[0]
    competition = competitions[0]

    response = client.post('/purchasePlaces', data={
        'competition': competition['name'],
        'club': club['name'],
        'places': 5
    }, follow_redirects=True)

    assert response.status_code == 200
    assert "Book Places" not in response.data.decode()
