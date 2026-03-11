# Task Manager API - Technical Specification

## Project Overview

A RESTful API for task management with user authentication, designed to help users organize and track their tasks efficiently.

## Technical Stack

### Backend Framework
**Decision Date**: 2024-03-01  
**Choice**: Node.js with Express.js  
**Reasoning**: 
- Fast development cycle
- Large ecosystem of packages
- Excellent for RESTful APIs
- Non-blocking I/O for better performance

### Database
**Decision Date**: 2024-03-01  
**Choice**: MongoDB with Mongoose ODM  
**Reasoning**:
- Flexible schema for task attributes
- Easy to scale horizontally
- JSON-like documents match JavaScript objects
- Mongoose provides excellent validation and middleware

### Authentication
**Decision Date**: 2024-03-02  
**Choice**: JWT (JSON Web Tokens)  
**Reasoning**:
- Stateless authentication
- Easy to scale across multiple servers
- Industry standard
- Works well with mobile and web clients

**Token Expiration**: 7 days  
**Security**: bcryptjs with salt rounds of 10

## Data Models

### User Model

```javascript
{
  username: String (3-30 chars, unique, required),
  email: String (valid email, unique, required),
  password: String (hashed, min 6 chars, required),
  createdAt: Date (auto-generated)
}
```

**Security Rules**:
- Passwords are hashed before storage using bcryptjs
- Password comparison uses constant-time comparison
- Email is stored in lowercase
- Username is trimmed of whitespace

### Task Model

```javascript
{
  title: String (max 100 chars, required),
  description: String (max 500 chars, optional),
  status: Enum ['pending', 'in-progress', 'completed'],
  priority: Enum ['low', 'medium', 'high'],
  category: Enum ['work', 'personal', 'shopping', 'health', 'other'],
  dueDate: Date (optional),
  user: ObjectId (reference to User, required),
  createdAt: Date (auto-generated),
  updatedAt: Date (auto-updated)
}
```

**Business Rules**:
- Default status: 'pending'
- Default priority: 'medium'
- Default category: 'other'
- Tasks are user-specific (isolated by user ID)
- updatedAt is automatically updated on save

## API Design

### URL Structure
**Decision**: RESTful URL path versioning  
**Format**: `/api/{resource}/{id}`  
**Example**: `/api/tasks/123`

### Response Format
**Decision**: Consistent JSON structure  
**Format**:
```json
{
  "success": boolean,
  "message": string (optional),
  "data": object/array (optional),
  "count": number (for lists)
}
```

### HTTP Status Codes
- `200 OK`: Successful GET, PUT
- `201 Created`: Successful POST
- `400 Bad Request`: Validation errors
- `401 Unauthorized`: Authentication required/failed
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server errors

## Security Measures

### Rate Limiting
**Decision Date**: 2024-03-03  
**Configuration**:
- Window: 15 minutes
- Max requests: 100 per IP
- Applies to all `/api/*` routes

**Warning**: Do not modify rate limiting without security review. This protects against brute force attacks.

### Input Validation
**Decision**: Joi validation library  
**Reasoning**:
- Schema-based validation
- Clear error messages
- Prevents injection attacks
- Validates data types and formats

**Validation Rules**:
- All user inputs are validated before processing
- Email format validation using regex
- Password minimum length: 6 characters
- Username length: 3-30 characters
- Task title max: 100 characters
- Task description max: 500 characters

### Authentication Flow

1. User registers/logs in
2. Server generates JWT with user ID
3. Client stores token (localStorage/cookie)
4. Client sends token in Authorization header: `Bearer <token>`
5. Server verifies token on protected routes
6. Server attaches user object to request

**Token Structure**:
```javascript
{
  userId: ObjectId,
  iat: timestamp,
  exp: timestamp
}
```

## API Endpoints

### Authentication Endpoints

#### POST /api/auth/register
**Purpose**: Create new user account  
**Access**: Public  
**Request Body**:
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepass123"
}
```
**Response**: JWT token + user data

#### POST /api/auth/login
**Purpose**: Authenticate existing user  
**Access**: Public  
**Request Body**:
```json
{
  "email": "john@example.com",
  "password": "securepass123"
}
```
**Response**: JWT token + user data

### Task Endpoints (All Protected)

#### GET /api/tasks
**Purpose**: Get all tasks for logged-in user  
**Query Parameters**:
- `status`: Filter by status (pending/in-progress/completed)
- `priority`: Filter by priority (low/medium/high)
- `category`: Filter by category
- `search`: Search in title and description

**Example**: `/api/tasks?status=pending&priority=high`

#### GET /api/tasks/:id
**Purpose**: Get single task by ID  
**Access**: Owner only

#### POST /api/tasks
**Purpose**: Create new task  
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

#### PUT /api/tasks/:id
**Purpose**: Update existing task  
**Access**: Owner only  
**Request Body**: Same as POST (all fields optional)

#### DELETE /api/tasks/:id
**Purpose**: Delete task  
**Access**: Owner only

## Error Handling

### Centralized Error Handling
**Decision**: Express error middleware  
**Location**: server.js

**Error Types**:
1. Validation errors (400)
2. Authentication errors (401)
3. Not found errors (404)
4. Server errors (500)

**Error Response Format**:
```json
{
  "success": false,
  "message": "Descriptive error message"
}
```

## Environment Variables

Required environment variables:
- `PORT`: Server port (default: 5000)
- `MONGODB_URI`: MongoDB connection string
- `JWT_SECRET`: Secret key for JWT signing
- `JWT_EXPIRE`: Token expiration time (default: 7d)
- `NODE_ENV`: Environment (development/production)

**Security Warning**: Never commit `.env` file to version control. Always use `.env.example` as template.

## Database Indexes

**Recommended Indexes**:
- User: `email` (unique), `username` (unique)
- Task: `user` (for user-specific queries), `status`, `priority`, `dueDate`

**Reasoning**: Improves query performance for common operations

## Future Enhancements

Potential features for future versions:
1. Task sharing between users
2. Task comments and attachments
3. Email notifications for due dates
4. Task templates
5. Recurring tasks
6. Task statistics and analytics
7. Export tasks to CSV/PDF
8. Mobile push notifications

## Performance Considerations

- Use MongoDB indexes for frequently queried fields
- Implement pagination for large task lists
- Consider caching for frequently accessed data
- Monitor database query performance
- Use connection pooling for MongoDB

## Deployment Notes

**Recommended Platform**: Heroku, AWS, or DigitalOcean  
**Database**: MongoDB Atlas (managed MongoDB)  
**Environment**: Node.js 14+ required  
**Process Manager**: PM2 for production

**Pre-deployment Checklist**:
- [ ] Set strong JWT_SECRET
- [ ] Configure CORS for production domain
- [ ] Enable MongoDB authentication
- [ ] Set up SSL/TLS
- [ ] Configure rate limiting
- [ ] Set up logging and monitoring
- [ ] Test all endpoints
- [ ] Review security settings
