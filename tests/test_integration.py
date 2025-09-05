import pytest
from server import app, loadClubs, loadCompetitions, saveClubs, saveCompetitions
from datetime import datetime


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_successful_purchase_workflow(client):
    """
    Tests the complete workflow of a successful purchase from login to saving data.
    """
    # 1. Capture the initial state of the clubs and competitions.
    clubs_initial = loadClubs()
    competitions_initial = loadCompetitions()

    # Find a valid club and competition with a future date
    if not clubs_initial or not competitions_initial:
        pytest.skip("Test requires non-empty clubs.json and competitions.json files.")

    club = clubs_initial[0]
    competition = None
    for c in competitions_initial:
        competition_date = datetime.strptime(c['date'], "%Y-%m-%d %H:%M:%S")
        if competition_date > datetime.now():
            competition = c
            break

    if not competition:
        pytest.skip("No future competitions available to test successful purchase.")

    # Get initial values from the valid data
    club_name = club['name']
    competition_name = competition['name']
    
    places_to_book = 1
    
    club_initial_points = int(club['points'])
    competition_initial_places = int(competition['numberOfPlaces'])
    club_email = club['email']

    try:
        # 2. Simulate the login POST request
        response_login = client.post('/showSummary', data={'email': club_email})
        assert response_login.status_code == 200
        assert b"Welcome" in response_login.data

        # 3. Simulate the purchase POST request
        response_purchase = client.post('/purchasePlaces', data={
            'club': club_name,
            'competition': competition_name,
            'places': str(places_to_book)
        })
        assert response_purchase.status_code == 200
        assert b"Great-booking complete!" in response_purchase.data

        # 4. Verify the changes were saved to the JSON files.
        clubs_final = loadClubs()
        competitions_final = loadCompetitions()
        
        club_final_points = int([c for c in clubs_final if c['name'] == club_name][0]['points'])
        competition_final_places = int([c for c in competitions_final if c['name'] == competition_name][0]['numberOfPlaces'])
        
        expected_points = club_initial_points - places_to_book
        expected_places = competition_initial_places - places_to_book

        assert club_final_points == expected_points
        assert competition_final_places == expected_places

    finally:
        # 5. Clean up the JSON files to their original state.
        saveClubs(clubs_initial)
        saveCompetitions(competitions_initial)