# Security Guidelines

## Overview

This document outlines the security measures implemented in the Task Manager API and best practices for maintaining security.

---

## Authentication & Authorization

### JWT (JSON Web Tokens)

**Implementation**:
- Tokens are generated upon successful login/registration
- Tokens contain user ID and expiration time
- Tokens are signed with JWT_SECRET
- Default expiration: 7 days

**Security Measures**:
- JWT_SECRET must be strong and kept secret
- Tokens are stateless (no server-side storage)
- Tokens are verified on every protected route
- Expired tokens are rejected

**Best Practices**:
```javascript
// ✅ Good: Strong secret (32+ characters, random)
JWT_SECRET=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6

// ❌ Bad: Weak secret
JWT_SECRET=secret123
```

**Token Storage (Client-side)**:
- Store in httpOnly cookies (most secure)
- Or localStorage (convenient but less secure)
- Never store in regular cookies or sessionStorage for sensitive apps

**Warning**: Do not modify JWT verification logic without security review. This is critical for authentication.

---

### Password Security

**Hashing**:
- Passwords are hashed using bcryptjs
- Salt rounds: 10 (good balance of security and performance)
- Passwords are never stored in plain text
- Passwords are never logged or exposed in responses

**Password Requirements**:
- Minimum length: 6 characters
- No maximum length (bcrypt handles long passwords)
- No complexity requirements (for demo purposes)

**Production Recommendations**:
- Increase minimum to 8-12 characters
- Require mix of uppercase, lowercase, numbers, symbols
- Implement password strength meter
- Check against common password lists
- Implement password history (prevent reuse)

**Password Comparison**:
```javascript
// ✅ Good: Constant-time comparison
const isMatch = await user.comparePassword(password);

// ❌ Bad: Direct comparison (timing attack vulnerable)
if (user.password === password) { }
```

---

## Input Validation

### Joi Validation

**Implementation**:
- All user inputs are validated before processing
- Schema-based validation with Joi
- Validation happens in middleware before route handlers

**Validation Rules**:

**User Registration**:
- username: 3-30 characters, alphanumeric
- email: valid email format
- password: minimum 6 characters

**Task Creation/Update**:
- title: required, max 100 characters
- description: optional, max 500 characters
- status: enum (pending, in-progress, completed)
- priority: enum (low, medium, high)
- category: enum (work, personal, shopping, health, other)
- dueDate: valid ISO 8601 date

**Why Validation Matters**:
- Prevents injection attacks (SQL, NoSQL, XSS)
- Ensures data integrity
- Provides clear error messages
- Prevents application crashes

**Example Attack Prevention**:
```javascript
// ❌ Without validation: NoSQL injection possible
{ "email": { "$ne": null } }

// ✅ With validation: Rejected as invalid email
"email" must be a valid email
```

---

## Rate Limiting

### Configuration

**Current Settings**:
- Window: 15 minutes
- Max requests: 100 per IP address
- Applies to all `/api/*` routes

**Purpose**:
- Prevents brute force attacks on login
- Protects against DoS (Denial of Service)
- Limits API abuse
- Reduces server load

**Response when limit exceeded**:
```json
{
  "success": false,
  "message": "Too many requests from this IP, please try again later."
}
```

**Production Recommendations**:
- Reduce to 50 requests per 15 minutes
- Implement stricter limits on auth endpoints (5 login attempts per 15 min)
- Use Redis for distributed rate limiting
- Implement user-based rate limiting (not just IP)
- Add CAPTCHA after multiple failed attempts

**Warning**: Do not disable rate limiting. This is a critical security feature that protects against brute force attacks.

---

## CORS (Cross-Origin Resource Sharing)

### Configuration

**Current**: Allows all origins (development)

**Production Recommendation**:
```javascript
const corsOptions = {
  origin: ['https://yourdomain.com', 'https://app.yourdomain.com'],
  credentials: true,
  optionsSuccessStatus: 200
};

app.use(cors(corsOptions));
```

**Why CORS Matters**:
- Prevents unauthorized domains from accessing your API
- Protects user data from malicious websites
- Required for browser security

---

