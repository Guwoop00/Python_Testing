from flask import render_template, request, redirect, flash, url_for
from flask_cors import CORS
from utils import loadClubs, loadCompetitions, to_datetime, validate_booking, completed_booking, date_now, app


CORS(app)
app.secret_key = 'something_special'
app.jinja_env.filters['to_datetime'] = to_datetime

competitions = loadCompetitions()
clubs = loadClubs()


@app.route('/')
def index():
    return render_template('index.html', clubs=clubs)


@app.route('/showSummary', methods=['POST'])
def showSummary():
    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
    except IndexError:
        flash("A valid email is required.")
        return render_template('index.html', clubs=clubs), 401

    sorted_competitions = sorted(competitions, key=lambda x: to_datetime(x['date']), reverse=True)
    return render_template('welcome.html', club=club, competitions=sorted_competitions, date_now=date_now)


@app.route('/book/<competition>/<club>', methods=['GET'])
def book(competition, club):
    sorted_competitions = sorted(competitions, key=lambda x: to_datetime(x['date']), reverse=True)
    try:
        foundClub = [c for c in clubs if c['name'] == club][0]
        foundCompetition = [c for c in competitions if c['name'] == competition][0]
        return render_template('booking.html', club=foundClub, competition=foundCompetition)

    except (IndexError, TypeError, KeyError):
        flash("Something went wrong-please try again")
    return render_template('welcome.html', club=club, competitions=sorted_competitions, date_now=date_now)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    places_required = int(request.form['places'])

    if validate_booking(club, places_required, competition, date_now):
        completed_booking(competition, club, places_required)

    sorted_competitions = sorted(competitions, key=lambda x: to_datetime(x['date']), reverse=True)
    return render_template('welcome.html', club=club, competitions=sorted_competitions, date_now=date_now)


@app.route('/logout')
def logout():
    return redirect(url_for('index', clubs=clubs))
