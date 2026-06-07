# Task Management REST API

A simple and clean REST API for managing tasks, built with Flask.

## Features

- ✅ Create, read, update, and delete tasks
- ✅ Input validation and error handling
- ✅ Persistent data storage (JSON file)
- ✅ CORS support for frontend integration
- ✅ Clean and consistent API responses

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the API:
```bash
python api.py
```

The API will start at `http://localhost:5000`

## API Endpoints

### Get All Tasks
```
GET /tasks
```
Returns all tasks in the system.

**Response (200):**
```json
{
  "success": true,
  "count": 2,
  "data": [
    {
      "id": 1,
      "title": "Buy groceries",
      "description": "Milk, eggs, bread",
      "completed": false,
      "created_at": "2026-05-10T10:30:00.000000",
      "updated_at": "2026-05-10T10:30:00.000000"
    }
  ]
}
```

### Create a Task
```
POST /tasks
Content-Type: application/json

{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

**Response (201):**
```json
{
  "success": true,
  "message": "Task created successfully",
  "data": {
    "id": 1,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false,
    "created_at": "2026-05-10T10:30:00.000000",
    "updated_at": "2026-05-10T10:30:00.000000"
  }
}
```

### Update a Task
```
PUT /tasks/:id
Content-Type: application/json

{
  "title": "Buy groceries",
  "description": "Updated description",
  "completed": true
}
```

**Response (200):**
```json
{
  "success": true,
  "message": "Task updated successfully",
  "data": { ... }
}
```

### Delete a Task
```
DELETE /tasks/:id
```

**Response (200):**
```json
{
  "success": true,
  "message": "Task 1 deleted successfully"
}
```

## Error Handling

### Validation Error (400)
```json
{
  "error": "Validation error",
  "message": "Task title is required and must be a string"
}
```

### Not Found (404)
```json
{
  "error": "Not found",
  "message": "Task with id 999 not found"
}
```

## Data Validation

- **title** (required): Must be a non-empty string
- **description** (optional): Additional task details
- **completed** (optional): Boolean flag for task completion status

## File Structure

- `api.py` - Main Flask application with all endpoints
- `requirements.txt` - Python dependencies
- `tasks.json` - Persistent storage for tasks
- `README.md` - This file

## Testing

You can test the API using curl, Postman, or any HTTP client:

```bash
# Get all tasks
curl http://localhost:5000/tasks

# Create a task
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"New task","description":"Task description"}'

# Update a task
curl -X PUT http://localhost:5000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"title":"Updated title","completed":true}'

# Delete a task
curl -X DELETE http://localhost:5000/tasks/1
```

## Health Check

```
GET /health
```

Returns API status:
```json
{
  "status": "API is running"
}
```