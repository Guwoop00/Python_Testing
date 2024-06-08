import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, flash, url_for


def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()
date_now = datetime.now()


@app.template_filter()
def to_datetime(value):
    return datetime.strptime(value, '%Y-%m-%d %H:%M:%S')


@app.route('/')
def index():
    return render_template('index.html', clubs=clubs)


@app.route('/showSummary', methods=['POST'])
def showSummary():
    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
        sorted_competitions = sorted(competitions, key=lambda x: to_datetime(x['date']), reverse=True)
        return render_template('welcome.html', club=club, competitions=sorted_competitions, date_now=date_now)
    except IndexError:
        if request.form['email'] == '':
            flash("Please enter a valid email.")
        else:
            flash("Email not found")
        return render_template('index.html', clubs=clubs), 401


@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    sorted_competitions = sorted(competitions, key=lambda x: to_datetime(x['date']), reverse=True)
    if foundClub and foundCompetition:
        return render_template('booking.html', club=foundClub, competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=sorted_competitions, date_now=date_now)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]

    placesRequired = int(request.form['places'])

    if placesRequired > 12:
        flash("You cannot book more than 12 places")

    elif placesRequired > int(club["points"]):
        flash("You do not have enough points")

    else:
        competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
        club["points"] = int(club["points"]) - placesRequired
        flash('Great-booking complete!')
    sorted_competitions = sorted(competitions, key=lambda x: to_datetime(x['date']), reverse=True)
    return render_template('welcome.html', club=club, competitions=sorted_competitions, date_now=date_now)


@app.route('/logout')
def logout():
    return redirect(url_for('index', clubs=clubs))
