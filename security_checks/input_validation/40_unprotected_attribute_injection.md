# 40. Unprotected Attribute Injection

## 🔴 Risk Level: **CRITICAL**

## 📋 Vulnerability Description

AI-generated update endpoints often dump the entire JSON body directly into a database update query. Attackers can include restricted fields like "is_admin": true, "role": "superuser", or "subscription_status": "pro" in the request payload to elevate privileges or bypass payment walls without proper authorization checks.

**Impact:**
- Privilege escalation
- Payment bypass
- Unauthorized access
- Data manipulation

## 🎯 Context: Why This Happens

AI code:
- Uses `req.body` directly
- Doesn't whitelist fields
- Trusts client input
- No field-level authorization

## 🔍 Detection Methods

### 1. Code Analysis

**Search for:**
```javascript
// ❌ VULNERABLE: Direct body usage
User.update(req.body, { where: { id: req.params.id } })
User.findByIdAndUpdate(id, req.body)
```

### 2. Testing

```bash
# Test privilege escalation
curl -X PUT https://api.example.com/users/123 \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"role": "admin", "is_admin": true}'

# If succeeds → VULNERABLE
```

## ✅ Verification Requirements

### Must Have:
1. **Field Whitelisting**
   - Only allow specific fields
   - Reject unexpected fields
   - Use DTOs or schemas

2. **Authorization Checks**
   - Verify user can modify field
   - Role-based field restrictions
   - Admin-only fields protected

## 🚨 Exploit Path

### Scenario 1: Privilege Escalation
```
1. Regular user authenticates
2. User updates profile: PUT /api/users/123
3. User includes: {"role": "admin", "is_admin": true}
4. Server updates all fields
5. User becomes admin
6. Privilege escalated
```

## 🔧 Remediation Steps

### Step 1: Whitelist Fields

```javascript
// ✅ SECURE: Whitelist allowed fields
const ALLOWED_UPDATE_FIELDS = ['name', 'email', 'avatar'];

function whitelistFields(data, allowed) {
  const filtered = {};
  for (const field of allowed) {
    if (data[field] !== undefined) {
      filtered[field] = data[field];
    }
  }
  return filtered;
}

app.put('/api/users/:id', requireAuth, async (req, res) => {
  // Only allow specific fields
  const allowedData = whitelistFields(req.body, ALLOWED_UPDATE_FIELDS);
  
  await User.update(allowedData, {
    where: { id: req.params.id, userId: req.user.id }
  });
  
  res.json({ success: true });
});
```

### Step 2: Use Zod/Joi Schemas

```javascript
const z = require('zod');

const userUpdateSchema = z.object({
  name: z.string().min(1).max(100).optional(),
  email: z.string().email().optional(),
  avatar: z.string().url().optional()
  // ❌ No role, is_admin, etc.
});

app.put('/api/users/:id', requireAuth, async (req, res) => {
  try {
    // Validate and strip unknown fields
    const validated = userUpdateSchema.parse(req.body);
    
    await User.update(validated, {
      where: { id: req.params.id, userId: req.user.id }
    });
    
    res.json({ success: true });
  } catch (err) {
    res.status(400).json({ error: err.errors });
  }
});
```

### Step 3: Separate Admin Endpoints

```javascript
// Regular user update
app.put('/api/users/:id', requireAuth, async (req, res) => {
  const allowedFields = ['name', 'email', 'avatar'];
  const data = whitelistFields(req.body, allowedFields);
  
  await User.update(data, {
    where: { id: req.params.id, userId: req.user.id }
  });
  
  res.json({ success: true });
});

// Admin update (separate endpoint)
app.put('/api/admin/users/:id',
  requireAuth,
  requireAdmin,
  async (req, res) => {
    // Admin can update role, etc.
    const allowedFields = ['name', 'email', 'role', 'is_admin'];
    const data = whitelistFields(req.body, allowedFields);
    
    await User.update(data, {
      where: { id: req.params.id }
    });
    
    res.json({ success: true });
  }
);
```

## 📝 Code Examples

### ❌ Vulnerable

```javascript
// ❌ VULNERABLE: Direct body update
app.put('/api/users/:id', requireAuth, async (req, res) => {
  await User.update(req.body, { // ❌ All fields accepted
    where: { id: req.params.id }
  });
  res.json({ success: true });
});
```

### ✅ Secure

```javascript
// ✅ SECURE: Whitelisted fields
app.put('/api/users/:id', requireAuth, async (req, res) => {
  const allowedFields = ['name', 'email', 'avatar'];
  const data = whitelistFields(req.body, allowedFields);
  
  await User.update(data, {
    where: { id: req.params.id, userId: req.user.id }
  });
  
  res.json({ success: true });
});
```

## 🧪 Testing Checklist

- [ ] Only whitelisted fields accepted
- [ ] Privilege fields rejected
- [ ] Unexpected fields stripped
- [ ] Schema validation used
- [ ] Admin fields in separate endpoint
- [ ] Field-level authorization checked

## 📚 References

- [OWASP: Mass Assignment](https://cheatsheetseries.owasp.org/cheatsheets/Mass_Assignment_Cheat_Sheet.html)
- [Zod Documentation](https://zod.dev/)

## 🔗 Related Vulnerabilities

- [43. Broken Object Level Authorization](../authentication_authorization/43_broken_object_authorization.md)
- [10. Client-Side Input Validation Only](./10_client_side_validation_only.md)

---

**Classification**:
- **Confirmed** if req.body used directly in updates
- **Likely** if field whitelisting incomplete
- **Not Applicable** if fields whitelisted and validated
