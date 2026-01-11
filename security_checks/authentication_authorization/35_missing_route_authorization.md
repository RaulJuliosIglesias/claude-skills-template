# 35. Missing Route-Level Authorization

## 🔴 Risk Level: **CRITICAL**

## 📋 Vulnerability Description

While some apps check if a user is "logged in," AI often fails to check if the user has the *correct permissions* for a specific route. This allows a standard user to access administrative pages (e.g., `/admin/users`) simply by guessing the URL, even if the UI buttons are hidden.

**Impact:**
- Unauthorized admin access
- Privilege escalation
- Data access violations
- Functionality abuse

## 🎯 Context: Why This Happens

AI-generated code:
- Checks authentication only
- Doesn't check authorization
- Hides UI but not routes
- Assumes frontend protection is enough

## 🔍 Detection Methods

### 1. Code Analysis

**Search for:**
```javascript
// ❌ VULNERABLE: Only auth check
app.get('/admin/users', requireAuth, (req, res) => {
  // No role check!
});

// ✅ SECURE: Auth + authorization
app.get('/admin/users', requireAuth, requireAdmin, (req, res) => {
  // Role checked
});
```

### 2. Testing

```bash
# Test as regular user
curl -H "Authorization: Bearer $USER_TOKEN" \
  https://api.example.com/admin/users

# If returns data → VULNERABLE
# Should return 403 Forbidden
```

## ✅ Verification Requirements

### Must Have:
1. **Role-Based Access Control (RBAC)**
   - Check user role on protected routes
   - Verify permissions before access
   - Different roles, different access

2. **Route Protection**
   - Middleware for role checks
   - Consistent authorization
   - Fail closed (deny by default)

## 🚨 Exploit Path

### Scenario 1: Admin Route Access
```
1. Regular user logs in
2. User guesses admin URL: /admin/users
3. User accesses directly (UI hidden but route open)
4. Server returns admin data
5. Unauthorized access granted
```

## 🔧 Remediation Steps

### Step 1: Create Authorization Middleware

```javascript
// middleware/authorization.js
function requireRole(...allowedRoles) {
  return (req, res, next) => {
    if (!req.user) {
      return res.status(401).json({ error: 'Unauthorized' });
    }
    
    if (!allowedRoles.includes(req.user.role)) {
      return res.status(403).json({ error: 'Forbidden' });
    }
    
    next();
  };
}

function requireAdmin(req, res, next) {
  return requireRole('admin')(req, res, next);
}

function requireModerator(req, res, next) {
  return requireRole('admin', 'moderator')(req, res, next);
}
```

### Step 2: Apply to Routes

```javascript
// Admin routes
app.get('/admin/users',
  requireAuth,
  requireAdmin, // ✅ Authorization check
  async (req, res) => {
    const users = await User.findAll();
    res.json(users);
  }
);

app.delete('/admin/users/:id',
  requireAuth,
  requireAdmin,
  async (req, res) => {
    await User.destroy({ where: { id: req.params.id } });
    res.json({ success: true });
  }
);

// Moderator routes
app.get('/moderate/posts',
  requireAuth,
  requireModerator,
  async (req, res) => {
    const posts = await Post.findAll({ where: { status: 'pending' } });
    res.json(posts);
  }
);
```

### Step 3: Permission-Based Access

```javascript
// More granular permissions
function requirePermission(permission) {
  return (req, res, next) => {
    if (!req.user) {
      return res.status(401).json({ error: 'Unauthorized' });
    }
    
    if (!req.user.permissions.includes(permission)) {
      return res.status(403).json({ error: 'Forbidden' });
    }
    
    next();
  };
}

app.delete('/users/:id',
  requireAuth,
  requirePermission('users.delete'),
  async (req, res) => {
    await User.destroy({ where: { id: req.params.id } });
    res.json({ success: true });
  }
);
```

## 📝 Code Examples

### ❌ Vulnerable

```javascript
// ❌ VULNERABLE: Only authentication
app.get('/admin/users', requireAuth, async (req, res) => {
  // Any authenticated user can access!
  const users = await User.findAll();
  res.json(users);
});
```

### ✅ Secure

```javascript
// ✅ SECURE: Authentication + authorization
app.get('/admin/users',
  requireAuth,
  requireAdmin, // ✅ Role check
  async (req, res) => {
    const users = await User.findAll();
    res.json(users);
  }
);
```

## 🧪 Testing Checklist

- [ ] Admin routes require admin role
- [ ] Regular users get 403 on admin routes
- [ ] Role checks on all protected routes
- [ ] Permission checks where applicable
- [ ] Frontend and backend both check
- [ ] Authorization middleware consistent

## 📚 References

- [OWASP: Broken Access Control](https://owasp.org/www-project-top-ten/)
- [RBAC Patterns](https://en.wikipedia.org/wiki/Role-based_access_control)

## 🔗 Related Vulnerabilities

- [07. Missing Row Level Security](../database_security/07_missing_row_level_security.md)
- [43. Broken Object Level Authorization](./43_broken_object_authorization.md)

---

**Classification**:
- **Confirmed** if routes only check authentication
- **Likely** if role checks incomplete
- **Not Applicable** if proper RBAC implemented
