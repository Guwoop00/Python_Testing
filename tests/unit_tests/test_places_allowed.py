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
            "points": 20
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


def test_booking_more_than_12_places(client, clubs, competitions):
    response = client.post("/purchasePlaces", data={
        "places": "15",
        "club": clubs[0]["name"],
        "competition": competitions[0]["name"]
    })
    assert response.status_code == 200
    assert "You cannot book more than 12 places" in response.data.decode()
