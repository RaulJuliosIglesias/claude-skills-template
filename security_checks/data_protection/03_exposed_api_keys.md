# 3. Exposed API Keys in Repositories

## 🔴 Risk Level: **CRITICAL**

## 📋 Vulnerability Description

Secret credentials such as AWS access keys, payment gateway tokens, database connection strings, and API keys are hardcoded directly into source files. These secrets are:
- Immediately visible to anyone with repository access
- Actively scraped by automated bots scanning GitHub/GitLab
- Permanently exposed in git history even if later removed
- Can lead to complete infrastructure compromise

## 🎯 Context: Why This Happens

AI code generators often include example code with hardcoded values:
- Quick setup examples with inline credentials
- Configuration files committed with real keys
- Copy-paste from documentation without sanitization
- `.env` files accidentally committed
- Test credentials left in production code

## 🔍 Detection Methods

### 1. Code Scanning

**Tools:**
- `git-secrets` - Prevents committing secrets
- `truffleHog` - Scans git history for secrets
- `gitleaks` - Fast secret scanner
- GitHub Secret Scanning (automatic)
- GitLab Secret Detection

**Manual Search:**
```bash
# Search for common patterns
grep -r "AKIA[0-9A-Z]" .  # AWS Access Keys
grep -r "sk_live_" .       # Stripe keys
grep -r "AIza" .           # Google API keys
grep -r "xoxb-" .          # Slack tokens
grep -r "mongodb://" .     # MongoDB connection strings
grep -r "postgres://" .    # PostgreSQL connection strings
```

### 2. Git History Analysis

```bash
# Scan entire git history
trufflehog git file://. --json

# Or with gitleaks
gitleaks detect --source . --verbose
```

### 3. Configuration File Review

**Check these files:**
- `.env` (should be in `.gitignore`)
- `config.json`
- `settings.py`
- `config.js`
- `secrets.yaml`
- `docker-compose.yml`
- Any file with "secret", "key", "password", "token" in name

## ✅ Verification Requirements

### Must Have:
1. **No secrets in source code**
   - All credentials in environment variables
   - `.env` files in `.gitignore`
   - No hardcoded API keys
   - No database connection strings in code

2. **Secrets Management**
   - Use environment variables
   - Use secrets management services (AWS Secrets Manager, HashiCorp Vault)
   - Use CI/CD secret injection
   - Rotate secrets regularly

3. **Git Protection**
   - Pre-commit hooks to prevent secret commits
   - Git history scanning
   - Secret scanning in CI/CD pipeline

## 🚨 Exploit Path

### Scenario 1: AWS Credentials Exposed
```
1. Attacker finds AWS access key in GitHub repository
2. Attacker uses key to access AWS account
3. Attacker creates new IAM users with admin access
4. Attacker spins up expensive resources (crypto mining)
5. Attacker accesses S3 buckets, databases, etc.
6. Complete infrastructure compromise
7. Massive bills and data breach
```

### Scenario 2: Database Credentials Exposed
```
1. Attacker finds database connection string
2. Attacker connects directly to database
3. Attacker extracts all user data
4. Attacker modifies or deletes data
5. Complete data breach
```

### Scenario 3: Payment Gateway Keys Exposed
```
1. Attacker finds Stripe API key
2. Attacker uses key to create refunds
3. Attacker steals customer payment information
4. Financial loss and compliance violations
```

## 🔧 Remediation Steps

### Step 1: Immediate Response (If Secrets Found)

**CRITICAL: Rotate all exposed secrets immediately**

```bash
# 1. Identify all exposed secrets
gitleaks detect --source . --verbose > exposed_secrets.txt

# 2. Rotate each secret:
# - AWS: Create new IAM keys, delete old ones
# - Database: Change passwords, rotate credentials
# - API keys: Regenerate in provider dashboard
# - Payment: Revoke and regenerate keys

# 3. Remove from git history
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all

# Or use BFG Repo-Cleaner
bfg --delete-files .env
git reflog expire --expire=now --all
git gc --prune=now --aggressive
```

### Step 2: Implement Environment Variables

**Create `.env.example`:**
```bash
# .env.example (committed to repo)
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
DATABASE_URL=postgresql://user:password@localhost/dbname
STRIPE_SECRET_KEY=sk_test_your_key_here
JWT_SECRET=your_jwt_secret_here
```

**Update `.gitignore`:**
```gitignore
# Environment variables
.env
.env.local
.env.*.local
*.env

# Secrets
secrets/
*.pem
*.key
*.p12
*.pfx

# Configuration with secrets
config/production.json
config/secrets.json
```

**Load in code:**
```javascript
// ❌ VULNERABLE
const awsKey = 'AKIAIOSFODNN7EXAMPLE';
const dbUrl = 'postgresql://user:pass@localhost/db';

// ✅ SECURE
require('dotenv').config();
const awsKey = process.env.AWS_ACCESS_KEY_ID;
const dbUrl = process.env.DATABASE_URL;

if (!awsKey || !dbUrl) {
  throw new Error('Missing required environment variables');
}
```

### Step 3: Use Secrets Management Services

**AWS Secrets Manager:**
```javascript
const AWS = require('aws-sdk');
const secretsManager = new AWS.SecretsManager();

async function getSecret(secretName) {
  const data = await secretsManager.getSecretValue({
    SecretId: secretName
  }).promise();
  
  return JSON.parse(data.SecretString);
}

// Usage
const dbConfig = await getSecret('prod/database/credentials');
```

