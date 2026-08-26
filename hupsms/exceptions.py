"""
HupSMS API Exception classes
"""


class HupSMSException(Exception):
    """Base exception for all HupSMS errors"""
    
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"[{code}] {message}")


class InvalidParametersError(HupSMSException):
    """Raised when request parameters are invalid"""
    pass


class ServiceNotFoundError(HupSMSException):
    """Raised when service is not found"""
    pass


class RentalLimitExceededError(HupSMSException):
    """Raised when rental limit is exceeded"""
    pass


class InsufficientBalanceError(HupSMSException):
    """Raised when account balance is insufficient"""
    pass


class ServiceUnavailableError(HupSMSException):
    """Raised when service is unavailable"""
    pass


class InvalidNetworkError(HupSMSException):
    """Raised when network is invalid or prefix is not valid"""
    pass


class NoNumberAvailableError(HupSMSException):
    """Raised when no phone numbers are available"""
    pass


class InvalidPhoneError(HupSMSException):
    """Raised when phone number is invalid"""
    pass


class OrderNotFoundError(HupSMSException):
    """Raised when order is not found"""
    pass


class OrderNotActiveError(HupSMSException):
    """Raised when order is not active"""
    pass


class OrderExpiredError(HupSMSException):
    """Raised when order has expired"""
    pass


class SMSLimitReachedError(HupSMSException):
    """Raised when SMS limit has been reached"""
    pass


class ReceiverNotAllowedError(HupSMSException):
    """Raised when receiver number is not allowed"""
    pass


class SendFailedError(HupSMSException):
    """Raised when SMS sending fails"""
    pass


class SMSAlreadySentError(HupSMSException):
    """Raised when SMS has already been sent"""
    pass


class CancelTooEarlyError(HupSMSException):
    """Raised when cancellation is too early"""
    pass


class CancelLimitExceededError(HupSMSException):
    """Raised when cancel limit is exceeded"""
    pass


class CancelTimeExceededError(HupSMSException):
    """Raised when cancel time has exceeded"""
    pass


class OrderNotPendingError(HupSMSException):
    """Raised when order is not in pending status"""
    pass


class RerentCooldownActiveError(HupSMSException):
    """Raised when rerent cooldown is still active"""
    pass


class RerentNotSupportedError(HupSMSException):
    """Raised when rerent is not supported for this service"""
    pass


class RerentFailedError(HupSMSException):
    """Raised when rerent operation fails"""
    pass


# Error code to exception mapping
ERROR_CODE_MAP = {
    "INVALID_PARAMETERS": InvalidParametersError,
    "SERVICE_NOT_FOUND": ServiceNotFoundError,
    "RENTAL_LIMIT_EXCEEDED": RentalLimitExceededError,
    "INSUFFICIENT_BALANCE": InsufficientBalanceError,
    "SERVICE_UNAVAILABLE": ServiceUnavailableError,
    "INVALID_NETWORK": InvalidNetworkError,
    "NO_NUMBER_AVAILABLE": NoNumberAvailableError,
    "INVALID_PHONE": InvalidPhoneError,
    "ORDER_NOT_FOUND": OrderNotFoundError,
    "ORDER_NOT_ACTIVE": OrderNotActiveError,
    "ORDER_EXPIRED": OrderExpiredError,
    "SMS_LIMIT_REACHED": SMSLimitReachedError,
    "RECEIVER_NOT_ALLOWED": ReceiverNotAllowedError,
    "SEND_FAILED": SendFailedError,
    "SMS_ALREADY_SENT": SMSAlreadySentError,
    "CANCEL_TOO_EARLY": CancelTooEarlyError,
    "CANCEL_LIMIT_EXCEEDED": CancelLimitExceededError,
    "CANCEL_TIME_EXCEEDED": CancelTimeExceededError,
    "ORDER_NOT_PENDING": OrderNotPendingError,
    "RERENT_COOLDOWN_ACTIVE": RerentCooldownActiveError,
    "RERENT_NOT_SUPPORTED": RerentNotSupportedError,
    "RERENT_FAILED": RerentFailedError,
}


def raise_for_error(code: str, message: str) -> None:
    """Raise appropriate exception based on error code"""
    exception_class = ERROR_CODE_MAP.get(code, HupSMSException)
    raise exception_class(code, message)
