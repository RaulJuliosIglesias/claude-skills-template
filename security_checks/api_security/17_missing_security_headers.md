# 17. Missing HTTP Security Headers

## 🟠 Risk Level: **HIGH**

## 📋 Vulnerability Description

Beyond Content Security Policy (CSP), AI-generated servers often omit standard hardening headers. Specifically, missing `Strict-Transport-Security` (HSTS) allows Man-in-the-Middle downgrade attacks, and missing `X-Content-Type-Options: nosniff` allows browsers to execute non-script files as code.

**Impact:**
- MITM attacks
- MIME type confusion attacks
- Clickjacking
- Information leakage

## 🎯 Context: Why This Happens

AI code generators:
- Don't include security headers by default
- Focus on functionality
- Don't understand header importance

## 🔍 Detection Methods

### 1. Header Testing

```bash
# Check security headers
curl -I https://example.com

# Look for:
# - Strict-Transport-Security
# - X-Content-Type-Options
# - X-Frame-Options
# - Content-Security-Policy
# - Referrer-Policy
```

### 2. Online Tools

- [SecurityHeaders.com](https://securityheaders.com)
- [Mozilla Observatory](https://observatory.mozilla.org)

## ✅ Verification Requirements

### Must Have:
1. **HSTS**
   - `Strict-Transport-Security: max-age=31536000; includeSubDomains`
   - Long max-age (1 year+)

2. **Content Type Protection**
   - `X-Content-Type-Options: nosniff`

3. **Frame Protection**
   - `X-Frame-Options: DENY` or `SAMEORIGIN`

4. **Referrer Policy**
   - `Referrer-Policy: strict-origin-when-cross-origin`

## 🚨 Exploit Path

### Scenario 1: MITM Downgrade
```
1. User visits site via HTTP
2. Attacker intercepts
3. No HSTS header
4. Browser doesn't force HTTPS
5. Traffic intercepted
6. Credentials stolen
```

## 🔧 Remediation Steps

### Step 1: Use Helmet (Express)

```bash
npm install helmet
```

```javascript
const helmet = require('helmet');

app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'", "https://trusted-cdn.com"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      imgSrc: ["'self'", "data:", "https:"],
    },
  },
  hsts: {
    maxAge: 31536000,
    includeSubDomains: true,
    preload: true
  }
}));
```

### Step 2: Manual Headers

```javascript
app.use((req, res, next) => {
  // HSTS
  if (req.secure) {
    res.setHeader('Strict-Transport-Security', 'max-age=31536000; includeSubDomains; preload');
  }
  
  // Content Type
  res.setHeader('X-Content-Type-Options', 'nosniff');
  
  // Frame Options
  res.setHeader('X-Frame-Options', 'DENY');
  
  // Referrer Policy
  res.setHeader('Referrer-Policy', 'strict-origin-when-cross-origin');
  
  // Permissions Policy
  res.setHeader('Permissions-Policy', 'geolocation=(), microphone=(), camera=()');
  
  next();
});
```

## 📝 Code Examples

### ❌ Vulnerable

```javascript
// ❌ VULNERABLE: No security headers
app.get('/', (req, res) => {
  res.json({ message: 'Hello' });
});
```

### ✅ Secure

```javascript
// ✅ SECURE: Helmet middleware
const helmet = require('helmet');
app.use(helmet());
```

## 🧪 Testing Checklist

- [ ] HSTS header present
- [ ] X-Content-Type-Options: nosniff
- [ ] X-Frame-Options set
- [ ] Referrer-Policy configured
- [ ] CSP header set
- [ ] Permissions-Policy configured

## 📚 References

- [OWASP: Secure Headers](https://owasp.org/www-project-secure-headers/)
- [Helmet.js](https://helmetjs.github.io/)

## 🔗 Related Vulnerabilities

- [29. Missing Content Security Policy](./29_missing_csp.md)
- [31. Unencrypted Traffic](../infrastructure_security/31_unencrypted_traffic.md)

---

**Classification**:
- **Confirmed** if security headers missing
- **Likely** if headers incomplete
- **Not Applicable** if all headers properly configured
