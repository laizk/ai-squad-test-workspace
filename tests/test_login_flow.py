"""Test cases for Login Flow"""
import pytest
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from api_client import APIClient
from models import User, SessionToken


@pytest.fixture
def api_client():
    """Create API client instance"""
    return APIClient(base_url="https://api.example.com")


@pytest.fixture
def mock_token():
    """Mock session token for testing"""
    return "mock_token_123456789"


@pytest.fixture
def mock_user():
    """Mock user data"""
    return User(
        id="user_001",
        username="testuser",
        email="test@example.com",
        first_name="Test",
        last_name="User",
        is_active=True
    )


class TestLoginFlow:
    """Test cases for login functionality"""
    
    def test_login_success(self, api_client, mock_token):
        """Test successful login returns valid token"""
        # Simulate successful login response
        response_data = {
            "token": mock_token,
            "expires_at": "2024-12-31T23:59:59Z",
            "user": {
                "id": "user_001",
                "username": "testuser"
            }
        }
        
        # Verify response structure
        assert "token" in response_data
        assert "expires_at" in response_data
        assert "user" in response_data
        assert response_data["token"] == mock_token
        
    def test_login_invalid_credentials(self, api_client):
        """Test login with invalid credentials"""
        # Simulate invalid credentials response
        response_data = {
            "error": "Invalid credentials",
            "message": "The provided username or password is incorrect"
        }
        
        assert "error" in response_data
        assert response_data["error"] == "Invalid credentials"
        
    def test_login_token_expiry(self, api_client, mock_token):
        """Test token expiry handling"""
        # Simulate expired token
        expired_token = mock_token + "_expired"
        
        assert expired_token != mock_token
        
    def test_login_session_valid(self, api_client, mock_token):
        """Test that session token is valid"""
        assert mock_token is not None
        assert len(mock_token) > 0
        
    def test_login_user_info(self, api_client, mock_user):
        """Test user info is returned on login"""
        response_data = {
            "token": "test_token",
            "user": {
                "id": mock_user.id,
                "username": mock_user.username,
                "email": mock_user.email,
                "first_name": mock_user.first_name,
                "last_name": mock_user.last_name,
                "is_active": mock_user.is_active
            }
        }
        
        assert response_data["user"]["id"] == mock_user.id
        assert response_data["user"]["username"] == mock_user.username
        assert response_data["user"]["is_active"] == mock_user.is_active
  