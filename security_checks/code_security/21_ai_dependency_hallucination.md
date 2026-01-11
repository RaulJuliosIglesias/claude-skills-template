# 21. AI Dependency Hallucination

## 🟡 Risk Level: **MEDIUM**

## 📋 Vulnerability Description

LLMs frequently hallucinate package names or suggest obscure, unverified libraries to solve specific problems. Attackers publish malicious packages using these hallucinated names (typosquatting), waiting for developers to copy-paste the generated install commands, leading to supply chain compromise.

**Impact:**
- Supply chain attacks
- Malware installation
- Credential theft
- Backdoor installation

## 🎯 Context: Why This Happens

AI models:
- Generate plausible package names
- Don't verify package existence
- Suggest unverified libraries
- Copy-paste without verification

## 🔍 Detection Methods

### 1. Package Verification

**Before installing:**
- Check package exists
- Verify download count
- Check maintainer
- Review creation date

### 2. Code Analysis

**Check for:**
- Unfamiliar packages
- Low download counts
- Suspicious names

## ✅ Verification Requirements

### Must Have:
1. **Package Verification**
   - Verify on official registry
   - Check download count
   - Review maintainer
   - Check creation date

2. **Supply Chain Security**
   - Use trusted packages
   - Review dependencies
   - Monitor for updates

## 🚨 Exploit Path

### Scenario 1: Typosquatting
```
1. AI suggests: npm install express-validator
2. Attacker creates: express-validatr (typo)
3. Developer installs typo package
4. Malware executes on install
5. Supply chain compromised
```

## 🔧 Remediation Steps

### Step 1: Verify Packages

```bash
# Check package exists
npm view package-name

# Check download count
npm view package-name downloads

# Check maintainer
npm view package-name maintainers

# Check creation date
npm view package-name time.created
```

### Step 2: Use Package Verification Script

```javascript
// scripts/verify-package.js
const https = require('https');

async function verifyPackage(name) {
  return new Promise((resolve, reject) => {
    https.get(`https://registry.npmjs.org/${name}`, (res) => {
      if (res.statusCode === 404) {
        reject(new Error(`Package ${name} not found`));
        return;
      }
      
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        const pkg = JSON.parse(data);
        
        // Check download count
        if (pkg.downloads < 1000) {
          console.warn(`⚠️  Low download count: ${pkg.downloads}`);
        }
        
        // Check creation date
        const created = new Date(pkg.time.created);
        const daysOld = (Date.now() - created) / (1000 * 60 * 60 * 24);
        if (daysOld < 30) {
          console.warn(`⚠️  New package: ${daysOld} days old`);
        }
        
        resolve(pkg);
      });
    });
  });
}
```

### Step 3: Review Before Installing

**Checklist:**
- [ ] Package exists on official registry
- [ ] Download count reasonable (>1000)
- [ ] Maintainer verified
- [ ] Creation date reasonable
- [ ] No typos in name
- [ ] Reviews/ratings checked

## 📝 Code Examples

### ❌ Vulnerable

```bash
# ❌ VULNERABLE: Install without verification
npm install express-validatr  # Typo - malicious package
```

### ✅ Secure

```bash
# ✅ SECURE: Verify first
npm view express-validatr
# If not found or suspicious, don't install

# Use correct package
npm install express-validator
```

## 🧪 Testing Checklist

- [ ] All packages verified
- [ ] Download counts checked
- [ ] Maintainers reviewed
- [ ] No typosquatting
- [ ] Supply chain monitored

## 📚 References

- [OWASP: Supply Chain Security](https://owasp.org/www-project-supply-chain-security/)
- [npm Package Verification](https://docs.npmjs.com/cli/v8/commands/npm-view)

## 🔗 Related Vulnerabilities

- [06. Outdated Dependencies](./06_outdated_dependencies.md)
- [32. Missing Dependency Lockfiles](../infrastructure_security/32_missing_lockfiles.md)

---

**Classification**:
- **Confirmed** if unverified packages installed
- **Likely** if packages not reviewed
- **Not Applicable** if all packages verified
