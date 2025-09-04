import json
from datetime import datetime
from flask import Flask,render_template,request,redirect,flash,url_for,session


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

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary',methods=['POST'])
def showSummary():
    found_clubs = [club for club in clubs if club['email'] == request.form['email']]

    if found_clubs:
        club = found_clubs[0]
        session['club_email'] = club['email']
        return render_template('welcome.html',club=club,competitions=competitions)
    else:
        flash("Sorry, that email was not found.")
        session.pop('club_email', None)
        return redirect(url_for('index'))


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])

    # FIX for Bug 4: Block bookings for past competitions
    competition_date = datetime.strptime(competition['date'], "%Y-%m-%d %H:%M:%S")
    if competition_date < datetime.now():
        flash("Booking for past competitions is not allowed.")
        return redirect(url_for('book', competition=competition['name'], club=club['name']))

    # FIX for Bug 3: Block bookings over 12 places
    if placesRequired > 12:
        flash("You cannot book more than 12 places per competition.")
        return redirect(url_for('book', competition=competition['name'], club=club['name']))

    # Check if club has enough points
    if int(club['points']) < placesRequired:
        flash(f"You do not have enough points to book {placesRequired} places. You currently have {club['points']} points.")
        return redirect(url_for('book', competition=competition['name'], club=club['name']))

    # Check if competition has enough places
    if int(competition['numberOfPlaces']) < placesRequired:
        flash(f"Not enough places available in this competition. Only {competition['numberOfPlaces']} places left.")
        return redirect(url_for('book', competition=competition['name'], club=club['name']))

    # Proceed with purchase only if all conditions are met
    competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
    club['points'] = str(int(club['points']) - placesRequired)
    
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)

# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))