# 37. Public Cloud Storage Buckets

## 🟠 Risk Level: **HIGH**

## 📋 Vulnerability Description

Vibe-coded apps using Firebase Storage or AWS S3 often leave buckets with default "public read" permissions to avoid dealing with signed URLs during development. This exposes all user uploads—including ID cards, private photos, and invoices—to anyone who can guess the bucket URL or use a scanner.

**Impact:**
- Private data exposure
- Unauthorized file access
- Privacy violations
- Data breach

## 🎯 Context: Why This Happens

AI-generated code:
- Uses public buckets for "easy access"
- Doesn't configure permissions
- Skips signed URL implementation
- Focuses on functionality

## 🔍 Detection Methods

### 1. Configuration Review

**Check bucket policies:**
- AWS S3: Public access settings
- Firebase: Storage rules
- Google Cloud: IAM policies

### 2. Testing

```bash
# Test if bucket is public
curl https://bucket-name.s3.amazonaws.com/file.jpg
# If accessible without auth → VULNERABLE
```

## ✅ Verification Requirements

### Must Have:
1. **Private Buckets**
   - Public access disabled
   - Signed URLs for access
   - Time-limited URLs

2. **Access Control**
   - User-specific access
   - Authentication required
   - Proper IAM policies

## 🚨 Exploit Path

### Scenario 1: Private Photo Exposure
```
1. User uploads private photo
2. Bucket is public
3. Attacker guesses URL pattern
4. Attacker accesses all photos
5. Private data exposed
```

## 🔧 Remediation Steps

### Step 1: Disable Public Access

**AWS S3:**
```javascript
// Disable public access
const s3 = new AWS.S3();

await s3.putBucketPublicAccessBlock({
  Bucket: 'my-bucket',
  PublicAccessBlockConfiguration: {
    BlockPublicAcls: true,
    IgnorePublicAcls: true,
    BlockPublicPolicy: true,
    RestrictPublicBuckets: true
  }
}).promise();
```

### Step 2: Use Signed URLs

```javascript
const AWS = require('aws-sdk');
const s3 = new AWS.S3();

// Generate signed URL (time-limited)
function generateSignedUrl(key, expiresIn = 3600) {
  return s3.getSignedUrl('getObject', {
    Bucket: 'my-bucket',
    Key: key,
    Expires: expiresIn // 1 hour
  });
}

app.get('/api/files/:id', requireAuth, async (req, res) => {
  const file = await File.findByPk(req.params.id);
  
  // Verify ownership
  if (file.userId !== req.user.id) {
    return res.status(403).json({ error: 'Forbidden' });
  }
  
  // Generate signed URL
  const url = generateSignedUrl(file.s3Key, 3600);
  res.json({ url });
});
```

### Step 3: Configure Bucket Policy

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Deny",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::my-bucket/*",
      "Condition": {
        "Bool": {
          "aws:PublicAccess": "true"
        }
      }
    }
  ]
}
```

## 📝 Code Examples

### ❌ Vulnerable

```javascript
// ❌ VULNERABLE: Public bucket
const url = `https://my-bucket.s3.amazonaws.com/${fileKey}`;
// Anyone can access
```

### ✅ Secure

```javascript
// ✅ SECURE: Signed URLs
const url = s3.getSignedUrl('getObject', {
  Bucket: 'my-bucket',
  Key: fileKey,
  Expires: 3600
});
// Time-limited, authenticated access
```

## 🧪 Testing Checklist

- [ ] Public access disabled
- [ ] Signed URLs used
- [ ] Access control configured
- [ ] URLs time-limited
- [ ] Ownership verified
- [ ] Bucket policy restrictive

## 📚 References

- [AWS S3 Security](https://docs.aws.amazon.com/AmazonS3/latest/userguide/security.html)
- [Firebase Storage Security](https://firebase.google.com/docs/storage/security)

## 🔗 Related Vulnerabilities

- [16. Unrestricted File Uploads](../input_validation/16_unrestricted_file_uploads.md)
- [07. Missing Row Level Security](../database_security/07_missing_row_level_security.md)

---

**Classification**:
- **Confirmed** if bucket publicly accessible
- **Likely** if public access not explicitly disabled
- **Not Applicable** if private with signed URLs
