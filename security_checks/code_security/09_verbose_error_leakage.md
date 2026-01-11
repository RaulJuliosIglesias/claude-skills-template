# 9. Verbose Error Information Leakage

## 🟠 Risk Level: **HIGH**

## 📋 Vulnerability Description

AI-generated catch blocks often blindly return the raw error message to the client to help with debugging (`res.send(err.message)`). This exposes internal database schemas, table names, file paths, and logic failures to attackers, significantly aiding in reconnaissance for SQL injection or other attacks.

**Impact:**
- Database schema exposure
- File system structure revealed
- Internal logic exposed
- Attack surface increased
- SQL injection reconnaissance

## 🎯 Context: Why This Happens

AI code generators prioritize developer experience:
- Helpful error messages for debugging
- Full stack traces in responses
- Detailed validation errors
- Database error messages passed through

## 🔍 Detection Methods

### 1. Code Analysis

**Search for:**
```javascript
// Dangerous patterns
res.send(err.message)
res.json({ error: err.message })
throw err
console.error(err) // If logged to client
```

**Check error handlers:**
- Global error middleware
- Try-catch blocks
- Promise catch handlers
- Async error handlers

### 2. Testing

**Trigger errors and check responses:**
```bash
# Test with invalid input
curl -X POST https://api.example.com/users \
  -d '{"invalid": "data"}'

# Check if response contains:
# - Stack traces
# - File paths
# - Database errors
# - Internal variable names
```

### 3. Production Error Review

**Check production logs:**
- Look for detailed errors in responses
- Verify error messages are generic
- Check if stack traces are exposed

## ✅ Verification Requirements

### Must Have:
1. **Generic Error Messages**
   - User-friendly messages only
   - No stack traces in production
   - No file paths or line numbers
   - No database schema information

2. **Centralized Error Handling**
   - Global error middleware
   - Consistent error format
   - Logging separated from responses

3. **Error Logging**
   - Full details logged server-side
   - Generic messages sent to client
   - Error tracking (Sentry, etc.)

## 🚨 Exploit Path

### Scenario 1: Database Schema Exposure
```
1. Attacker sends malformed request
2. Server returns: "Error: relation 'users' does not exist"
3. Attacker learns table name: 'users'
4. Attacker tries: "Error: column 'password' does not exist"
5. Attacker learns column names
6. Attacker crafts SQL injection with known schema
7. Database compromised
```

### Scenario 2: File Path Exposure
```
1. Attacker triggers file read error
2. Server returns: "Error: ENOENT: no such file or directory, open '/var/www/app/config/secrets.json'"
3. Attacker learns:
   - Server uses Node.js
   - Application path: /var/www/app
   - Config file location
4. Attacker targets known paths
5. Path traversal attack succeeds
```

### Scenario 3: Internal Logic Exposure
```
1. Attacker sends invalid data
2. Server returns: "Error: User validation failed: email must be unique"
3. Attacker learns validation logic
4. Attacker learns email uniqueness requirement
5. Attacker can enumerate existing emails
```

## 🔧 Remediation Steps

### Step 1: Create Error Handling Middleware

**Express.js:**
```javascript
// middleware/errorHandler.js
const logger = require('./logger');
const { isDevelopment } = require('./config');

function errorHandler(err, req, res, next) {
  // Log full error details server-side
  logger.error('Error occurred', {
    error: err.message,
    stack: err.stack,
    url: req.url,
    method: req.method,
    ip: req.ip,
    user: req.user?.id
  });
  
  // Send generic message to client
  const statusCode = err.statusCode || 500;
  const message = isDevelopment 
    ? err.message  // Detailed in development
    : 'An unexpected error occurred'; // Generic in production
  
  res.status(statusCode).json({
    error: message,
    ...(isDevelopment && { stack: err.stack }) // Stack only in dev
  });
}

module.exports = errorHandler;
```

