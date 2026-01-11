# 6. Outdated Dependencies

## 🟠 Risk Level: **HIGH**

## 📋 Vulnerability Description

Applications built with outdated third-party libraries inherit known security flaws found in those versions. Attackers scan for specific library signatures to exploit well-documented vulnerabilities that have already been patched in newer releases.

**Impact:**
- Known CVEs exploited
- Supply chain attacks
- Data breaches
- Service compromise

## 🎯 Context: Why This Happens

AI code generators:
- Use latest packages at generation time
- Don't update dependencies over time
- Copy package.json without version pinning
- Don't include security update processes

## 🔍 Detection Methods

### 1. Dependency Audit

**Automated tools:**
```bash
# npm audit
npm audit

# npm audit with fix
npm audit fix

# yarn audit
yarn audit

# Check for outdated packages
npm outdated

# Snyk (comprehensive)
npx snyk test

# OWASP Dependency Check
dependency-check --scan . --format JSON
```

### 2. Manual Review

**Check package.json:**
```json
{
  "dependencies": {
    "express": "^4.17.1", // Check if latest is 4.18.x
    "lodash": "4.17.20"    // Check for known CVEs
  }
}
```

**Check lock files:**
- `package-lock.json`
- `yarn.lock`
- `requirements.txt` (Python)
- `Gemfile.lock` (Ruby)

### 3. Security Advisories

**Monitor:**
- GitHub Security Advisories
- npm Security Advisories
- CVE Database
- Snyk Vulnerability DB

## ✅ Verification Requirements

### Must Have:
1. **Regular Dependency Updates**
   - Automated dependency updates (Dependabot, Renovate)
   - Monthly security audits
   - Critical updates applied within 24 hours

2. **Version Pinning**
   - Lock files committed
   - Exact versions in production
   - Semantic versioning respected

3. **Security Monitoring**
   - CI/CD security scanning
   - Automated vulnerability alerts
   - Regular dependency reviews

## 🚨 Exploit Path

### Scenario 1: Known CVE Exploitation
```
1. Attacker identifies application stack
2. Attacker finds outdated library version
3. Attacker searches for known CVEs in that version
4. Attacker exploits CVE (e.g., RCE in old Express version)
5. Attacker gains server access
6. Complete system compromise
```

### Scenario 2: Supply Chain Attack
```
1. Attacker publishes malicious package with similar name
2. Developer updates dependency to malicious version
3. Malicious code executes on install/build
4. Attacker gains access
5. Data exfiltration or backdoor installation
```

## 🔧 Remediation Steps

### Step 1: Audit Current Dependencies

```bash
# Run security audit
npm audit

# Get detailed report
npm audit --json > audit-report.json

# Check for outdated packages
npm outdated

# Use Snyk for comprehensive scan
npx snyk test --json > snyk-report.json
```

### Step 2: Update Dependencies

**Safe update process:**
```bash
# 1. Update patch versions (safe)
npm update

# 2. Update minor versions (test first)
npm install package@latest

# 3. Update major versions (requires code changes)
npm install package@^new-major-version

# 4. Update all (risky - test thoroughly)
npm install package@latest --save
```

**Automated updates with Dependabot:**
```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
    reviewers:
      - "security-team"
    labels:
      - "dependencies"
      - "security"
```

### Step 3: Pin Versions and Use Lock Files

**package.json:**
```json
{
  "dependencies": {
    "express": "^4.18.2", // Use caret for minor updates
    "lodash": "4.17.21"    // Pin exact version for critical packages
  }
}
```

**Always commit lock files:**
```bash
# Commit package-lock.json
git add package-lock.json
git commit -m "chore: update dependencies"

# Use npm ci in production (uses lock file exactly)
npm ci
```

### Step 4: Implement CI/CD Security Scanning

**GitHub Actions:**
```yaml
name: Security Scan

on: [push, pull_request]

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run npm audit
        run: npm audit --audit-level=moderate
      
      - name: Run Snyk test
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
        with:
          args: --severity-threshold=high
```

