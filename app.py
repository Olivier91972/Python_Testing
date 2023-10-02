import datetime
import json
from flask import Flask, render_template, request, redirect, flash, url_for, sessions

from functions import date_is_passed


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

now = datetime.datetime.now()
current_date = now.strftime("%Y-%m-%d, %H:%M:%S")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary',methods=['POST'])
def showSummary():
    """
    Displays the summary of all competitions
    and points available by the connected club
    """

    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
        return render_template('welcome.html', club=club, competitions=competitions, current_date=current_date)
    except IndexError:
        flash("Sorry, this email wasn't found. Please try again with a correct email !!")
        return redirect(url_for('index'))


@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html', club=foundClub, competition=foundCompetition)
    # elif date_is_passed(competition['date']):
    #     flash('You cannot buy a place for a competition that has already passed.')
    #     return render_template('welcome.html', club=club, competitions=competitions)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)
# Book_past_competition


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
    if date_is_passed(competition['date']):
        flash('You cannot buy a place for a competition that has already passed.')
        competition['numberOfPlaces'] = int(competition['numberOfPlaces']) + placesRequired
        return render_template('welcome.html', club=club, competitions=competitions)

    else:
        flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)

    #
    # except TypeError:
    #     print("TypeError: The view function for 'purchasePlaces' did not return a valid response.")



# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
