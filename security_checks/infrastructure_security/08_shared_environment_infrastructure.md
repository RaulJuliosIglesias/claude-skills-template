# 8. Shared Environment Infrastructure

## 🟠 Risk Level: **HIGH**

## 📋 Vulnerability Description

To save time, vibe coders often deploy development and production branches to the same cloud account or database instance. A logical error, accidental "nuke" command, or compromised API key in the development environment can inadvertently wipe production data or take down live services.

**Impact:**
- Production data loss
- Service disruption
- Cross-environment contamination
- Complete system failure

## 🎯 Context: Why This Happens

AI-generated configs:
- Use same resources for dev/prod
- Don't separate environments
- Share databases
- Use same cloud account

## 🔍 Detection Methods

### 1. Configuration Review

**Check:**
- Same database for dev/prod
- Same cloud account
- Shared resources
- Environment variables

### 2. Infrastructure Review

**Check:**
- Separate AWS accounts
- Separate databases
- Environment isolation

## ✅ Verification Requirements

### Must Have:
1. **Environment Isolation**
   - Separate cloud accounts
   - Separate databases
   - No shared resources

2. **Access Control**
   - Different credentials
   - Separate IAM roles
   - Environment-specific access

## 🚨 Exploit Path

### Scenario 1: Accidental Production Deletion
```
1. Developer runs: npm run db:reset
2. Script connects to "production" database (shared)
3. All production data deleted
4. Service down
5. Data loss
```

## 🔧 Remediation Steps

### Step 1: Separate Cloud Accounts

**AWS Organizations:**
- Create separate accounts for dev/prod
- Use Organizations for management
- Isolate billing and resources

### Step 2: Separate Databases

```javascript
// config/database.js
const config = {
  development: {
    host: 'dev-db.example.com',
    database: 'app_dev'
  },
  production: {
    host: 'prod-db.example.com',
    database: 'app_prod'
  }
};

const env = process.env.NODE_ENV || 'development';
module.exports = config[env];
```

### Step 3: Environment Validation

```javascript
function validateEnvironment() {
  const env = process.env.NODE_ENV;
  
  if (!env) {
    throw new Error('NODE_ENV must be set');
  }
  
  if (env === 'production') {
    // Additional production checks
    if (!process.env.DATABASE_URL) {
      throw new Error('Production database URL required');
    }
    
    // Verify not using dev database
    if (process.env.DATABASE_URL.includes('dev')) {
      throw new Error('Cannot use dev database in production!');
    }
  }
}

validateEnvironment();
```

## 📝 Code Examples

### ❌ Vulnerable

```javascript
// ❌ VULNERABLE: Shared database
const db = process.env.DATABASE_URL || 'postgres://localhost/app';
// Same URL for dev and prod!
```

### ✅ Secure

```javascript
// ✅ SECURE: Separate databases
const config = {
  development: {
    database: 'app_dev',
    host: 'dev-db.internal'
  },
  production: {
    database: 'app_prod',
    host: 'prod-db.internal'
  }
};

const env = process.env.NODE_ENV;
if (!config[env]) {
  throw new Error(`Invalid NODE_ENV: ${env}`);
}

const db = config[env];
```

## 🧪 Testing Checklist

- [ ] Separate cloud accounts
- [ ] Separate databases
- [ ] No shared resources
- [ ] Environment validation
- [ ] Different credentials
- [ ] Isolation verified

## 📚 References

- [AWS Organizations](https://aws.amazon.com/organizations/)
- [Environment Separation Best Practices](https://12factor.net/config)

## 🔗 Related Vulnerabilities

- [05. Hardcoded Default Credentials](./05_hardcoded_default_credentials.md)
- [18. Publicly Exposed Database](./18_publicly_exposed_database.md)

---

**Classification**:
- **Confirmed** if dev/prod share resources
- **Likely** if environment separation unclear
- **Not Applicable** if properly isolated
