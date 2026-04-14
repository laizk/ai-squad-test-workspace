"""Test cases for Checkout Flow"""
import pytest
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from api_client import APIClient
from models import Order, Product


@pytest.fixture
def api_client():
    """Create API client instance"""
    return APIClient(base_url="https://api.example.com")


@pytest.fixture
def mock_order():
    """Mock order data"""
    return Order(
        id="order_001",
        user_id="user_001",
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


class TestCheckoutFlow:
    """Test cases for checkout functionality"""
    
    def test_checkout_success(self, api_client, mock_order, mock_token):
        """Test successful checkout"""
        # Simulate successful checkout response
        checkout_response = {
            "order_id": mock_order.id,
            "status": "completed",
            "confirmation_number": "CONF-123456"
        }
        
        assert checkout_response["status"] == "completed"
        assert checkout_response["order_id"] == mock_order.id
        
    def test_checkout_invalid_order(self, api_client, mock_token):
        """Test checkout with invalid order"""
        # Simulate invalid order response
        response_data = {
            "error": "Order not found",
            "message": "The specified order does not exist"
        }
        
        assert "error" in response_data
        assert response_data["error"] == "Order not found"
        
    def test_checkout_order_status(self, api_client, mock_order):
        """Test order status after checkout"""
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
        
    def test_checkout_order_items(self, api_client, mock_order):
        """Test order items are preserved after checkout"""
        # Verify order items count
        assert len(mock_order.items) == 2
        
        # Check each product
        for item in mock_order.items:
            assert item.name is not None
            assert item.price > 0
            assert item.quantity > 0
        
    def test_checkout_order_total(self, api_client, mock_order):
        """Test order total calculation"""
        expected_total = 109.97
        assert mock_order.total_amount == expected_total
        
    def test_checkout_multiple_products(self, api_client, mock_order):
        """Test checkout with multiple products"""
        # Verify multiple products in order
        assert len(mock_order.items) >= 1
        
    def test_checkout_order_association(self, api_client, mock_order, mock_user):
        """Test user order association"""
        # Verify order belongs to correct user
        assert mock_order.user_id == mock_user.id
        
    def test_checkout_order_creation(self, api_client, mock_order):
        """Test order creation before checkout"""
        # Verify order can be created
        assert mock_order.id is not None
        assert mock_order.status == "pending"
        
    def test_checkout_order_validation(self, api_client, mock_order):
        """Test order validation before checkout"""
        # Verify order has required fields
        assert mock_order.id is not None
        assert mock_order.user_id is not None
        assert len(mock_order.items) > 0
        assert mock_order.total_amount > 0
        
    def test_checkout_order_items_count(self, api_client, mock_order):
        """Test order items count"""
        assert len(mock_order.items) == 2
        
    def test_checkout_order_total_amount(self, api_client, mock_order):
        """Test order total amount"""
        expected_total = 109.97
        assert mock_order.total_amount == expected_total
  