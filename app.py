import datetime
# import json
from flask import Flask, render_template, request, redirect, flash, url_for

from functions import date_is_passed

from utils import (
    load_clubs,
    load_competitions,
    sort_competitions_date,
    initialize_booked_places,
    update_booked_places
)


# def loadClubs():
#     with open('clubs.json') as c:
#         listOfClubs = json.load(c)['clubs']
#         return listOfClubs
#
#
# def loadCompetitions():
#     with open('competitions.json') as comps:
#         listOfCompetitions = json.load(comps)['competitions']
#         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = load_competitions()
clubs = load_clubs()
past_competitions, present_competitions = sort_competitions_date(competitions)
places_booked = initialize_booked_places(competitions, clubs)


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
    try:
        foundClub = [c for c in clubs if c['name'] == club][0]

        foundCompetition = [c for c in competitions if c['name'] == competition][0]
        if foundClub and foundCompetition:
            return render_template('booking.html', club=foundClub, competition=foundCompetition)
        else:
            flash("Something went wrong-please try again")
            return render_template('welcome.html', club=club, competitions=competitions)
    except IndexError:
        flash("list index out of range")


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    try:
        try:
            competition = [c for c in competitions if c['name'] == request.form['competition']][0]
            # print(competition)

            club = [c for c in clubs if c['name'] == request.form['club']][0]
            try:
                placesRequired = int(request.form['places'])
                if date_is_passed(competition['date']):
                    flash('You cannot buy a place for a competition that has already passed.')
                    return render_template('welcome.html', club=club, competitions=competitions)
                elif placesRequired > 12:
                    flash('You cannot take more than 12 places')
                    return render_template('booking.html', club=club, competition=competition)
                elif placesRequired > int(club["points"]):
                    flash("Try again - your points is less than what you book. ")
                    return render_template('booking.html', club=club, competition=competition)
                else:
                    flash('Great-booking complete!')
                    update_booked_places(competition, club, places_booked, placesRequired)
                    competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
                    club["points"] = int(club["points"]) - placesRequired
                    return render_template('welcome.html', club=club, competitions=competitions)
            except ValueError:
                flash('invalid literal, please retry')
                return render_template('booking.html', club=club, competition=competition)
        except AttributeError:
            flash("'NoneType' object has no attribute")
    except IndexError:
        flash('list index out of range')


@app.route('/logout')
def logout():
    return redirect(url_for('index'))


# route for points_display
@app.route('/points_display')
def points_display():
    club = [clu for clu in clubs]
    # print(club)
    return render_template('club_points.html', club=club, competitions=competitions)