## Common Vulnerabilities & Mitigations

### 1. SQL/NoSQL Injection

**Risk**: Attackers inject malicious queries

**Mitigation**:
- ✅ Use Mongoose (parameterized queries)
- ✅ Validate all inputs with Joi
- ✅ Never concatenate user input into queries

**Example**:
```javascript
// ✅ Safe: Mongoose query
Task.find({ user: userId, status: userStatus });

// ❌ Unsafe: String concatenation
db.collection.find(`{ user: "${userId}" }`);
```

---

### 2. Cross-Site Scripting (XSS)

**Risk**: Attackers inject malicious scripts

**Mitigation**:
- ✅ Validate and sanitize all inputs
- ✅ Limit string lengths (title: 100, description: 500)
- ✅ Use Content-Security-Policy headers (future enhancement)
- ✅ Escape output in frontend

**Example**:
```javascript
// ❌ Dangerous input
title: "<script>alert('XSS')</script>"

// ✅ Validation rejects it
"title" must not contain HTML tags
```

---

### 3. Brute Force Attacks

**Risk**: Attackers try many passwords

**Mitigation**:
- ✅ Rate limiting (100 req/15min)
- ✅ Strong password hashing (bcrypt)
- ✅ Account lockout (future enhancement)
- ✅ CAPTCHA (future enhancement)

---

### 4. JWT Token Theft

**Risk**: Attackers steal and use tokens

**Mitigation**:
- ✅ Use HTTPS in production
- ✅ Short token expiration (7 days)
- ✅ Secure token storage (httpOnly cookies)
- ⏳ Token refresh mechanism (future)
- ⏳ Token blacklist on logout (future)

**If token is compromised**:
- User should change password
- Old tokens become invalid after expiration
- Implement token revocation for immediate invalidation

---

### 5. Man-in-the-Middle (MITM)

**Risk**: Attackers intercept communication

**Mitigation**:
- ✅ Use HTTPS in production (SSL/TLS)
- ✅ HSTS headers (future enhancement)
- ✅ Secure cookies (httpOnly, secure flags)

---

### 6. Denial of Service (DoS)

**Risk**: Attackers overwhelm server

**Mitigation**:
- ✅ Rate limiting
- ✅ Request size limits (express.json limit)
- ⏳ Load balancing (production)
- ⏳ CDN (production)

---

## Environment Variables Security

### Critical Variables

**Never commit to version control**:
- JWT_SECRET
- MONGODB_URI (with credentials)
- API keys
- Passwords

**Use .gitignore**:
```
.env
.env.local
.env.production
```

**Production Checklist**:
- [ ] Use strong, random JWT_SECRET (32+ characters)
- [ ] Use environment-specific .env files
- [ ] Store secrets in secure vault (AWS Secrets Manager, etc.)
- [ ] Rotate secrets regularly
- [ ] Limit access to production secrets

---

## Database Security

### MongoDB Security

**Current** (Development):
- Local MongoDB without authentication
- No encryption

**Production Requirements**:
- ✅ Enable MongoDB authentication
- ✅ Use strong passwords
- ✅ Limit network access (firewall)
- ✅ Enable encryption at rest
- ✅ Enable encryption in transit (SSL/TLS)
- ✅ Regular backups
- ✅ Audit logging

**MongoDB Atlas** (Recommended):
- Built-in authentication
- Encryption at rest and in transit
- IP whitelisting
- Automated backups
- Monitoring and alerts

**Connection String Security**:
```javascript
// ❌ Bad: Credentials in code
mongoose.connect('mongodb://admin:password123@localhost:27017/db');

// ✅ Good: Credentials in environment variables
mongoose.connect(process.env.MONGODB_URI);
```

---

## API Security Best Practices

### 1. Use HTTPS

**Production**: Always use HTTPS
- Encrypts data in transit
- Prevents MITM attacks
- Required for secure cookies

