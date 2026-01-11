# 26. Insecure RPC Parameter Exposure

## 🔴 Risk Level: **CRITICAL**

## 📋 Vulnerability Description

Server-side functions (RPCs) meant for internal logic are often exposed to the public API with sensitive parameters like "user_id" or "credit_amount" as arguments. Attackers can call these functions directly via the REST API, passing their own ID and arbitrary amounts to grant themselves free credits or manipulate other users' data.

**Impact:**
- Unauthorized operations
- Privilege escalation
- Financial manipulation
- Data corruption

## 🎯 Context: Why This Happens

AI-generated RPC endpoints:
- Accept user_id as parameter
- Trust client-provided values
- Don't verify context
- Expose internal functions

## 🔍 Detection Methods

### 1. Code Analysis

**Search for:**
```javascript
// ❌ VULNERABLE: User ID from client
app.post('/api/credits', async (req, res) => {
  await addCredits(req.body.userId, req.body.amount);
  // ❌ Client provides userId
});
```

### 2. Testing

```bash
# Test parameter manipulation
curl -X POST https://api.example.com/credits \
  -d '{"userId": "admin-id", "amount": 10000}'
# If succeeds → VULNERABLE
```

## ✅ Verification Requirements

### Must Have:
1. **Context from Session**
   - Derive user ID from token
   - Never accept from client
   - Verify ownership

2. **Parameter Validation**
   - Validate amounts
   - Check permissions
   - Enforce business rules

## 🚨 Exploit Path

### Scenario 1: Free Credits
```
1. Attacker finds credits endpoint
2. Attacker sends: {"userId": "attacker-id", "amount": 10000}
3. Server processes request
4. Attacker gets free credits
5. Financial loss
```

## 🔧 Remediation Steps

### Step 1: Derive User from Session

```javascript
// ❌ VULNERABLE
app.post('/api/credits', requireAuth, async (req, res) => {
  await addCredits(req.body.userId, req.body.amount);
  // ❌ Client provides userId
});

// ✅ SECURE
app.post('/api/credits', requireAuth, async (req, res) => {
  // ✅ User ID from session, not client
  const userId = req.user.id;
  const amount = req.body.amount;
  
  // Validate amount
  if (amount > 1000) {
    return res.status(400).json({ error: 'Amount too large' });
  }
  
  await addCredits(userId, amount);
  res.json({ success: true });
});
```

### Step 2: Database-Level Security

```sql
-- ✅ SECURE: User ID from auth context
CREATE FUNCTION add_credits(amount INTEGER)
RETURNS VOID AS $$
BEGIN
  -- ✅ User ID from auth, not parameter
  UPDATE users
  SET credits = credits + amount
  WHERE id = auth.uid();
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```

## 📝 Code Examples

### ❌ Vulnerable

```javascript
// ❌ VULNERABLE: Client provides user ID
app.post('/api/credits', requireAuth, async (req, res) => {
  await addCredits(req.body.userId, req.body.amount);
  // ❌ Can manipulate userId
});
```

### ✅ Secure

```javascript
// ✅ SECURE: User from session
app.post('/api/credits', requireAuth, async (req, res) => {
  const userId = req.user.id; // ✅ From token
  const amount = req.body.amount;
  
  // Validate
  if (amount <= 0 || amount > 1000) {
    return res.status(400).json({ error: 'Invalid amount' });
  }
  
  await addCredits(userId, amount);
  res.json({ success: true });
});
```

## 🧪 Testing Checklist

- [ ] User ID from session, not client
- [ ] Sensitive parameters not accepted
- [ ] Amounts validated
- [ ] Permissions checked
- [ ] Database functions use auth context

## 📚 References

- [OWASP: Insecure Direct Object Reference](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/05-Authorization_Testing/04-Testing_for_Insecure_Direct_Object_References)

## 🔗 Related Vulnerabilities

- [43. Broken Object Level Authorization](../authentication_authorization/43_broken_object_authorization.md)
- [40. Unprotected Attribute Injection](../input_validation/40_unprotected_attribute_injection.md)

---

**Classification**:
- **Confirmed** if user ID accepted from client
- **Likely** if sensitive parameters exposed
- **Not Applicable** if context derived from session
