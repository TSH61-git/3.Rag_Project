# API Documentation

## Base URL

```
http://localhost:5000/api
```

## Authentication

All protected endpoints require a JWT token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

## Response Format

All responses follow this structure:

```json
{
  "success": true/false,
  "message": "Optional message",
  "data": {}, // or []
  "count": 0  // For list responses
}
```

---

## Authentication Endpoints

### Register User

Create a new user account.

**Endpoint**: `POST /auth/register`  
**Access**: Public

**Request Body**:
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepass123"
}
```

**Validation Rules**:
- username: 3-30 characters, required
- email: valid email format, required
- password: minimum 6 characters, required

**Success Response** (201 Created):
```json
{
  "success": true,
  "message": "User registered successfully",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "id": "507f1f77bcf86cd799439011",
      "username": "john_doe",
      "email": "john@example.com"
    }
  }
}
```

**Error Responses**:
- 400: Validation error or user already exists
- 500: Server error

---

### Login User

Authenticate an existing user.

**Endpoint**: `POST /auth/login`  
**Access**: Public

**Request Body**:
```json
{
  "email": "john@example.com",
  "password": "securepass123"
}
```

**Success Response** (200 OK):
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "id": "507f1f77bcf86cd799439011",
      "username": "john_doe",
      "email": "john@example.com"
    }
  }
}
```

**Error Responses**:
- 400: Validation error
- 401: Invalid email or password
- 500: Server error

---

## Task Endpoints

All task endpoints require authentication.

### Get All Tasks

Retrieve all tasks for the authenticated user with optional filters.

**Endpoint**: `GET /tasks`  
**Access**: Private (requires authentication)

**Query Parameters**:
- `status`: Filter by status (pending, in-progress, completed)
- `priority`: Filter by priority (low, medium, high)
- `category`: Filter by category (work, personal, shopping, health, other)
- `search`: Search in title and description (case-insensitive)

**Examples**:
```
GET /tasks
GET /tasks?status=pending
GET /tasks?priority=high&category=work
GET /tasks?search=meeting
```

**Success Response** (200 OK):
```json
{
  "success": true,
  "count": 2,
  "data": [
    {
      "_id": "507f1f77bcf86cd799439011",
      "title": "Complete project documentation",
      "description": "Write comprehensive API docs",
      "status": "in-progress",
      "priority": "high",
      "category": "work",
      "dueDate": "2024-03-15T00:00:00.000Z",
      "user": "507f1f77bcf86cd799439012",
      "createdAt": "2024-03-10T10:00:00.000Z",
      "updatedAt": "2024-03-10T10:00:00.000Z"
    },
    {
      "_id": "507f1f77bcf86cd799439013",
      "title": "Buy groceries",
      "description": "Milk, eggs, bread",
      "status": "pending",
      "priority": "medium",
      "category": "shopping",
      "dueDate": null,
      "user": "507f1f77bcf86cd799439012",
      "createdAt": "2024-03-09T15:30:00.000Z",
      "updatedAt": "2024-03-09T15:30:00.000Z"
    }
  ]
}
```

**Error Responses**:
- 401: Unauthorized (invalid/missing token)
- 500: Server error

---

### Get Single Task

Retrieve a specific task by ID.

**Endpoint**: `GET /tasks/:id`  
**Access**: Private (requires authentication, owner only)

**Success Response** (200 OK):
```json
{
  "success": true,
  "data": {
    "_id": "507f1f77bcf86cd799439011",
    "title": "Complete project documentation",
    "description": "Write comprehensive API docs",
    "status": "in-progress",
    "priority": "high",
    "category": "work",
    "dueDate": "2024-03-15T00:00:00.000Z",
    "user": "507f1f77bcf86cd799439012",
    "createdAt": "2024-03-10T10:00:00.000Z",
    "updatedAt": "2024-03-10T10:00:00.000Z"
  }
}
```

**Error Responses**:
- 401: Unauthorized
- 404: Task not found
- 500: Server error

---

### Create Task

Create a new task.

**Endpoint**: `POST /tasks`  
**Access**: Private (requires authentication)

**Request Body**:
```json
{
  "title": "Complete project documentation",
  "description": "Write comprehensive API docs",
  "priority": "high",
  "category": "work",
  "dueDate": "2024-03-15"
}
```

