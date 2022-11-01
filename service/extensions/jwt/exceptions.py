class BearerInvalidTokenError(Exception):
    """Invalid Bearer Token Error"""

    description: str = "Invalid Bearer Token"


class InvalidTokenError(Exception):
    """Invalid Token"""

    description: str = "Invalid Token"


class ExpiredTokenError(Exception):
    """Expired Token"""

    description: str = "Expired Token"
