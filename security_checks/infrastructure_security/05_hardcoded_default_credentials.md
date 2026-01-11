# 5. Hardcoded Default Credentials

## 🔴 Risk Level: **CRITICAL**

## 📋 Vulnerability Description

AI models frequently generate database seed scripts or initial migration files containing default administrative accounts (e.g., `admin@example.com` / `password123`) to make the app "ready to run." Developers often forget to remove these seed users before production, granting attackers instant admin access.

**Impact:**
- Immediate admin account compromise
- Complete system access
- Data breach
- Service disruption

## 🎯 Context: Why This Happens

AI code generators create:
- Seed files with example users for testing
- Migration files with default admin accounts
- Quick-start scripts with hardcoded credentials
- Documentation examples that get copied to production

## 🔍 Detection Methods

### 1. Code Analysis

**Search for:**
```bash
# Common default credentials
grep -r "admin@example.com\|admin@test.com" .
grep -r "password123\|admin123\|password" .
grep -r "INSERT INTO.*users.*admin" .
grep -r "seed.*admin\|fixture.*admin" .
```

**Check files:**
- `seed.js`, `seeds.js`
- `fixtures.json`, `fixtures.js`
- Migration files (`migrations/`, `db/migrate/`)
- `init.sql`, `setup.sql`
- Test data files

### 2. Database Review

**Check database:**
```sql
-- Check for default admin users
SELECT * FROM users WHERE email LIKE '%example.com%';
SELECT * FROM users WHERE email LIKE '%test.com%';
SELECT * FROM users WHERE email = 'admin@example.com';
SELECT * FROM users WHERE username = 'admin';
```

### 3. Environment Review

**Check for:**
- Default passwords in environment variables
- Hardcoded credentials in config files
- Example credentials in documentation

## ✅ Verification Requirements

### Must Have:
1. **No Default Credentials in Code**
   - Seed files use environment variables
   - No hardcoded passwords
   - No example.com emails in production

2. **Production Seed Protection**
   - Seeding disabled in production
   - Initial admin created via secure process
   - Credentials rotated after first use

3. **Secure Initial Setup**
   - Admin account created via CLI/script
   - Strong random password generated
   - Password change required on first login

## 🚨 Exploit Path

### Scenario 1: Default Admin Account
```
1. Attacker finds seed file with admin@example.com / password123
2. Attacker tries credentials on production
3. Login succeeds
4. Attacker has admin access
5. Attacker can modify/delete all data
6. Complete system compromise
```

### Scenario 2: Migration File Credentials
```
1. Attacker examines git history or codebase
2. Finds migration file with INSERT statement
3. Sees default admin credentials
4. Tries credentials on production
5. Gains admin access
```

## 🔧 Remediation Steps

### Step 1: Audit Existing Code

**Find all default credentials:**
```bash
# Search codebase
grep -r "admin@example\|password123\|admin123" . --include="*.js" --include="*.ts" --include="*.sql" --include="*.json"

# Check seed files
find . -name "*seed*" -o -name "*fixture*" | xargs grep -l "admin\|password"

# Check migrations
find . -path "*/migrations/*" -name "*.js" -o -name "*.sql" | xargs grep -l "INSERT.*users"
```

### Step 2: Remove Hardcoded Credentials

**Before (Vulnerable):**
```javascript
// db/seed.js - ❌ VULNERABLE
const users = [
  {
    email: 'admin@example.com',
    password: 'password123',
    role: 'admin'
  }
];

await User.bulkCreate(users);
```

**After (Secure):**
```javascript
// db/seed.js - ✅ SECURE
// Only run in development
if (process.env.NODE_ENV === 'production') {
  throw new Error('Seeding is disabled in production');
}

// Use environment variables
const adminEmail = process.env.ADMIN_EMAIL;
const adminPassword = process.env.ADMIN_PASSWORD;

if (!adminEmail || !adminPassword) {
  throw new Error('ADMIN_EMAIL and ADMIN_PASSWORD must be set');
}

// Hash password properly
const hashedPassword = await bcrypt.hash(adminPassword, 10);

await User.create({
  email: adminEmail,
  password: hashedPassword,
  role: 'admin',
  emailVerified: true
});
```

### Step 3: Secure Initial Admin Creation

**Option 1: CLI Script**
```javascript
// scripts/create-admin.js
const bcrypt = require('bcrypt');
const readline = require('readline');
const { User } = require('../models');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

async function createAdmin() {
  rl.question('Admin email: ', async (email) => {
    rl.question('Admin password: ', async (password) => {
      const hashedPassword = await bcrypt.hash(password, 10);
      
      const admin = await User.create({
        email,
        password: hashedPassword,
        role: 'admin',
        emailVerified: true
      });
      
      console.log('Admin user created:', admin.email);
      rl.close();
    });
  });
}

createAdmin();
```

**Option 2: Environment Variables**
```bash
# .env (not committed)
ADMIN_EMAIL=admin@yourdomain.com
ADMIN_PASSWORD=$(openssl rand -base64 32) # Generate random password
```

```javascript
// scripts/setup-admin.js
require('dotenv').config();
const bcrypt = require('bcrypt');
const { User } = require('../models');

async function setupAdmin() {
  if (process.env.NODE_ENV === 'production' && !process.env.ADMIN_PASSWORD) {
    throw new Error('ADMIN_PASSWORD must be set in production');
  }
  
  const email = process.env.ADMIN_EMAIL;
  const password = process.env.ADMIN_PASSWORD;
  
  if (!email || !password) {
    throw new Error('ADMIN_EMAIL and ADMIN_PASSWORD required');
  }
  
  // Check if admin exists
  const existing = await User.findOne({ email, role: 'admin' });
  if (existing) {
    console.log('Admin user already exists');
    return;
  }
  
  const hashedPassword = await bcrypt.hash(password, 10);
  
  await User.create({
    email,
    password: hashedPassword,
    role: 'admin',
    emailVerified: true,
    mustChangePassword: true // Force password change on first login
  });
  
  console.log('Admin user created. Please change password on first login.');
}

setupAdmin();
```

