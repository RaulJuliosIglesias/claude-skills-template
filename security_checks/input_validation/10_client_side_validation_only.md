# 10. Client-Side Input Validation Only

## 🔴 Risk Level: **CRITICAL**

## 📋 Vulnerability Description

Relying solely on browser-based validation allows attackers to bypass checks by sending raw API requests. This leads to the injection of malicious scripts (XSS) or SQL commands directly into the backend processing logic.

**Impact:**
- XSS attacks
- SQL injection
- Command injection
- Data corruption
- Unauthorized access

## 🎯 Context: Why This Happens

AI-generated forms often:
- Focus on user experience (client-side validation)
- Don't implement server-side validation
- Trust client input
- Copy frontend validation to backend without adaptation

## 🔍 Detection Methods

### 1. Code Analysis

**Check for:**
- Server-side validation middleware
- Input sanitization functions
- Schema validation (Zod, Joi, Yup)
- Type checking

**Red Flags:**
```javascript
// ❌ VULNERABLE: No server-side validation
app.post('/api/users', async (req, res) => {
  const user = await User.create(req.body); // ❌ Trusts client input
  res.json(user);
});

// ✅ SECURE: Server-side validation
const { body, validationResult } = require('express-validator');
app.post('/api/users', 
  body('email').isEmail(),
  body('password').isLength({ min: 8 }),
  async (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }
    const user = await User.create(req.body);
    res.json(user);
  }
);
```

### 2. Testing

**Bypass client validation:**
```bash
# Send request directly to API, bypassing frontend
curl -X POST https://api.example.com/users \
  -H "Content-Type: application/json" \
  -d '{"email":"<script>alert(1)</script>","password":"x"}'

# If request succeeds → No server-side validation
```

## ✅ Verification Requirements

### Must Have:
1. **Server-Side Validation**
   - All inputs validated on server
   - Type checking
   - Length limits
   - Format validation

2. **Input Sanitization**
   - HTML sanitization
   - SQL injection prevention
   - Command injection prevention
   - Path traversal prevention

3. **Schema Validation**
   - Use validation libraries (Zod, Joi, Yup)
   - Define expected structure
   - Reject unexpected fields

## 🚨 Exploit Path

### Scenario 1: XSS Attack
```
1. Attacker opens browser DevTools
2. Attacker disables JavaScript (bypasses client validation)
3. Attacker sends POST request directly to API
4. Attacker includes: <script>alert(document.cookie)</script>
5. Server accepts input (no validation)
6. Script stored in database
7. Script executes when displayed
8. Cookies stolen
```

### Scenario 2: SQL Injection
```
1. Attacker bypasses frontend validation
2. Attacker sends: email = "admin' OR '1'='1"
3. Server uses input directly in query
4. SQL injection succeeds
5. Database compromised
```

## 🔧 Remediation Steps

### Step 1: Install Validation Library

```bash
# Express
npm install express-validator

# Or Zod (TypeScript-friendly)
npm install zod

# Or Joi
npm install joi
```

### Step 2: Implement Server-Side Validation

**Express-Validator:**
```javascript
const { body, validationResult } = require('express-validator');

app.post('/api/users',
  // Validation rules
  body('email')
    .isEmail()
    .normalizeEmail()
    .withMessage('Invalid email address'),
  body('password')
    .isLength({ min: 8 })
    .matches(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/)
    .withMessage('Password must be at least 8 characters with uppercase, lowercase, and number'),
  body('name')
    .trim()
    .isLength({ min: 1, max: 100 })
    .escape()
    .withMessage('Name must be between 1 and 100 characters'),
  
  // Validation middleware
  (req, res, next) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }
    next();
  },
  
  // Handler
  async (req, res) => {
    const user = await User.create(req.body);
    res.json(user);
  }
);
```

**Zod (TypeScript):**
```typescript
import { z } from 'zod';

const userSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8).regex(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/),
  name: z.string().min(1).max(100),
  age: z.number().int().min(0).max(120)
});

app.post('/api/users', async (req, res) => {
  try {
    // Validate and parse
    const validated = userSchema.parse(req.body);
    const user = await User.create(validated);
    res.json(user);
  } catch (err) {
    if (err instanceof z.ZodError) {
      return res.status(400).json({ errors: err.errors });
    }
    throw err;
  }
});
```