**Required Fields**:
- title (max 100 characters)

**Optional Fields**:
- description (max 500 characters)
- status (default: "pending")
- priority (default: "medium")
- category (default: "other")
- dueDate (ISO 8601 date)

**Success Response** (201 Created):
```json
{
  "success": true,
  "message": "Task created successfully",
  "data": {
    "_id": "507f1f77bcf86cd799439011",
    "title": "Complete project documentation",
    "description": "Write comprehensive API docs",
    "status": "pending",
    "priority": "high",
    "category": "work",
    "dueDate": "2024-03-15T00:00:00.000Z",
    "user": "507f1f77bcf86cd799439012",
    "createdAt": "2024-03-10T10:00:00.000Z",
    "updatedAt": "2024-03-10T10:00:00.000Z"
  }
}
```

**Error Responses**:
- 400: Validation error
- 401: Unauthorized
- 500: Server error

---

### Update Task

Update an existing task.

**Endpoint**: `PUT /tasks/:id`  
**Access**: Private (requires authentication, owner only)

**Request Body** (all fields optional):
```json
{
  "title": "Updated title",
  "description": "Updated description",
  "status": "completed",
  "priority": "low",
  "category": "personal",
  "dueDate": "2024-03-20"
}
```

**Success Response** (200 OK):
```json
{
  "success": true,
  "message": "Task updated successfully",
  "data": {
    "_id": "507f1f77bcf86cd799439011",
    "title": "Updated title",
    "description": "Updated description",
    "status": "completed",
    "priority": "low",
    "category": "personal",
    "dueDate": "2024-03-20T00:00:00.000Z",
    "user": "507f1f77bcf86cd799439012",
    "createdAt": "2024-03-10T10:00:00.000Z",
    "updatedAt": "2024-03-11T14:30:00.000Z"
  }
}
```

**Error Responses**:
- 400: Validation error
- 401: Unauthorized
- 404: Task not found
- 500: Server error

---

### Delete Task

Delete a task.

**Endpoint**: `DELETE /tasks/:id`  
**Access**: Private (requires authentication, owner only)

**Success Response** (200 OK):
```json
{
  "success": true,
  "message": "Task deleted successfully"
}
```

**Error Responses**:
- 401: Unauthorized
- 404: Task not found
- 500: Server error

---

## Error Codes

| Code | Meaning |
|------|---------|
| 200 | OK - Request successful |
| 201 | Created - Resource created successfully |
| 400 | Bad Request - Validation error or invalid data |
| 401 | Unauthorized - Authentication required or failed |
| 404 | Not Found - Resource not found |
| 429 | Too Many Requests - Rate limit exceeded |
| 500 | Internal Server Error - Server error |

---

## Rate Limiting

All API endpoints are rate-limited to prevent abuse:

- **Window**: 15 minutes
- **Max Requests**: 100 per IP address

When rate limit is exceeded:
```json
{
  "success": false,
  "message": "Too many requests from this IP, please try again later."
}
```

---

## Example Workflow

### 1. Register a new user
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepass123"
  }'
```

### 2. Login (or use token from registration)
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "securepass123"
  }'
```

### 3. Create a task
```bash
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "title": "Complete project",
    "priority": "high",
    "category": "work"
  }'
```

### 4. Get all tasks
```bash
curl -X GET http://localhost:5000/api/tasks \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### 5. Update a task
```bash
curl -X PUT http://localhost:5000/api/tasks/TASK_ID \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "status": "completed"
  }'
```

### 6. Delete a task
```bash
curl -X DELETE http://localhost:5000/api/tasks/TASK_ID \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## Testing with Postman

1. Import the API endpoints into Postman
2. Create an environment variable for `token`
3. After login/register, save the token to the environment
4. Use `{{token}}` in Authorization header for protected routes

---

## Common Issues

### Issue: "No token provided"
**Solution**: Make sure to include the Authorization header with Bearer token

### Issue: "Invalid token"
**Solution**: Token may be expired or malformed. Login again to get a new token

### Issue: "Task not found"
**Solution**: Verify the task ID and that the task belongs to the authenticated user

### Issue: "Too many requests"
**Solution**: Wait 15 minutes or reduce request frequency
