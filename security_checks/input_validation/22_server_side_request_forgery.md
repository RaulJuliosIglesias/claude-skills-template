# 22. Server-Side Request Forgery (SSRF)

## 🔴 Risk Level: **CRITICAL**

## 📋 Vulnerability Description

Vibe-coded apps frequently include features to "fetch" or "summarize" external URLs. Without proper validation, attackers can force the server to send requests to internal infrastructure (e.g., AWS Metadata) to steal cloud credentials or scan the internal network.

**Impact:**
- Internal network scanning
- Cloud credential theft
- Internal service access
- Data exfiltration

## 🎯 Context: Why This Happens

AI code:
- Fetches user-provided URLs
- Doesn't validate URLs
- Allows any URL
- Doesn't block internal IPs

## 🔍 Detection Methods

### 1. Code Analysis

**Search for:**
```javascript
// ❌ VULNERABLE: Direct URL fetch
fetch(req.body.url)
axios.get(req.query.url)
```

### 2. Testing

```bash
# Test SSRF
curl -X POST https://api.example.com/fetch \
  -d '{"url": "http://169.254.169.254/latest/meta-data/"}'

# If returns metadata → VULNERABLE
```

## ✅ Verification Requirements

### Must Have:
1. **URL Validation**
   - Whitelist allowed domains
   - Block internal IPs
   - Validate URL format

2. **Network Restrictions**
   - Block private IP ranges
   - Block localhost
   - Use proxy for external requests

## 🚨 Exploit Path

### Scenario 1: AWS Metadata Access
```
1. Attacker finds URL fetch endpoint
2. Attacker sends: http://169.254.169.254/latest/meta-data/
3. Server fetches URL
4. Returns AWS metadata
5. Attacker gets credentials
6. Cloud account compromised
```

## 🔧 Remediation Steps

### Step 1: Validate URLs

```javascript
const url = require('url');
const dns = require('dns').promises;

const ALLOWED_DOMAINS = [
  'example.com',
  'trusted-cdn.com'
];

const BLOCKED_IPS = [
  '127.0.0.1',
  'localhost',
  '169.254.169.254', // AWS metadata
  '10.0.0.0/8',
  '172.16.0.0/12',
  '192.168.0.0/16'
];

async function validateUrl(userUrl) {
  const parsed = url.parse(userUrl);
  
  // Check protocol
  if (!['http:', 'https:'].includes(parsed.protocol)) {
    throw new Error('Invalid protocol');
  }
  
  // Check domain whitelist
  if (!ALLOWED_DOMAINS.some(domain => parsed.hostname.endsWith(domain))) {
    throw new Error('Domain not allowed');
  }
  
  // Resolve and check IP
  const addresses = await dns.resolve4(parsed.hostname);
  for (const ip of addresses) {
    if (isBlockedIP(ip)) {
      throw new Error('IP not allowed');
    }
  }
  
  return parsed;
}

function isBlockedIP(ip) {
  // Check against blocked ranges
  // Implementation of IP range checking
  return BLOCKED_IPS.some(blocked => ipMatches(ip, blocked));
}
```

### Step 2: Use Proxy for External Requests

```javascript
const { createProxyMiddleware } = require('http-proxy-middleware');

// Proxy that blocks internal IPs
app.use('/api/fetch', async (req, res) => {
  const userUrl = req.body.url;
  
  try {
    const validated = await validateUrl(userUrl);
    
    // Use proxy that blocks internal IPs
    const response = await fetch(validated.href, {
      // Use proxy
      agent: new HttpsProxyAgent('http://proxy:8080'),
      // Disable redirects
      redirect: 'manual'
    });
    
    const data = await response.text();
    res.json({ data });
  } catch (err) {
    res.status(400).json({ error: 'Invalid URL' });
  }
});
```

## 📝 Code Examples

### ❌ Vulnerable

```javascript
// ❌ VULNERABLE: Direct fetch
app.post('/api/fetch', async (req, res) => {
  const response = await fetch(req.body.url); // ❌ No validation
  const data = await response.text();
  res.json({ data });
});
```

### ✅ Secure

```javascript
// ✅ SECURE: Validated URL
app.post('/api/fetch', async (req, res) => {
  try {
    const validated = await validateUrl(req.body.url);
    const response = await fetch(validated.href);
    const data = await response.text();
    res.json({ data });
  } catch (err) {
    res.status(400).json({ error: 'Invalid URL' });
  }
});
```

## 🧪 Testing Checklist

- [ ] URLs validated against whitelist
- [ ] Internal IPs blocked
- [ ] Localhost blocked
- [ ] AWS metadata IP blocked
- [ ] Redirects disabled
- [ ] Proxy used for external requests

## 📚 References

- [OWASP: Server Side Request Forgery](https://owasp.org/www-community/attacks/Server_Side_Request_Forgery)
- [CWE-918: SSRF](https://cwe.mitre.org/data/definitions/918.html)

## 🔗 Related Vulnerabilities

- [10. Client-Side Input Validation Only](./10_client_side_validation_only.md)
- [23. Unsanitized LLM Integration](./23_unsanitized_llm_integration.md)

---

**Classification**:
- **Confirmed** if URLs fetched without validation
- **Likely** if validation incomplete
- **Not Applicable** if URLs validated and internal IPs blocked
