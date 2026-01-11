# 28. Homebrewed Cryptography

## 🔴 Risk Level: **CRITICAL**

## 📋 Vulnerability Description

When asked to "encrypt" data without a specific library, AI often generates custom XOR functions, simple substitution ciphers, or uses obsolete algorithms like MD5/DES. These "roll-your-own" crypto implementations provide a false sense of security and are trivially breakable by modern cracking tools.

**Impact:**
- Easily breakable encryption
- False sense of security
- Data compromise
- Regulatory violations

## 🎯 Context: Why This Happens

AI code generators:
- Create "simple" encryption
- Don't understand crypto complexity
- Use weak algorithms
- Don't use proven libraries

## 🔍 Detection Methods

### 1. Code Analysis

**Search for:**
```javascript
// ❌ VULNERABLE patterns
function encrypt(text) {
  return text.split('').map(c => String.fromCharCode(c.charCodeAt(0) ^ 5)).join('');
}
crypto.createHash('md5')
crypto.createHash('sha1')
```

### 2. Review Encryption Usage

**Check:**
- Custom encryption functions
- Weak hash algorithms
- XOR "encryption"
- Base64 as "encryption"

## ✅ Verification Requirements

### Must Have:
1. **Proven Libraries**
   - libsodium, bcrypt, crypto (Node.js)
   - Modern algorithms (AES-GCM, Argon2)
   - No custom crypto

2. **Proper Algorithms**
   - AES-256-GCM for encryption
   - Argon2/bcrypt for hashing
   - RSA/ECDSA for signatures

## 🚨 Exploit Path

### Scenario 1: XOR "Encryption"
```
1. Developer uses XOR for "encryption"
2. Attacker intercepts encrypted data
3. XOR is easily reversible
4. Attacker decrypts immediately
5. Data exposed
```

## 🔧 Remediation Steps

### Step 1: Use Proven Libraries

**Node.js:**
```javascript
const crypto = require('crypto');

// ✅ SECURE: AES-256-GCM
function encrypt(text, key) {
  const iv = crypto.randomBytes(16);
  const cipher = crypto.createCipheriv('aes-256-gcm', key, iv);
  
  let encrypted = cipher.update(text, 'utf8', 'hex');
  encrypted += cipher.final('hex');
  
  const authTag = cipher.getAuthTag();
  
  return {
    iv: iv.toString('hex'),
    encrypted: encrypted,
    authTag: authTag.toString('hex')
  };
}

function decrypt(encryptedData, key) {
  const decipher = crypto.createDecipheriv(
    'aes-256-gcm',
    key,
    Buffer.from(encryptedData.iv, 'hex')
  );
  
  decipher.setAuthTag(Buffer.from(encryptedData.authTag, 'hex'));
  
  let decrypted = decipher.update(encryptedData.encrypted, 'hex', 'utf8');
  decrypted += decipher.final('utf8');
  
  return decrypted;
}
```

### Step 2: Use libsodium (Recommended)

```bash
npm install sodium-native
```

```javascript
const sodium = require('sodium-native');

function encrypt(text, key) {
  const nonce = Buffer.allocUnsafe(sodium.crypto_secretbox_NONCEBYTES);
  sodium.randombytes_buf(nonce);
  
  const ciphertext = Buffer.allocUnsafe(text.length + sodium.crypto_secretbox_MACBYTES);
  sodium.crypto_secretbox_easy(ciphertext, Buffer.from(text), nonce, key);
  
  return {
    nonce: nonce.toString('hex'),
    ciphertext: ciphertext.toString('hex')
  };
}
```

## 📝 Code Examples

### ❌ Vulnerable

```javascript
// ❌ VULNERABLE: XOR "encryption"
function encrypt(text) {
  return text.split('').map(c => 
    String.fromCharCode(c.charCodeAt(0) ^ 5)
  ).join('');
}

// ❌ VULNERABLE: MD5 (not encryption, and broken)
const hash = crypto.createHash('md5').update(password).digest('hex');
```

### ✅ Secure

```javascript
// ✅ SECURE: AES-256-GCM
const crypto = require('crypto');

function encrypt(text, key) {
  const iv = crypto.randomBytes(16);
  const cipher = crypto.createCipheriv('aes-256-gcm', key, iv);
  
  let encrypted = cipher.update(text, 'utf8', 'hex');
  encrypted += cipher.final('hex');
  
  return {
    iv: iv.toString('hex'),
    encrypted: encrypted,
    authTag: cipher.getAuthTag().toString('hex')
  };
}
```

## 🧪 Testing Checklist

- [ ] No custom encryption functions
- [ ] Proven libraries used
- [ ] Modern algorithms (AES-GCM, Argon2)
- [ ] No MD5/SHA1 for security
- [ ] Proper key management
- [ ] IV/nonce used correctly

## 📚 References

- [OWASP: Cryptographic Storage](https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html)
- [libsodium](https://libsodium.gitbook.io/doc/)
- [NIST Cryptographic Standards](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines)

## 🔗 Related Vulnerabilities

- [27. Plaintext Password Storage](./27_plaintext_passwords.md)
- [38. Unencrypted Sensitive Data at Rest](./38_unencrypted_data_at_rest.md)

---

**Classification**:
- **Confirmed** if custom crypto or weak algorithms used
- **Likely** if encryption implementation unclear
- **Not Applicable** if proven libraries with modern algorithms