**Setup**:
- Get SSL certificate (Let's Encrypt is free)
- Configure reverse proxy (Nginx, Apache)
- Redirect HTTP to HTTPS

---

### 2. Security Headers

**Recommended Headers** (future enhancement):
```javascript
app.use(helmet()); // Sets multiple security headers

// Or manually:
app.use((req, res, next) => {
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('X-Frame-Options', 'DENY');
  res.setHeader('X-XSS-Protection', '1; mode=block');
  res.setHeader('Strict-Transport-Security', 'max-age=31536000');
  next();
});
```

---

### 3. Error Handling

**Current**: Generic error messages

**Security Consideration**:
```javascript
// ✅ Good: Generic message to client
res.status(500).json({ message: 'Server error' });

// ❌ Bad: Exposes internal details
res.status(500).json({ 
  message: error.message,
  stack: error.stack 
});
```

**Logging**:
- Log detailed errors server-side
- Send generic messages to client
- Never expose stack traces in production

---

### 4. Dependency Security

**Regular Updates**:
```bash
# Check for vulnerabilities
npm audit

# Fix vulnerabilities
npm audit fix

# Update dependencies
npm update
```

**Best Practices**:
- Review dependencies before installing
- Use exact versions in package.json (no ^)
- Monitor for security advisories
- Remove unused dependencies

---

## Sensitive Areas

### Authentication Module

**Sensitivity**: CRITICAL  
**Files**: 
- `src/middleware/auth.js`
- `src/routes/auth.js`
- `src/models/User.js`

**Warning**: Any changes to authentication logic must be reviewed by security team. This module handles user credentials and tokens.

**Last Modified**: 2024-03-02

**Critical Functions**:
- Password hashing (User model pre-save hook)
- Password comparison (User.comparePassword)
- JWT generation (auth routes)
- JWT verification (auth middleware)

**Do Not**:
- Remove password hashing
- Weaken JWT verification
- Log passwords or tokens
- Expose user passwords in responses

---

### Rate Limiting

**Sensitivity**: HIGH  
**File**: `src/server.js`

**Warning**: Do not disable or weaken rate limiting without security review. This protects against brute force attacks.

**Configuration**: 100 requests per 15 minutes per IP

---

## Security Checklist

### Development
- [x] Passwords are hashed
- [x] JWT tokens are used for authentication
- [x] Input validation on all endpoints
- [x] Rate limiting enabled
- [x] CORS configured
- [x] .env file in .gitignore
- [ ] Security headers (future)
- [ ] HTTPS (production only)

### Pre-Production
- [ ] Strong JWT_SECRET generated
- [ ] MongoDB authentication enabled
- [ ] CORS restricted to production domains
- [ ] HTTPS configured
- [ ] Security headers added
- [ ] Error messages sanitized
- [ ] Dependencies audited
- [ ] Secrets stored in vault
- [ ] Logging configured
- [ ] Monitoring set up

### Production
- [ ] All pre-production items completed
- [ ] Regular security audits scheduled
- [ ] Incident response plan in place
- [ ] Backup and recovery tested
- [ ] Rate limits reviewed and adjusted
- [ ] SSL certificate auto-renewal configured

---

## Incident Response

### If Security Breach Occurs:

1. **Immediate Actions**:
   - Identify and stop the breach
   - Revoke compromised credentials
   - Change JWT_SECRET (invalidates all tokens)
   - Review logs for extent of breach

2. **Investigation**:
   - Determine what data was accessed
   - Identify vulnerability exploited
   - Document timeline of events

3. **Remediation**:
   - Fix vulnerability
   - Deploy patch
   - Notify affected users
   - Reset passwords if needed

4. **Prevention**:
   - Implement additional security measures
   - Update security documentation
   - Train team on new procedures

---

## Security Resources

- OWASP Top 10: https://owasp.org/www-project-top-ten/
- Node.js Security Best Practices: https://nodejs.org/en/docs/guides/security/
- Express Security: https://expressjs.com/en/advanced/best-practice-security.html
- MongoDB Security: https://docs.mongodb.com/manual/security/
- JWT Best Practices: https://tools.ietf.org/html/rfc8725

---

## Contact

For security concerns or to report vulnerabilities:
- Email: security@yourdomain.com
- Do not disclose vulnerabilities publicly
- Allow reasonable time for fixes before disclosure
