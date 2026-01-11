# Security Check Document Template

Use this template to create new security check documents. Copy this structure and fill in the details for each vulnerability.

```markdown
# [Number]. [Vulnerability Name]

## 🔴 Risk Level: **[CRITICAL/HIGH/MEDIUM/LOW]**

## 📋 Vulnerability Description

[Clear, concise description of the vulnerability and its impact]

## 🎯 Context: Why This Happens

[Explain why AI-generated code often has this issue]

## 🔍 Detection Methods

### 1. Code Analysis

**Search for:**
- [What to look for in code]
- [Libraries/frameworks to check]
- [Configuration files to review]

**Red Flags:**
```[language]
// ❌ VULNERABLE: [Example of vulnerable code]
[code example]

// ✅ SECURE: [Example of secure code]
[code example]
```

### 2. Configuration Review

**Check for:**
- [Configuration items to verify]
- [Settings to review]

### 3. Testing

**Manual Testing:**
```bash
# [Test commands]
```

**Automated Testing:**
```[language]
# [Test script]
```

## ✅ Verification Requirements

### Must Have:
1. **[Requirement 1]**
   - [Detail]
   - [Detail]

2. **[Requirement 2]**
   - [Detail]

## 🚨 Exploit Path

### Scenario 1: [Attack Scenario]
```
1. [Step 1]
2. [Step 2]
3. [Step 3]
...
```

## 🔧 Remediation Steps

### Step 1: [Action]

```[language]
[Code example]
```

### Step 2: [Action]

```[language]
[Code example]
```

## 📝 Code Examples

### ❌ Vulnerable Code

```[language]
[Vulnerable code example]
```

### ✅ Secure Code

```[language]
[Secure code example]
```

## 🧪 Testing Checklist

- [ ] [Test item 1]
- [ ] [Test item 2]
- [ ] [Test item 3]

## 📚 References

- [Reference 1](URL)
- [Reference 2](URL)
- [OWASP: Related Topic](URL)

## 🔗 Related Vulnerabilities

- [Related vulnerability 1](./path)
- [Related vulnerability 2](./path)

---

**Classification**: 
- **Confirmed** if [condition]
- **Likely** if [condition]
- **Not Applicable** if [condition]
```

## Document Structure Guidelines

1. **Risk Level**: Use emoji and text (🔴 CRITICAL, 🟠 HIGH, 🟡 MEDIUM, 🟢 LOW)

2. **Vulnerability Description**: 
   - Start with impact
   - Include statistics if available
   - Mention common scenarios

3. **Context**: 
   - Explain why AI code has this issue
   - Common patterns in generated code

4. **Detection Methods**:
   - Code analysis (what to search for)
   - Configuration review
   - Testing methods (manual and automated)

5. **Verification Requirements**:
   - Must-have items
   - Implementation details
   - Configuration examples

6. **Exploit Path**:
   - Step-by-step attack scenarios
   - Real-world examples

7. **Remediation Steps**:
   - Numbered steps
   - Code examples for each step
   - Multiple framework examples when applicable

8. **Code Examples**:
   - Clear vulnerable vs secure comparison
   - Multiple languages/frameworks when relevant

9. **Testing Checklist**:
   - Actionable test items
   - Can be used as verification

10. **References**:
    - OWASP links
    - Official documentation
    - Security advisories

11. **Related Vulnerabilities**:
    - Link to other checks
    - Show relationships

## Tips for Writing

- **Be specific**: Include exact code patterns
- **Be practical**: Provide working examples
- **Be comprehensive**: Cover all aspects
- **Be actionable**: Steps should be clear
- **Be framework-agnostic**: Show multiple examples when possible
