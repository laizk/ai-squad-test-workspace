"""API Client for Login and Checkout operations"""
import sys
import os
from typing import Optional, Dict, Any

# Lazy import to avoid ImportError when tests don't use actual API calls
requests = None


class APIClient:
    """Client for interacting with the API"""
    
    def __init__(self, base_url: str = "https://api.example.com", timeout: int = 30):
        self.base_url = base_url
        self.timeout = timeout
        self.session = None
        self.session_headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    
    def _ensure_requests(self):
        """Lazy import of requests module"""
        global requests
        if requests is None:
            try:
                import requests as req
                requests = req
            except ImportError:
                # If requests is not available, raise a more descriptive error
                raise ImportError(
                    "The 'requests' library is required for API operations. "
                    "Install it with: pip install requests"
                )
        return requests
    
    def _init_session(self):
        """Initialize session with headers"""
        if self.session is None:
            requests = self._ensure_requests()
            self.session = requests.Session()
            self.session.headers.update(self.session_headers)
    
    def login(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """Perform login and return session token"""
        requests = self._ensure_requests()
        url = f"{self.base_url}/auth/login"
        payload = {"username": username, "password": password}
        response = self.session.post(url, json=payload, timeout=self.timeout)
        response.raise_for_status()
        return response.json()
    
    def logout(self, token: str) -> bool:
        """Perform logout"""
        requests = self._ensure_requests()
        url = f"{self.base_url}/auth/logout"
        headers = {"Authorization": f"Bearer {token}"}
        response = self.session.post(url, headers=headers, timeout=self.timeout)
        return response.status_code in [200, 204]
    
    def get_user(self, token: str, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user information"""
        requests = self._ensure_requests()
        url = f"{self.base_url}/users/{user_id}"
        headers = {"Authorization": f"Bearer {token}"}
        response = self.session.get(url, headers=headers, timeout=self.timeout)
        response.raise_for_status()
        return response.json()
    
    def create_order(self, token: str, items: list) -> Optional[Dict[str, Any]]:
        """Create a new order"""
        requests = self._ensure_requests()
        url = f"{self.base_url}/orders"
        headers = {"Authorization": f"Bearer {token}"}
        payload = {"items": items}
        response = self.session.post(url, headers=headers, json=payload, timeout=self.timeout)
        response.raise_for_status()
        return response.json()
    
    def checkout(self, token: str, order_id: str) -> Optional[Dict[str, Any]]:
        """Process checkout for an order"""
        requests = self._ensure_requests()
        url = f"{self.base_url}/orders/{order_id}/checkout"
        headers = {"Authorization": f"Bearer {token}"}
        response = self.session.post(url, headers=headers, timeout=self.timeout)
        response.raise_for_status()
        return response.json()
    
    def get_order_status(self, token: str, order_id: str) -> Optional[Dict[str, Any]]:
        """Get order status"""
        requests = self._ensure_requests()
        url = f"{self.base_url}/orders/{order_id}/status"
        headers = {"Authorization": f"Bearer {token}"}
        response = self.session.get(url, headers=headers, timeout=self.timeout)
        response.raise_for_status()
        return response.json()
    
    def get(self, url: str, headers: Optional[Dict[str, str]] = None) -> Optional[Dict[str, Any]]:
        """Generic GET request"""
        requests = self._ensure_requests()
        response = self.session.get(url, headers=headers or {}, timeout=self.timeout)
        response.raise_for_status()
        return response.json()
    
    def post(self, url: str, headers: Optional[Dict[str, str]] = None, json_data: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """Generic POST request"""
        requests = self._ensure_requests()
        response = self.session.post(url, headers=headers or {}, json=json_data, timeout=self.timeout)
        response.raise_for_status()
        return response.json()
    
    def put(self, url: str, headers: Optional[Dict[str, str]] = None, json_data: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """Generic PUT request"""
        requests = self._ensure_requests()
        response = self.session.put(url, headers=headers or {}, json=json_data, timeout=self.timeout)
        response.raise_for_status()
        return response.json()
    
    def delete(self, url: str, headers: Optional[Dict[str, str]] = None) -> bool:
        """Generic DELETE request"""
        requests = self._ensure_requests()
        response = self.session.delete(url, headers=headers or {}, timeout=self.timeout)
        return response.status_code in [200, 204]
  