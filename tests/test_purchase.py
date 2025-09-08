import pytest
from server import app
from datetime import datetime
from unittest.mock import patch, MagicMock


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_purchase_with_insufficient_points(client):
    """Test that a purchase is blocked when the club has insufficient points."""
    with patch('server.clubs', [{'name': 'Test Club', 'email': 'test@test.com', 'points': '10'}]):
        with patch('server.competitions', [{'name': 'Test Competition', 'numberOfPlaces': '20', 'date': '2025-12-31 09:00:00'}]):
            with patch('server.flash') as mock_flash:
                response = client.post('/purchasePlaces', data={
                    'club': 'Test Club',
                    'competition': 'Test Competition',
                    'places': '11'
                }, follow_redirects=False)

                mock_flash.assert_called_once_with("You do not have enough points to book 11 places. You currently have 10 points.")
                assert response.status_code == 302
                assert response.location == '/book/Test%20Competition/Test%20Club'


def test_purchase_with_sufficient_points_and_places_without_save(client):
    """Test a successful purchase with enough points and places without relying on save functions."""
    # Mock the lists to set up the test scenario
    mock_clubs = [{'name': 'Test Club', 'email': 'test@test.com', 'points': '10'}]
    mock_competitions = [{'name': 'Test Competition', 'numberOfPlaces': '20', 'date': '2025-12-31 09:00:00'}]

    with patch('server.clubs', mock_clubs):
        with patch('server.competitions', mock_competitions):
            with patch('server.flash') as mock_flash:
                response = client.post('/purchasePlaces', data={
                    'club': 'Test Club',
                    'competition': 'Test Competition',
                    'places': '5'
                }, follow_redirects=False)

                # Assertions for the happy path
                mock_flash.assert_called_once_with("Great-booking complete!")
                assert response.status_code == 200
                assert b'Welcome' in response.data
                # Verify that the points and places were updated in the mock data
                assert int(mock_clubs[0]['points']) == 5
                assert int(mock_competitions[0]['numberOfPlaces']) == 15


def test_purchase_more_than_max_places(client):
    """Test that a club cannot book more than 12 places per competition."""
    with patch('server.clubs', [{'name': 'Test Club', 'email': 'test@test.com', 'points': '20'}]):
        with patch('server.competitions', [{'name': 'Test Competition', 'numberOfPlaces': '20', 'date': '2025-12-31 09:00:00'}]):
            with patch('server.flash') as mock_flash:
                response = client.post('/purchasePlaces', data={
                    'club': 'Test Club',
                    'competition': 'Test Competition',
                    'places': '13'
                }, follow_redirects=False)

                mock_flash.assert_called_once_with("You cannot book more than 12 places per competition.")
                assert response.status_code == 302
                assert response.location == '/book/Test%20Competition/Test%20Club'


def test_purchase_on_past_competition(client):
    """Test that a purchase is blocked for a past competition."""
    # Patch the datetime class imported in server.py and give it a mock 'now' method.
    from datetime import datetime as original_datetime
    with patch('server.datetime') as mock_datetime:
        mock_datetime.now = MagicMock(return_value=original_datetime(2025, 1, 1, 10, 0, 0))
        mock_datetime.strptime.side_effect = original_datetime.strptime
        
        with patch('server.clubs', [{'name': 'Test Club', 'email': 'test@test.com', 'points': '20'}]):
            with patch('server.competitions', [{'name': 'Test Competition', 'numberOfPlaces': '20', 'date': '2024-12-31 09:00:00'}]):
                with patch('server.flash') as mock_flash:
                    response = client.post('/purchasePlaces', data={
                        'club': 'Test Club',
                        'competition': 'Test Competition',
                        'places': '5'
                    }, follow_redirects=False)

                mock_flash.assert_called_once_with("Booking for past competitions is not allowed.")
                assert response.status_code == 302
                assert response.location == '/book/Test%20Competition/Test%20Club'