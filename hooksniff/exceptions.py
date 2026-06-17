class HookSniffError(Exception):
    """Base exception for HookSniff SDK."""
    def __init__(self, message: str, status_code: int = None, code: str = None):
        super().__init__(message)
        self.status_code = status_code
        self.code = code

class AuthenticationError(HookSniffError):
    """Invalid API key."""
    def __init__(self, message: str = "Invalid API key"):
        super().__init__(message, 401, "UNAUTHORIZED")

class NotFoundError(HookSniffError):
    """Resource not found."""
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, 404, "NOT_FOUND")

class RateLimitError(HookSniffError):
    """Rate limited."""
    def __init__(self, message: str = "Rate limited", retry_after: int = 60):
        super().__init__(message, 429, "RATE_LIMITED")
        self.retry_after = retry_after

class ValidationError(HookSniffError):
    """Validation failed."""
    def __init__(self, message: str = "Validation failed"):
        super().__init__(message, 400, "BAD_REQUEST")

class ServerError(HookSniffError):
    """Internal server error."""
    def __init__(self, message: str = "Internal server error"):
        super().__init__(message, 500, "INTERNAL_ERROR")

def map_error(status_code: int, body: dict) -> HookSniffError:
    error = body.get("error", {})
    code = error.get("code", "UNKNOWN")
    detail = error.get("detail") or error.get("message") or "Unknown error"
    
    if status_code == 401:
        return AuthenticationError(detail)
    elif status_code == 404:
        return NotFoundError(detail)
    elif status_code == 429:
        return RateLimitError(detail)
    elif status_code in (400, 422):
        return ValidationError(detail)
    elif status_code >= 500:
        return ServerError(detail)
    else:
        return HookSniffError(detail, status_code, code)
