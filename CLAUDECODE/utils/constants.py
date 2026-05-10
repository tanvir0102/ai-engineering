APP_NAME = "TaskManager"
APP_VERSION = "1.0.0"
AUTHOR = "Tanvir"

DATABASE_NAME = "taskmanager.db"
LOG_FILE = "app.log"

ALLOWED_FILE_TYPES = ['.txt', '.pdf', '.doc', '.docx', '.xlsx', '.csv']
MAX_FILE_SIZE = 10 * 1024 * 1024

TIMEZONE = "UTC"
DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H:%M:%S"

HTTP_STATUS_OK = 200
HTTP_STATUS_CREATED = 201
HTTP_STATUS_BAD_REQUEST = 400
HTTP_STATUS_UNAUTHORIZED = 401
HTTP_STATUS_FORBIDDEN = 403
HTTP_STATUS_NOT_FOUND = 404
HTTP_STATUS_SERVER_ERROR = 500

COLORS = {
    "primary": "#667eea",
    "secondary": "#764ba2",
    "success": "#2e7d32",
    "warning": "#f57c00",
    "danger": "#c62828"
}