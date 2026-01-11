# 7. Missing Row Level Security (RLS)

## 🔴 Risk Level: **CRITICAL**

## 📋 Vulnerability Description

Administrative dashboards and user profile endpoints lack database-level access controls. Attackers can modify user IDs in URL parameters (IDOR - Insecure Direct Object Reference) to view or modify sensitive data belonging to other users or administrators.

**Impact:**
- Unauthorized data access
- Data modification/deletion
- Privacy violations (GDPR, CCPA)
- Complete data breach

## 🎯 Context: Why This Happens

AI-generated code often implements authorization only at the application level:
- Frontend hides buttons but doesn't prevent API access
- Backend checks authentication but not resource ownership
- Database queries don't filter by user ID
- No database-level policies

## 🔍 Detection Methods

### 1. Code Analysis

**Search for:**
- RLS policies (PostgreSQL/Supabase)
- User ID filtering in queries
- Resource ownership checks
- Authorization middleware

**Red Flags:**
```javascript
// ❌ VULNERABLE: No user ID check
app.get('/api/users/:id', async (req, res) => {
  const user = await User.findById(req.params.id);
  res.json(user); // Returns any user's data!
});

// ✅ SECURE: User ID verified
app.get('/api/users/:id', requireAuth, async (req, res) => {
  if (req.params.id !== req.user.id) {
    return res.status(403).json({ error: 'Forbidden' });
  }
  const user = await User.findById(req.params.id);
  res.json(user);
});
```

### 2. Database Policy Review

**PostgreSQL/Supabase:**
```sql
-- Check if RLS is enabled
SELECT tablename, rowsecurity 
FROM pg_tables 
WHERE schemaname = 'public';

-- Check existing policies
SELECT * FROM pg_policies 
WHERE schemaname = 'public';
```

### 3. Testing

**IDOR Test:**
```bash
# Test if user can access other user's data
curl -H "Authorization: Bearer $TOKEN" \
  https://api.example.com/users/123

# Change ID to another user's ID
curl -H "Authorization: Bearer $TOKEN" \
  https://api.example.com/users/456

# If both succeed → VULNERABLE
```

## ✅ Verification Requirements

### Must Have:
1. **RLS Enabled on All Tables**
   - Multi-tenant data tables
   - User-specific data tables
   - Any table with user_id or owner_id

2. **Policies for All Operations**
   - SELECT: Users can only read their own data
   - INSERT: Users can only create data for themselves
   - UPDATE: Users can only update their own data
   - DELETE: Users can only delete their own data

3. **Application-Level Checks**
   - Verify user ID matches resource owner
   - Check user roles/permissions
   - Validate resource access before operations

## 🚨 Exploit Path

### Scenario 1: Profile Data Access
```
1. User authenticates and gets token
2. User accesses their profile: GET /api/users/123
3. User changes ID in URL: GET /api/users/456
4. Without RLS, server returns user 456's data
5. Attacker can enumerate all user IDs
6. Complete user database exposed
```

### Scenario 2: Data Modification
```
1. Attacker finds invoice endpoint: PUT /api/invoices/789
2. Attacker changes invoice ID: PUT /api/invoices/999
3. Without ownership check, update succeeds
4. Attacker modifies other user's invoices
5. Financial data compromised
```

### Scenario 3: Admin Access
```
1. Attacker finds admin endpoint: GET /api/admin/users
2. Attacker guesses admin user ID: GET /api/users/1
3. Without RLS, admin data returned
4. Attacker gains admin privileges
5. Complete system compromise
```

## 🔧 Remediation Steps

### Step 1: Enable RLS (PostgreSQL/Supabase)

```sql
-- Enable RLS on users table
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- Policy: Users can only read their own data
CREATE POLICY "Users can view own data"
  ON users
  FOR SELECT
  USING (auth.uid() = id);

-- Policy: Users can only update their own data
CREATE POLICY "Users can update own data"
  ON users
  FOR UPDATE
  USING (auth.uid() = id);

-- Policy: Users can only delete their own data
CREATE POLICY "Users can delete own data"
  ON users
  FOR DELETE
  USING (auth.uid() = id);
```

