# 41. Missing Multi-Factor Authentication (MFA)

## 🟠 Risk Level: **HIGH**

## 📋 Vulnerability Description

AI-generated authentication flows usually implement only basic Email/Password logins. This leaves high-value accounts (like Admins) vulnerable to credential stuffing or phishing attacks, as there is no second layer of verification to stop an attacker who has stolen a password.

**Impact:**
- Account compromise
- Privilege escalation
- Data breach
- Service disruption

## 🎯 Context: Why This Happens

AI code:
- Implements basic auth only
- Doesn't add MFA
- Focuses on core functionality
- Doesn't consider security layers

## 🔍 Detection Methods

### 1. Code Analysis

**Search for:**
- MFA/TOTP implementation
- 2FA setup
- MFA verification

### 2. Testing

**Check if MFA available:**
- Login flow
- Account settings
- Admin accounts

## ✅ Verification Requirements

### Must Have:
1. **MFA Implementation**
   - TOTP (Google Authenticator)
   - SMS (less secure)
   - WebAuthn (most secure)
   - At minimum for admin accounts

2. **MFA Enforcement**
   - Required for sensitive operations
   - Required for admin accounts
   - Optional but recommended for all users

## 🚨 Exploit Path

### Scenario 1: Credential Stuffing
```
1. Attacker obtains leaked password
2. Attacker tries password on site
3. No MFA required
4. Login succeeds
5. Account compromised
```

## 🔧 Remediation Steps

### Step 1: Implement TOTP

```bash
npm install speakeasy qrcode
```

```javascript
const speakeasy = require('speakeasy');
const QRCode = require('qrcode');

// Generate secret
app.post('/api/mfa/setup', requireAuth, async (req, res) => {
  const secret = speakeasy.generateSecret({
    name: `YourApp (${req.user.email})`,
    issuer: 'YourApp'
  });
  
  // Store secret (encrypted)
  await User.update({
    mfaSecret: encrypt(secret.base32),
    mfaEnabled: false
  }, { where: { id: req.user.id } });
  
  // Generate QR code
  const qrCode = await QRCode.toDataURL(secret.otpauth_url);
  
  res.json({
    secret: secret.base32,
    qrCode: qrCode
  });
});

// Verify and enable
app.post('/api/mfa/verify', requireAuth, async (req, res) => {
  const { token } = req.body;
  const user = await User.findByPk(req.user.id);
  
  const verified = speakeasy.totp.verify({
    secret: decrypt(user.mfaSecret),
    encoding: 'base32',
    token: token,
    window: 2 // Allow 2 time steps
  });
  
  if (verified) {
    await user.update({ mfaEnabled: true });
    res.json({ success: true });
  } else {
    res.status(400).json({ error: 'Invalid token' });
  }
});

// Require MFA on login
app.post('/api/login', async (req, res) => {
  const { email, password, mfaToken } = req.body;
  
  const user = await authenticate(email, password);
  
  if (user.mfaEnabled) {
    if (!mfaToken) {
      return res.status(401).json({ requiresMFA: true });
    }
    
    const verified = speakeasy.totp.verify({
      secret: decrypt(user.mfaSecret),
      encoding: 'base32',
      token: mfaToken
    });
    
    if (!verified) {
      return res.status(401).json({ error: 'Invalid MFA token' });
    }
  }
  
  const jwt = generateToken(user);
  res.json({ token: jwt });
});
```

### Step 2: Use Managed Auth (Recommended)

**Supabase Auth:**
```javascript
// Enable MFA in Supabase dashboard
// Automatically handled by Supabase
```

**Auth0:**
```javascript
// Enable MFA in Auth0 dashboard
// No custom code needed
```

## 📝 Code Examples

### ❌ Vulnerable

```javascript
// ❌ VULNERABLE: No MFA
app.post('/api/login', async (req, res) => {
  const { email, password } = req.body;
  const user = await authenticate(email, password);
  const token = generateToken(user);
  res.json({ token }); // ❌ No MFA check
});
```

### ✅ Secure

```javascript
// ✅ SECURE: MFA required
app.post('/api/login', async (req, res) => {
  const { email, password, mfaToken } = req.body;
  const user = await authenticate(email, password);
  
  if (user.mfaEnabled) {
    if (!mfaToken) {
      return res.status(401).json({ requiresMFA: true });
    }
    
    if (!verifyMFA(user, mfaToken)) {
      return res.status(401).json({ error: 'Invalid MFA token' });
    }
  }
  
  const token = generateToken(user);
  res.json({ token });
});
```

## 🧪 Testing Checklist

- [ ] MFA setup available
- [ ] TOTP implementation
- [ ] MFA required for admin
- [ ] MFA verification works
- [ ] Backup codes provided
- [ ] MFA can be disabled (with verification)

## 📚 References

- [OWASP: Multi-Factor Authentication](https://cheatsheetseries.owasp.org/cheatsheets/Multifactor_Authentication_Cheat_Sheet.html)
- [TOTP RFC 6238](https://tools.ietf.org/html/rfc6238)

## 🔗 Related Vulnerabilities

- [01. Missing API Rate Limiting](../authentication_authorization/01_missing_rate_limiting.md)
- [27. Plaintext Password Storage](../data_protection/27_plaintext_passwords.md)

---

**Classification**:
- **Confirmed** if no MFA implementation
- **Likely** if MFA optional for admin
- **Not Applicable** if MFA required for sensitive accounts
