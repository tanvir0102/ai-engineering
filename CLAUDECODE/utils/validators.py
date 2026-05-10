import re

def validate_email(email):
    """
    Validate an email address.

    Args:
        email: email string to validate

    Returns:
        True if valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_phone(phone):
    """Validate a phone number (basic format: XXX-XXX-XXXX or XXXXXXXXXX)"""
    pattern = r'^(\d{3}-\d{3}-\d{4}|\d{10})$'
    return bool(re.match(pattern, phone))

def validate_url(url):
    """Validate a URL"""
    pattern = r'^https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}.*$'
    return bool(re.match(pattern, url))

def validate_username(username, min_length=3, max_length=20):
    """Validate a username (alphanumeric and underscores only)"""
    if not (min_length <= len(username) <= max_length):
        return False
    pattern = r'^[a-zA-Z0-9_]+$'
    return bool(re.match(pattern, username))