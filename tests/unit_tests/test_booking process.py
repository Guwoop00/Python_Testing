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


def test_book_valid_competition_and_club(client, clubs, competitions):
    club = clubs[0]
    competition = competitions[0]

    response = client.get(f'/book/{competition["name"]}/{club["name"]}')

    assert response.status_code == 200
    assert f"<title>Booking for {competition['name']} || GUDLFT</title>" in response.data.decode()


def test_book_unvalid_competition(client, clubs):
    club = clubs[0]

    response = client.get(f'/book/invalid_competition_name/{club["name"]}', follow_redirects=True)
    assert response.status_code == 200
    assert "Please check the name of the competition" in response.data.decode()


def test_book_unvalid_club(client, competitions):
    competition = competitions[0]

    response = client.get(f'/book/{competition["name"]}/invalid_club_name', follow_redirects=True)
    assert response.status_code == 200
    assert "Please check the name of the club" in response.data.decode()


def test_book_unvalid_club_and_competition(client):
    response = client.get('/book/invalid_competition_name/invalid_club_name', follow_redirects=True)
    assert response.status_code == 200
    assert "Please check the name of the club and competition" in response.data.decode()
