# 11. Debug Mode Enabled in Production

## 🟠 Risk Level: **HIGH**

## 📋 Vulnerability Description

AI tools prioritize developer experience, often generating configuration files with `DEBUG=True` (Flask/Django) or `NODE_ENV=development`. Deploying with these flags exposes interactive debuggers, verbose stack traces, and environment variables to the public internet whenever an error occurs.

**Impact:**
- Interactive debugger exposed
- Environment variables leaked
- Source code exposed
- Internal paths revealed
- Attack surface increased

## 🎯 Context: Why This Happens

AI code generators:
- Default to development settings
- Include debug mode for easier development
- Don't distinguish dev/prod configurations
- Copy example configs without modification

## 🔍 Detection Methods

### 1. Configuration Review

**Check environment variables:**
```bash
# Check for debug flags
grep -r "DEBUG.*=.*True\|NODE_ENV.*development" .
grep -r "debug.*true" . -i
```

**Common patterns:**
- `DEBUG=True` (Flask/Django)
- `NODE_ENV=development`
- `debug: true` (config files)

### 2. Testing

**Trigger error and check response:**
```bash
# Cause an error
curl https://api.example.com/invalid-endpoint

# Check if response contains:
# - Interactive debugger (Werkzeug, etc.)
# - Stack traces with file paths
# - Environment variables
# - Source code snippets
```

## ✅ Verification Requirements

### Must Have:
1. **Debug Mode Disabled in Production**
   - `DEBUG=False` or not set
   - `NODE_ENV=production`
   - No debug middleware enabled

2. **Generic Error Pages**
   - Static 500 error page
   - No stack traces
   - No environment information

3. **Environment Separation**
   - Separate configs for dev/prod
   - Environment variables properly set
   - No debug tools in production

## 🚨 Exploit Path

### Scenario 1: Interactive Debugger
```
1. Attacker triggers error on production
2. Server returns Werkzeug debugger page
3. Attacker can execute Python code
4. Attacker gains shell access
5. Server compromised
```

### Scenario 2: Environment Variable Leakage
```
1. Attacker triggers error
2. Error page shows environment variables
3. Attacker sees database credentials
4. Attacker sees API keys
5. Attacker gains database access
```

## 🔧 Remediation Steps

### Step 1: Disable Debug Mode

**Flask:**
```python
# config.py
import os

class Config:
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    # Never True in production

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True

# app.py
import os
from config import ProductionConfig, DevelopmentConfig

env = os.getenv('FLASK_ENV', 'production')
config = ProductionConfig if env == 'production' else DevelopmentConfig
app.config.from_object(config)
```

**Django:**
```python
# settings.py
import os

DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# Never allow debug in production
if DEBUG:
    ALLOWED_HOSTS = ['*']  # Development
else:
    ALLOWED_HOSTS = ['yourdomain.com']  # Production
```

**Node.js/Express:**
```javascript
// .env.production
NODE_ENV=production
DEBUG=

// app.js
if (process.env.NODE_ENV === 'production') {
  // Disable debug
  delete process.env.DEBUG;
  
  // Use production error handler
  app.use(productionErrorHandler);
} else {
  // Development error handler with details
  app.use(developmentErrorHandler);
}
```

### Step 2: Create Production Error Handler

**Express:**
```javascript
// middleware/errorHandler.js
function productionErrorHandler(err, req, res, next) {
  // Log error server-side
  console.error('Error:', err);
  
  // Send generic message
  res.status(500).json({
    error: 'An unexpected error occurred'
  });
}

function developmentErrorHandler(err, req, res, next) {
  // Detailed error in development
  res.status(500).json({
    error: err.message,
    stack: err.stack
  });
}

// Use based on environment
if (process.env.NODE_ENV === 'production') {
  app.use(productionErrorHandler);
} else {
  app.use(developmentErrorHandler);
}
```

