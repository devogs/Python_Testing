import pytest
from server import app
from unittest.mock import patch


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


# Mock data to simulate the clubs with different point values
MOCK_CLUBS_DATA = [
    {'name': 'Club Alpha', 'email': 'alpha@test.com', 'points': '5'},
    {'name': 'Club Beta', 'email': 'beta@test.com', 'points': '20'},
    {'name': 'Club Gamma', 'email': 'gamma@test.com', 'points': '10'}
]


@patch('server.clubs', MOCK_CLUBS_DATA)
def test_points_display_board(client):
    """
    Test that the points display board loads and correctly sorts clubs by points.
    """
    response = client.get('/pointsDisplay')
    
    # Assert that the page loads successfully
    assert response.status_code == 200
    assert b"Club Points Board" in response.data
    
    # Assert that the clubs are displayed in the correct sorted order (descending)
    data = response.data.decode('utf-8')
    assert "Club Beta" in data
    assert "Club Gamma" in data
    assert "Club Alpha" in data
    
    # A more robust check for order: find the index of each club name in the response.
    beta_index = data.find("Club Beta")
    gamma_index = data.find("Club Gamma")
    alpha_index = data.find("Club Alpha")
    
    assert beta_index < gamma_index < alpha_index