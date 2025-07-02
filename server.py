import json
from flask import Flask,render_template,request,redirect,flash,url_for,session
from datetime import datetime


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs

def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions

def saveClubs(clubs_data):
    with open('clubs.json', 'w') as c:
        json.dump({"clubs": clubs_data}, c, indent=4)

def saveCompetitions(competitions_data):
    with open('competitions.json', 'w') as comps:
        json.dump({"competitions": competitions_data}, comps, indent=4)


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()


@app.route('/')
def index():
    if 'club_email' in session:
        club_email = session['club_email']
        found_clubs = [c for c in clubs if c['email'] == club_email]
        if found_clubs:
            club = found_clubs[0]
            return render_template('welcome.html', club=club, competitions=competitions,
                                   current_date_str=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        else:
            session.pop('club_email', None)
            flash("Your club's email was not found. Please log in again.")
            return render_template('index.html')
    return render_template('index.html')


@app.route('/showSummary',methods=['POST'])
def showSummary():
    user_email = request.form['email']
    found_clubs = [club for club in clubs if club['email'] == user_email]

    if found_clubs:
        club = found_clubs[0]
        session['club_email'] = club['email']
        return render_template('welcome.html',club=club,competitions=competitions,
                               current_date_str=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    else:
        flash("Sorry, that email was not found.")
        session.pop('club_email', None)
        return redirect(url_for('index'))


@app.route('/book/<competition_name>/<club_name>')
def book(competition_name,club_name):
    if 'club_email' not in session:
        flash("You need to be logged in to book places.")
        return redirect(url_for('index'))
    
    logged_in_club_email = session['club_email']
    foundClub = [c for c in clubs if c['email'] == logged_in_club_email][0]

    foundCompetition = [c for c in competitions if c['name'] == competition_name][0]
    
    if foundClub['name'] != club_name:
        flash("Attempted to book for a different club. Action blocked.")
        return redirect(url_for('index'))

    competition_date = datetime.strptime(foundCompetition['date'], '%Y-%m-%d %H:%M:%S')
    if competition_date < datetime.now():
        flash("This competition has already passed. Booking is not allowed.")
        return redirect(url_for('index'))
    
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return redirect(url_for('index'))


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    if 'club_email' not in session:
        flash("You need to be logged in to purchase places.")
        return redirect(url_for('index'))

    logged_in_club_email = session['club_email']
    club = [c for c in clubs if c['email'] == logged_in_club_email][0]

    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    placesRequired = int(request.form['places'])

    if club['name'] != request.form['club']:
        flash("Attempted to purchase for a different club. Action blocked.")
        return redirect(url_for('index'))

    competition_date = datetime.strptime(competition['date'], '%Y-%m-%d %H:%M:%S')
    if competition_date < datetime.now():
        flash("Booking for past competitions is not allowed.")
        return redirect(url_for('index'))

    if placesRequired > 12:
        flash("You cannot book more than 12 places per competition.")
        return redirect(url_for('index'))

    if int(club['points']) >= placesRequired:
        if int(competition['numberOfPlaces']) >= placesRequired:
            competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
            club['points'] = str(int(club['points']) - placesRequired)

            saveClubs(clubs)
            saveCompetitions(competitions)

            flash('Great-booking complete!')
        else:
            flash(f"Not enough places available in this competition. Only {competition['numberOfPlaces']} places left.")
    else:
        flash(f"You do not have enough points to book {placesRequired} places. You currently have {club['points']} points.")
    
    return redirect(url_for('index'))


@app.route('/pointsDisplay')
def pointsDisplay():      
    sorted_clubs = sorted(clubs, key=lambda c: int(c['points']), reverse=True)
    return render_template('points.html', clubs=sorted_clubs)


@app.route('/logout')
def logout():
    session.pop('club_email', None)
    flash("You have been logged out.")
    return redirect(url_for('index'))