**FastAPI:**
```python
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import logging
import os

logger = logging.getLogger(__name__)
is_development = os.getenv("ENVIRONMENT") == "development"

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # Log full error
    logger.error(
        f"Error: {str(exc)}",
        exc_info=True,
        extra={
            "url": str(request.url),
            "method": request.method,
            "client": request.client.host
        }
    )
    
    # Return generic message
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "An unexpected error occurred" if not is_development else str(exc)
        }
    )
```

### Step 2: Sanitize Database Errors

```javascript
// utils/errorSanitizer.js
function sanitizeDatabaseError(err) {
  // Don't expose database errors directly
  if (err.name === 'SequelizeDatabaseError') {
    return new Error('Database operation failed');
  }
  
  if (err.name === 'SequelizeValidationError') {
    // Return generic validation error
    return new Error('Validation failed');
  }
  
  if (err.name === 'SequelizeUniqueConstraintError') {
    // Don't reveal which field is duplicate
    return new Error('A record with this information already exists');
  }
  
  return err;
}

// Usage
try {
  await User.create(data);
} catch (err) {
  const sanitized = sanitizeDatabaseError(err);
  throw sanitized;
}
```

### Step 3: Create Custom Error Classes

```javascript
// errors/AppError.js
class AppError extends Error {
  constructor(message, statusCode = 500, isOperational = true) {
    super(message);
    this.statusCode = statusCode;
    this.isOperational = isOperational;
    Error.captureStackTrace(this, this.constructor);
  }
}

class ValidationError extends AppError {
  constructor(message = 'Validation failed') {
    super(message, 400);
  }
}

class NotFoundError extends AppError {
  constructor(resource = 'Resource') {
    super(`${resource} not found`, 404);
  }
}

class UnauthorizedError extends AppError {
  constructor(message = 'Unauthorized') {
    super(message, 401);
  }
}

module.exports = {
  AppError,
  ValidationError,
  NotFoundError,
  UnauthorizedError
};
```

### Step 4: Update Error Handler

```javascript
// middleware/errorHandler.js
const { AppError } = require('../errors/AppError');
const logger = require('./logger');
const { isDevelopment } = require('./config');

function errorHandler(err, req, res, next) {
  // Log all errors with full details
  logger.error('Error', {
    message: err.message,
    stack: err.stack,
    name: err.name,
    statusCode: err.statusCode,
    url: req.url,
    method: req.method,
    ip: req.ip
  });
  
  // Operational errors (expected) - send message
  if (err.isOperational) {
    return res.status(err.statusCode || 500).json({
      error: err.message
    });
  }
  
  // Programming errors (unexpected) - send generic message
  return res.status(500).json({
    error: isDevelopment 
      ? err.message 
      : 'An unexpected error occurred'
  });
}
```

### Step 5: Handle Specific Error Types

```javascript
// routes/users.js
const { ValidationError, NotFoundError } = require('../errors/AppError');

app.post('/api/users', async (req, res, next) => {
  try {
    const user = await User.create(req.body);
    res.json(user);
  } catch (err) {
    if (err.name === 'SequelizeValidationError') {
      return next(new ValidationError('Invalid user data'));
    }
    if (err.name === 'SequelizeUniqueConstraintError') {
      return next(new ValidationError('Email already exists'));
    }
    next(err); // Pass to error handler
  }
});

app.get('/api/users/:id', async (req, res, next) => {
  try {
    const user = await User.findByPk(req.params.id);
    if (!user) {
      return next(new NotFoundError('User'));
    }
    res.json(user);
  } catch (err) {
    next(err);
  }
});
```

### Step 6: Set Up Error Tracking

**Sentry Integration:**
```javascript
const Sentry = require('@sentry/node');

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: process.env.NODE_ENV,
  tracesSampleRate: 1.0
});

// In error handler
function errorHandler(err, req, res, next) {
  // Send to Sentry (includes full details)
  Sentry.captureException(err, {
    tags: {
      url: req.url,
      method: req.method
    },
    user: {
      id: req.user?.id
    }
  });
  
  // Send generic message to client
  res.status(500).json({
    error: 'An unexpected error occurred'
  });
}
```

