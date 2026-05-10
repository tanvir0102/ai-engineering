from datetime import datetime

def format_date(date_obj, format_string="%Y-%m-%d"):
    """
    Format a datetime object into a string.

    Args:
        date_obj: datetime object or string
        format_string: desired output format (default: YYYY-MM-DD)

    Returns:
        Formatted date string
    """
    if isinstance(date_obj, str):
        date_obj = datetime.fromisoformat(date_obj)

    return date_obj.strftime(format_string)

def get_readable_date(date_obj):
    """Format date in a human-readable way (e.g., 'Jan 10, 2026')"""
    return format_date(date_obj, "%b %d, %Y")

def get_time_ago(date_obj):
    """Return a simple 'time ago' string"""
    now = datetime.now()
    if isinstance(date_obj, str):
        date_obj = datetime.fromisoformat(date_obj)

    diff = now - date_obj
    seconds = diff.total_seconds()

    if seconds < 60:
        return "just now"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
    elif seconds < 86400:
        hours = int(seconds // 3600)
        return f"{hours} hour{'s' if hours > 1 else ''} ago"
    else:
        days = int(seconds // 86400)
        return f"{days} day{'s' if days > 1 else ''} ago"