**HashiCorp Vault:**
```javascript
const vault = require('node-vault')({
  endpoint: process.env.VAULT_ADDR,
  token: process.env.VAULT_TOKEN
});

async function getSecret(path) {
  const result = await vault.read(path);
  return result.data;
}
```

### Step 4: Implement Pre-commit Hooks

**Install git-secrets:**
```bash
git secrets --install
git secrets --register-aws
```

**Create `.git/hooks/pre-commit`:**
```bash
#!/bin/bash
# Pre-commit hook to prevent secret commits

# Check for common secret patterns
if git diff --cached | grep -E "(AKIA[0-9A-Z]{16}|sk_live_|xoxb-|mongodb://.*:.*@)" ; then
  echo "ERROR: Potential secrets detected in commit!"
  echo "Please remove secrets and use environment variables instead."
  exit 1
fi

# Run gitleaks
if command -v gitleaks &> /dev/null; then
  gitleaks protect --staged --verbose
  if [ $? -ne 0 ]; then
    exit 1
  fi
fi
```

### Step 5: CI/CD Secret Scanning

**GitHub Actions:**
```yaml
name: Secret Scanning

on: [push, pull_request]

jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0
      
      - name: Run Gitleaks
        uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

**GitLab CI:**
```yaml
secret_detection:
  stage: test
  image: 
    name: trufflesecurity/trufflehog:latest
  script:
    - trufflehog git file://$CI_PROJECT_DIR --json
  artifacts:
    reports:
      secret_detection: gl-secret-detection-report.json
```

### Step 6: Code Review Checklist

**Before committing:**
- [ ] No hardcoded credentials
- [ ] `.env` files in `.gitignore`
- [ ] All secrets in environment variables
- [ ] `.env.example` updated (without real values)
- [ ] Pre-commit hooks installed
- [ ] CI/CD secret scanning enabled

## 📝 Code Examples

### ❌ Vulnerable Code

```javascript
// config.js - VULNERABLE
module.exports = {
  aws: {
    accessKeyId: 'AKIAIOSFODNN7EXAMPLE',
    secretAccessKey: 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY'
  },
  database: {
    url: 'postgresql://admin:password123@db.example.com:5432/mydb'
  },
  stripe: {
    secretKey: 'sk_live_51Habc123...'
  }
};

// .env - VULNERABLE (if committed)
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
DATABASE_URL=postgresql://admin:password123@db.example.com:5432/mydb
```

### ✅ Secure Code

```javascript
// config.js - SECURE
require('dotenv').config();

if (!process.env.AWS_ACCESS_KEY_ID) {
  throw new Error('AWS_ACCESS_KEY_ID environment variable is required');
}

module.exports = {
  aws: {
    accessKeyId: process.env.AWS_ACCESS_KEY_ID,
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
    region: process.env.AWS_REGION || 'us-east-1'
  },
  database: {
    url: process.env.DATABASE_URL
  },
  stripe: {
    secretKey: process.env.STRIPE_SECRET_KEY
  }
};

// .env - SECURE (not committed, in .gitignore)
# Load from secrets manager or CI/CD
AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
DATABASE_URL=${DATABASE_URL}
STRIPE_SECRET_KEY=${STRIPE_SECRET_KEY}
```

### ✅ Using AWS Secrets Manager

```javascript
const AWS = require('aws-sdk');
const secretsManager = new AWS.SecretsManager({
  region: process.env.AWS_REGION
});

let cachedSecrets = null;

async function getSecrets() {
  if (cachedSecrets) {
    return cachedSecrets;
  }
  
  const secret = await secretsManager.getSecretValue({
    SecretId: process.env.SECRETS_NAME || 'app/secrets'
  }).promise();
  
  cachedSecrets = JSON.parse(secret.SecretString);
  return cachedSecrets;
}

// Usage
const secrets = await getSecrets();
const dbUrl = secrets.DATABASE_URL;
```

## 🧪 Testing Checklist

- [ ] No secrets found in codebase scan
- [ ] `.env` file in `.gitignore`
- [ ] `.env.example` exists (without real values)
- [ ] Pre-commit hooks prevent secret commits
- [ ] CI/CD pipeline scans for secrets
- [ ] Secrets loaded from environment variables
- [ ] Secrets management service configured (if applicable)
- [ ] Documentation explains how to set up secrets
- [ ] Secrets rotated regularly
- [ ] Access to secrets logged and monitored

## 📚 References

- [OWASP: Use of Hard-coded Cryptographic Key](https://owasp.org/www-community/vulnerabilities/Use_of_hard-coded_cryptographic_key)
- [GitHub: Secret Scanning](https://docs.github.com/en/code-security/secret-scanning)
- [GitLeaks Documentation](https://github.com/gitleaks/gitleaks)
- [AWS Secrets Manager](https://aws.amazon.com/secrets-manager/)
- [HashiCorp Vault](https://www.vaultproject.io/)

## 🔗 Related Vulnerabilities

- [04. Privileged Secrets in Frontend Bundles](./04_privileged_secrets_frontend.md)
- [14. Leaked Secrets in Git History](./14_leaked_secrets_git.md)
- [42. Sensitive Data Exposure in Logs](./42_sensitive_data_in_logs.md)

---

**Classification**:
- **Confirmed** if secrets found in committed files
- **Likely** if `.env` files exist but `.gitignore` status unknown
- **Not Applicable** if using secrets management service and no secrets in code