## 📝 Code Examples

### ❌ Vulnerable Code

```javascript
// ❌ VULNERABLE: Raw error exposed
app.post('/api/users', async (req, res) => {
  try {
    const user = await User.create(req.body);
    res.json(user);
  } catch (err) {
    res.status(400).json({ error: err.message }); // ❌ Exposes database errors
  }
});

// ❌ VULNERABLE: Stack trace exposed
app.use((err, req, res, next) => {
  res.status(500).json({
    error: err.message,
    stack: err.stack // ❌ Exposes file paths
  });
});

// ❌ VULNERABLE: Database error passed through
app.get('/api/users/:id', async (req, res) => {
  try {
    const user = await db.query(
      `SELECT * FROM users WHERE id = ${req.params.id}` // ❌ SQL injection risk
    );
    res.json(user);
  } catch (err) {
    res.json({ error: err.message }); // ❌ "relation 'users' does not exist"
  }
});
```

### ✅ Secure Code

```javascript
// ✅ SECURE: Generic error messages
const { AppError, ValidationError, NotFoundError } = require('./errors/AppError');
const logger = require('./logger');

app.post('/api/users', async (req, res, next) => {
  try {
    const user = await User.create(req.body);
    res.json(user);
  } catch (err) {
    if (err.name === 'SequelizeValidationError') {
      return next(new ValidationError('Invalid user data'));
    }
    if (err.name === 'SequelizeUniqueConstraintError') {
      return next(new ValidationError('Email already exists'));
    }
    next(err);
  }
});

// ✅ SECURE: Centralized error handler
app.use((err, req, res, next) => {
  // Log full details server-side
  logger.error('Error', {
    message: err.message,
    stack: err.stack,
    url: req.url,
    method: req.method
  });
  
  // Send generic message to client
  const statusCode = err.statusCode || 500;
  const message = process.env.NODE_ENV === 'production'
    ? (err.isOperational ? err.message : 'An unexpected error occurred')
    : err.message; // Detailed in development
  
  res.status(statusCode).json({ error: message });
});

// ✅ SECURE: Parameterized queries + generic errors
app.get('/api/users/:id', async (req, res, next) => {
  try {
    const user = await db.query(
      'SELECT * FROM users WHERE id = $1',
      [req.params.id] // ✅ Parameterized
    );
    
    if (!user) {
      return next(new NotFoundError('User'));
    }
    
    res.json(user);
  } catch (err) {
    // Generic error - no database details
    next(new AppError('Failed to retrieve user', 500));
  }
});
```

## 🧪 Testing Checklist

- [ ] No stack traces in production responses
- [ ] No file paths in error messages
- [ ] No database schema information exposed
- [ ] Generic error messages for users
- [ ] Full errors logged server-side
- [ ] Error tracking configured (Sentry, etc.)
- [ ] Different error messages for dev/prod
- [ ] Validation errors are user-friendly
- [ ] Database errors are sanitized
- [ ] Error handler catches all errors

## 📚 References

- [OWASP: Improper Error Handling](https://owasp.org/www-community/Improper_Error_Handling)
- [CWE-209: Information Exposure Through an Error Message](https://cwe.mitre.org/data/definitions/209.html)
- [Express Error Handling](https://expressjs.com/en/guide/error-handling.html)
- [Sentry Error Tracking](https://sentry.io/)

## 🔗 Related Vulnerabilities

- [10. Client-Side Input Validation Only](../input_validation/10_client_side_validation_only.md)
- [34. Path Traversal](../input_validation/34_path_traversal.md)
- [42. Sensitive Data Exposure in Logs](../data_protection/42_sensitive_data_in_logs.md)

---

**Classification**:
- **Confirmed** if stack traces or detailed errors returned to client
- **Likely** if error messages contain internal information
- **Not Applicable** if errors are properly sanitized and generic
