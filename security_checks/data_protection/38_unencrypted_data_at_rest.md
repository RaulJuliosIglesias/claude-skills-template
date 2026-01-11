# 38. Unencrypted Sensitive Data at Rest

## 🟠 Risk Level: **HIGH**

## 📋 Vulnerability Description

While developers often encrypt passwords, AI-generated schemas frequently store other Personally Identifiable Information (PII)—like phone numbers, home addresses, or government IDs—as plain text in the database. If a database dump is stolen, this data is immediately readable.

**Impact:**
- PII exposure
- Privacy violations
- Regulatory non-compliance (GDPR, CCPA)
- Identity theft risk

## 🎯 Context: Why This Happens

AI code:
- Encrypts passwords only
- Doesn't encrypt other PII
- Stores sensitive data as-is
- Doesn't consider data classification

## 🔍 Detection Methods

### 1. Database Schema Review

**Check for:**
- Phone numbers (plain text)
- Addresses (plain text)
- Government IDs (plain text)
- Credit card numbers (plain text)
- Social security numbers (plain text)

### 2. Data Classification

**Identify sensitive fields:**
- PII (personally identifiable information)
- PHI (protected health information)
- Financial data
- Authentication data

## ✅ Verification Requirements

### Must Have:
1. **PII Encryption**
   - Encrypt sensitive columns
   - Use application-level encryption
   - Or TDE (Transparent Data Encryption)

2. **Access Control**
   - RLS policies
   - Column-level permissions
   - Audit logging

## 🚨 Exploit Path

### Scenario 1: Database Breach
```
1. Attacker gains database access
2. Exports entire database
3. Finds plain text PII
4. SSNs, addresses, phone numbers exposed
5. Identity theft possible
6. Regulatory violations
```

## 🔧 Remediation Steps

### Step 1: Identify Sensitive Data

```javascript
// Classify data sensitivity
const SENSITIVE_FIELDS = [
  'ssn',
  'phone',
  'address',
  'credit_card',
  'government_id'
];
```

### Step 2: Encrypt Sensitive Columns

```javascript
const crypto = require('crypto');

const ENCRYPTION_KEY = crypto.scryptSync(
  process.env.ENCRYPTION_PASSWORD,
  'salt',
  32
);

function encryptSensitive(text) {
  const iv = crypto.randomBytes(16);
  const cipher = crypto.createCipheriv('aes-256-gcm', ENCRYPTION_KEY, iv);
  
  let encrypted = cipher.update(text, 'utf8', 'hex');
  encrypted += cipher.final('hex');
  
  return {
    iv: iv.toString('hex'),
    encrypted: encrypted,
    authTag: cipher.getAuthTag().toString('hex')
  };
}

function decryptSensitive(encryptedData) {
  const decipher = crypto.createDecipheriv(
    'aes-256-gcm',
    ENCRYPTION_KEY,
    Buffer.from(encryptedData.iv, 'hex')
  );
  
  decipher.setAuthTag(Buffer.from(encryptedData.authTag, 'hex'));
  
  let decrypted = decipher.update(encryptedData.encrypted, 'hex', 'utf8');
  decrypted += decipher.final('utf8');
  
  return decrypted;
}

// Usage
app.post('/api/users', async (req, res) => {
  const user = await User.create({
    email: req.body.email,
    phone: encryptSensitive(req.body.phone), // ✅ Encrypted
    ssn: encryptSensitive(req.body.ssn) // ✅ Encrypted
  });
  
  res.json(user);
});
```

### Step 3: Use Database Encryption

**PostgreSQL with pgcrypto:**
```sql
-- Enable extension
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Encrypt on insert
INSERT INTO users (email, phone, ssn) VALUES (
  'user@example.com',
  pgp_sym_encrypt('555-1234', 'encryption_key'),
  pgp_sym_encrypt('123-45-6789', 'encryption_key')
);

-- Decrypt on select
SELECT 
  email,
  pgp_sym_decrypt(phone, 'encryption_key') as phone,
  pgp_sym_decrypt(ssn, 'encryption_key') as ssn
FROM users;
```

### Step 4: Implement TDE (If Available)

**AWS RDS:**
- Enable encryption at rest
- Use KMS for key management
- Automatic encryption/decryption

## 📝 Code Examples

### ❌ Vulnerable

```javascript
// ❌ VULNERABLE: Plain text PII
await User.create({
  email: req.body.email,
  phone: req.body.phone, // ❌ Plain text
  ssn: req.body.ssn, // ❌ Plain text
  address: req.body.address // ❌ Plain text
});
```

### ✅ Secure

```javascript
// ✅ SECURE: Encrypted PII
await User.create({
  email: req.body.email,
  phone: encryptSensitive(req.body.phone), // ✅ Encrypted
  ssn: encryptSensitive(req.body.ssn), // ✅ Encrypted
  address: encryptSensitive(req.body.address) // ✅ Encrypted
});
```

## 🧪 Testing Checklist

- [ ] Sensitive fields identified
- [ ] PII encrypted at rest
- [ ] Encryption keys managed securely
- [ ] Decryption only for authorized access
- [ ] TDE enabled (if available)
- [ ] Access controls in place

## 📚 References

- [OWASP: Cryptographic Storage](https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html)
- [GDPR: Data Protection](https://gdpr.eu/)
- [NIST: Data Encryption](https://csrc.nist.gov/publications/detail/sp/800-111/final)

## 🔗 Related Vulnerabilities

- [27. Plaintext Password Storage](./27_plaintext_passwords.md)
- [28. Homebrewed Cryptography](./28_homebrewed_cryptography.md)
- [07. Missing Row Level Security](../database_security/07_missing_row_level_security.md)

---

**Classification**:
- **Confirmed** if PII stored in plain text
- **Likely** if encryption status unclear
- **Not Applicable** if sensitive data properly encrypted
