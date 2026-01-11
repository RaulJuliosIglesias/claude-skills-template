# 19. Unbounded Payload Processing (DoS)

## 🟠 Risk Level: **HIGH**

## 📋 Vulnerability Description

AI-generated socket servers often read data into memory until a specific delimiter is found or the connection closes, without enforcing a maximum size limit. Attackers can send a multi-gigabyte payload (e.g., a "zip bomb" or massive string) to exhaust server RAM and crash the application (Denial of Service).

**Impact:**
- Denial of Service
- Server crash
- Resource exhaustion
- Service unavailability

## 🎯 Context: Why This Happens

AI code:
- Reads until delimiter
- No size limits
- Loads entire payload into memory
- Doesn't consider DoS attacks

## 🔍 Detection Methods

### 1. Code Analysis

**Search for:**
```javascript
// ❌ VULNERABLE: No size limit
req.on('data', (chunk) => {
  buffer += chunk; // No limit!
});
```

### 2. Testing

```bash
# Send large payload
dd if=/dev/zero bs=1M count=1000 | curl -X POST https://api.example.com/upload -d @-
# If server crashes → VULNERABLE
```

## ✅ Verification Requirements

### Must Have:
1. **Size Limits**
   - Maximum payload size
   - Chunked reading with limits
   - Timeout on large requests

2. **Resource Protection**
   - Memory limits
   - Request timeouts
   - Connection limits

## 🚨 Exploit Path

### Scenario 1: Memory Exhaustion
```
1. Attacker sends 10GB payload
2. Server reads entire payload into memory
3. Server RAM exhausted
4. Server crashes
5. Service unavailable
```

## 🔧 Remediation Steps

### Step 1: Set Payload Limits

**Express:**
```javascript
const express = require('express');
const app = express();

// Limit request size
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ limit: '10mb', extended: true }));

// Or use body-parser
const bodyParser = require('body-parser');
app.use(bodyParser.json({ limit: '10mb' }));
```

**FastAPI:**
```python
from fastapi import FastAPI, Request
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app = FastAPI()

@app.middleware("http")
async def limit_upload_size(request: Request, call_next):
    if request.headers.get("content-length"):
        size = int(request.headers["content-length"])
        if size > 10 * 1024 * 1024:  # 10MB
            return Response("Payload too large", status_code=413)
    return await call_next(request)
```

### Step 2: Chunked Reading with Limits

```javascript
const MAX_SIZE = 10 * 1024 * 1024; // 10MB
let totalSize = 0;

req.on('data', (chunk) => {
  totalSize += chunk.length;
  
  if (totalSize > MAX_SIZE) {
    req.destroy(); // ✅ Stop reading
    return res.status(413).json({ error: 'Payload too large' });
  }
  
  buffer += chunk;
});
```

### Step 3: Set Timeouts

```javascript
// Request timeout
app.use((req, res, next) => {
  req.setTimeout(30000); // 30 seconds
  next();
});

// Or use express-timeout
const timeout = require('connect-timeout');
app.use(timeout('30s'));
```

## 📝 Code Examples

### ❌ Vulnerable

```javascript
// ❌ VULNERABLE: No size limit
app.post('/api/upload', (req, res) => {
  let buffer = '';
  req.on('data', (chunk) => {
    buffer += chunk; // ❌ Can grow infinitely
  });
  req.on('end', () => {
    // Process buffer
  });
});
```

### ✅ Secure

```javascript
// ✅ SECURE: Size limit enforced
const MAX_SIZE = 10 * 1024 * 1024;

app.post('/api/upload', (req, res) => {
  let buffer = '';
  let totalSize = 0;
  
  req.on('data', (chunk) => {
    totalSize += chunk.length;
    
    if (totalSize > MAX_SIZE) {
      req.destroy();
      return res.status(413).json({ error: 'Payload too large' });
    }
    
    buffer += chunk;
  });
  
  req.on('end', () => {
    // Process buffer
  });
  
  req.setTimeout(30000); // 30 second timeout
});
```

## 🧪 Testing Checklist

- [ ] Payload size limits enforced
- [ ] Large requests rejected
- [ ] Timeouts configured
- [ ] Memory usage controlled
- [ ] Chunked reading with limits
- [ ] Error handling for oversized requests

## 📚 References

- [OWASP: Denial of Service](https://owasp.org/www-community/attacks/Denial_of_Service)
- [CWE-400: Uncontrolled Resource Consumption](https://cwe.mitre.org/data/definitions/400.html)

## 🔗 Related Vulnerabilities

- [22. Server-Side Request Forgery](./22_server_side_request_forgery.md)
- [20. Memory Safety Violations](../code_security/20_memory_safety_violations.md)

---

**Classification**:
- **Confirmed** if no payload size limits
- **Likely** if limits too high or unenforced
- **Not Applicable** if proper limits and timeouts configured
