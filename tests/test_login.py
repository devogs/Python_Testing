import pytest
from server import app, clubs, competitions
from unittest.mock import patch, MagicMock

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_unknown_email_shows_error(client):
    """Test that an unknown email results in a flash message and redirection."""
    with patch('server.clubs', [{'email': 'test@test.com'}]):
        response = client.post('/showSummary', data={'email': 'unknown@test.com'}, follow_redirects=True)
        assert b"Sorry, that email was not found." in response.data
        assert response.status_code == 200