# 30. Overprivileged Container Execution

## 🟠 Risk Level: **HIGH**

## 📋 Vulnerability Description

AI-generated Dockerfiles almost always default to running the application as the `root` user. If an attacker manages to compromise the application (via RCE), they immediately inherit root privileges within the container, making it significantly easier to break out to the host system or modify system-level configurations.

**Impact:**
- Container escape
- Host system compromise
- System-level modifications
- Increased attack surface

## 🎯 Context: Why This Happens

AI-generated Dockerfiles:
- Default to root user
- Don't create non-root users
- Focus on "making it work"
- Don't consider security implications

## 🔍 Detection Methods

### 1. Dockerfile Review

**Check for:**
```dockerfile
# ❌ VULNERABLE: Runs as root
FROM node:18
# No USER directive

# ✅ SECURE: Non-root user
FROM node:18
USER node
```

### 2. Container Inspection

```bash
# Check running user
docker exec container id
# If returns 0 (root) → VULNERABLE
```

## ✅ Verification Requirements

### Must Have:
1. **Non-Root User**
   - Create dedicated user
   - Switch to user before CMD
   - Minimal permissions

2. **Read-Only Filesystem**
   - Mount only writable directories
   - Restrict write permissions

## 🚨 Exploit Path

### Scenario 1: Container Escape
```
1. Attacker gains RCE in app
2. App runs as root
3. Attacker modifies container config
4. Attacker escapes to host
5. Host system compromised
```

## 🔧 Remediation Steps

### Step 1: Create Non-Root User

```dockerfile
# ✅ SECURE: Non-root user
FROM node:18-alpine

# Create app user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

# Create app directory
WORKDIR /app

# Copy files
COPY --chown=nodejs:nodejs . .

# Switch to non-root user
USER nodejs

# Run as non-root
CMD ["node", "index.js"]
```

### Step 2: Minimal Permissions

```dockerfile
FROM node:18-alpine

# Create user with minimal permissions
RUN addgroup -g 1001 -S appgroup && \
    adduser -S appuser -u 1001 -G appgroup

WORKDIR /app

# Only give write access to needed directories
RUN mkdir -p /app/uploads /app/logs && \
    chown -R appuser:appgroup /app/uploads /app/logs

USER appuser

CMD ["node", "index.js"]
```

### Step 3: Read-Only Root

```dockerfile
FROM node:18-alpine

USER nodejs

# Run with read-only root
docker run --read-only \
  --tmpfs /tmp \
  --tmpfs /app/uploads \
  your-image
```

## 📝 Code Examples

### ❌ Vulnerable

```dockerfile
# ❌ VULNERABLE: Runs as root
FROM node:18
WORKDIR /app
COPY . .
RUN npm install
CMD ["node", "index.js"]
# Runs as root (uid 0)
```

### ✅ Secure

```dockerfile
# ✅ SECURE: Non-root user
FROM node:18-alpine

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

WORKDIR /app

# Copy with correct ownership
COPY --chown=nodejs:nodejs . .

# Install as non-root
USER nodejs
RUN npm install

# Run as non-root
CMD ["node", "index.js"]
```

## 🧪 Testing Checklist

- [ ] Container runs as non-root
- [ ] USER directive in Dockerfile
- [ ] Minimal permissions granted
- [ ] Read-only filesystem where possible
- [ ] Only necessary directories writable

## 📚 References

- [Docker Security Best Practices](https://docs.docker.com/develop/security-best-practices/)
- [OWASP: Container Security](https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html)

## 🔗 Related Vulnerabilities

- [20. Memory Safety Violations](../code_security/20_memory_safety_violations.md)
- [44. Insecure Infrastructure as Code](./44_insecure_iac.md)

---

**Classification**:
- **Confirmed** if container runs as root
- **Likely** if user has excessive permissions
- **Not Applicable** if non-root user with minimal permissions
