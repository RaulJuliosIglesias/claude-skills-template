# 24. Prototype Pollution in Server Actions

## 🟠 Risk Level: **HIGH**

## 📋 Vulnerability Description

Modern frameworks like Next.js (v15/16) use Server Actions to bridge client and server. Attackers can send malicious JSON payloads containing properties like `constructor` or `__proto__` to pollute the application state, potentially leading to Remote Code Execution (RCE) if the server logic blindly merges inputs.

**Impact:**
- Application state pollution
- Remote Code Execution (potential)
- Unexpected behavior
- Security bypass

## 🎯 Context: Why This Happens

AI-generated code:
- Merges objects recursively
- Doesn't check for prototype properties
- Uses unsafe object operations
- Doesn't validate object structure

## 🔍 Detection Methods

### 1. Code Analysis

**Search for:**
```javascript
// ❌ VULNERABLE: Recursive merge
Object.assign(target, source)
{...target, ...source}
deepMerge(target, source)
```

### 2. Testing

```bash
# Test prototype pollution
curl -X POST https://api.example.com/update \
  -d '{"__proto__": {"isAdmin": true}}'
```

## ✅ Verification Requirements

### Must Have:
1. **Safe Object Operations**
   - Check for prototype properties
   - Use Object.hasOwnProperty
   - Avoid recursive merges on untrusted input

2. **Framework Updates**
   - Use latest framework versions
   - Apply security patches
   - Follow framework best practices

## 🚨 Exploit Path

### Scenario 1: State Pollution
```
1. Attacker sends: {"__proto__": {"isAdmin": true}}
2. Server merges object
3. Prototype polluted
4. All objects now have isAdmin
5. Privilege escalation
```

## 🔧 Remediation Steps

### Step 1: Safe Object Merging

```javascript
function safeMerge(target, source) {
  const result = { ...target };
  
  for (const key in source) {
    // ✅ Check for prototype properties
    if (!Object.prototype.hasOwnProperty.call(source, key)) {
      continue; // Skip prototype properties
    }
    
    // ✅ Check for dangerous keys
    if (key === '__proto__' || key === 'constructor') {
      continue; // Skip dangerous keys
    }
    
    result[key] = source[key];
  }
  
  return result;
}

// Usage
app.post('/api/update', async (req, res) => {
  const safeData = safeMerge({}, req.body);
  await Model.update(safeData);
});
```

### Step 2: Use Schema Validation

```javascript
const z = require('zod');

const updateSchema = z.object({
  name: z.string().optional(),
  email: z.string().email().optional()
}).strict(); // Reject unknown properties

app.post('/api/update', async (req, res) => {
  try {
    const validated = updateSchema.parse(req.body);
    // ✅ Only known properties, no prototype pollution
    await Model.update(validated);
  } catch (err) {
    res.status(400).json({ error: err.errors });
  }
});
```

### Step 3: Update Framework

```bash
# Update to latest versions
npm install next@latest react@latest
# Patches often include prototype pollution fixes
```

## 📝 Code Examples

### ❌ Vulnerable

```javascript
// ❌ VULNERABLE: Unsafe merge
app.post('/api/update', async (req, res) => {
  const data = Object.assign({}, req.body); // ❌ Prototype pollution
  await Model.update(data);
});
```

### ✅ Secure

```javascript
// ✅ SECURE: Safe merge
function safeMerge(target, source) {
  const result = { ...target };
  for (const key in source) {
    if (Object.prototype.hasOwnProperty.call(source, key) &&
        key !== '__proto__' && key !== 'constructor') {
      result[key] = source[key];
    }
  }
  return result;
}

app.post('/api/update', async (req, res) => {
  const data = safeMerge({}, req.body);
  await Model.update(data);
});
```

## 🧪 Testing Checklist

- [ ] Prototype properties rejected
- [ ] Safe object merging implemented
- [ ] Schema validation used
- [ ] Framework updated to latest
- [ ] hasOwnProperty checks in place
- [ ] Dangerous keys filtered

## 📚 References

- [OWASP: Prototype Pollution](https://owasp.org/www-community/vulnerabilities/Prototype_Pollution)
- [CVE-2021-3803](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-3803)

## 🔗 Related Vulnerabilities

- [40. Unprotected Attribute Injection](./40_unprotected_attribute_injection.md)
- [10. Client-Side Input Validation Only](./10_client_side_validation_only.md)

---

**Classification**:
- **Confirmed** if recursive merges on untrusted input
- **Likely** if object operations unsafe
- **Not Applicable** if safe merging and validation implemented
