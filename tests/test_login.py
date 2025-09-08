import pytest
from server import app, clubs, competitions
from unittest.mock import patch, MagicMock


@pytest.fixture
def client():
    """Configures the Flask test client and yields it for testing."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_unknown_email_flashes_message(client):
    """Test that an unknown email results in a flash message being stored."""
    # Mock the 'clubs' data so that the email is not found
    with patch('server.clubs', []):
        response = client.post('/showSummary', data={'email': 'unknown@test.com'}, follow_redirects=False)

        # Check the flash messages stored in the session
        with client.session_transaction() as sess:
            flashed_messages = dict(sess.get('_flashes', []))
            
        assert response.status_code == 302
        assert response.location == '/'
        assert "Sorry, that email was not found." in flashed_messages.values()

def test_existing_email_login_is_successful(client):
    """Test that a user with an existing email can log in and view the welcome page."""
    # Mock the 'clubs' data to include a known user
    with patch('server.clubs', [{'name': 'Test Club', 'email': 'test@test.com', 'points': '10'}]):
        response = client.post('/showSummary', data={'email': 'test@test.com'})

        # Assertions
        assert response.status_code == 200
        assert b'Welcome' in response.data
        
        # Check that the email was stored in the session
        with client.session_transaction() as sess:
            assert 'club_email' in sess
            assert sess['club_email'] == 'test@test.com'