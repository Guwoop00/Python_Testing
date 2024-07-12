import pytest
import server


@pytest.fixture
def client():
    server.app.config["TESTING"] = True
    with server.app.test_client() as client:
        yield client


def test_login(client):
    result = client.get("/")
    assert result.status_code == 200


def test_logout(client):
    result = client.get("/logout")
    assert result.status_code == 302
