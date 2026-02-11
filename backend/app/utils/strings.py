"""
Utility for generating random strings
"""
import secrets
import string


def generate_random_string(length: int = 32) -> str:
    """Generate a random string of specified length"""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def generate_secret_key() -> str:
    """Generate a secure secret key"""
    return secrets.token_urlsafe(32)
