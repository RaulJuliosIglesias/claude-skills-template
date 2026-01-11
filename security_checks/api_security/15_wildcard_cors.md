# 15. Wildcard CORS Configuration

## 🟠 Risk Level: **HIGH**

## 📋 Vulnerability Description

To quickly fix "Cross-Origin" errors during development, AI tools often suggest setting the CORS header `Access-Control-Allow-Origin` to `*`. In production, this allows any malicious website to read data from your API on behalf of an authenticated user, leading to data exfiltration.

**Impact:**
- Data exfiltration
- CSRF attacks
- Unauthorized API access
- Privacy violations

## 🎯 Context: Why This Happens

Developers:
- Copy quick-fix solutions
- Don't understand CORS security implications
- Use wildcard for "easy" setup
- Forget to restrict in production

## 🔍 Detection Methods

### 1. Code Analysis

**Search for:**
```javascript
// ❌ VULNERABLE
Access-Control-Allow-Origin: *
origin: '*'
cors({ origin: '*' })
```

**Check CORS configuration:**
- Express: `cors` middleware
- FastAPI: `CORSMiddleware`
- Django: `CORS_ALLOWED_ORIGINS`

### 2. Testing

**Check CORS headers:**
```bash
curl -H "Origin: https://evil.com" \
  -H "Access-Control-Request-Method: GET" \
  -X OPTIONS https://api.example.com/users

# Check response headers
# If Access-Control-Allow-Origin: * → VULNERABLE
```

## ✅ Verification Requirements

### Must Have:
1. **Whitelist Specific Origins**
   - Only allow trusted domains
   - No wildcard in production
   - Environment-based configuration

2. **Credentials Handling**
   - `Access-Control-Allow-Credentials: true` only with specific origins
   - Never use wildcard with credentials

3. **Method and Header Restrictions**
   - Only allow necessary HTTP methods
   - Only allow necessary headers

## 🚨 Exploit Path

### Scenario 1: Data Exfiltration
```
1. User is logged into victim-site.com
2. User visits attacker-site.com
3. Attacker's page makes request:
   fetch('https://api.victim-site.com/users/me', {
     credentials: 'include'
   })
4. Browser sends request with user's cookies
5. API returns data (CORS allows *)
6. Attacker receives user data
7. Data exfiltrated
```

## 🔧 Remediation Steps

### Step 1: Configure CORS Properly

**Express:**
```javascript
const cors = require('cors');

const allowedOrigins = [
  'https://yourdomain.com',
  'https://www.yourdomain.com',
  ...(process.env.NODE_ENV === 'development' ? ['http://localhost:3000'] : [])
];

app.use(cors({
  origin: function (origin, callback) {
    // Allow requests with no origin (mobile apps, Postman, etc.)
    if (!origin) return callback(null, true);
    
    if (allowedOrigins.indexOf(origin) !== -1) {
      callback(null, true);
    } else {
      callback(new Error('Not allowed by CORS'));
    }
  },
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));
```

**FastAPI:**
```python
from fastapi.middleware.cors import CORSMiddleware

allowed_origins = [
    "https://yourdomain.com",
    "https://www.yourdomain.com",
]

if os.getenv("ENVIRONMENT") == "development":
    allowed_origins.append("http://localhost:3000")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
)
```

### Step 2: Environment-Based Configuration

```javascript
// config/cors.js
const allowedOrigins = {
  production: [
    'https://yourdomain.com',
    'https://www.yourdomain.com'
  ],
  development: [
    'http://localhost:3000',
    'http://localhost:3001'
  ]
};

module.exports = {
  origin: allowedOrigins[process.env.NODE_ENV] || allowedOrigins.production,
  credentials: true
};
```

### Step 3: Validate Origin Header

```javascript
function validateOrigin(req, res, next) {
  const origin = req.get('origin');
  const allowedOrigins = process.env.ALLOWED_ORIGINS.split(',');
  
  if (!origin) {
    // No origin header (same-origin or non-browser)
    return next();
  }
  
  if (allowedOrigins.includes(origin)) {
    res.setHeader('Access-Control-Allow-Origin', origin);
    res.setHeader('Access-Control-Allow-Credentials', 'true');
    return next();
  }
  
  res.status(403).json({ error: 'Origin not allowed' });
}
```

## 📝 Code Examples

### ❌ Vulnerable Code

```javascript
// ❌ VULNERABLE: Wildcard CORS
const cors = require('cors');
app.use(cors({
  origin: '*' // ❌ Allows any origin
}));

// ❌ VULNERABLE: Wildcard with credentials (invalid but common mistake)
app.use(cors({
  origin: '*',
  credentials: true // ❌ Browser will reject this
}));
```

### ✅ Secure Code

```javascript
// ✅ SECURE: Whitelist specific origins
const cors = require('cors');

const allowedOrigins = [
  'https://yourdomain.com',
  'https://www.yourdomain.com'
];

if (process.env.NODE_ENV === 'development') {
  allowedOrigins.push('http://localhost:3000');
}

app.use(cors({
  origin: function (origin, callback) {
    if (!origin || allowedOrigins.includes(origin)) {
      callback(null, true);
    } else {
      callback(new Error('Not allowed by CORS'));
    }
  },
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));
```

## 🧪 Testing Checklist

- [ ] No wildcard (*) in CORS configuration
- [ ] Only trusted origins allowed
- [ ] Credentials handled correctly
- [ ] Methods restricted appropriately
- [ ] Headers restricted appropriately
- [ ] Environment-based configuration
- [ ] Development origins separate from production
- [ ] CORS errors logged for monitoring

## 📚 References

- [OWASP: CORS Misconfiguration](https://owasp.org/www-community/attacks/CORS_Misconfiguration)
- [MDN: CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
- [Express CORS](https://expressjs.com/en/resources/middleware/cors.html)

## 🔗 Related Vulnerabilities

- [13. Missing CSRF Protection](./13_missing_csrf_protection.md)
- [25. Insecure Session Storage](../data_protection/25_insecure_session_storage.md)
- [29. Missing Content Security Policy](./29_missing_csp.md)

---

**Classification**:
- **Confirmed** if CORS set to wildcard (*) in production
- **Likely** if origins not properly validated
- **Not Applicable** if specific origins whitelisted and validated
