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
            "name": "Simply Lift",
            "email": "john@simplylift.co",
            "points": 13
        }
    ]
    yield server.clubs


def test_unvalid(client):
    response = client.post('/showSummary', data={'email': ''})
    assert response.status_code == 401
    assert "A valid email is required." in response.data.decode()


def test_valid_email(client, clubs):
    club = clubs[0]
    response = client.post("/showSummary", data={"email": club["email"]})
    assert response.status_code == 200
    assert f"{clubs[0]['email']}" in response.data.decode()
