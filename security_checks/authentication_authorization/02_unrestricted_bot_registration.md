# 2. Unrestricted Bot Registration

## 🔴 Risk Level: **CRITICAL**

## 📋 Vulnerability Description

Registration and login forms lack rate limiting and bot detection mechanisms, allowing automated scripts to create thousands of fake accounts in minutes. This leads to:
- Database bloat with garbage data
- Email sending quota exhaustion
- Increased infrastructure costs
- Potential for spam/abuse campaigns

## 🎯 Context: Why This Happens

AI-generated registration forms focus on functionality, not abuse prevention:
- Simple form validation only
- No CAPTCHA or bot detection
- No rate limiting on registration endpoints
- No email verification delays

## 🔍 Detection Methods

### 1. Code Analysis

**Search for:**
- CAPTCHA implementation (reCAPTCHA, hCaptcha, Turnstile)
- Rate limiting on registration endpoints
- Email verification requirements
- Bot detection services (Cloudflare Bot Management, etc.)

**Red Flags:**
```javascript
// ❌ VULNERABLE: No bot protection
app.post('/api/register', async (req, res) => {
  const { email, password } = req.body;
  const user = await User.create({ email, password });
  res.json({ success: true });
});

// ✅ SECURE: Multiple layers of protection
app.post('/api/register', 
  rateLimiter,
  verifyCaptcha,
  validateEmail,
  async (req, res) => {
    // Registration logic
  }
);
```

### 2. Testing

**Automated Bot Test:**
```python
import requests
import time

def test_bot_registration(url, num_accounts=100):
    """Test if registration can be automated"""
    success_count = 0
    
    for i in range(num_accounts):
        email = f"bot{i}@example.com"
        password = "Password123!"
        
        response = requests.post(url, json={
            "email": email,
            "password": password
        })
        
        if response.status_code == 200:
            success_count += 1
        
        time.sleep(0.1)  # Small delay
    
    if success_count == num_accounts:
        return "VULNERABLE: No bot protection"
    return f"Protected: {success_count}/{num_accounts} succeeded"
```

## ✅ Verification Requirements

### Must Have:
1. **Rate Limiting**
   - Max 3 registrations per hour per IP
   - Max 1 registration per email address

2. **CAPTCHA or Bot Detection**
   - reCAPTCHA v3 (invisible) or v2 (challenge)
   - hCaptcha
   - Cloudflare Turnstile
   - Cloudflare Bot Management

3. **Email Verification**
   - Require email verification before account activation
   - Rate limit verification emails

4. **Progressive Delays**
   - Increasing delays between registration attempts
   - Temporary IP bans after repeated violations

## 🚨 Exploit Path

```
1. Attacker creates automated script
2. Script generates random emails
3. Script submits registration forms at high speed
4. Without protection, thousands of accounts created
5. Database filled with fake accounts
6. Email service quota exhausted
7. Infrastructure costs increase
8. Legitimate users may be affected
```

## 🔧 Remediation Steps

### Step 1: Implement Rate Limiting

```javascript
const rateLimit = require('express-rate-limit');

const registrationLimiter = rateLimit({
  windowMs: 60 * 60 * 1000, // 1 hour
  max: 3, // 3 registrations per hour
  message: 'Too many registration attempts. Please try again later.',
  skipSuccessfulRequests: false
});

app.post('/api/register', registrationLimiter, registerHandler);
```

### Step 2: Add CAPTCHA

**reCAPTCHA v3 (Recommended):**
```javascript
const { verifyRecaptcha } = require('./recaptcha');

app.post('/api/register', 
  registrationLimiter,
  async (req, res, next) => {
    const { recaptchaToken } = req.body;
    
    const score = await verifyRecaptcha(recaptchaToken, req.ip);
    
    if (score < 0.5) { // Threshold for suspicious
      return res.status(429).json({
        error: 'Bot detected. Please try again.',
        requiresVerification: true
      });
    }
    
    next();
  },
  registerHandler
);
```

**Client-side (React):**
```jsx
import { useGoogleReCaptcha } from 'react-google-recaptcha-v3';

function RegisterForm() {
  const { executeRecaptcha } = useGoogleReCaptcha();
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    const token = await executeRecaptcha('register');
    
    const response = await fetch('/api/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email,
        password,
        recaptchaToken: token
      })
    });
  };
}
```

### Step 3: Email Verification

```javascript
const crypto = require('crypto');
const { sendVerificationEmail } = require('./email');

app.post('/api/register', 
  registrationLimiter,
  verifyCaptcha,
  async (req, res) => {
    const { email, password } = req.body;
    
    // Check if email already exists
    const existing = await User.findOne({ email });
    if (existing) {
      return res.status(400).json({ error: 'Email already registered' });
    }
    
    // Generate verification token
    const verificationToken = crypto.randomBytes(32).toString('hex');
    const expiresAt = new Date(Date.now() + 24 * 60 * 60 * 1000); // 24 hours
    
    // Create unverified user
    const user = await User.create({
      email,
      password: await bcrypt.hash(password, 10),
      verified: false,
      verificationToken,
      verificationExpires: expiresAt
    });
    
    // Send verification email
    await sendVerificationEmail(email, verificationToken);
    
    res.json({
      message: 'Registration successful. Please check your email to verify your account.'
    });
  }
);

// Verification endpoint
app.get('/api/verify/:token', async (req, res) => {
  const { token } = req.params;
  
  const user = await User.findOne({
    verificationToken: token,
    verificationExpires: { $gt: new Date() }
  });
  
  if (!user) {
    return res.status(400).json({ error: 'Invalid or expired token' });
  }
  
  user.verified = true;
  user.verificationToken = undefined;
  user.verificationExpires = undefined;
  await user.save();
  
  res.json({ message: 'Email verified successfully' });
});
```

