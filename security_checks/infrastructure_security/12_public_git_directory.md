# 12. Public .git Directory Exposure

## 🟠 Risk Level: **HIGH**

## 📋 Vulnerability Description

Misconfigured web servers often serve the hidden .git directory to the public internet. This allows remote attackers to download the entire repository structure, source code, and commit logs simply by requesting `/.git/config` on the production domain.

**Impact:**
- Complete source code exposure
- Commit history revealed
- Configuration files exposed
- Secrets in git history accessible
- Internal structure revealed

## 🎯 Context: Why This Happens

Common misconfigurations:
- Web server serves all files
- .git directory not excluded
- Deployment includes .git folder
- No .gitignore in web server config

## 🔍 Detection Methods

### 1. Testing

**Check if .git is accessible:**
```bash
# Test for .git/config
curl https://example.com/.git/config

# If returns git config → VULNERABLE
# Should return 404 or 403
```

### 2. Code Review

**Check deployment:**
- Is .git directory included?
- Web server configuration
- Docker images include .git?

## ✅ Verification Requirements

### Must Have:
1. **.git Directory Blocked**
   - Web server denies access
   - .git not in deployment
   - 404/403 for .git requests

2. **Secure Deployment**
   - Only production files deployed
   - No version control files
   - No hidden directories

## 🚨 Exploit Path

### Scenario 1: Source Code Theft
```
1. Attacker requests: https://site.com/.git/config
2. Server returns git configuration
3. Attacker uses tools (git-dumper, etc.)
4. Attacker downloads entire repository
5. Source code, secrets, history exposed
6. Complete codebase compromised
```

## 🔧 Remediation Steps

### Step 1: Block .git in Web Server

**Nginx:**
```nginx
# Block .git and other hidden files
location ~ /\. {
    deny all;
    return 404;
}

# Specifically block .git
location ~ /\.git {
    deny all;
    return 404;
}
```

**Apache:**
```apache
# .htaccess
<DirectoryMatch "^/.*/\.git/">
    Require all denied
</DirectoryMatch>

# Block all dotfiles
RedirectMatch 403 /\..*$
```

**Express:**
```javascript
// Block .git requests
app.use((req, res, next) => {
  if (req.path.includes('/.git')) {
    return res.status(404).send('Not found');
  }
  next();
});
```

### Step 2: Exclude .git from Deployment

**Docker:**
```dockerfile
# .dockerignore
.git
.gitignore
.gitattributes
```

**Build process:**
```bash
# Only copy necessary files
rsync -av --exclude='.git' src/ dist/
```

### Step 3: Use .gitignore in Web Root

**Create .gitignore in public directory:**
```
.git
.gitignore
.env
*.log
```

## 📝 Code Examples

### ❌ Vulnerable Setup

```nginx
# ❌ VULNERABLE: Serves all files
server {
    root /var/www/html;
    # No restrictions on .git
}
```

### ✅ Secure Setup

```nginx
# ✅ SECURE: Block .git
server {
    root /var/www/html;
    
    # Block .git and hidden files
    location ~ /\. {
        deny all;
        return 404;
    }
}
```

## 🧪 Testing Checklist

- [ ] .git/config returns 404/403
- [ ] .git directory not accessible
- [ ] .git not in deployment
- [ ] Web server blocks hidden files
- [ ] Docker excludes .git
- [ ] Build process excludes .git

## 📚 References

- [OWASP: Information Exposure](https://owasp.org/www-community/vulnerabilities/Information_exposure)
- [Git Security](https://git-scm.com/docs/git-config#_security)

## 🔗 Related Vulnerabilities

- [14. Leaked Secrets in Git History](../data_protection/14_leaked_secrets_git.md)
- [03. Exposed API Keys in Repos](../data_protection/03_exposed_api_keys.md)

---

**Classification**:
- **Confirmed** if .git/config accessible publicly
- **Likely** if .git directory in deployment
- **Not Applicable** if .git properly blocked and excluded
