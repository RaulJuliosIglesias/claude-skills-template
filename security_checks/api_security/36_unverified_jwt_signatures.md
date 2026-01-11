# 36. Unverified JWT Signatures

## 🔴 Risk Level: **CRITICAL**

## 📋 Vulnerability Description

When implementing "Login with Google" or OAuth flows, AI tools often generate code that simply decodes the JWT (`jwt.decode()`) to extract the email address without verifying the cryptographic signature. Attackers can trivially craft fake tokens with arbitrary emails to take over any account.

**Impact:**
- Account takeover
- Unauthorized access
- Identity spoofing
- Complete authentication bypass

## 🎯 Context: Why This Happens

AI code:
- Uses `jwt.decode()` instead of `jwt.verify()`
- Doesn't understand signature verification
- Focuses on extracting data
- Doesn't validate token authenticity

## 🔍 Detection Methods

### 1. Code Analysis

**Search for:**
```javascript
// ❌ VULNERABLE
jwt.decode(token)
JSON.parse(atob(token.split('.')[1]))

// ✅ SECURE
jwt.verify(token, secret)
```

### 2. Testing

```bash
# Create fake token
# If server accepts → VULNERABLE
```

## ✅ Verification Requirements

### Must Have:
1. **Signature Verification**
   - Always use jwt.verify()
   - Never use jwt.decode() alone
   - Verify with correct secret/key

2. **Token Validation**
   - Check expiration
   - Verify issuer (iss)
   - Verify audience (aud)
   - Check algorithm

## 🚨 Exploit Path

### Scenario 1: Fake Google Token
```
1. Attacker creates fake JWT with admin@example.com
2. Attacker sends token to server
3. Server decodes without verification
4. Server trusts email from token
5. Attacker gains admin access
6. Account compromised
```

## 🔧 Remediation Steps

### Step 1: Always Verify Signatures

```javascript
const jwt = require('jsonwebtoken');

// ❌ VULNERABLE: Decode only
const decoded = jwt.decode(token);
const email = decoded.email; // ❌ Not verified!

// ✅ SECURE: Verify signature
try {
  const decoded = jwt.verify(token, process.env.JWT_SECRET, {
    algorithms: ['HS256'] // Specify algorithm
  });
  const email = decoded.email; // ✅ Verified
} catch (err) {
  return res.status(401).json({ error: 'Invalid token' });
}
```

### Step 2: Verify OAuth Tokens

**Google OAuth:**
```javascript
const { OAuth2Client } = require('google-auth-library');

const client = new OAuth2Client(process.env.GOOGLE_CLIENT_ID);

async function verifyGoogleToken(token) {
  try {
    const ticket = await client.verifyIdToken({
      idToken: token,
      audience: process.env.GOOGLE_CLIENT_ID
    });
    
    const payload = ticket.getPayload();
    return payload;
  } catch (err) {
    throw new Error('Invalid Google token');
  }
}

app.post('/api/auth/google', async (req, res) => {
  const { token } = req.body;
  
  try {
    const payload = await verifyGoogleToken(token);
    // ✅ Token verified
    const user = await findOrCreateUser(payload.email);
    res.json({ user });
  } catch (err) {
    res.status(401).json({ error: 'Invalid token' });
  }
});
```

### Step 3: Validate Token Claims

```javascript
const jwt = require('jsonwebtoken');

function verifyToken(token) {
  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET, {
      algorithms: ['HS256'],
      issuer: 'your-app', // ✅ Verify issuer
      audience: 'your-app' // ✅ Verify audience
    });
    
    // Check expiration (automatically checked by verify)
    // Check other claims
    if (decoded.role && !['user', 'admin'].includes(decoded.role)) {
      throw new Error('Invalid role');
    }
    
    return decoded;
  } catch (err) {
    if (err.name === 'TokenExpiredError') {
      throw new Error('Token expired');
    }
    if (err.name === 'JsonWebTokenError') {
      throw new Error('Invalid token');
    }
    throw err;
  }
}
```

## 📝 Code Examples

### ❌ Vulnerable

```javascript
// ❌ VULNERABLE: Decode without verification
const jwt = require('jsonwebtoken');

app.post('/api/auth/google', async (req, res) => {
  const { token } = req.body;
  
  // ❌ Just decodes, doesn't verify
  const decoded = jwt.decode(token);
  const email = decoded.email;
  
  // Attacker can create fake token with any email!
  const user = await findOrCreateUser(email);
  res.json({ user });
});
```

### ✅ Secure

```javascript
// ✅ SECURE: Verify signature
const { OAuth2Client } = require('google-auth-library');

const client = new OAuth2Client(process.env.GOOGLE_CLIENT_ID);

app.post('/api/auth/google', async (req, res) => {
  const { token } = req.body;
  
  try {
    // ✅ Verify with Google's public keys
    const ticket = await client.verifyIdToken({
      idToken: token,
      audience: process.env.GOOGLE_CLIENT_ID
    });
    
    const payload = ticket.getPayload();
    
    // ✅ Additional validation
    if (!payload.email_verified) {
      return res.status(401).json({ error: 'Email not verified' });
    }
    
    const user = await findOrCreateUser(payload.email);
    res.json({ user });
  } catch (err) {
    res.status(401).json({ error: 'Invalid token' });
  }
});
```

## 🧪 Testing Checklist

- [ ] jwt.verify() used, not jwt.decode()
- [ ] Signatures verified
- [ ] Expiration checked
- [ ] Issuer verified
- [ ] Audience verified
- [ ] Algorithm specified
- [ ] OAuth tokens verified with provider

## 📚 References

- [OWASP: JWT Security](https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html)
- [JWT.io](https://jwt.io/)

## 🔗 Related Vulnerabilities

- [25. Insecure Session Storage](../data_protection/25_insecure_session_storage.md)
- [13. Missing CSRF Protection](./13_missing_csrf_protection.md)

---

**Classification**:
- **Confirmed** if jwt.decode() used without verify()
- **Likely** if verification incomplete
- **Not Applicable** if signatures properly verified
