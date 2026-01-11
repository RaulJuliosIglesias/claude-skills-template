# 4. Privileged Secrets in Frontend Bundles

## 🔴 Risk Level: **CRITICAL**

## 📋 Vulnerability Description

Developers often confuse "Anon" keys (safe for public) with "Service Role" keys (admin access). High-privilege keys are frequently compiled into minified JavaScript bundles (React/Vue/Next.js), granting full backend access to anyone who inspects the page source or network requests.

**Impact:**
- Complete backend access from client-side
- Database manipulation
- User data access/modification
- Billing manipulation
- Service disruption

## 🎯 Context: Why This Happens

AI code generators often:
- Use service role keys in examples for "quick setup"
- Don't distinguish between public and private keys
- Bundle environment variables without filtering
- Copy-paste backend code to frontend

## 🔍 Detection Methods

### 1. Bundle Analysis

**Inspect built JavaScript:**
```bash
# Search for service role keys in bundle
grep -r "service_role\|serviceRole\|ADMIN_\|SERVICE_" dist/ build/

# Or in browser DevTools
# Sources → Page → static/js → Search for keys
```

**Common patterns:**
- `service_role_key`
- `ADMIN_API_KEY`
- `SERVICE_SECRET`
- Supabase `service_role` keys
- Firebase Admin SDK keys

### 2. Network Inspection

**Check browser DevTools → Network:**
- Look for API keys in request headers
- Check for admin endpoints accessible from frontend
- Verify if service role keys are sent in requests

### 3. Build Configuration Review

**Check build tools:**
- Webpack: `DefinePlugin` configuration
- Vite: `import.meta.env` usage
- Next.js: `NEXT_PUBLIC_` prefix usage
- Environment variable injection

## ✅ Verification Requirements

### Must Have:
1. **No Service Role Keys in Frontend**
   - Only anon/public keys in client code
   - Service role keys only in server-side code
   - Admin operations only via API endpoints

2. **Build Process Protection**
   - Environment variables filtered before bundling
   - Build-time validation of exposed variables
   - Separate configs for client/server

3. **Key Type Verification**
   - Anon keys: Safe for public exposure
   - Service role keys: Never in frontend
   - API keys: Scoped to specific operations

## 🚨 Exploit Path

### Scenario 1: Supabase Service Role Key
```
1. Attacker inspects page source or network tab
2. Finds Supabase service_role key in JavaScript bundle
3. Attacker uses key to access Supabase directly
4. Attacker bypasses all RLS policies (service role ignores RLS)
5. Attacker reads/writes all data
6. Complete database compromise
```

### Scenario 2: Firebase Admin SDK
```
1. Attacker finds Firebase Admin credentials in bundle
2. Attacker uses credentials to access Firebase Admin SDK
3. Attacker can read/write all data
4. Attacker can manage users
5. Attacker can modify security rules
6. Complete Firebase project compromise
```

### Scenario 3: Payment Gateway Admin Key
```
1. Attacker finds Stripe secret key in frontend
2. Attacker uses key to access Stripe API
3. Attacker can create refunds
4. Attacker can access customer data
5. Financial loss and data breach
```

## 🔧 Remediation Steps

### Step 1: Identify Exposed Keys

**Audit your bundles:**
```bash
# Build your app
npm run build

# Search for dangerous patterns
grep -r "service_role\|ADMIN_\|SERVICE_" dist/ build/ .next/

# Check what's exposed in browser
# Open DevTools → Sources → Check bundled JS files
```

### Step 2: Separate Client/Server Keys

**Supabase Example:**
```javascript
// ❌ VULNERABLE: Service role in frontend
const supabase = createClient(
  'https://project.supabase.co',
  'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...' // Service role key!
);

// ✅ SECURE: Anon key in frontend
const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY // Anon key only
);

// ✅ SECURE: Service role only in server
// server/api/admin.js
import { createClient } from '@supabase/supabase-js';

const supabaseAdmin = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY, // Server-side only
  {
    auth: {
      autoRefreshToken: false,
      persistSession: false
    }
  }
);
```

### Step 3: Configure Build Tools

**Next.js:**
```javascript
// next.config.js
module.exports = {
  env: {
    // Only NEXT_PUBLIC_ vars are exposed to browser
    NEXT_PUBLIC_SUPABASE_URL: process.env.NEXT_PUBLIC_SUPABASE_URL,
    NEXT_PUBLIC_SUPABASE_ANON_KEY: process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY,
    // Service role key NOT included - server-only
  },
  // Prevent accidental exposure
  webpack: (config) => {
    // Remove any service role keys
    config.plugins.push(
      new webpack.DefinePlugin({
        'process.env.SUPABASE_SERVICE_ROLE_KEY': JSON.stringify(''),
      })
    );
    return config;
  }
};
```

**Vite:**
```javascript
// vite.config.js
export default {
  define: {
    // Only expose VITE_ prefixed vars
    'import.meta.env.VITE_SUPABASE_URL': JSON.stringify(process.env.VITE_SUPABASE_URL),
    'import.meta.env.VITE_SUPABASE_ANON_KEY': JSON.stringify(process.env.VITE_SUPABASE_ANON_KEY),
    // Service role key NOT included
  },
  // Build-time validation
  build: {
    rollupOptions: {
      output: {
        // Validate no service keys in output
        manualChunks: undefined,
      }
    }
  }
};
```

**Webpack:**
```javascript
// webpack.config.js
const webpack = require('webpack');

module.exports = {
  plugins: [
    new webpack.DefinePlugin({
      // Only expose REACT_APP_ vars
      'process.env.REACT_APP_SUPABASE_URL': JSON.stringify(process.env.REACT_APP_SUPABASE_URL),
      'process.env.REACT_APP_SUPABASE_ANON_KEY': JSON.stringify(process.env.REACT_APP_SUPABASE_ANON_KEY),
      // Explicitly exclude service role
      'process.env.SUPABASE_SERVICE_ROLE_KEY': JSON.stringify(''),
    }),
  ],
};
```

