import pytest
from server import app
from unittest.mock import patch

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
        assert response.location == 'http://localhost/'
        assert "Sorry, that email was not found." in flashed_messages.values()