# Task Manager API

A RESTful API for managing tasks with user authentication, built with Node.js, Express, and MongoDB.

## Features

- **User Authentication**: JWT-based authentication with secure password hashing
- **Task Management**: Full CRUD operations for tasks
- **Task Organization**: Categories, priorities, and status tracking
- **Search & Filter**: Find tasks by status, priority, category, or search term
- **Security**: Rate limiting, input validation, and secure authentication
- **RESTful Design**: Clean API structure following REST principles

## Tech Stack

- **Backend**: Node.js + Express.js
- **Database**: MongoDB + Mongoose
- **Authentication**: JWT (JSON Web Tokens)
- **Validation**: Joi
- **Security**: bcryptjs, express-rate-limit, CORS

## Quick Start

### Prerequisites

- Node.js (v14 or higher)
- MongoDB (local or Atlas)
- npm or yarn

### Installation

1. Clone the repository
```bash
git clone <repository-url>
cd task-manager-api
```

2. Install dependencies
```bash
npm install
```

3. Create `.env` file
```bash
cp .env.example .env
```

4. Update `.env` with your configuration
```
PORT=5000
MONGODB_URI=mongodb://localhost:27017/task-manager
JWT_SECRET=your_secret_key
JWT_EXPIRE=7d
```

5. Start the server
```bash
# Development mode
npm run dev

# Production mode
npm start
```

## API Endpoints

### Authentication

- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user

### Tasks (Protected)

- `GET /api/tasks` - Get all tasks (with filters)
- `GET /api/tasks/:id` - Get single task
- `POST /api/tasks` - Create new task
- `PUT /api/tasks/:id` - Update task
- `DELETE /api/tasks/:id` - Delete task

## Documentation

- [API Documentation](docs/api.md) - Detailed API endpoints and examples
- [Setup Guide](docs/setup.md) - Installation and configuration
- [Security Guidelines](docs/security.md) - Security best practices

## Project Structure

```
task-manager-api/
├── src/
│   ├── config/          # Configuration files
│   ├── models/          # Mongoose models
│   ├── routes/          # API routes
│   ├── middleware/      # Custom middleware
│   └── server.js        # Entry point
├── docs/                # Documentation
├── .cursor/             # Development notes
├── .env.example         # Environment variables template
└── package.json         # Dependencies
```

## Development Notes

See `.cursor/` directory for:
- Technical decisions
- Development tasks
- API specifications

## License

MIT
