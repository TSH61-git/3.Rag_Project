# Technical Decisions Log

## Decision: Backend Framework Selection
**Date**: 2024-03-01  
**Status**: Approved  
**Decision**: Use Node.js with Express.js  
**Alternatives Considered**:
- Python with FastAPI
- Go with Gin
- Java with Spring Boot

**Reasoning**:
- JavaScript full-stack (same language for frontend if needed)
- Massive ecosystem (npm packages)
- Fast development cycle
- Excellent for I/O-heavy operations
- Team familiarity with JavaScript

**Impact**: All backend code will be in JavaScript/Node.js

---

## Decision: Database Choice
**Date**: 2024-03-01  
**Status**: Approved  
**Decision**: MongoDB with Mongoose ODM  
**Alternatives Considered**:
- PostgreSQL with Sequelize
- MySQL
- SQLite

**Reasoning**:
- Flexible schema (tasks can have varying attributes)
- JSON-like documents match JavaScript objects naturally
- Easy horizontal scaling
- Mongoose provides excellent validation and middleware
- No need for complex joins in this application

**Impact**: 
- Database schema can evolve easily
- No SQL migrations needed
- Requires MongoDB installation/Atlas account

---

## Decision: Authentication Strategy
**Date**: 2024-03-02  
**Status**: Approved  
**Decision**: JWT (JSON Web Tokens) with bcryptjs for password hashing  
**Alternatives Considered**:
- Session-based authentication with cookies
- OAuth 2.0
- Passport.js with local strategy

**Reasoning**:
- Stateless authentication (no server-side session storage)
- Scales well across multiple servers
- Works seamlessly with mobile apps and SPAs
- Industry standard
- Simple to implement

**Configuration**:
- Token expiration: 7 days
- bcrypt salt rounds: 10
- Token stored in Authorization header

**Impact**:
- Clients must store and send JWT with each request
- No server-side session management needed
- Logout requires client-side token deletion

**Security Note**: JWT_SECRET must be strong and kept secure. Never commit to version control.

---

## Decision: Input Validation Library
**Date**: 2024-03-02  
**Status**: Approved  
**Decision**: Joi for schema-based validation  
**Alternatives Considered**:
- express-validator
- Yup
- Manual validation

**Reasoning**:
- Schema-based approach is clean and maintainable
- Excellent error messages
- Type coercion and transformation
- Well-documented and widely used
- Prevents injection attacks

**Impact**: All user inputs validated before processing

---

## Decision: Rate Limiting Strategy
**Date**: 2024-03-03  
**Status**: Approved  
**Decision**: express-rate-limit with 100 requests per 15 minutes per IP  
**Alternatives Considered**:
- No rate limiting
- Redis-based rate limiting
- Custom middleware

**Reasoning**:
- Protects against brute force attacks
- Simple to implement
- No external dependencies (Redis)
- Sufficient for small to medium applications

