# Common status codes
HTTP_OK = 200
HTTP_CREATED = 201
HTTP_BAD_REQUEST = 400
HTTP_UNAUTHORIZED = 401
HTTP_FORBIDDEN = 403
HTTP_NOT_FOUND = 404
HTTP_INTERNAL_ERROR = 500

# User roles
ROLE_ADMIN = "admin"
ROLE_USER = "user"
ROLE_GUEST = "guest"

# Task statuses
TASK_PENDING = "pending"
TASK_IN_PROGRESS = "in_progress"
TASK_COMPLETED = "completed"
TASK_CANCELLED = "cancelled"

# Date formats
DATE_FORMAT_SHORT = "%Y-%m-%d"
DATE_FORMAT_LONG = "%B %d, %Y"
DATETIME_FORMAT_ISO = "%Y-%m-%dT%H:%M:%S"
DATETIME_FORMAT_US = "%m/%d/%Y %I:%M %p"

# Pagination
DEFAULT_PAGE_SIZE = 10
MAX_PAGE_SIZE = 100

# Time constants (in seconds)
MINUTES_5 = 5 * 60
HOUR_1 = 60 * 60
DAY_1 = 24 * 60 * 60
WEEK_1 = 7 * 24 * 60 * 60

# File size limits (in bytes)
MAX_FILE_SIZE_MB = 10
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

# Common error messages
ERROR_INVALID_EMAIL = "Invalid email address"
ERROR_INVALID_PASSWORD = "Password does not meet requirements"
ERROR_UNAUTHORIZED = "You are not authorized to perform this action"
ERROR_NOT_FOUND = "The requested resource was not found"
ERROR_SERVER_ERROR = "An internal server error occurred"

# Success messages
SUCCESS_CREATED = "Resource created successfully"
SUCCESS_UPDATED = "Resource updated successfully"
SUCCESS_DELETED = "Resource deleted successfully"
SUCCESS_LOGIN = "Login successful"
