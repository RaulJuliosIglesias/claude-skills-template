# 1. Missing API Rate Limiting

## 🔴 Risk Level: **CRITICAL**

## 📋 Vulnerability Description

API endpoints lack rate limiting mechanisms, making them vulnerable to brute-force attacks, credential stuffing, and resource exhaustion (Application-Layer DDoS). This is the **most common vulnerability** in AI-generated applications, found in **35% of analyzed projects**.

## 🎯 Context: Why This Happens

AI code generators prioritize functionality over security. They create endpoints that work but don't include protective middleware. Common scenarios:

- Login endpoints without throttling
- Registration endpoints open to abuse
- API endpoints without request limits
- Public endpoints vulnerable to scraping

## 🔍 Detection Methods

### 1. Code Analysis

**Search for:**
- Express.js: Look for `express-rate-limit` or similar middleware
- FastAPI: Check for `SlowAPI` or rate limiting decorators
- Django: Look for `django-ratelimit` or throttling classes
- Flask: Check for `Flask-Limiter`

**Red Flags:**
```javascript
// ❌ VULNERABLE: No rate limiting
app.post('/api/login', async (req, res) => {
  // Authentication logic
});

// ✅ SECURE: Rate limiting applied
const rateLimit = require('express-rate-limit');
const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5 // 5 attempts per window
});
app.post('/api/login', loginLimiter, async (req, res) => {
  // Authentication logic
});
```

### 2. Configuration Review

**Check for:**
- Rate limiting middleware configuration
- NGINX `limit_req` directives
- Cloud provider rate limiting (AWS WAF, Cloudflare)
- API Gateway throttling settings

### 3. Testing

**Manual Testing:**
```bash
# Test if rate limiting exists
for i in {1..100}; do
  curl -X POST https://api.example.com/login \
    -d "email=test@example.com&password=test"
done

# If all requests succeed → No rate limiting
# If requests start failing after threshold → Rate limiting exists
```

**Automated Testing:**
```python
import requests
import time

def test_rate_limit(url, max_requests=100):
    success_count = 0
    for i in range(max_requests):
        response = requests.post(url, json={"email": "test@example.com"})
        if response.status_code == 200:
            success_count += 1
        time.sleep(0.1)
    
    if success_count == max_requests:
        return "VULNERABLE: No rate limiting detected"
    return f"Rate limiting active: {success_count}/{max_requests} succeeded"
```

## ✅ Verification Requirements

### Must Have:
1. **Rate limiting on authentication endpoints**
   - Login: Max 5 attempts per 15 minutes per IP
   - Registration: Max 3 attempts per hour per IP
   - Password reset: Max 5 attempts per hour per IP

2. **Rate limiting on public API endpoints**
   - General API: 100 requests per minute per IP
   - Search endpoints: 30 requests per minute per IP
   - File upload: 10 requests per hour per IP

3. **Progressive penalties**
   - Temporary IP ban after repeated violations
   - CAPTCHA challenge after threshold

### Implementation Examples

**Express.js:**
```javascript
const rateLimit = require('express-rate-limit');
const { RedisStore } = require('rate-limit-redis');
const Redis = require('ioredis');

const redis = new Redis({
  host: process.env.REDIS_HOST,
  port: process.env.REDIS_PORT
});

// Login rate limiter
const loginLimiter = rateLimit({
  store: new RedisStore({
    client: redis,
    prefix: 'rl:login:'
  }),
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5, // 5 attempts
  message: 'Too many login attempts, please try again later',
  standardHeaders: true,
  legacyHeaders: false,
  skipSuccessfulRequests: true, // Don't count successful logins
  skipFailedRequests: false
});

// Apply to login route
app.post('/api/auth/login', loginLimiter, loginHandler);
```

**FastAPI:**
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import FastAPI, Request

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/api/auth/login")
@limiter.limit("5/15minutes")
async def login(request: Request):
    # Login logic
    pass
