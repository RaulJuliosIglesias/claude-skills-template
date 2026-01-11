# 27. Plaintext Password Storage

## 🔴 Risk Level: **CRITICAL**

## 📋 Vulnerability Description

AI-generated authentication logic often inserts passwords directly into the database as plain text (`INSERT INTO users...`) or uses weak encoding like Base64. If the database is compromised, every user account is immediately accessible to attackers without the need for cracking.

**Impact:**
- Immediate account compromise if database leaked
- No protection against database breaches
- Violation of security best practices
- Regulatory compliance issues (GDPR, etc.)

## 🎯 Context: Why This Happens

AI code generators:
- Use simple examples with plain text
- Don't include password hashing by default
- May use Base64 (not encryption, just encoding)
- Focus on functionality over security

## 🔍 Detection Methods

### 1. Code Analysis

**Search for:**
```bash
# Plain text passwords
grep -r "password.*=.*['\"].*['\"]" .
grep -r "INSERT INTO.*password" .
grep -r "password.*req.body" .

# Check for hashing
grep -r "bcrypt\|argon2\|scrypt\|pbkdf2" .
```

**Red Flags:**
```javascript
// ❌ VULNERABLE: Plain text
await User.create({
  email: req.body.email,
  password: req.body.password // ❌ Plain text!
});

// ✅ SECURE: Hashed
const bcrypt = require('bcrypt');
await User.create({
  email: req.body.email,
  password: await bcrypt.hash(req.body.password, 10) // ✅ Hashed
});
```

### 2. Database Review

**Check database:**
```sql
-- Check if passwords look hashed
SELECT email, password FROM users LIMIT 5;

-- Hashed passwords should look like:
-- $2b$10$... (bcrypt)
-- $argon2id$v=19$m=65536,t=3,p=4$... (argon2)
-- NOT like: "password123" or "YWRtaW4=" (Base64)
```

## ✅ Verification Requirements

### Must Have:
1. **Password Hashing**
   - Use bcrypt, Argon2, or scrypt
   - Salt included automatically
   - Cost factor appropriate (10+ for bcrypt)

