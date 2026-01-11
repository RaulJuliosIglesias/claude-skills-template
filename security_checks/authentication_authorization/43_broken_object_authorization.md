# 43. Broken Object Level Authorization (BOLA)

## 🔴 Risk Level: **CRITICAL**

## 📋 Vulnerability Description

This vulnerability occurs when an API endpoint validates that a user is logged in but fails to verify that the specific resource ID belongs to them. Attackers can iterate through IDs to view or modify sensitive data belonging to other users.

**Impact:**
- Unauthorized data access
- Data modification
- Privacy violations
- Complete data breach

## 🎯 Context: Why This Happens

AI-generated endpoints:
- Check authentication
- Don't check resource ownership
- Trust user-provided IDs
- Don't verify user-resource relationship

## 🔍 Detection Methods

### 1. Code Analysis

**Search for:**
```javascript
// ❌ VULNERABLE: No ownership check
app.get('/api/invoices/:id', requireAuth, async (req, res) => {
  const invoice = await Invoice.findByPk(req.params.id);
  res.json(invoice); // ❌ No user ID check
});

// ✅ SECURE: Ownership verified
app.get('/api/invoices/:id', requireAuth, async (req, res) => {
  const invoice = await Invoice.findOne({
    where: {
      id: req.params.id,
      userId: req.user.id // ✅ Ownership check
    }
  });
  res.json(invoice);
});
```

### 2. Testing

```bash
# Test with different user's ID
curl -H "Authorization: Bearer $USER1_TOKEN" \
  https://api.example.com/invoices/123

# Change to another user's invoice ID
curl -H "Authorization: Bearer $USER1_TOKEN" \
  https://api.example.com/invoices/456

# If both succeed → VULNERABLE
```

## ✅ Verification Requirements

### Must Have:
1. **Ownership Verification**
   - Check user ID matches resource owner
   - Verify in database query
   - Don't trust client-provided ownership

2. **Consistent Checks**
   - All user-specific resources
   - Every GET, PUT, DELETE
   - No exceptions

## 🚨 Exploit Path

### Scenario 1: Invoice Enumeration
```
1. User authenticates
2. User accesses their invoice: /api/invoices/123
3. User changes ID: /api/invoices/124
4. Server returns invoice 124 (no ownership check)
5. User can enumerate all invoices
6. Sensitive data exposed
```

## 🔧 Remediation Steps

### Step 1: Always Check Ownership

```javascript
// ✅ SECURE: Ownership in query
app.get('/api/invoices/:id', requireAuth, async (req, res) => {
  const invoice = await Invoice.findOne({
    where: {
      id: req.params.id,
      userId: req.user.id // ✅ Always check ownership
    }
  });
  
  if (!invoice) {
    return res.status(404).json({ error: 'Not found' });
  }
  
  res.json(invoice);
});

app.put('/api/invoices/:id', requireAuth, async (req, res) => {
  const invoice = await Invoice.findOne({
    where: {
      id: req.params.id,
      userId: req.user.id
    }
  });
  
  if (!invoice) {
    return res.status(404).json({ error: 'Not found' });
  }
  
  await invoice.update(req.body);
  res.json(invoice);
});
```

### Step 2: Create Ownership Middleware

```javascript
function verifyOwnership(Model, idParam = 'id', userIdField = 'userId') {
  return async (req, res, next) => {
    const resourceId = req.params[idParam];
    const userId = req.user.id;
    
    const resource = await Model.findOne({
      where: {
        [idParam === 'id' ? 'id' : idParam]: resourceId,
        [userIdField]: userId
      }
    });
    
    if (!resource) {
      return res.status(404).json({ error: 'Resource not found' });
    }
    
    req.resource = resource;
    next();
  };
}

// Usage
app.get('/api/invoices/:id',
  requireAuth,
  verifyOwnership(Invoice, 'id', 'userId'),
  async (req, res) => {
    res.json(req.resource); // Already verified
  }
);
```

### Step 3: Use RLS (Database Level)

```sql
-- PostgreSQL/Supabase RLS
CREATE POLICY "Users can only access own invoices"
  ON invoices
  FOR ALL
  USING (user_id = auth.uid());
```

## 📝 Code Examples

### ❌ Vulnerable

```javascript
// ❌ VULNERABLE: No ownership check
app.get('/api/invoices/:id', requireAuth, async (req, res) => {
  const invoice = await Invoice.findByPk(req.params.id);
  res.json(invoice); // ❌ Returns any invoice
});

app.put('/api/invoices/:id', requireAuth, async (req, res) => {
  const invoice = await Invoice.findByPk(req.params.id);
  await invoice.update(req.body); // ❌ Can modify any invoice
  res.json(invoice);
});
```

### ✅ Secure

```javascript
// ✅ SECURE: Ownership always checked
app.get('/api/invoices/:id', requireAuth, async (req, res) => {
  const invoice = await Invoice.findOne({
    where: {
      id: req.params.id,
      userId: req.user.id // ✅ Ownership verified
    }
  });
  
  if (!invoice) {
    return res.status(404).json({ error: 'Not found' });
  }
  
  res.json(invoice);
});

app.put('/api/invoices/:id', requireAuth, async (req, res) => {
  const invoice = await Invoice.findOne({
    where: {
      id: req.params.id,
      userId: req.user.id
    }
  });
  
  if (!invoice) {
    return res.status(404).json({ error: 'Not found' });
  }
  
  await invoice.update(req.body);
  res.json(invoice);
});
```

## 🧪 Testing Checklist

- [ ] User cannot access other user's resources
- [ ] Ownership checked in all queries
- [ ] 404 returned for non-owned resources
- [ ] ID enumeration prevented
- [ ] RLS enabled (if using database that supports it)
- [ ] All user-specific endpoints protected

## 📚 References

- [OWASP: Broken Object Level Authorization](https://owasp.org/www-project-api-security/)
- [OWASP: Insecure Direct Object Reference](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/05-Authorization_Testing/04-Testing_for_Insecure_Direct_Object_References)

## 🔗 Related Vulnerabilities

- [07. Missing Row Level Security](../database_security/07_missing_row_level_security.md)
- [35. Missing Route-Level Authorization](./35_missing_route_authorization.md)
- [40. Unprotected Attribute Injection](../input_validation/40_unprotected_attribute_injection.md)

---

**Classification**:
- **Confirmed** if resources accessible without ownership check
- **Likely** if ownership checks incomplete
- **Not Applicable** if ownership verified in all queries
