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


def test_clubs_cannot_use_more_points_than_allowed(client, clubs, competitions):
    club = clubs[0]
    club['points'] = 5
    competition = competitions[0]
    competition['numberOfPlaces'] = 10

    response = client.post('/purchasePlaces', data={
        'competition': competition['name'],
        'club': club['name'],
        'places': '6'
    })
    assert response.status_code == 200


def test_clubs_cannot_book_more_than_12_places_per_competition(client, clubs, competitions):
    club = clubs[0]
    club['points'] = 100
    competition = competitions[0]
    competition['numberOfPlaces'] = 15

    response = client.post('/purchasePlaces', data={
        'competition': competition['name'],
        'club': club['name'],
        'places': '13'
    })
    assert response.status_code == 200
