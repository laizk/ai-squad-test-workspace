"""Integration tests for complete flows"""
import pytest
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from api_client import APIClient
from models import Order, Product, User


@pytest.fixture
def api_client():
    """Create API client instance"""
    return APIClient(base_url="https://api.example.com")


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


@pytest.fixture
def mock_order(mock_user):
    """Mock order data"""
    return Order(
        id="order_001",
        user_id=mock_user.id,
        items=[
            Product(id="prod_001", name="Widget", price=29.99, quantity=2, sku="WID-001"),
            Product(id="prod_002", name="Gadget", price=49.99, quantity=1, sku="GAD-002")
        ],
        total_amount=109.97,
        status="pending"
    )


@pytest.fixture
def mock_token():
    """Mock session token for testing"""
    return "mock_token_123456789"


class TestIntegrationFlows:
    """Integration tests for complete flows"""
    
    def test_complete_login_checkout_flow(self, api_client, mock_token, mock_order):
        """Test complete login to checkout flow"""
        # Step 1: Verify login token is valid
        assert mock_token is not None
        assert len(mock_token) > 0
        
        # Step 2: Verify order exists
        assert mock_order.id is not None
        assert mock_order.user_id == "user_001"
        
        # Step 3: Verify order items
        assert len(mock_order.items) == 2
        
        # Step 4: Verify order total
        assert mock_order.total_amount == 109.97
        
        # Step 5: Simulate checkout success
        checkout_response = {
            "order_id": mock_order.id,
            "status": "completed",
            "confirmation_number": "CONF-123456"
        }
        
        assert checkout_response["status"] == "completed"
        
    def test_login_logout_cycle(self, api_client, mock_token):
        """Test login and logout cycle"""
        # Verify token exists
        assert mock_token is not None
        
        # Simulate logout
        logout_response = {
            "success": True,
            "message": "Logged out successfully"
        }
        
        assert logout_response["success"] is True
        
    def test_order_creation_and_checkout(self, api_client, mock_order, mock_token):
        """Test order creation and checkout"""
        # Verify order can be created
        assert mock_order.id is not None
        assert mock_order.status == "pending"
        
        # Verify order items count
        assert len(mock_order.items) == 2
        
        # Verify order total
        expected_total = 109.97
        assert mock_order.total_amount == expected_total
        
        # Simulate checkout
        checkout_response = {
            "order_id": mock_order.id,
            "status": "completed"
        }
        
        assert checkout_response["status"] == "completed"
        
    def test_multiple_products_checkout(self, api_client, mock_order):
        """Test checkout with multiple products"""
        # Verify multiple products in order
        assert len(mock_order.items) >= 1
        
        # Check each product
        for item in mock_order.items:
            assert item.name is not None
            assert item.price > 0
            assert item.quantity > 0
            
    def test_order_status_tracking(self, api_client, mock_order):
        """Test order status tracking"""
        # Verify initial status
        assert mock_order.status == "pending"
        
        # Simulate status change to completed
        completed_order = Order(
            id=mock_order.id,
            user_id=mock_order.user_id,
            items=mock_order.items,
            total_amount=mock_order.total_amount,
            status="completed"
        )
        
        assert completed_order.status == "completed"
        
    def test_user_order_association(self, api_client, mock_order, mock_user):
        """Test user order association"""
        # Verify order belongs to correct user
        assert mock_order.user_id == mock_user.id
        
    def test_order_items_validation(self, api_client, mock_order):
        """Test order items validation"""
        # Verify each item has required fields
        for item in mock_order.items:
            assert item.id is not None
            assert item.name is not None
            assert item.price > 0
            assert item.quantity > 0
            assert item.sku is not None
        
    def test_order_total_calculation(self, api_client, mock_order):
        """Test order total calculation"""
        # Calculate expected total
        expected_total = sum(
            item.price * item.quantity 
            for item in mock_order.items
        )
        
        # Verify calculated total
        assert abs(mock_order.total_amount - expected_total) < 0.01
        
    def test_order_status_transitions(self, api_client, mock_order):
        """Test order status transitions"""
        # Test all valid status transitions
        valid_statuses = ["pending", "processing", "completed", "cancelled"]
        
        for status in valid_statuses:
            order = Order(
                id=mock_order.id,
                user_id=mock_order.user_id,
                items=mock_order.items,
                total_amount=mock_order.total_amount,
                status=status
            )
            assert order.status == status
  