**GitLab CI:**
```yaml
dependency_scanning:
  stage: test
  image: 
    name: snyk/snyk:docker
  script:
    - snyk auth $SNYK_TOKEN
    - snyk test --severity-threshold=high
  artifacts:
    reports:
      sast: snyk-report.json
```

### Step 5: Set Up Automated Alerts

**Snyk Integration:**
```bash
# Install Snyk CLI
npm install -g snyk

# Authenticate
snyk auth

# Monitor project
snyk monitor

# Set up GitHub integration for alerts
snyk monitor --org=your-org
```

**GitHub Dependabot Alerts:**
- Automatically enabled on GitHub
- Configure in repository settings
- Set up email/Slack notifications

### Step 6: Create Update Policy

**Document update process:**
```markdown
# DEPENDENCY_UPDATE_POLICY.md

## Update Schedule
- **Critical vulnerabilities**: Update within 24 hours
- **High vulnerabilities**: Update within 1 week
- **Medium vulnerabilities**: Update within 1 month
- **Low vulnerabilities**: Update in next major release

## Update Process
1. Review security advisory
2. Check breaking changes
3. Update in development branch
4. Run full test suite
5. Deploy to staging
6. Monitor for issues
7. Deploy to production
```

### Step 7: Remove Unused Dependencies

```bash
# Find unused dependencies
npx depcheck

# Remove unused
npm uninstall unused-package
```

## 📝 Code Examples

### ❌ Vulnerable Setup

```json
// package.json - VULNERABLE
{
  "dependencies": {
    "express": "4.17.1", // ❌ Old version with known CVEs
    "lodash": "^4.17.0", // ❌ Old version
    "axios": "*"          // ❌ Wildcard - dangerous!
  }
}
```

```bash
# No lock file committed
# .gitignore includes package-lock.json ❌
```

### ✅ Secure Setup

```json
// package.json - SECURE
{
  "dependencies": {
    "express": "^4.18.2", // ✅ Latest stable
    "lodash": "4.17.21",   // ✅ Pinned, latest patch
    "axios": "^1.6.0"      // ✅ Specific version range
  },
  "devDependencies": {
    "snyk": "^1.1200.0"    // ✅ Security scanning tool
  }
}
```

```bash
# Lock file committed
# package-lock.json in repository ✅

# Production uses exact versions
npm ci # Uses lock file exactly
```

**Automated updates:**
```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
    reviewers:
      - "security-team"
```

**CI/CD security:**
```yaml
# .github/workflows/security.yml
name: Security Audit

on: [push, pull_request]

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: npm ci
      - run: npm audit --audit-level=moderate
      - uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
```

## 🧪 Testing Checklist

- [ ] All dependencies up to date
- [ ] No known CVEs in dependencies
- [ ] Lock files committed to repository
- [ ] CI/CD runs security scans
- [ ] Automated dependency updates configured
- [ ] Security alerts set up
- [ ] Update policy documented
- [ ] Regular dependency reviews scheduled
- [ ] Unused dependencies removed
- [ ] Production uses `npm ci` (exact versions)

## 📚 References

- [OWASP: Using Components with Known Vulnerabilities](https://owasp.org/www-project-top-ten/)
- [npm Security Best Practices](https://docs.npmjs.com/security-best-practices)
- [Snyk Vulnerability Database](https://security.snyk.io/)
- [GitHub Dependabot](https://docs.github.com/en/code-security/dependabot)
- [CVE Database](https://cve.mitre.org/)

## 🔗 Related Vulnerabilities

- [21. AI Dependency Hallucination](./21_ai_dependency_hallucination.md)
- [32. Missing Dependency Lockfiles](../infrastructure_security/32_missing_lockfiles.md)
- [44. Insecure Infrastructure as Code](../infrastructure_security/44_insecure_iac.md)

---

**Classification**:
- **Confirmed** if outdated packages with known CVEs found
- **Likely** if packages haven't been updated in 6+ months
- **Not Applicable** if all dependencies are up to date and scanned