### Step 4: Implement Honeypot Fields

```jsx
// Client-side: Hidden field that bots will fill
<input
  type="text"
  name="website"
  style={{ display: 'none' }}
  tabIndex="-1"
  autoComplete="off"
/>

// Server-side: Reject if filled
if (req.body.website) {
  return res.status(400).json({ error: 'Bot detected' });
}
```

### Step 5: Monitor and Detect Patterns

```javascript
const registrationLimiter = rateLimit({
  windowMs: 60 * 60 * 1000,
  max: 3,
  onLimitReached: async (req, res) => {
    // Log suspicious activity
    await SecurityLog.create({
      type: 'registration_abuse',
      ip: req.ip,
      email: req.body.email,
      userAgent: req.get('user-agent'),
      timestamp: new Date()
    });
    
    // Check for bot patterns
    const recentAttempts = await SecurityLog.countDocuments({
      ip: req.ip,
      type: 'registration_abuse',
      timestamp: { $gt: new Date(Date.now() - 3600000) }
    });
    
    if (recentAttempts > 10) {
      // Ban IP for 24 hours
      await IPBan.create({
        ip: req.ip,
        reason: 'excessive_registration_attempts',
        expiresAt: new Date(Date.now() + 24 * 60 * 60 * 1000)
      });
    }
  }
});
```

## 📝 Code Examples

### ❌ Vulnerable Code

```javascript
app.post('/api/register', async (req, res) => {
  const { email, password } = req.body;
  
  // No rate limiting
  // No CAPTCHA
  // No email verification
  
  const user = await User.create({
    email,
    password: await bcrypt.hash(password, 10)
  });
  
  res.json({ success: true, userId: user.id });
});
```

### ✅ Secure Code

```javascript
const rateLimit = require('express-rate-limit');
const { verifyRecaptcha } = require('./recaptcha');
const { sendVerificationEmail } = require('./email');
const crypto = require('crypto');

// Rate limiter
const registrationLimiter = rateLimit({
  windowMs: 60 * 60 * 1000, // 1 hour
  max: 3,
  message: 'Too many registration attempts. Please try again later.',
  standardHeaders: true
});

// Honeypot check middleware
const checkHoneypot = (req, res, next) => {
  if (req.body.website) {
    // Bot filled honeypot field
    return res.status(400).json({ error: 'Invalid request' });
  }
  next();
};

// CAPTCHA verification middleware
const verifyCaptcha = async (req, res, next) => {
  const { recaptchaToken } = req.body;
  
  if (!recaptchaToken) {
    return res.status(400).json({ error: 'CAPTCHA verification required' });
  }
  
  const score = await verifyRecaptcha(recaptchaToken, req.ip);
  
  if (score < 0.5) {
    return res.status(429).json({
      error: 'Bot detected. Please try again.',
      requiresVerification: true
    });
  }
  
  next();
};

// Registration handler
app.post('/api/register',
  registrationLimiter,
  checkHoneypot,
  verifyCaptcha,
  async (req, res) => {
    const { email, password } = req.body;
    
    // Validate email format
    if (!isValidEmail(email)) {
      return res.status(400).json({ error: 'Invalid email format' });
    }
    
    // Check if email already exists
    const existing = await User.findOne({ email });
    if (existing) {
      return res.status(400).json({ error: 'Email already registered' });
    }
    
    // Generate verification token
    const verificationToken = crypto.randomBytes(32).toString('hex');
    const expiresAt = new Date(Date.now() + 24 * 60 * 60 * 1000);
    
    // Create unverified user
    const user = await User.create({
      email,
      password: await bcrypt.hash(password, 10),
      verified: false,
      verificationToken,
      verificationExpires: expiresAt
    });
    
    // Send verification email
    await sendVerificationEmail(email, verificationToken);
    
    res.json({
      message: 'Registration successful. Please check your email to verify your account.'
    });
  }
);
```

## 🧪 Testing Checklist

- [ ] Registration endpoint has rate limiting (max 3/hour)
- [ ] CAPTCHA verification required
- [ ] Honeypot fields implemented
- [ ] Email verification required before account activation
- [ ] Duplicate email registration prevented
- [ ] Bot patterns detected and logged
- [ ] IP bans applied after repeated violations
- [ ] Verification emails rate limited
- [ ] Suspicious activity alerts configured

## 📚 References

- [OWASP: Automated Threats](https://owasp.org/www-community/vulnerabilities/Automated_Threats)
- [Google reCAPTCHA](https://www.google.com/recaptcha/)
- [Cloudflare Turnstile](https://developers.cloudflare.com/turnstile/)
- [hCaptcha](https://www.hcaptcha.com/)

## 🔗 Related Vulnerabilities

- [01. Missing API Rate Limiting](./01_missing_rate_limiting.md)
- [27. Plaintext Password Storage](../data_protection/27_plaintext_passwords.md)
- [41. Missing Multi-Factor Authentication](./41_missing_mfa.md)

---

**Classification**: 
- **Confirmed** if registration endpoint has no rate limiting or CAPTCHA
- **Likely** if protection exists but is insufficient
- **Not Applicable** if registration is disabled or invitation-only
