# 34. Path Traversal (LFI)

## 🔴 Risk Level: **CRITICAL**

## 📋 Vulnerability Description

AI-generated file serving endpoints often trust user-supplied file names or paths without sanitization. Attackers can manipulate these inputs (e.g., using `../../`) to step out of the intended directory and read sensitive system files like `/etc/passwd` or `.env` files located elsewhere on the server.

**Impact:**
- Sensitive file reading
- Configuration file exposure
- Source code theft
- System file access

## 🎯 Context: Why This Happens

AI code:
- Uses user input directly in file paths
- Doesn't sanitize `../` sequences
- Doesn't validate file locations
- Trusts user-provided paths

## 🔍 Detection Methods

### 1. Code Analysis

**Search for:**
```javascript
// ❌ VULNERABLE patterns
fs.readFile(req.params.filename)
fs.readFileSync(req.body.path)
path.join(UPLOAD_DIR, req.query.file)
```

### 2. Testing

```bash
# Test path traversal
curl "https://api.example.com/files?path=../../etc/passwd"
curl "https://api.example.com/files/../../.env"
```

## ✅ Verification Requirements

### Must Have:
1. **Path Sanitization**
   - Remove `../` sequences
   - Use `path.basename()`
   - Validate against whitelist

2. **Directory Validation**
   - Ensure file in allowed directory
   - Check path doesn't escape

## 🚨 Exploit Path

### Scenario 1: .env File Access
```
1. Attacker finds file endpoint: /api/files/:filename
2. Attacker requests: /api/files/../../.env
3. Server uses path directly
4. Reads .env file
5. Secrets exposed
```

## 🔧 Remediation Steps

### Step 1: Sanitize Paths

```javascript
const path = require('path');

function sanitizePath(userInput, baseDir) {
  // Get basename (removes directory components)
  const basename = path.basename(userInput);
  
  // Remove dangerous characters
  const sanitized = basename.replace(/[^a-zA-Z0-9.-]/g, '');
  
  // Join with base directory
  const fullPath = path.join(baseDir, sanitized);
  
  // Verify it's still in base directory
  const resolved = path.resolve(fullPath);
  const baseResolved = path.resolve(baseDir);
  
  if (!resolved.startsWith(baseResolved)) {
    throw new Error('Invalid path');
  }
  
  return resolved;
}

app.get('/api/files/:filename', async (req, res) => {
  try {
    const safePath = sanitizePath(req.params.filename, UPLOAD_DIR);
    res.sendFile(safePath);
  } catch (err) {
    res.status(400).json({ error: 'Invalid filename' });
  }
});
```

### Step 2: Use Whitelist

```javascript
const allowedFiles = new Map([
  ['file1.pdf', 'actual-file-id-1'],
  ['file2.pdf', 'actual-file-id-2']
]);

app.get('/api/files/:filename', async (req, res) => {
  const fileId = allowedFiles.get(req.params.filename);
  if (!fileId) {
    return res.status(404).json({ error: 'File not found' });
  }
  
  const filePath = path.join(UPLOAD_DIR, fileId);
  res.sendFile(filePath);
});
```

## 📝 Code Examples

### ❌ Vulnerable

```javascript
// ❌ VULNERABLE: Direct path usage
app.get('/api/files/:filename', (req, res) => {
  const filePath = path.join(UPLOAD_DIR, req.params.filename);
  res.sendFile(filePath); // ❌ Path traversal possible
});
```

### ✅ Secure

```javascript
// ✅ SECURE: Sanitized path
app.get('/api/files/:filename', (req, res) => {
  const safePath = sanitizePath(req.params.filename, UPLOAD_DIR);
  res.sendFile(safePath);
});
```

## 🧪 Testing Checklist

- [ ] Path traversal attempts blocked
- [ ] Only basename used
- [ ] Path validated against base directory
- [ ] Whitelist used when possible
- [ ] No direct user input in file paths

## 📚 References

- [OWASP: Path Traversal](https://owasp.org/www-community/attacks/Path_Traversal)
- [CWE-22: Path Traversal](https://cwe.mitre.org/data/definitions/22.html)

## 🔗 Related Vulnerabilities

- [16. Unrestricted File Uploads](./16_unrestricted_file_uploads.md)
- [10. Client-Side Input Validation Only](./10_client_side_validation_only.md)

---

**Classification**:
- **Confirmed** if user input used directly in file paths
- **Likely** if path sanitization incomplete
- **Not Applicable** if paths properly sanitized and validated
