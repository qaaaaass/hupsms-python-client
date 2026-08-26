"""
HupSMS Python Client Library
A Python client for interacting with the HupSMS API for SMS rental and sending services.
"""

from .client import HupSMSClient
from .exceptions import (
    HupSMSException,
    InvalidParametersError,
    ServiceNotFoundError,
    RentalLimitExceededError,
    InsufficientBalanceError,
    ServiceUnavailableError,
    InvalidNetworkError,
    NoNumberAvailableError,
    InvalidPhoneError,
    OrderNotFoundError,
    OrderNotActiveError,
    OrderExpiredError,
    SMSLimitReachedError,
    ReceiverNotAllowedError,
    SendFailedError,
    SMSAlreadySentError,
    CancelTooEarlyError,
    CancelLimitExceededError,
    CancelTimeExceededError,
    OrderNotPendingError,
    RerentCooldownActiveError,
    RerentNotSupportedError,
    RerentFailedError,
)

__version__ = "1.0.0"
__author__ = "HupSMS Python Client"
__all__ = [
    "HupSMSClient",
    "HupSMSException",
    "InvalidParametersError",
    "ServiceNotFoundError",
    "RentalLimitExceededError",
    "InsufficientBalanceError",
    "ServiceUnavailableError",
    "InvalidNetworkError",
    "NoNumberAvailableError",
    "InvalidPhoneError",
    "OrderNotFoundError",
    "OrderNotActiveError",
    "OrderExpiredError",
    "SMSLimitReachedError",
    "ReceiverNotAllowedError",
    "SendFailedError",
    "SMSAlreadySentError",
    "CancelTooEarlyError",
    "CancelLimitExceededError",
    "CancelTimeExceededError",
    "OrderNotPendingError",
    "RerentCooldownActiveError",
    "RerentNotSupportedError",
    "RerentFailedError",
]
