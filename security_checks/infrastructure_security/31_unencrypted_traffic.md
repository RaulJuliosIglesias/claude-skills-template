# 31. Unencrypted Traffic (HTTP)

## 🟠 Risk Level: **HIGH**

## 📋 Vulnerability Description

Applications failing to enforce encrypted connections allow traffic to pass over plain HTTP. This enables attackers on the same network to intercept sensitive data packets, including session cookies, passwords, and API keys, in clear text.

**Impact:**
- Man-in-the-middle attacks
- Credential theft
- Session hijacking
- Data interception

## 🎯 Context: Why This Happens

Common issues:
- HTTP still allowed
- No HTTPS redirect
- Missing TLS certificates
- Development config in production

## 🔍 Detection Methods

### 1. Testing

```bash
# Test HTTP access
curl http://example.com

# If returns content → HTTP enabled
# Should redirect to HTTPS
```

### 2. Configuration Review

**Check:**
- HTTPS redirect configured
- TLS certificates valid
- HSTS headers set

## ✅ Verification Requirements

### Must Have:
1. **HTTPS Enforced**
   - All HTTP redirects to HTTPS
   - TLS certificates valid
   - HSTS headers configured

2. **No HTTP in Production**
   - HTTP completely disabled
   - Only HTTPS accessible

## 🚨 Exploit Path

### Scenario 1: Credential Theft
```
1. User connects to public WiFi
2. Attacker on same network
3. User accesses site via HTTP
4. Attacker intercepts traffic
5. Sees login credentials in plain text
6. Credentials stolen
```

## 🔧 Remediation Steps

### Step 1: Configure HTTPS Redirect

**Nginx:**
```nginx
server {
    listen 80;
    server_name example.com;
    
    # Redirect all HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name example.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    # ... rest of config
}
```

**Express:**
```javascript
// Force HTTPS
app.use((req, res, next) => {
  if (req.header('x-forwarded-proto') !== 'https' && process.env.NODE_ENV === 'production') {
    res.redirect(`https://${req.header('host')}${req.url}`);
  } else {
    next();
  }
});
```

### Step 2: Set HSTS Headers

```javascript
app.use((req, res, next) => {
  if (req.secure || req.header('x-forwarded-proto') === 'https') {
    res.setHeader('Strict-Transport-Security', 'max-age=31536000; includeSubDomains');
  }
  next();
});
```

### Step 3: Use Let's Encrypt

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d example.com
```

## 📝 Code Examples

### ❌ Vulnerable

```nginx
# ❌ VULNERABLE: HTTP allowed
server {
    listen 80;
    # No redirect to HTTPS
}
```

### ✅ Secure

```nginx
# ✅ SECURE: HTTPS enforced
server {
    listen 80;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
}
```

## 🧪 Testing Checklist

- [ ] HTTP redirects to HTTPS
- [ ] TLS certificates valid
- [ ] HSTS headers set
- [ ] No mixed content warnings
- [ ] Certificate auto-renewal configured

## 📚 References

- [OWASP: Transport Layer Protection](https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Protection_Cheat_Sheet.html)
- [Let's Encrypt](https://letsencrypt.org/)

## 🔗 Related Vulnerabilities

- [17. Missing HTTP Security Headers](../api_security/17_missing_security_headers.md)
- [25. Insecure Session Storage](../data_protection/25_insecure_session_storage.md)

---

**Classification**:
- **Confirmed** if HTTP accessible without redirect
- **Likely** if HTTPS not enforced
- **Not Applicable** if HTTPS enforced with HSTS
