# 13. Missing CSRF Protection

## 🟠 Risk Level: **HIGH**

## 📋 Vulnerability Description

AI-generated REST APIs frequently lack Cross-Site Request Forgery (CSRF) tokens. This allows attackers to create malicious websites that trick authenticated users into silently performing actions (like changing their email or deleting their account) simply by visiting a link.

**Impact:**
- Unauthorized actions on behalf of users
- Account takeover
- Data modification
- Financial transactions

## 🎯 Context: Why This Happens

Modern SPAs often:
- Use token-based auth (JWT) which seems CSRF-safe
- Don't implement CSRF protection
- Rely on CORS alone (insufficient)
- Forget CSRF for state-changing operations

## 🔍 Detection Methods

### 1. Code Analysis

**Search for:**
- CSRF middleware (csurf, csrf)
- CSRF token generation
- Token validation in requests

**Red Flags:**
```javascript
// ❌ VULNERABLE: No CSRF protection
app.post('/api/users/email', requireAuth, async (req, res) => {
  await User.update({ email: req.body.email });
  res.json({ success: true });
});

// ✅ SECURE: CSRF protection
const csrf = require('csurf');
const csrfProtection = csrf({ cookie: true });
app.post('/api/users/email', 
  requireAuth,
  csrfProtection,
  async (req, res) => {
    await User.update({ email: req.body.email });
    res.json({ success: true });
  }
);
```

### 2. Testing

**CSRF Test:**
```html
<!-- malicious-site.com/attack.html -->
<form action="https://victim-site.com/api/users/email" method="POST">
  <input type="hidden" name="email" value="attacker@evil.com">
</form>
<script>document.forms[0].submit();</script>
```

If request succeeds → CSRF vulnerability exists.

## ✅ Verification Requirements

### Must Have:
1. **CSRF Tokens for State-Changing Operations**
   - POST, PUT, DELETE, PATCH requests
   - Token in request header or body
   - Token validated server-side

2. **SameSite Cookie Attribute**
   - `SameSite=Strict` or `SameSite=Lax`
   - Prevents cross-site cookie sending

3. **Origin/Referer Validation**
   - Verify request origin
   - Reject cross-origin state-changing requests

## 🚨 Exploit Path

### Scenario 1: Email Change Attack
```
1. User is logged into victim-site.com
2. User visits attacker-site.com
3. Attacker's page contains hidden form:
   <form action="https://victim-site.com/api/users/email" method="POST">
     <input name="email" value="attacker@evil.com">
   </form>
4. Form auto-submits (or user clicks link)
5. Browser sends request with user's session cookie
6. Server processes request (no CSRF token check)
7. User's email changed to attacker's
8. Attacker resets password using new email
9. Account compromised
```

## 🔧 Remediation Steps

### Step 1: Install CSRF Protection

```bash
npm install csurf
# Or for Express
npm install express-session csurf
```

### Step 2: Implement CSRF Tokens

**Express with Sessions:**
```javascript
const express = require('express');
const session = require('express-session');
const csrf = require('csurf');

const app = express();

// Session middleware (required for csurf)
app.use(session({
  secret: process.env.SESSION_SECRET,
  resave: false,
  saveUninitialized: false,
  cookie: {
    secure: true, // HTTPS only
    httpOnly: true,
    sameSite: 'strict'
  }
}));

// CSRF protection
const csrfProtection = csrf({ cookie: true });

// Get CSRF token endpoint
app.get('/api/csrf-token', csrfProtection, (req, res) => {
  res.json({ csrfToken: req.csrfToken() });
});

// Protected endpoint
app.post('/api/users/email',
  requireAuth,
  csrfProtection, // Validate CSRF token
  async (req, res) => {
    await User.update({ email: req.body.email });
    res.json({ success: true });
  }
);
```

**Frontend (React):**
```jsx
import { useState, useEffect } from 'react';

function EmailForm() {
  const [csrfToken, setCsrfToken] = useState('');
  
  useEffect(() => {
    // Get CSRF token on mount
    fetch('/api/csrf-token', { credentials: 'include' })
      .then(res => res.json())
      .then(data => setCsrfToken(data.csrfToken));
  }, []);
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    await fetch('/api/users/email', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRF-Token': csrfToken // Include token
      },
      credentials: 'include',
      body: JSON.stringify({ email: newEmail })
    });
  };
  
  return (
    <form onSubmit={handleSubmit}>
      <input type="hidden" name="_csrf" value={csrfToken} />
      {/* form fields */}
    </form>
  );
}
```