**Configuration**:
- Window: 15 minutes
- Max requests: 100 per IP
- Applies to all /api/* routes

**Warning**: This is a critical security feature. Do not disable without security review.

---

## Decision: API Response Format
**Date**: 2024-03-03  
**Status**: Approved  
**Decision**: Consistent JSON structure with success flag  
**Format**:
```json
{
  "success": boolean,
  "message": string,
  "data": object/array,
  "count": number
}
```

**Alternatives Considered**:
- Minimal response (just data)
- JSend specification
- JSON:API specification

**Reasoning**:
- Consistent structure across all endpoints
- Easy for clients to handle success/error
- Clear error messages
- Simple and not over-engineered

**Impact**: All API responses follow this format

---

## Decision: Task Status Workflow
**Date**: 2024-03-04  
**Status**: Approved  
**Decision**: Three-state workflow: pending → in-progress → completed  
**Alternatives Considered**:
- Two-state: todo → done
- Five-state: backlog → todo → in-progress → review → done
- Custom states per user

**Reasoning**:
- Simple enough for most use cases
- Clear progression
- Not overwhelming for users
- Can be extended later if needed

**Impact**: Task model has status enum with three values

---

## Decision: Task Categories
**Date**: 2024-03-04  
**Status**: Approved  
**Decision**: Fixed categories: work, personal, shopping, health, other  
**Alternatives Considered**:
- User-defined categories
- No categories
- Tags instead of categories

**Reasoning**:
- Provides structure without complexity
- Covers most common use cases
- Easier to implement filtering
- Can add custom tags later if needed

**Impact**: Task model has category enum

---

## Decision: Task Priority Levels
**Date**: 2024-03-04  
**Status**: Approved  
**Decision**: Three levels: low, medium, high  
**Alternatives Considered**:
- Five levels (critical, high, medium, low, trivial)
- Numeric priority (1-10)
- No priority system

**Reasoning**:
- Simple and intuitive
- Avoids decision paralysis
- Sufficient for most users
- Industry standard

**Impact**: Task model has priority enum with three values

---

## Decision: Error Handling Approach
**Date**: 2024-03-05  
**Status**: Approved  
**Decision**: Centralized error handling middleware  
**Implementation**:
- Try-catch blocks in route handlers
- Consistent error response format
- Logging of all errors

**Alternatives Considered**:
- Error handling in each route
- Third-party error handling library
- Custom error classes

**Reasoning**:
- DRY principle (Don't Repeat Yourself)
- Consistent error responses
- Easier to maintain
- Single place to add logging/monitoring

**Impact**: All routes use try-catch and pass errors to middleware

---

## Decision: CORS Configuration
**Date**: 2024-03-05  
**Status**: Approved  
**Decision**: Enable CORS for all origins in development, restrict in production  
**Reasoning**:
- Allows frontend development on different port
- Security in production by restricting origins
- Standard practice

**Configuration**:
- Development: Allow all origins
- Production: Whitelist specific domains

**Impact**: Frontend can call API from different domain

---

## Decision: Password Requirements
**Date**: 2024-03-06  
**Status**: Approved  
**Decision**: Minimum 6 characters, no complexity requirements  
**Alternatives Considered**:
- 8+ characters with complexity (uppercase, numbers, symbols)
- 12+ characters
- Passphrase approach

**Reasoning**:
- Balance between security and usability
- Users can choose stronger passwords if desired
- Prevents overly weak passwords
- Not too restrictive for demo/personal use

**Impact**: User model validates password length

**Note**: For production with sensitive data, consider stronger requirements

---

## Decision: Task Search Implementation
**Date**: 2024-03-07  
**Status**: Approved  
**Decision**: MongoDB regex search on title and description  
**Alternatives Considered**:
- Full-text search with MongoDB text indexes
- Elasticsearch integration
- Third-party search service

**Reasoning**:
- Simple to implement
- Sufficient for small to medium datasets
- No additional dependencies
- Case-insensitive search

**Limitations**: Not performant for very large datasets

**Future Enhancement**: Consider MongoDB text indexes or Elasticsearch for scale

---

## Decision: Date Handling
**Date**: 2024-03-07  
**Status**: Approved  
**Decision**: Store dates as ISO 8601 strings, use JavaScript Date objects  
**Reasoning**:
- Standard format
- Easy to parse in any language
- MongoDB handles Date objects well
- Timezone-aware

**Impact**: dueDate field is Date type in MongoDB

---

## Decision: API Versioning Strategy
**Date**: 2024-03-08  
**Status**: Approved  
**Decision**: No versioning for v1, add /v2 prefix when breaking changes needed  
**Alternatives Considered**:
- Version in URL from start (/api/v1/tasks)
- Version in header
- No versioning

**Reasoning**:
- YAGNI (You Aren't Gonna Need It) for initial version
- Easy to add later
- Keeps URLs clean
- Can maintain v1 and v2 simultaneously when needed

**Impact**: Current URLs: /api/tasks, future: /api/v2/tasks

---

## Decision: Logging Strategy
**Date**: 2024-03-08  
**Status**: Approved  
**Decision**: Console logging for development, structured logging for production  
**Future Enhancement**: Add Winston or Pino for production

**Reasoning**:
- Simple for development
- Can be enhanced later
- Logs errors and important events

**Impact**: console.log and console.error used throughout

---

## Decision: Testing Strategy
**Date**: 2024-03-09  
**Status**: Deferred  
**Decision**: Manual testing for MVP, add automated tests in next phase  
**Future Plan**:
- Unit tests with Jest
- Integration tests with Supertest
- 80% coverage target

**Reasoning**:
- Faster initial development
- Tests can be added incrementally
- Focus on core functionality first

**Impact**: No test files in current version

---

## Decision: Documentation Approach
**Date**: 2024-03-10  
**Status**: Approved  
**Decision**: Markdown documentation in docs/ and .cursor/ directories  
**Alternatives Considered**:
- Swagger/OpenAPI
- Postman collection
- Wiki

**Reasoning**:
- Simple and version-controlled
- Easy to read and edit
- No additional tools needed
- Can generate Swagger later if needed

**Impact**: Documentation in markdown files
