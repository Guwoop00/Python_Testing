from locust import HttpUser, task, between
from server import loadClubs, loadCompetitions


class LocustTest(HttpUser):
    wait_time = between(1, 5)
    competition = loadCompetitions()[0]
    club = loadClubs()[0]

    def on_start(self):
        self.client.post("/showSummary", data={'email': 'john@simplylift.co'})

    def on_stop(self):
        self.client.get("/logout")

    @task
    def login_and_board(self):
        self.client.get("/")

    @task
    def get_booking(self):
        self.client.get(f"/book/{self.competition['name']}/{self.club['name']}")

    @task
    def post_booking(self):
        self.client.post("/purchasePlaces", data={
            "places": 1,
            "club": self.club["name"],
            "competition": self.competition["name"]
        })