```

**Django:**
```python
from django_ratelimit.decorators import ratelimit
from django.views.decorators.http import require_http_methods

@ratelimit(key='ip', rate='5/15m', method='POST')
@require_http_methods(["POST"])
def login_view(request):
    # Login logic
    pass
```

**NGINX Configuration:**
```nginx
http {
    limit_req_zone $binary_remote_addr zone=login:10m rate=5r/15m;
    limit_req_zone $binary_remote_addr zone=api:10m rate=100r/m;
    
    server {
        location /api/auth/login {
            limit_req zone=login burst=2 nodelay;
            # ... rest of config
        }
        
        location /api/ {
            limit_req zone=api burst=20 nodelay;
            # ... rest of config
        }
    }
}
```

## 🚨 Exploit Path

### Scenario 1: Brute Force Attack
```
1. Attacker identifies login endpoint: /api/auth/login
2. Attacker creates script to try 10,000 common passwords
3. Script sends requests at 100 requests/second
4. Without rate limiting, all requests are processed
5. Attacker eventually finds correct password
6. Account compromised
```

### Scenario 2: Credential Stuffing
```
1. Attacker obtains leaked credentials database
2. Attacker tests credentials against your API
3. Without rate limiting, can test millions of combinations
4. Finds accounts using same password from leak
5. Multiple accounts compromised
```

### Scenario 3: Resource Exhaustion (DoS)
```
1. Attacker targets expensive endpoint (e.g., /api/search)
2. Sends thousands of requests per second
3. Server CPU/memory exhausted
4. Legitimate users cannot access service
5. Application becomes unavailable
```

## 🔧 Remediation Steps

### Step 1: Install Rate Limiting Library

**Node.js/Express:**
```bash
npm install express-rate-limit
# For Redis-backed (recommended for production)
npm install rate-limit-redis ioredis
```

**Python/FastAPI:**
```bash
pip install slowapi
```

**Python/Django:**
```bash
pip install django-ratelimit
```

### Step 2: Configure Rate Limiters

Create separate limiters for different endpoint types:
- Authentication endpoints (strict)
- Public API endpoints (moderate)
- Internal/admin endpoints (lenient)

### Step 3: Use Redis for Distributed Systems

If your application runs on multiple servers, use Redis to share rate limit state:

```javascript
const RedisStore = require('rate-limit-redis');
const Redis = require('ioredis');

const redis = new Redis(process.env.REDIS_URL);

const limiter = rateLimit({
  store: new RedisStore({
    client: redis,
    prefix: 'rl:'
  }),
  // ... config
});
```

### Step 4: Implement Progressive Penalties

```javascript
const createProgressiveLimiter = (baseWindow, baseMax) => {
  return async (req, res, next) => {
    const key = `rl:${req.ip}`;
    const violations = await redis.incr(`${key}:violations`);
    
    let windowMs = baseWindow;
    let max = baseMax;
    
    if (violations > 10) {
      // After 10 violations, ban for 1 hour
      await redis.setex(`${key}:banned`, 3600, '1');
      return res.status(429).json({ error: 'IP banned for 1 hour' });
    } else if (violations > 5) {
      // After 5 violations, stricter limits
      windowMs = baseWindow * 2;
      max = Math.floor(baseMax / 2);
    }
    
    // Apply rate limit with adjusted values
    // ... rate limiting logic
  };
};
```

### Step 5: Add CAPTCHA After Threshold

```javascript
const rateLimit = require('express-rate-limit');
const { verifyCaptcha } = require('./captcha');

const strictLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5,
  handler: async (req, res) => {
    // After 5 failed attempts, require CAPTCHA
    return res.status(429).json({
      error: 'Too many attempts',
      requiresCaptcha: true
    });
  }
});

