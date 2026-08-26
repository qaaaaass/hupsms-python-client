"""
HupSMS API Client
Main client class for interacting with HupSMS API
"""

import requests
from typing import Optional, List, Dict, Any
from urllib.parse import quote

from .exceptions import raise_for_error


class HupSMSClient:
    """
    HupSMS API Client for SMS rental and sending services
    
    Example:
        >>> client = HupSMSClient(api_key="your_api_key")
        >>> services = client.get_services()
        >>> order = client.create_rental(service_id=1, networks="VIETTEL")
        >>> client.send_sms(order["orderId"], "0901234567", "Hello!")
    """
    
    BASE_URL = "https://hupsms.com/api/v1"
    
    def __init__(self, api_key: str):
        """
        Initialize HupSMS client
        
        Args:
            api_key (str): Your HupSMS API key
        """
        self.api_key = api_key
        self.session = requests.Session()
    
    def _make_request(self, method: str, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Make HTTP request to HupSMS API
        
        Args:
            method (str): HTTP method (GET, POST, etc.)
            endpoint (str): API endpoint path
            params (dict, optional): Query parameters
            
        Returns:
            dict: Response data
            
        Raises:
            HupSMSException: If API returns an error
        """
        url = f"{self.BASE_URL}{endpoint}"
        
        # Add API key to params
        if params is None:
            params = {}
        params["api_key"] = self.api_key
        
        response = self.session.request(method, url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        # Check if response indicates an error
        if data.get("status") != "success":
            error_code = data.get("code", "UNKNOWN_ERROR")
            error_message = data.get("message", "Unknown error")
            raise_for_error(error_code, error_message)
        
        return data.get("data", {})
    
    def get_services(self) -> List[Dict[str, Any]]:
        """
        Get list of available SMS rental services
        
        Returns:
            list: List of available services with details
            
        Example:
            >>> services = client.get_services()
            >>> for service in services:
            ...     print(f"{service['name']}: {service['price']} VND")
        """
        return self._make_request("GET", "/sms/services")
    
    def create_rental(
        self,
        service_id: int,
        networks: Optional[str] = None,
        prefixes: Optional[List[str]] = None,
        exclude_prefixes: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Rent a phone number for SMS sending
        
        Args:
            service_id (int): Service ID from get_services()
            networks (str, optional): Desired network (e.g., "VIETTEL")
            prefixes (list, optional): Desired prefixes (max 15), e.g., ["032", "033"]
            exclude_prefixes (list, optional): Prefixes to exclude (max 15), e.g., ["086", "096"]
            
        Returns:
            dict: Order details including phone number and order ID
            
        Example:
            >>> order = client.create_rental(
            ...     service_id=1,
            ...     networks="VIETTEL",
            ...     prefixes=["032", "033"]
            ... )
            >>> print(f"Rented: {order['phone']}")
        """
        params = {"serviceId": service_id}
        
        if networks:
            params["networks"] = networks
        if prefixes:
            params["prefixes"] = ",".join(prefixes)
        if exclude_prefixes:
            params["excludePrefixes"] = ",".join(exclude_prefixes)
        
        return self._make_request("GET", "/sms/create", params)
    
    def send_sms(
        self,
        order_id: str,
        receiver_number: str,
        content: str
    ) -> Dict[str, Any]:
        """
        Send SMS from rented phone number
        
        Args:
            order_id (str): Order ID from create_rental()
            receiver_number (str): Recipient phone number (9-12 digits)
            content (str): SMS content (1-500 characters)
            
        Returns:
            dict: SMS sending result with remaining SMS count
            
        Example:
            >>> result = client.send_sms("HupSMSnE8fG2hJ", "0901234567", "Hello!")
            >>> print(f"Remaining SMS: {result['remaining']}")
        """
        # Validate inputs
        if not receiver_number or len(receiver_number) < 9 or len(receiver_number) > 12:
            raise ValueError("Receiver number must be 9-12 digits")
        
        if not content or len(content) < 1 or len(content) > 500:
            raise ValueError("Content must be 1-500 characters")
        
        params = {
            "receiverNumber": receiver_number,
            "content": content
        }
        
        return self._make_request("GET", f"/sms/{order_id}/send", params)
    
    def check_order(self, order_id: str) -> Dict[str, Any]:
        """
        Check SMS order status
        
        Args:
            order_id (str): Order ID to check
            
        Returns:
            dict: Order status and details including received OTP if any
            
        Example:
            >>> order_info = client.check_order("HupSMSnE8fG2hJ")
            >>> print(f"Status: {order_info['status']}")
            >>> if order_info.get('otp'):
            ...     print(f"Received OTP: {order_info['otp']}")
        """
        return self._make_request("GET", f"/sms/{order_id}/check")
    
    def cancel_order(self, order_id: str) -> Dict[str, Any]:
        """
        Cancel SMS rental order and get refund
        
        Note: Can only cancel within 3 minutes and if no SMS has been sent
        
        Args:
            order_id (str): Order ID to cancel
            
        Returns:
            dict: Refund amount
            
        Example:
            >>> result = client.cancel_order("HupSMSnE8fG2hJ")
            >>> print(f"Refunded: {result['refund']} VND")
        """
        return self._make_request("GET", f"/sms/{order_id}/cancel")
    
    def get_sms_history(self, order_id: str) -> List[Dict[str, Any]]:
        """
        Get SMS sending history for an order
        
        Args:
            order_id (str): Order ID to get history for
            
        Returns:
            list: List of sent SMS messages with details
            
        Example:
            >>> history = client.get_sms_history("HupSMSnE8fG2hJ")
            >>> for sms in history:
            ...     print(f"To {sms['toPhone']}: {sms['content']}")
        """
        result = self._make_request("GET", f"/sms/{order_id}/history")
        return result.get("history", [])
    
    def rerent_sms(self, phone: str) -> Dict[str, Any]:
        """
        Rent the same phone number again
        
        Note: Phone must be from a completed/expired/cancelled order
        
        Args:
            phone (str): Phone number to rerent (accepts formats like 0987654321, 987654321, 84987654321, +84987654321)
            
        Returns:
            dict: New order details
            
        Example:
            >>> new_order = client.rerent_sms("0987654321")
            >>> print(f"New order ID: {new_order['orderId']}")
        """
        params = {"phone": phone}
        return self._make_request("GET", "/sms/rerent", params)
    
    def close(self):
        """Close the HTTP session"""
        self.session.close()
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
