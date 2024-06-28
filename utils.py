import json
from datetime import datetime
from flask import Flask, flash
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.secret_key = 'something_special'
date_now = datetime.now()


def to_datetime(value):
    return datetime.strptime(value, '%Y-%m-%d %H:%M:%S')


def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


def validate_booking(club, places_required, competition, date_now):
    if competition['numberOfPlaces'] <= 0 or to_datetime(competition['date']) <= date_now:
        flash("The competition is over or full")
        return False

    if places_required > 12:
        flash("You cannot book more than 12 places")
        return False

    if places_required > club["points"]:
        flash("You do not have enough points")
        return False

    return True


def completed_booking(competition, club, places_required):
    competition['numberOfPlaces'] = competition['numberOfPlaces']-places_required
    club["points"] = club["points"] - places_required
    flash('Great-booking complete!')
