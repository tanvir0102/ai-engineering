from datetime import datetime, timedelta

def format_date(date, format_str="%Y-%m-%d"):
    """Format a date object or string into a specified format.

    Args:
        date: datetime object or string representation
        format_str: desired output format (default: YYYY-MM-DD)

    Returns:
        Formatted date string
    """
    if isinstance(date, str):
        date = datetime.fromisoformat(date)
    return date.strftime(format_str)

def format_datetime(dt, format_str="%Y-%m-%d %H:%M:%S"):
    """Format a datetime object into a specified format.

    Args:
        dt: datetime object or string representation
        format_str: desired output format (default: YYYY-MM-DD HH:MM:SS)

    Returns:
        Formatted datetime string
    """
    if isinstance(dt, str):
        dt = datetime.fromisoformat(dt)
    return dt.strftime(format_str)

def time_ago(date):
    """Return a human-readable relative time string.

    Args:
        date: datetime object or ISO format string

    Returns:
        String like "2 hours ago" or "3 days ago"
    """
    if isinstance(date, str):
        date = datetime.fromisoformat(date)

    now = datetime.now()
    delta = now - date

    if delta.total_seconds() < 60:
        return "just now"
    elif delta.total_seconds() < 3600:
        minutes = int(delta.total_seconds() // 60)
        return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
    elif delta.total_seconds() < 86400:
        hours = int(delta.total_seconds() // 3600)
        return f"{hours} hour{'s' if hours > 1 else ''} ago"
    else:
        days = delta.days
        return f"{days} day{'s' if days > 1 else ''} ago"