### Step 2: Multi-Tenant RLS

```sql
-- For tables with user_id foreign key
ALTER TABLE invoices ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own invoices"
  ON invoices
  FOR SELECT
  USING (user_id = auth.uid());

CREATE POLICY "Users can create own invoices"
  ON invoices
  FOR INSERT
  WITH CHECK (user_id = auth.uid());

CREATE POLICY "Users can update own invoices"
  ON invoices
  FOR UPDATE
  USING (user_id = auth.uid())
  WITH CHECK (user_id = auth.uid());
```

### Step 3: Application-Level Checks

**Express.js:**
```javascript
// Middleware to verify resource ownership
const verifyOwnership = (Model, idParam = 'id', userIdField = 'userId') => {
  return async (req, res, next) => {
    const resourceId = req.params[idParam];
    const userId = req.user.id;
    
    const resource = await Model.findById(resourceId);
    
    if (!resource) {
      return res.status(404).json({ error: 'Resource not found' });
    }
    
    // Check ownership
    if (resource[userIdField] !== userId && req.user.role !== 'admin') {
      return res.status(403).json({ error: 'Forbidden' });
    }
    
    req.resource = resource;
    next();
  };
};

// Usage
app.get('/api/invoices/:id',
  requireAuth,
  verifyOwnership(Invoice, 'id', 'userId'),
  async (req, res) => {
    res.json(req.resource);
  }
);

app.put('/api/invoices/:id',
  requireAuth,
  verifyOwnership(Invoice, 'id', 'userId'),
  async (req, res) => {
    const updated = await Invoice.findByIdAndUpdate(
      req.params.id,
      req.body,
      { new: true }
    );
    res.json(updated);
  }
);
```

### Step 4: Query-Level Filtering

```javascript
// Always filter by user ID in queries
app.get('/api/invoices', requireAuth, async (req, res) => {
  // ✅ SECURE: Always filter by user ID
  const invoices = await Invoice.find({ userId: req.user.id });
  res.json(invoices);
});

// ❌ VULNERABLE: No user filter
app.get('/api/invoices', requireAuth, async (req, res) => {
  const invoices = await Invoice.find(); // Returns all invoices!
  res.json(invoices);
});
```

### Step 5: Role-Based Access Control

```javascript
// Admin can access all, users only their own
app.get('/api/users/:id', requireAuth, async (req, res) => {
  const targetUserId = req.params.id;
  const currentUser = req.user;
  
  // Admin can access any user
  if (currentUser.role === 'admin') {
    const user = await User.findById(targetUserId);
    return res.json(user);
  }
  
  // Regular users can only access themselves
  if (targetUserId !== currentUser.id) {
    return res.status(403).json({ error: 'Forbidden' });
  }
  
  const user = await User.findById(targetUserId);
  res.json(user);
});
```

### Step 6: Supabase RLS Example

```sql
-- Enable RLS
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;

-- Policy: Users can read their own profile
CREATE POLICY "Users can view own profile"
  ON profiles
  FOR SELECT
  USING (auth.uid() = user_id);

-- Policy: Users can update their own profile
CREATE POLICY "Users can update own profile"
  ON profiles
  FOR UPDATE
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

-- Policy: Users can insert their own profile
CREATE POLICY "Users can insert own profile"
  ON profiles
  FOR INSERT
  WITH CHECK (auth.uid() = user_id);
```

**Client-side (Supabase):**
```javascript
// Supabase automatically enforces RLS
const { data, error } = await supabase
  .from('profiles')
  .select('*')
  .eq('id', userId); // RLS ensures user can only access their own

// Even if user tries to access another user's ID, RLS blocks it
const { data, error } = await supabase
  .from('profiles')
  .select('*')
  .eq('id', otherUserId); // Returns empty - RLS blocked
```