### Step 4: Create API Endpoints for Admin Operations

**Instead of using service role in frontend:**
```javascript
// ❌ VULNERABLE: Direct service role usage in frontend
const { data } = await supabaseAdmin
  .from('users')
  .select('*'); // Bypasses RLS

// ✅ SECURE: Admin operations via API
// Frontend
const response = await fetch('/api/admin/users', {
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${userToken}`
  }
});

// Backend API route
// pages/api/admin/users.js (Next.js)
import { createClient } from '@supabase/supabase-js';

export default async function handler(req, res) {
  // Verify admin role
  const user = await verifyAdmin(req);
  if (!user) {
    return res.status(403).json({ error: 'Forbidden' });
  }
  
  // Use service role only on server
  const supabaseAdmin = createClient(
    process.env.SUPABASE_URL,
    process.env.SUPABASE_SERVICE_ROLE_KEY // Server-side only
  );
  
  const { data, error } = await supabaseAdmin
    .from('users')
    .select('*');
  
  res.json(data);
}
```

### Step 5: Build-Time Validation

**Create validation script:**
```javascript
// scripts/validate-build.js
const fs = require('fs');
const path = require('path');

const DANGEROUS_PATTERNS = [
  /service[_-]?role/i,
  /ADMIN[_-]?KEY/i,
  /SERVICE[_-]?SECRET/i,
  /sk_live_/,
  /serviceAccount/i
];

function scanDirectory(dir) {
  const files = fs.readdirSync(dir);
  
  for (const file of files) {
    const filePath = path.join(dir, file);
    const stat = fs.statSync(filePath);
    
    if (stat.isDirectory()) {
      scanDirectory(filePath);
    } else if (file.endsWith('.js') || file.endsWith('.js.map')) {
      const content = fs.readFileSync(filePath, 'utf8');
      
      for (const pattern of DANGEROUS_PATTERNS) {
        if (pattern.test(content)) {
          console.error(`❌ DANGER: Found ${pattern} in ${filePath}`);
          process.exit(1);
        }
      }
    }
  }
}

// Run after build
const buildDir = path.join(__dirname, '../dist');
if (fs.existsSync(buildDir)) {
  console.log('Scanning build directory...');
  scanDirectory(buildDir);
  console.log('✅ Build validation passed');
}
```

**Add to package.json:**
```json
{
  "scripts": {
    "build": "next build",
    "postbuild": "node scripts/validate-build.js"
  }
}
```

### Step 6: Rotate Exposed Keys

**If keys were exposed:**
```bash
# 1. Immediately rotate all exposed keys
# Supabase: Dashboard → Settings → API → Reset service role key
# Stripe: Dashboard → Developers → API keys → Revoke
# Firebase: Console → Project Settings → Service accounts → Delete key

# 2. Update environment variables
# 3. Redeploy application
# 4. Monitor for unauthorized access
```

## 📝 Code Examples

### ❌ Vulnerable Code

```javascript
// Frontend code - VULNERABLE
// .env.local
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

// Component
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY // ❌ Exposed in bundle!
);

// This bypasses all RLS policies
const { data } = await supabase
  .from('users')
  .select('*');
```

### ✅ Secure Code

```javascript
// Frontend - Only anon key
// .env.local
NEXT_PUBLIC_SUPABASE_URL=https://project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9... // Anon key

// Component
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY // ✅ Safe for public
);

// RLS policies apply
const { data } = await supabase
  .from('users')
  .select('*')
  .eq('id', userId); // User can only see their own data

// Server-side API route for admin operations
// pages/api/admin/users.js
import { createClient } from '@supabase/supabase-js';

export default async function handler(req, res) {
  // Verify admin
  const user = await verifyAdmin(req);
  if (!user || user.role !== 'admin') {
    return res.status(403).json({ error: 'Forbidden' });
  }
  
  // Service role only on server
  const supabaseAdmin = createClient(
    process.env.SUPABASE_URL,
    process.env.SUPABASE_SERVICE_ROLE_KEY // ✅ Server-side only
  );
  
  const { data } = await supabaseAdmin
    .from('users')
    .select('*');
  
  res.json(data);
}
```

## 🧪 Testing Checklist

- [ ] No service role keys found in built bundles
- [ ] Only anon/public keys in frontend code
- [ ] Build validation script passes
- [ ] Admin operations only via API endpoints
- [ ] Service role keys only in server-side code
- [ ] Environment variables properly prefixed (NEXT_PUBLIC_, VITE_, REACT_APP_)
- [ ] Network tab shows no admin keys in requests
- [ ] Source maps don't expose keys
- [ ] Documentation explains key types

## 📚 References

- [Supabase: API Keys](https://supabase.com/docs/guides/api/api-keys)
- [Firebase: Service Accounts](https://firebase.google.com/docs/admin/setup)
- [Next.js: Environment Variables](https://nextjs.org/docs/basic-features/environment-variables)
- [OWASP: Client-Side Storage](https://cheatsheetseries.owasp.org/cheatsheets/HTML5_Security_Cheat_Sheet.html)

## 🔗 Related Vulnerabilities

- [03. Exposed API Keys in Repos](./03_exposed_api_keys.md)
- [14. Leaked Secrets in Git History](./14_leaked_secrets_git.md)
- [25. Insecure Session Storage](./25_insecure_session_storage.md)

---

**Classification**:
- **Confirmed** if service role keys found in frontend bundles
- **Likely** if admin operations performed directly from frontend
- **Not Applicable** if using proper key separation and API endpoints
