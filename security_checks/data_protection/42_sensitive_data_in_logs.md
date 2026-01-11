# 42. Sensitive Data Exposure in Logs

## 🟠 Risk Level: **HIGH**

## 📋 Vulnerability Description

AI-generated code frequently uses `console.log(req.body)` or `print(payload)` to help developers debug issues. This results in sensitive data—including user passwords, session tokens, and PII—being permanently recorded in server logs (e.g., Vercel, AWS CloudWatch), where it is accessible to third-party log aggregators and DevOps staff.

**Impact:**
- Credential exposure in logs
- PII in log files
- Token leakage
- Compliance violations

## 🎯 Context: Why This Happens

AI code:
- Logs everything for "debugging"
- Doesn't sanitize logs
- Uses console.log everywhere
- Doesn't distinguish dev/prod logging

## 🔍 Detection Methods

### 1. Code Analysis

**Search for:**
```javascript
console.log(req.body)
console.log(password)
print(payload)
logger.info(req.body)
```

### 2. Log Review

**Check logs for:**
- Passwords
- Tokens
- API keys
- PII

## ✅ Verification Requirements

### Must Have:
1. **Log Sanitization**
   - Redact sensitive fields
   - Use structured logging
   - Sanitize before logging

2. **No Sensitive Data**
   - No passwords in logs
   - No tokens in logs
   - No PII in logs

## 🚨 Exploit Path

### Scenario 1: Password in Logs
```
1. User logs in
2. Code logs: console.log(req.body)
3. Password logged: {email: "user@example.com", password: "secret123"}
4. Logs stored in CloudWatch
5. Attacker accesses logs
6. Password exposed
```

## 🔧 Remediation Steps

### Step 1: Create Log Sanitizer

```javascript
const SENSITIVE_FIELDS = [
  'password',
  'token',
  'authorization',
  'api_key',
  'secret',
  'ssn',
  'credit_card'
];

function sanitizeForLogging(obj) {
  if (typeof obj !== 'object' || obj === null) {
    return obj;
  }
  
  const sanitized = { ...obj };
  
  for (const key in sanitized) {
    const lowerKey = key.toLowerCase();
    
    // Check if field is sensitive
    if (SENSITIVE_FIELDS.some(field => lowerKey.includes(field))) {
      sanitized[key] = '[REDACTED]';
    } else if (typeof sanitized[key] === 'object') {
      sanitized[key] = sanitizeForLogging(sanitized[key]);
    }
  }
  
  return sanitized;
}

// Usage
app.post('/api/login', async (req, res) => {
  // ❌ VULNERABLE
  // console.log('Login request:', req.body);
  
  // ✅ SECURE
  console.log('Login request:', sanitizeForLogging(req.body));
  // Output: { email: 'user@example.com', password: '[REDACTED]' }
});
```

### Step 2: Use Structured Logging

```javascript
const winston = require('winston');

const logger = winston.createLogger({
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' })
  ]
});

// Add sanitization
logger.add(new winston.transports.Console({
  format: winston.format.printf((info) => {
    const sanitized = sanitizeForLogging(info);
    return JSON.stringify(sanitized);
  })
}));

// Usage
logger.info('User login', {
  email: req.body.email,
  ip: req.ip
  // password automatically redacted
});
```

### Step 3: Environment-Based Logging

```javascript
const isDevelopment = process.env.NODE_ENV === 'development';

function safeLog(level, message, data) {
  if (isDevelopment) {
    // More details in development
    console[level](message, data);
  } else {
    // Sanitized in production
    const sanitized = sanitizeForLogging(data);
    logger[level](message, sanitized);
  }
}

// Usage
safeLog('info', 'Login attempt', req.body);
```

## 📝 Code Examples

### ❌ Vulnerable

```javascript
// ❌ VULNERABLE: Logs sensitive data
app.post('/api/login', async (req, res) => {
  console.log('Login:', req.body); // ❌ Password logged!
  // ...
});

app.post('/api/payment', async (req, res) => {
  console.log('Payment:', req.body); // ❌ Credit card logged!
  // ...
});
```

### ✅ Secure

```javascript
// ✅ SECURE: Sanitized logging
app.post('/api/login', async (req, res) => {
  logger.info('Login attempt', {
    email: req.body.email,
    ip: req.ip
    // password not logged
  });
  // ...
});

app.post('/api/payment', async (req, res) => {
  logger.info('Payment processed', {
    amount: req.body.amount,
    userId: req.user.id
    // credit card not logged
  });
  // ...
});
```

## 🧪 Testing Checklist

- [ ] No passwords in logs
- [ ] No tokens in logs
- [ ] No PII in logs
- [ ] Log sanitization implemented
- [ ] Structured logging used
- [ ] Sensitive fields redacted
- [ ] Log access restricted

## 📚 References

- [OWASP: Logging](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html)
- [Winston Logger](https://github.com/winstonjs/winston)

## 🔗 Related Vulnerabilities

- [03. Exposed API Keys in Repos](./03_exposed_api_keys.md)
- [09. Verbose Error Information Leakage](../code_security/09_verbose_error_leakage.md)

---

**Classification**:
- **Confirmed** if sensitive data found in logs
- **Likely** if console.log used with user input
- **Not Applicable** if logs properly sanitized
