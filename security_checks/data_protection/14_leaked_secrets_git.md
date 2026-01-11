# 14. Leaked Secrets in Git History

## 🔴 Risk Level: **CRITICAL**

## 📋 Vulnerability Description

Developers often accidentally commit sensitive files like `.env` and then simply delete them in a subsequent commit. While the file appears gone, the secrets remain permanently accessible in the hidden `.git` folder history, allowing automated scanners to scrape credentials from the repository's past.

**Impact:**
- Permanent secret exposure
- Credentials in git history forever
- Automated bot scanning
- Complete credential compromise

## 🎯 Context: Why This Happens

Common mistakes:
- Commit .env file accidentally
- Add secrets to code for testing
- Commit then delete (secrets still in history)
- Force push doesn't remove from history

## 🔍 Detection Methods

### 1. Git History Scan

**Tools:**
```bash
# gitleaks
gitleaks detect --source . --verbose

# truffleHog
trufflehog git file://. --json

# git-secrets
git secrets --scan-history
```

### 2. Manual Check

```bash
# Check git log for .env
git log --all --full-history -- .env

# Check for secrets in history
git log -p | grep -i "password\|secret\|key"
```

## ✅ Verification Requirements

### Must Have:
1. **No Secrets in History**
   - Scan entire git history
   - Remove committed secrets
   - Rotate exposed credentials

2. **Prevention**
   - Pre-commit hooks
   - .gitignore configured
   - Git secrets installed

## 🚨 Exploit Path

### Scenario 1: Automated Scanning
```
1. Attacker scans public GitHub repos
2. Finds .env in git history
3. Extracts API keys, passwords
4. Uses credentials to access services
5. Complete infrastructure compromise
```

## 🔧 Remediation Steps

### Step 1: Scan History

```bash
# Install gitleaks
brew install gitleaks
# or
go install github.com/gitleaks/gitleaks/v8@latest

# Scan repository
gitleaks detect --source . --verbose
```

### Step 2: Remove from History

**BFG Repo-Cleaner (Recommended):**
```bash
# Install BFG
brew install bfg
# or download from https://rtyley.github.io/bfg-repo-cleaner/

# Remove .env file from history
bfg --delete-files .env

# Clean up
git reflog expire --expire=now --all
git gc --prune=now --aggressive
```

**git filter-repo:**
```bash
# Install
pip install git-filter-repo

# Remove file from history
git filter-repo --path .env --invert-paths

# Force push (if on remote)
git push origin --force --all
```

### Step 3: Rotate Exposed Secrets

**CRITICAL: Rotate all exposed secrets immediately**
- Change all API keys
- Rotate database passwords
- Regenerate JWT secrets
- Update all service credentials

### Step 4: Prevent Future Leaks

**Pre-commit hook:**
```bash
# .git/hooks/pre-commit
#!/bin/bash
gitleaks protect --staged --verbose
if [ $? -ne 0 ]; then
  echo "❌ Secrets detected in staged files!"
  exit 1
fi
```

**git-secrets:**
```bash
git secrets --install
git secrets --register-aws
git secrets --add 'password.*=.*'
```

## 📝 Code Examples

### ❌ Vulnerable

```bash
# ❌ VULNERABLE: Committed .env
git add .env
git commit -m "Add config"
# Secrets now in history forever
```

### ✅ Secure

```bash
# ✅ SECURE: .gitignore
echo ".env" >> .gitignore
git add .gitignore
git commit -m "Add .gitignore"

# ✅ SECURE: Pre-commit hook prevents commits
```

## 🧪 Testing Checklist

- [ ] No secrets in git history (scanned)
- [ ] .gitignore includes .env
- [ ] Pre-commit hooks installed
- [ ] git-secrets configured
- [ ] Exposed secrets rotated
- [ ] History cleaned if needed

## 📚 References

- [OWASP: Use of Hard-coded Credentials](https://owasp.org/www-community/vulnerabilities/Use_of_hard-coded_credentials)
- [GitLeaks](https://github.com/gitleaks/gitleaks)
- [BFG Repo-Cleaner](https://rtyley.github.io/bfg-repo-cleaner/)

## 🔗 Related Vulnerabilities

- [03. Exposed API Keys in Repos](./03_exposed_api_keys.md)
- [12. Public .git Directory](../infrastructure_security/12_public_git_directory.md)

---

**Classification**:
- **Confirmed** if secrets found in git history
- **Likely** if .env was ever committed
- **Not Applicable** if history clean and prevention in place
