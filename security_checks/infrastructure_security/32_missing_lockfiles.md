# 32. Missing Dependency Lockfiles

## 🟡 Risk Level: **MEDIUM**

## 📋 Vulnerability Description

Vibe coders often ignore `package-lock.json` or `yarn.lock` files, or fail to commit them to version control. This causes CI/CD pipelines to pull the absolute latest versions of dependencies during deployment, which may contain breaking changes or recently injected malware (supply chain attacks) that were not present during development.

**Impact:**
- Supply chain attacks
- Unexpected breaking changes
- Inconsistent environments
- Security vulnerabilities from new versions

## 🎯 Context: Why This Happens

Common mistakes:
- Lock files in .gitignore
- Not understanding lock file importance
- Using `npm install` instead of `npm ci`
- Assuming latest is always better

## 🔍 Detection Methods

### 1. Repository Check

```bash
# Check if lock file exists
ls package-lock.json yarn.lock

# Check if in .gitignore
grep "package-lock.json\|yarn.lock" .gitignore
```

### 2. CI/CD Review

**Check build scripts:**
```yaml
# ❌ VULNERABLE
- run: npm install

# ✅ SECURE
- run: npm ci
```

## ✅ Verification Requirements

### Must Have:
1. **Lock Files Committed**
   - package-lock.json in repo
   - yarn.lock in repo
   - Not in .gitignore

2. **CI/CD Uses Lock Files**
   - `npm ci` not `npm install`
   - `yarn install --frozen-lockfile`
   - Exact versions used

## 🚨 Exploit Path

### Scenario 1: Supply Chain Attack
```
1. Developer uses npm install (no lock file)
2. CI/CD also uses npm install
3. Malicious package published
4. CI/CD installs malicious version
5. Malware executes in build
6. Supply chain compromised
```

## 🔧 Remediation Steps

### Step 1: Commit Lock Files

```bash
# Generate lock file
npm install

# Commit it
git add package-lock.json
git commit -m "chore: add package-lock.json"
```

**Update .gitignore:**
```gitignore
# Don't ignore lock files!
# package-lock.json  ❌ Remove this
# yarn.lock          ❌ Remove this

# Only ignore node_modules
node_modules/
```

### Step 2: Use npm ci in CI/CD

```yaml
# .github/workflows/ci.yml
- name: Install dependencies
  run: npm ci  # ✅ Uses lock file exactly
  # Not: npm install ❌
```

### Step 3: Validate Lock File

```bash
# Pre-commit hook
#!/bin/bash
if [ ! -f package-lock.json ]; then
  echo "❌ package-lock.json missing!"
  echo "Run: npm install"
  exit 1
fi
```

## 📝 Code Examples

### ❌ Vulnerable

```bash
# ❌ VULNERABLE: No lock file
npm install
# package-lock.json not committed

# CI/CD
npm install  # Installs latest versions
```

### ✅ Secure

```bash
# ✅ SECURE: Lock file committed
npm install
git add package-lock.json
git commit -m "Add lock file"

# CI/CD
npm ci  # Uses exact versions from lock file
```

## 🧪 Testing Checklist

- [ ] package-lock.json committed
- [ ] Lock file not in .gitignore
- [ ] CI/CD uses npm ci
- [ ] Dependencies match lock file
- [ ] Lock file updated on changes

## 📚 References

- [npm ci Documentation](https://docs.npmjs.com/cli/v8/commands/npm-ci)
- [Supply Chain Security](https://owasp.org/www-project-supply-chain-security/)

## 🔗 Related Vulnerabilities

- [06. Outdated Dependencies](../code_security/06_outdated_dependencies.md)
- [21. AI Dependency Hallucination](../code_security/21_ai_dependency_hallucination.md)

---

**Classification**:
- **Confirmed** if lock file missing or ignored
- **Likely** if CI/CD uses npm install
- **Not Applicable** if lock file committed and npm ci used
