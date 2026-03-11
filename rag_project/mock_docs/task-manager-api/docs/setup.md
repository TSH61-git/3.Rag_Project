# Setup Guide

## Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js**: Version 14.x or higher
  - Download from: https://nodejs.org/
  - Verify: `node --version`

- **npm**: Comes with Node.js
  - Verify: `npm --version`

- **MongoDB**: Version 4.x or higher
  - Option 1: Local installation from https://www.mongodb.com/try/download/community
  - Option 2: MongoDB Atlas (cloud) from https://www.mongodb.com/cloud/atlas
  - Verify local: `mongod --version`

- **Git**: For cloning the repository
  - Download from: https://git-scm.com/
  - Verify: `git --version`

---

## Installation Steps

### 1. Clone the Repository

```bash
git clone <repository-url>
cd task-manager-api
```

### 2. Install Dependencies

```bash
npm install
```

This will install all required packages:
- express
- mongoose
- bcryptjs
- jsonwebtoken
- dotenv
- joi
- cors
- express-rate-limit

### 3. Set Up MongoDB

#### Option A: Local MongoDB

1. Start MongoDB service:
   ```bash
   # Windows
   net start MongoDB
   
   # macOS (with Homebrew)
   brew services start mongodb-community
   
   # Linux
   sudo systemctl start mongod
   ```

2. Verify MongoDB is running:
   ```bash
   mongo --eval "db.version()"
   ```

#### Option B: MongoDB Atlas (Cloud)

1. Create account at https://www.mongodb.com/cloud/atlas
2. Create a new cluster (free tier available)
3. Create a database user
4. Whitelist your IP address (or use 0.0.0.0/0 for development)
5. Get connection string from "Connect" → "Connect your application"

### 4. Configure Environment Variables

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` file with your configuration:

   ```env
   # Server Configuration
   PORT=5000
   NODE_ENV=development

   # MongoDB Configuration
   # For local MongoDB:
   MONGODB_URI=mongodb://localhost:27017/task-manager
   
   # For MongoDB Atlas:
   # MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/task-manager?retryWrites=true&w=majority

   # JWT Configuration
   JWT_SECRET=your_super_secret_jwt_key_change_this_in_production
   JWT_EXPIRE=7d
   ```

3. **Important**: Generate a strong JWT_SECRET:
   ```bash
   # Using Node.js
   node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
   
   # Or use an online generator
   ```

### 5. Verify Installation

Check that all dependencies are installed:
```bash
npm list --depth=0
```

---

## Running the Application

### Development Mode (with auto-restart)

```bash
npm run dev
```

This uses nodemon to automatically restart the server when files change.

### Production Mode

```bash
npm start
```

### Verify Server is Running

You should see:
```
Server running on port 5000
MongoDB Connected: localhost
```

Test the health endpoint:
```bash
curl http://localhost:5000/health
```

Expected response:
```json
{
  "success": true,
  "message": "Server is running",
  "timestamp": "2024-03-11T10:00:00.000Z"
}
```

---

## Testing the API

### Using cURL

#### 1. Register a user
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
  }'
```

#### 2. Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

Save the token from the response!

#### 3. Create a task
```bash
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "title": "My first task",
    "priority": "high",
    "category": "work"
  }'
```

#### 4. Get all tasks
```bash
curl -X GET http://localhost:5000/api/tasks \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Using Postman

1. Download Postman from https://www.postman.com/downloads/
2. Create a new collection "Task Manager API"
3. Add requests for each endpoint
4. Set up environment variables:
   - `baseUrl`: http://localhost:5000/api
   - `token`: (will be set after login)
5. Use `{{baseUrl}}` and `{{token}}` in requests

### Using Thunder Client (VS Code Extension)

1. Install Thunder Client extension in VS Code
2. Create new request
3. Set URL: http://localhost:5000/api/auth/register
4. Set method: POST
5. Add JSON body
6. Send request

---

## Troubleshooting

### Issue: "Cannot connect to MongoDB"

**Symptoms**: 
```
Error: connect ECONNREFUSED 127.0.0.1:27017
```

**Solutions**:
1. Verify MongoDB is running:
   ```bash
   # Check if MongoDB process is running
   ps aux | grep mongod
   ```

2. Start MongoDB service (see step 3 above)

3. Check MongoDB URI in `.env` file

4. For Atlas: Verify IP whitelist and credentials

---

### Issue: "Port 5000 already in use"

**Symptoms**:
```
Error: listen EADDRINUSE: address already in use :::5000
```

**Solutions**:
1. Change PORT in `.env` file to another port (e.g., 5001)

2. Or kill the process using port 5000:
   ```bash
   # Find process
   lsof -i :5000
   
   # Kill process
   kill -9 <PID>
   ```

---

### Issue: "JWT_SECRET is not defined"

**Symptoms**:
```
Error: JWT_SECRET is not defined
```

**Solutions**:
1. Verify `.env` file exists in project root
2. Check JWT_SECRET is set in `.env`
3. Restart the server after changing `.env`

---

### Issue: "Module not found"

**Symptoms**:
```
Error: Cannot find module 'express'
```

**Solutions**:
1. Delete `node_modules` and reinstall:
   ```bash
   rm -rf node_modules
   npm install
   ```

2. Verify you're in the correct directory

---

### Issue: "Validation error" when creating user

**Symptoms**:
```json
{
  "success": false,
  "message": "\"email\" must be a valid email"
}
```

**Solutions**:
1. Check email format is valid
2. Verify all required fields are provided
3. Check password is at least 6 characters
4. Ensure username is 3-30 characters

---

## Database Management

### View Database Contents

Using MongoDB Shell:
```bash
mongo
use task-manager
db.users.find().pretty()
db.tasks.find().pretty()
```

Using MongoDB Compass (GUI):
1. Download from https://www.mongodb.com/products/compass
2. Connect to mongodb://localhost:27017
3. Browse collections

### Clear Database

**Warning**: This will delete all data!

```bash
mongo
use task-manager
db.users.deleteMany({})
db.tasks.deleteMany({})
```

### Backup Database

```bash
mongodump --db task-manager --out ./backup
```

### Restore Database

```bash
mongorestore --db task-manager ./backup/task-manager
```

---

## Development Tips

### Auto-reload on File Changes

The `npm run dev` command uses nodemon to automatically restart the server when you make changes to the code.

### Debugging

Add this to your code to debug:
```javascript
console.log('Debug:', variable);
```

Or use VS Code debugger:
1. Add breakpoint in code
2. Press F5 to start debugging
3. Use Debug Console to inspect variables

### Environment-specific Configuration

You can create multiple environment files:
- `.env.development`
- `.env.production`
- `.env.test`

Load them based on NODE_ENV:
```javascript
require('dotenv').config({ 
  path: `.env.${process.env.NODE_ENV}` 
});
```

---

## Next Steps

After successful setup:

1. Read the [API Documentation](api.md) for detailed endpoint information
2. Review [Security Guidelines](security.md) for best practices
3. Check `.cursor/` directory for technical decisions and tasks
4. Start building your frontend or mobile app!

---

## Getting Help

If you encounter issues:

1. Check this troubleshooting section
2. Review error messages carefully
3. Check MongoDB and Node.js logs
4. Verify all environment variables are set
5. Ensure all dependencies are installed
6. Try restarting the server

Common log locations:
- Application logs: Console output
- MongoDB logs: `/var/log/mongodb/mongod.log` (Linux)
- npm logs: `npm-debug.log` in project directory
