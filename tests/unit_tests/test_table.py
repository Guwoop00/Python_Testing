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


def test_table_view(client, clubs):
    club = clubs[0]

    response = client.get("/")
    assert response.status_code == 200
    assert "<h1>GUDLFT Club's display board</h1>" in response.data.decode()
    assert "<th>Club</th>" in response.data.decode()
    assert "<th>Points</th>" in response.data.decode()
    assert f"<td>{club['name']}</td>" in response.data.decode()
    assert f"<td>{club['points']}</td>" in response.data.decode()