### Step 3: Use SameSite Cookies

```javascript
app.use(session({
  secret: process.env.SESSION_SECRET,
  cookie: {
    secure: true,
    httpOnly: true,
    sameSite: 'strict' // Prevents cross-site requests
  }
}));
```

### Step 4: Origin/Referer Validation

```javascript
function validateOrigin(req, res, next) {
  const origin = req.get('origin');
  const referer = req.get('referer');
  const allowedOrigins = [
    'https://yourdomain.com',
    'https://www.yourdomain.com'
  ];
  
  if (req.method === 'GET') {
    return next(); // GET requests are safe
  }
  
  // Check origin
  if (origin && allowedOrigins.includes(origin)) {
    return next();
  }
  
  // Check referer
  if (referer) {
    const refererUrl = new URL(referer);
    if (allowedOrigins.includes(refererUrl.origin)) {
      return next();
    }
  }
  
  res.status(403).json({ error: 'Invalid origin' });
}

app.use(validateOrigin);
```

### Step 5: Double Submit Cookie Pattern (JWT)

**For JWT-based auth (no sessions):**
```javascript
// Generate CSRF token
function generateCSRFToken() {
  return crypto.randomBytes(32).toString('hex');
}

// Set CSRF token in cookie
app.get('/api/csrf-token', (req, res) => {
  const token = generateCSRFToken();
  res.cookie('XSRF-TOKEN', token, {
    httpOnly: false, // Must be readable by JavaScript
    secure: true,
    sameSite: 'strict'
  });
  res.json({ csrfToken: token });
});

// Validate CSRF token
function validateCSRF(req, res, next) {
  const cookieToken = req.cookies['XSRF-TOKEN'];
  const headerToken = req.get('X-CSRF-Token') || req.body._csrf;
  
  if (!cookieToken || !headerToken || cookieToken !== headerToken) {
    return res.status(403).json({ error: 'Invalid CSRF token' });
  }
  
  next();
}

app.post('/api/users/email',
  requireAuth,
  validateCSRF,
  async (req, res) => {
    await User.update({ email: req.body.email });
    res.json({ success: true });
  }
);
```

## 📝 Code Examples

### ❌ Vulnerable Code

```javascript
// ❌ VULNERABLE: No CSRF protection
app.post('/api/users/email', requireAuth, async (req, res) => {
  await User.update({ email: req.body.email });
  res.json({ success: true });
});

app.delete('/api/users/:id', requireAuth, async (req, res) => {
  await User.destroy({ where: { id: req.params.id } });
  res.json({ success: true });
});
```

### ✅ Secure Code

```javascript
// ✅ SECURE: CSRF protection
const csrf = require('csurf');
const csrfProtection = csrf({ cookie: true });

// Get token
app.get('/api/csrf-token', csrfProtection, (req, res) => {
  res.json({ csrfToken: req.csrfToken() });
});

// Protected endpoints
app.post('/api/users/email',
  requireAuth,
  csrfProtection,
  async (req, res) => {
    await User.update({ email: req.body.email });
    res.json({ success: true });
  }
);

app.delete('/api/users/:id',
  requireAuth,
  csrfProtection,
  async (req, res) => {
    await User.destroy({ where: { id: req.params.id } });
    res.json({ success: true });
  }
);
```

## 🧪 Testing Checklist

- [ ] CSRF tokens required for POST/PUT/DELETE
- [ ] Tokens validated server-side
- [ ] SameSite cookie attribute set
- [ ] Origin validation implemented
- [ ] GET requests don't require tokens
- [ ] Token generation endpoint exists
- [ ] Frontend includes tokens in requests
- [ ] Invalid tokens rejected
- [ ] Token rotation on login/logout

## 📚 References

- [OWASP: CSRF Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html)
- [Express CSRF](https://github.com/expressjs/csurf)
- [SameSite Cookies](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie/SameSite)

## 🔗 Related Vulnerabilities

- [15. Wildcard CORS Configuration](./15_wildcard_cors.md)
- [25. Insecure Session Storage](../data_protection/25_insecure_session_storage.md)
- [29. Missing Content Security Policy](./29_missing_csp.md)

---

**Classification**:
- **Confirmed** if state-changing endpoints have no CSRF protection
- **Likely** if using JWT without CSRF tokens
- **Not Applicable** if using SameSite=Strict cookies and proper validation
