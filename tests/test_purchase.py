import pytest
from server import app
from datetime import datetime
from unittest.mock import patch, MagicMock
import json


# Mock data to be used by the tests
MOCK_CLUBS_DATA = [
    {'name': 'Test Club', 'email': 'test@test.com', 'points': '10'},
    {'name': 'Another Club', 'email': 'another@test.com', 'points': '20'}
]

MOCK_COMPETITIONS_DATA = [
    {'name': 'Test Competition', 'numberOfPlaces': '20', 'date': '2025-12-31 09:00:00'},
    {'name': 'Past Competition', 'numberOfPlaces': '10', 'date': '2024-01-01 09:00:00'}
]


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@patch('server.clubs', MOCK_CLUBS_DATA)
@patch('server.competitions', MOCK_COMPETITIONS_DATA)
@patch('server.flash')
def test_purchase_with_insufficient_points(mock_flash, client):
    """Test that a purchase is blocked when the club has insufficient points."""
    response = client.post('/purchasePlaces', data={
        'club': 'Test Club',
        'competition': 'Test Competition',
        'places': '11'
    }, follow_redirects=False)

    mock_flash.assert_called_once_with("You do not have enough points to book 11 places. You currently have 10 points.")
    assert response.status_code == 302
    assert response.location == '/book/Test%20Competition/Test%20Club'


@patch('server.clubs', MOCK_CLUBS_DATA)
@patch('server.competitions', MOCK_COMPETITIONS_DATA)
@patch('server.flash')
def test_purchase_more_than_max_places(mock_flash, client):
    """Test that a club cannot book more than 12 places per competition."""
    response = client.post('/purchasePlaces', data={
        'club': 'Test Club',
        'competition': 'Test Competition',
        'places': '13'
    }, follow_redirects=False)

    mock_flash.assert_called_once_with("You cannot book more than 12 places per competition.")
    assert response.status_code == 302
    assert response.location == '/book/Test%20Competition/Test%20Club'


@patch('server.clubs', MOCK_CLUBS_DATA)
@patch('server.competitions', MOCK_COMPETITIONS_DATA)
@patch('server.flash')
def test_purchase_on_past_competition(mock_flash, client):
    """Test that a purchase is blocked for a past competition."""
    from datetime import datetime as original_datetime
    with patch('server.datetime') as mock_datetime:
        mock_datetime.now.return_value = original_datetime(2025, 1, 1, 10, 0, 0)
        mock_datetime.strptime.side_effect = original_datetime.strptime
        
        response = client.post('/purchasePlaces', data={
            'club': 'Test Club',
            'competition': 'Past Competition',
            'places': '5'
        }, follow_redirects=False)

        mock_flash.assert_called_once_with("Booking for past competitions is not allowed.")
        assert response.status_code == 302
        assert response.location == '/book/Past%20Competition/Test%20Club'


@patch('server.saveClubs')
@patch('server.saveCompetitions')
@patch('server.clubs', MOCK_CLUBS_DATA)
@patch('server.competitions', MOCK_COMPETITIONS_DATA)
@patch('server.flash')
def test_saving_on_successful_purchase(mock_flash, mock_save_competitions, mock_save_clubs, client):
    """Test that the save functions are called on a successful purchase."""
    client.post('/purchasePlaces', data={
        'club': 'Test Club',
        'competition': 'Test Competition',
        'places': '5'
    })
    
    mock_save_clubs.assert_called_once()
    mock_save_competitions.assert_called_once()
    mock_flash.assert_called_once_with('Great-booking complete!')


@patch('server.saveClubs')
@patch('server.saveCompetitions')
@patch('server.clubs', MOCK_CLUBS_DATA)
@patch('server.competitions', MOCK_COMPETITIONS_DATA)
def test_no_saving_on_failed_purchase(mock_save_competitions, mock_save_clubs, client):
    """Test that the save functions are NOT called on a failed purchase."""
    client.post('/purchasePlaces', data={
        'club': 'Test Club',
        'competition': 'Test Competition',
        'places': '11'
    })

    mock_save_clubs.assert_not_called()
    mock_save_competitions.assert_not_called()