app.post('/api/auth/login', strictLimiter, async (req, res) => {
  if (req.body.requiresCaptcha && !await verifyCaptcha(req.body.captchaToken)) {
    return res.status(400).json({ error: 'Invalid CAPTCHA' });
  }
  // ... login logic
});
```

### Step 6: Monitor and Alert

```javascript
const rateLimit = require('express-rate-limit');

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5,
  onLimitReached: (req, res) => {
    // Log security event
    securityLogger.warn('Rate limit exceeded', {
      ip: req.ip,
      endpoint: req.path,
      timestamp: new Date()
    });
    
    // Alert security team if pattern detected
    if (isAttackPattern(req)) {
      alertSecurityTeam(req);
    }
  }
});
```

## 📝 Code Examples

### ❌ Vulnerable Code

```javascript
// No rate limiting - VULNERABLE
app.post('/api/auth/login', async (req, res) => {
  const { email, password } = req.body;
  const user = await User.findOne({ email });
  
  if (user && await bcrypt.compare(password, user.password)) {
    const token = generateToken(user);
    res.json({ token });
  } else {
    res.status(401).json({ error: 'Invalid credentials' });
  }
});
```

### ✅ Secure Code

```javascript
const rateLimit = require('express-rate-limit');
const RedisStore = require('rate-limit-redis');
const Redis = require('ioredis');

const redis = new Redis(process.env.REDIS_URL);

// Strict rate limiter for login
const loginLimiter = rateLimit({
  store: new RedisStore({
    client: redis,
    prefix: 'rl:login:'
  }),
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5, // 5 attempts
  message: {
    error: 'Too many login attempts. Please try again in 15 minutes.',
    retryAfter: 15 * 60
  },
  standardHeaders: true,
  legacyHeaders: false,
  skipSuccessfulRequests: true,
  handler: (req, res) => {
    securityLogger.warn('Login rate limit exceeded', {
      ip: req.ip,
      email: req.body.email,
      timestamp: new Date()
    });
    res.status(429).json({
      error: 'Too many login attempts. Please try again in 15 minutes.',
      retryAfter: 15 * 60
    });
  }
});

app.post('/api/auth/login', loginLimiter, async (req, res) => {
  const { email, password } = req.body;
  const user = await User.findOne({ email });
  
  if (user && await bcrypt.compare(password, user.password)) {
    const token = generateToken(user);
    res.json({ token });
  } else {
    res.status(401).json({ error: 'Invalid credentials' });
  }
});
```

## 🧪 Testing Checklist

- [ ] Login endpoint rejects requests after 5 attempts in 15 minutes
- [ ] Rate limit resets after window expires
- [ ] Different IPs have separate rate limits
- [ ] Successful logins don't count toward limit
- [ ] Rate limit headers are returned (X-RateLimit-*)
- [ ] Redis-backed rate limiting works across multiple servers
- [ ] CAPTCHA required after threshold (if implemented)
- [ ] Security events logged when limit exceeded
- [ ] Rate limits configured for all public endpoints
- [ ] Admin endpoints have appropriate limits

## 📚 References

- [OWASP: API Security Top 10 - API4:2019 Lack of Resources & Rate Limiting](https://owasp.org/www-project-api-security/)
- [Express Rate Limit Documentation](https://github.com/express-rate-limit/express-rate-limit)
- [NGINX Rate Limiting](https://www.nginx.com/blog/rate-limiting-nginx/)
- [AWS WAF Rate-Based Rules](https://docs.aws.amazon.com/waf/latest/developerguide/waf-rule-statement-type-rate-based.html)
- [Cloudflare Rate Limiting](https://developers.cloudflare.com/waf/rate-limiting-rules/)

## 🔗 Related Vulnerabilities

- [02. Unrestricted Bot Registration](./02_unrestricted_bot_registration.md)
- [13. Missing CSRF Protection](../api_security/13_missing_csrf_protection.md)
- [35. Missing Route-Level Authorization](./35_missing_route_authorization.md)

---

**Classification**: When reviewing code, mark as:
- **Confirmed** if no rate limiting middleware is found
- **Likely** if rate limiting exists but is too lenient
- **Not Applicable** if endpoint is internal-only with network-level protection
