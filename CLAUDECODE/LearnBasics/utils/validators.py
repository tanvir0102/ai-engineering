import re

def validate_email(email):
    """Validate an email address format.

    Args:
        email: email address string to validate

    Returns:
        True if email is valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """Validate a phone number (10+ digits with optional +, -, () symbols).

    Args:
        phone: phone number string to validate

    Returns:
        True if phone is valid, False otherwise
    """
    pattern = r'^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,}$'
    return re.match(pattern, phone) is not None

def validate_url(url):
    """Validate a URL format.

    Args:
        url: URL string to validate

    Returns:
        True if URL is valid, False otherwise
    """
    pattern = r'^https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(/.*)?$'
    return re.match(pattern, url) is not None

def validate_password(password, min_length=8):
    """Validate password strength.

    Args:
        password: password string to validate
        min_length: minimum password length (default: 8)

    Returns:
        Dictionary with validation result and any error messages
    """
    errors = []

    if len(password) < min_length:
        errors.append(f"Password must be at least {min_length} characters")
    if not re.search(r'[a-z]', password):
        errors.append("Password must contain lowercase letters")
    if not re.search(r'[A-Z]', password):
        errors.append("Password must contain uppercase letters")
    if not re.search(r'[0-9]', password):
        errors.append("Password must contain numbers")
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        errors.append("Password must contain special characters")

    return {
        "valid": len(errors) == 0,
        "errors": errors
    }