### Step 3: Sanitize Inputs

```javascript
const validator = require('validator');
const xss = require('xss');

function sanitizeInput(input) {
  if (typeof input === 'string') {
    // Remove HTML tags
    input = validator.escape(input);
    // XSS protection
    input = xss(input);
    // Trim whitespace
    input = input.trim();
  }
  return input;
}

function sanitizeObject(obj) {
  const sanitized = {};
  for (const [key, value] of Object.entries(obj)) {
    if (typeof value === 'string') {
      sanitized[key] = sanitizeInput(value);
    } else if (typeof value === 'object' && value !== null) {
      sanitized[key] = sanitizeObject(value);
    } else {
      sanitized[key] = value;
    }
  }
  return sanitized;
}

app.post('/api/users', async (req, res) => {
  // Sanitize all inputs
  const sanitized = sanitizeObject(req.body);
  const user = await User.create(sanitized);
  res.json(user);
});
```

### Step 4: Use Parameterized Queries

```javascript
// ❌ VULNERABLE: String concatenation
const query = `SELECT * FROM users WHERE email = '${email}'`;

// ✅ SECURE: Parameterized query
const query = 'SELECT * FROM users WHERE email = $1';
const result = await db.query(query, [email]);
```

### Step 5: Whitelist Allowed Fields

```javascript
const allowedFields = ['email', 'name', 'password'];

function whitelistFields(data, allowed) {
  const filtered = {};
  for (const field of allowed) {
    if (data[field] !== undefined) {
      filtered[field] = data[field];
    }
  }
  return filtered;
}

app.post('/api/users', async (req, res) => {
  // Only allow specific fields
  const filtered = whitelistFields(req.body, allowedFields);
  const user = await User.create(filtered);
  res.json(user);
});
```

## 📝 Code Examples

### ❌ Vulnerable Code

```javascript
// ❌ VULNERABLE: No server-side validation
app.post('/api/users', async (req, res) => {
  // Trusts client input completely
  const user = await User.create(req.body);
  res.json(user);
});

// ❌ VULNERABLE: Client validation only
// Frontend (React)
function RegisterForm() {
  const handleSubmit = (e) => {
    e.preventDefault();
    // Client-side validation only
    if (!email.includes('@')) {
      alert('Invalid email');
      return;
    }
    fetch('/api/users', {
      method: 'POST',
      body: JSON.stringify({ email, password })
    });
  };
}
```

### ✅ Secure Code

```javascript
// ✅ SECURE: Server-side validation
const { body, validationResult } = require('express-validator');

app.post('/api/users',
  // Validation rules
  body('email')
    .isEmail()
    .normalizeEmail()
    .withMessage('Invalid email'),
  body('password')
    .isLength({ min: 8 })
    .matches(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/)
    .withMessage('Password requirements not met'),
  body('name')
    .trim()
    .isLength({ min: 1, max: 100 })
    .escape(),
  
  // Check validation results
  (req, res, next) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }
    next();
  },
  
  // Handler
  async (req, res) => {
    const user = await User.create(req.body);
    res.json(user);
  }
);

// ✅ SECURE: Client + Server validation
// Frontend validates for UX, backend validates for security
```

## 🧪 Testing Checklist

- [ ] All API endpoints have server-side validation
- [ ] Inputs are sanitized (HTML, SQL, etc.)
- [ ] Type checking implemented
- [ ] Length limits enforced
- [ ] Format validation (email, URL, etc.)
- [ ] Unexpected fields rejected
- [ ] Parameterized queries used
- [ ] Client validation bypassed in tests
- [ ] XSS payloads rejected
- [ ] SQL injection attempts blocked

## 📚 References

- [OWASP: Input Validation](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html)
- [OWASP: XSS Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)
- [Express Validator](https://express-validator.github.io/docs/)
- [Zod Documentation](https://zod.dev/)

## 🔗 Related Vulnerabilities

- [16. Unrestricted File Uploads](./16_unrestricted_file_uploads.md)
- [34. Path Traversal](./34_path_traversal.md)
- [39. Unsanitized DOM Injection](./39_unsanitized_dom_injection.md)

---

**Classification**:
- **Confirmed** if API accepts input without server-side validation
- **Likely** if validation exists but is incomplete
- **Not Applicable** if all inputs validated and sanitized server-side