### Step 4: Protect Seed Files

**Add environment check:**
```javascript
// db/seed.js
if (process.env.NODE_ENV === 'production') {
  console.error('Seeding is disabled in production');
  process.exit(1);
}

// Only seed test data in development
if (process.env.NODE_ENV === 'development') {
  // Seed test users (not admin)
  await User.bulkCreate([
    {
      email: 'test@example.com',
      password: await bcrypt.hash('test123', 10),
      role: 'user'
    }
  ]);
}
```

### Step 5: Secure Migrations

**Before (Vulnerable):**
```sql
-- migrations/001_create_admin.sql - ❌ VULNERABLE
INSERT INTO users (email, password, role) VALUES
  ('admin@example.com', 'password123', 'admin');
```

**After (Secure):**
```sql
-- migrations/001_create_admin.sql - ✅ SECURE
-- Don't create admin in migration
-- Admin should be created via setup script

-- Or use environment variable (if supported)
-- INSERT INTO users (email, password, role) VALUES
--   (:admin_email, crypt(:admin_password, gen_salt('bf')), 'admin');
```

**Better: Separate migration and seed:**
```javascript
// migrations/001_create_users_table.js
exports.up = async (knex) => {
  await knex.schema.createTable('users', (table) => {
    table.uuid('id').primary();
    table.string('email').unique().notNullable();
    table.string('password').notNullable();
    table.string('role').defaultTo('user');
    // ... other fields
  });
};

// seeds/001_test_users.js (development only)
exports.seed = async (knex) => {
  if (process.env.NODE_ENV === 'production') {
    return; // Skip in production
  }
  
  await knex('users').insert([
    {
      id: 'test-user-id',
      email: 'test@example.com',
      password: await bcrypt.hash('test123', 10),
      role: 'user'
    }
  ]);
};
```

### Step 6: Remove Existing Default Accounts

**If default accounts exist:**
```javascript
// scripts/remove-default-accounts.js
const { User } = require('../models');

async function removeDefaultAccounts() {
  const defaultEmails = [
    'admin@example.com',
    'admin@test.com',
    'test@example.com'
  ];
  
  for (const email of defaultEmails) {
    const user = await User.findOne({ email });
    if (user) {
      console.log(`Removing default account: ${email}`);
      await user.destroy();
    }
  }
}

removeDefaultAccounts();
```

## 📝 Code Examples

### ❌ Vulnerable Code

```javascript
// db/seed.js - VULNERABLE
const users = [
  {
    email: 'admin@example.com',
    password: 'password123', // ❌ Plain text!
    role: 'admin'
  },
  {
    email: 'user@example.com',
    password: 'user123',
    role: 'user'
  }
];

await User.bulkCreate(users); // ❌ Creates in production too!
```

```sql
-- migrations/001_init.sql - VULNERABLE
INSERT INTO users (email, password, role) VALUES
  ('admin@example.com', 'password123', 'admin'); -- ❌ Hardcoded!
```

### ✅ Secure Code

```javascript
// db/seed.js - SECURE
if (process.env.NODE_ENV === 'production') {
  throw new Error('Seeding disabled in production');
}

// Only seed test users in development
if (process.env.NODE_ENV === 'development') {
  await User.bulkCreate([
    {
      email: 'test@example.com',
      password: await bcrypt.hash('test123', 10), // ✅ Hashed
      role: 'user' // ✅ Not admin
    }
  ]);
}

// Admin created separately via setup script
// scripts/setup-admin.js
require('dotenv').config();
const bcrypt = require('bcrypt');
const { User } = require('../models');

const email = process.env.ADMIN_EMAIL;
const password = process.env.ADMIN_PASSWORD;

if (!email || !password) {
  throw new Error('ADMIN_EMAIL and ADMIN_PASSWORD required');
}

const hashedPassword = await bcrypt.hash(password, 10);

await User.create({
  email,
  password: hashedPassword,
  role: 'admin',
  emailVerified: true,
  mustChangePassword: true
});
```

## 🧪 Testing Checklist

- [ ] No hardcoded credentials in seed files
- [ ] No default admin accounts in migrations
- [ ] Seed files check NODE_ENV before running
- [ ] Admin creation uses environment variables
- [ ] Passwords are hashed, not plain text
- [ ] Production database has no example.com emails
- [ ] Initial admin password change required
- [ ] Documentation explains secure setup process
- [ ] CI/CD doesn't run seeds in production

## 📚 References

- [OWASP: Use of Hard-coded Credentials](https://owasp.org/www-community/vulnerabilities/Use_of_hard-coded_credentials)
- [CWE-798: Use of Hard-coded Credentials](https://cwe.mitre.org/data/definitions/798.html)
- [NIST: Password Guidelines](https://pages.nist.gov/800-63-3/sp800-63b.html)

## 🔗 Related Vulnerabilities

- [03. Exposed API Keys in Repos](../data_protection/03_exposed_api_keys.md)
- [27. Plaintext Password Storage](../data_protection/27_plaintext_passwords.md)
- [08. Shared Environment Infrastructure](./08_shared_environment_infrastructure.md)

---

**Classification**:
- **Confirmed** if default credentials found in seed/migration files
- **Likely** if example credentials exist but production status unknown
- **Not Applicable** if using secure admin creation process