## 📝 Code Examples

### ❌ Vulnerable Code

```javascript
// No ownership check - VULNERABLE
app.get('/api/users/:id', requireAuth, async (req, res) => {
  const user = await User.findById(req.params.id);
  res.json(user); // Returns any user!
});

app.get('/api/invoices', requireAuth, async (req, res) => {
  const invoices = await Invoice.find();
  res.json(invoices); // Returns all invoices!
});

app.put('/api/invoices/:id', requireAuth, async (req, res) => {
  const invoice = await Invoice.findByIdAndUpdate(
    req.params.id,
    req.body
  );
  res.json(invoice); // Can modify any invoice!
});
```

### ✅ Secure Code

```javascript
// With ownership verification - SECURE
app.get('/api/users/:id', requireAuth, async (req, res) => {
  const targetId = req.params.id;
  
  // Check ownership
  if (targetId !== req.user.id && req.user.role !== 'admin') {
    return res.status(403).json({ error: 'Forbidden' });
  }
  
  const user = await User.findById(targetId);
  res.json(user);
});

app.get('/api/invoices', requireAuth, async (req, res) => {
  // Always filter by user ID
  const invoices = await Invoice.find({ userId: req.user.id });
  res.json(invoices);
});

app.put('/api/invoices/:id', requireAuth, async (req, res) => {
  const invoice = await Invoice.findById(req.params.id);
  
  if (!invoice) {
    return res.status(404).json({ error: 'Not found' });
  }
  
  // Verify ownership
  if (invoice.userId !== req.user.id) {
    return res.status(403).json({ error: 'Forbidden' });
  }
  
  const updated = await Invoice.findByIdAndUpdate(
    req.params.id,
    req.body,
    { new: true }
  );
  res.json(updated);
});
```

### ✅ With RLS (PostgreSQL/Supabase)

```sql
-- Database-level protection
ALTER TABLE invoices ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can only access own invoices"
  ON invoices
  FOR ALL
  USING (user_id = auth.uid());
```

```javascript
// Application code - RLS handles protection
app.get('/api/invoices/:id', requireAuth, async (req, res) => {
  // RLS automatically filters by auth.uid()
  const invoice = await db
    .from('invoices')
    .select('*')
    .eq('id', req.params.id)
    .single();
  
  // If user doesn't own invoice, RLS returns null
  if (!invoice) {
    return res.status(404).json({ error: 'Not found' });
  }
  
  res.json(invoice);
});
```

## 🧪 Testing Checklist

- [ ] RLS enabled on all user-specific tables
- [ ] Policies created for SELECT, INSERT, UPDATE, DELETE
- [ ] Application-level ownership checks implemented
- [ ] User cannot access other user's data (IDOR test)
- [ ] User cannot modify other user's data
- [ ] Admin access properly restricted
- [ ] Multi-tenant data properly isolated
- [ ] Policies tested with different user roles
- [ ] Edge cases handled (deleted users, etc.)

## 📚 References

- [OWASP: Insecure Direct Object References](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/05-Authorization_Testing/04-Testing_for_Insecure_Direct_Object_References)
- [PostgreSQL Row Level Security](https://www.postgresql.org/docs/current/ddl-rowsecurity.html)
- [Supabase Row Level Security](https://supabase.com/docs/guides/auth/row-level-security)
- [OWASP API Security: API5:2019 Broken Function Level Authorization](https://owasp.org/www-project-api-security/)

## 🔗 Related Vulnerabilities

- [35. Missing Route-Level Authorization](../authentication_authorization/35_missing_route_authorization.md)
- [43. Broken Object Level Authorization](../authentication_authorization/43_broken_object_authorization.md)
- [40. Unprotected Attribute Injection](../input_validation/40_unprotected_attribute_injection.md)

---

**Classification**:
- **Confirmed** if database queries don't filter by user ID and RLS not enabled
- **Likely** if application checks exist but RLS not enabled
- **Not Applicable** if data is public or properly protected with RLS