**Flask:**
```python
# app.py
@app.errorhandler(500)
def internal_error(error):
    if app.config['DEBUG']:
        # Development: show details
        return str(error), 500
    else:
        # Production: generic message
        return render_template('500.html'), 500
```

### Step 3: Use Static Error Pages

**Nginx:**
```nginx
error_page 500 502 503 504 /50x.html;
location = /50x.html {
    root /var/www/static;
    internal;
}
```

**Express:**
```javascript
// Serve static error page
app.use((err, req, res, next) => {
  if (process.env.NODE_ENV === 'production') {
    return res.status(500).sendFile(path.join(__dirname, 'public/500.html'));
  }
  next(err);
});
```

### Step 4: Environment Variable Validation

```javascript
// startup.js
function validateEnvironment() {
  const required = ['DATABASE_URL', 'JWT_SECRET'];
  const missing = required.filter(key => !process.env[key]);
  
  if (missing.length > 0) {
    throw new Error(`Missing environment variables: ${missing.join(', ')}`);
  }
  
  // Warn if debug enabled in production
  if (process.env.NODE_ENV === 'production' && process.env.DEBUG) {
    console.warn('WARNING: DEBUG is enabled in production!');
  }
  
  // Force production mode
  if (process.env.NODE_ENV !== 'production') {
    process.env.NODE_ENV = 'production';
  }
}

validateEnvironment();
```

## 📝 Code Examples

### ❌ Vulnerable Code

```python
# ❌ VULNERABLE: Debug enabled
# config.py
DEBUG = True  # ❌ Always enabled

# app.py
if __name__ == '__main__':
    app.run(debug=True)  # ❌ Debug mode
```

```javascript
// ❌ VULNERABLE: Development mode
// .env
NODE_ENV=development  # ❌ In production

// app.js
if (process.env.NODE_ENV === 'development') {
  app.use(errorHandler); // ❌ Shows stack traces
}
```

### ✅ Secure Code

```python
# ✅ SECURE: Environment-based config
# config.py
import os

DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# Never True in production
if os.getenv('ENVIRONMENT') == 'production':
    DEBUG = False

# app.py
if __name__ == '__main__':
    app.run(debug=DEBUG)  # ✅ Based on environment
```

```javascript
// ✅ SECURE: Production mode
// .env.production
NODE_ENV=production
DEBUG=

// app.js
if (process.env.NODE_ENV === 'production') {
  // Generic error handler
  app.use((err, req, res, next) => {
    console.error('Error:', err);
    res.status(500).json({ error: 'An unexpected error occurred' });
  });
} else {
  // Detailed errors in development
  app.use((err, req, res, next) => {
    res.status(500).json({
      error: err.message,
      stack: err.stack
    });
  });
}
```

## 🧪 Testing Checklist

- [ ] DEBUG=False in production
- [ ] NODE_ENV=production set
- [ ] No interactive debuggers enabled
- [ ] Generic error pages served
- [ ] No stack traces in production
- [ ] No environment variables exposed
- [ ] Error logging works server-side
- [ ] Static 500 page configured
- [ ] Environment validation on startup

## 📚 References

- [OWASP: Information Exposure](https://owasp.org/www-community/vulnerabilities/Information_exposure)
- [Flask Debug Mode](https://flask.palletsprojects.com/en/2.3.x/debugging/)
- [Django DEBUG Setting](https://docs.djangoproject.com/en/stable/ref/settings/#debug)

## 🔗 Related Vulnerabilities

- [09. Verbose Error Information Leakage](../code_security/09_verbose_error_leakage.md)
- [08. Shared Environment Infrastructure](./08_shared_environment_infrastructure.md)
- [42. Sensitive Data Exposure in Logs](../data_protection/42_sensitive_data_in_logs.md)

---

**Classification**:
- **Confirmed** if DEBUG=True or NODE_ENV=development in production
- **Likely** if error pages show detailed information
- **Not Applicable** if debug disabled and generic errors shown