2. **No Plain Text Storage**
   - Never store passwords as-is
   - Never use Base64 (it's encoding, not encryption)
   - Never use MD5, SHA1 (too fast, vulnerable)

3. **Password Verification**
   - Use library's compare function
   - Never compare plain text
   - Timing attack protection

## 🚨 Exploit Path

### Scenario 1: Database Breach
```
1. Attacker gains database access
2. Attacker queries users table
3. Finds passwords stored in plain text
4. Attacker can login as any user
5. Complete account compromise
6. Data breach
```

### Scenario 2: Base64 "Encryption"
```
1. Developer uses Base64 encoding (not encryption)
2. Attacker gains database access
3. Attacker decodes Base64: echo "YWRtaW4=" | base64 -d
4. Gets plain text password
5. Account compromised
```

## 🔧 Remediation Steps

### Step 1: Install Hashing Library

```bash
# Node.js - bcrypt (recommended)
npm install bcrypt

# Or Argon2 (more secure, newer)
npm install argon2

# Python
pip install bcrypt
# or
pip install argon2-cffi
```

### Step 2: Hash Passwords on Registration

**bcrypt (Node.js):**
```javascript
const bcrypt = require('bcrypt');

app.post('/api/register', async (req, res) => {
  const { email, password } = req.body;
  
  // Hash password with cost factor 10
  const hashedPassword = await bcrypt.hash(password, 10);
  
  const user = await User.create({
    email,
    password: hashedPassword // ✅ Store hash, not plain text
  });
  
  res.json({ success: true });
});
```

**Argon2 (More Secure):**
```javascript
const argon2 = require('argon2');

app.post('/api/register', async (req, res) => {
  const { email, password } = req.body;
  
  // Argon2 with recommended parameters
  const hashedPassword = await argon2.hash(password, {
    type: argon2.argon2id,
    memoryCost: 65536, // 64 MB
    timeCost: 3,
    parallelism: 4
  });
  
  const user = await User.create({
    email,
    password: hashedPassword
  });
  
  res.json({ success: true });
});
```

### Step 3: Verify Passwords on Login

**bcrypt:**
```javascript
const bcrypt = require('bcrypt');

app.post('/api/login', async (req, res) => {
  const { email, password } = req.body;
  
  const user = await User.findOne({ email });
  if (!user) {
    return res.status(401).json({ error: 'Invalid credentials' });
  }
  
  // Compare password with hash
  const isValid = await bcrypt.compare(password, user.password);
  
  if (!isValid) {
    return res.status(401).json({ error: 'Invalid credentials' });
  }
  
  // Generate token
  const token = generateToken(user);
  res.json({ token });
});
```

**Argon2:**
```javascript
const argon2 = require('argon2');

app.post('/api/login', async (req, res) => {
  const { email, password } = req.body;
  
  const user = await User.findOne({ email });
  if (!user) {
    return res.status(401).json({ error: 'Invalid credentials' });
  }
  
  // Verify password
  const isValid = await argon2.verify(user.password, password);
  
  if (!isValid) {
    return res.status(401).json({ error: 'Invalid credentials' });
  }
  
  const token = generateToken(user);
  res.json({ token });
});
```

### Step 4: Migrate Existing Plain Text Passwords

**One-time migration script:**
```javascript
const bcrypt = require('bcrypt');
const { User } = require('./models');

async function migratePasswords() {
  const users = await User.findAll({
    where: {
      // Find users with plain text passwords
      // (passwords that don't start with $2b$ for bcrypt)
      password: {
        [Op.notLike]: '$2b$%'
      }
    }
  });
  
  for (const user of users) {
    // Check if it's Base64
    let plainPassword = user.password;
    try {
      plainPassword = Buffer.from(user.password, 'base64').toString();
    } catch (e) {
      // Not Base64, assume plain text
    }
    
    // Hash the password
    const hashedPassword = await bcrypt.hash(plainPassword, 10);
    
    // Update user
    await user.update({ password: hashedPassword });
    
    // Force password reset on next login
    await user.update({ mustChangePassword: true });
    
    console.log(`Migrated password for ${user.email}`);
  }
}

migratePasswords();
```

### Step 5: Use Managed Auth (Recommended)

**Supabase Auth:**
```javascript
// Supabase handles password hashing automatically
const { data, error } = await supabase.auth.signUp({
  email: 'user@example.com',
  password: 'securepassword'
});
```

**Auth0:**
```javascript
// Auth0 handles everything
const auth0 = require('auth0');

const management = new auth0.ManagementClient({
  domain: process.env.AUTH0_DOMAIN,
  clientId: process.env.AUTH0_CLIENT_ID,
  clientSecret: process.env.AUTH0_CLIENT_SECRET
});
```

## 📝 Code Examples

### ❌ Vulnerable Code

```javascript
// ❌ VULNERABLE: Plain text
app.post('/api/register', async (req, res) => {
  const user = await User.create({
    email: req.body.email,
    password: req.body.password // ❌ Plain text!
  });
  res.json(user);
});

// ❌ VULNERABLE: Base64 (not encryption!)
app.post('/api/register', async (req, res) => {
  const encoded = Buffer.from(req.body.password).toString('base64');
  const user = await User.create({
    email: req.body.email,
    password: encoded // ❌ Base64 is NOT encryption!
  });
  res.json(user);
});

// ❌ VULNERABLE: Weak hashing (MD5, SHA1)
const crypto = require('crypto');
app.post('/api/register', async (req, res) => {
  const hash = crypto.createHash('md5').update(req.body.password).digest('hex');
  const user = await User.create({
    email: req.body.email,
    password: hash // ❌ MD5 is too fast, vulnerable to rainbow tables
  });
  res.json(user);
});
```

### ✅ Secure Code

```javascript
// ✅ SECURE: bcrypt
const bcrypt = require('bcrypt');

app.post('/api/register', async (req, res) => {
  const { email, password } = req.body;
  
  // Hash with cost factor 10
  const hashedPassword = await bcrypt.hash(password, 10);
  
  const user = await User.create({
    email,
    password: hashedPassword // ✅ Properly hashed
  });
  
  res.json({ success: true });
});

app.post('/api/login', async (req, res) => {
  const { email, password } = req.body;
  
  const user = await User.findOne({ email });
  if (!user) {
    return res.status(401).json({ error: 'Invalid credentials' });
  }
  
  // Compare using bcrypt (timing-safe)
  const isValid = await bcrypt.compare(password, user.password);
  
  if (!isValid) {
    return res.status(401).json({ error: 'Invalid credentials' });
  }
  
  const token = generateToken(user);
  res.json({ token });
});
```

## 🧪 Testing Checklist

- [ ] Passwords hashed with bcrypt/Argon2
- [ ] No plain text passwords in database
- [ ] No Base64 encoding used
- [ ] Cost factor appropriate (10+ for bcrypt)
- [ ] Password verification uses compare function
- [ ] Migration script for existing plain text passwords
- [ ] Password reset requires new hash
- [ ] No password logging
- [ ] Password strength requirements enforced

## 📚 References

- [OWASP: Password Storage](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
- [NIST Password Guidelines](https://pages.nist.gov/800-63-3/sp800-63b.html)
- [bcrypt Documentation](https://github.com/kelektiv/node.bcrypt.js)
- [Argon2](https://github.com/ranisalt/node-argon2)

## 🔗 Related Vulnerabilities

- [03. Exposed API Keys in Repos](./03_exposed_api_keys.md)
- [28. Homebrewed Cryptography](./28_homebrewed_cryptography.md)
- [42. Sensitive Data Exposure in Logs](./42_sensitive_data_in_logs.md)

---

**Classification**:
- **Confirmed** if passwords stored in plain text or Base64
- **Likely** if using weak hashing (MD5, SHA1)
- **Not Applicable** if using bcrypt/Argon2 with proper configuration
