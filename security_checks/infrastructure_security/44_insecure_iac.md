# 44. Insecure Infrastructure as Code (IaC)

## 🟠 Risk Level: **HIGH**

## 📋 Vulnerability Description

When generating Terraform or CloudFormation scripts, AI models tend to prioritize "making it work" over security. This results in Security Groups allowing `0.0.0.0/0` (open to the world) ingress rules, or IAM Roles granted `AdministratorAccess` wildcard permissions, significantly increasing the blast radius of a breach.

**Impact:**
- Overly permissive access
- Increased attack surface
- Privilege escalation risk
- Resource exposure

## 🎯 Context: Why This Happens

AI-generated IaC:
- Uses wildcard permissions
- Opens ports to 0.0.0.0/0
- Grants admin access
- Focuses on functionality

## 🔍 Detection Methods

### 1. Code Analysis

**Search for:**
```hcl
# ❌ VULNERABLE
cidr_blocks = ["0.0.0.0/0"]
"Effect": "Allow",
"Action": "*",
"Resource": "*"
```

### 2. Infrastructure Review

**Check:**
- Security group rules
- IAM policies
- Network ACLs
- Resource permissions

## ✅ Verification Requirements

### Must Have:
1. **Least Privilege**
   - Specific permissions only
   - No wildcards
   - Minimal required access

2. **Network Security**
   - Specific IP ranges
   - No 0.0.0.0/0
   - VPN/private networks

## 🚨 Exploit Path

### Scenario 1: Overly Permissive IAM
```
1. Attacker compromises service
2. Service has AdministratorAccess
3. Attacker can access all resources
4. Complete cloud account compromise
```

## 🔧 Remediation Steps

### Step 1: Restrict Security Groups

```hcl
# ❌ VULNERABLE
resource "aws_security_group" "web" {
  ingress {
    from_port = 80
    to_port = 80
    cidr_blocks = ["0.0.0.0/0"] # ❌ Open to world
  }
}

# ✅ SECURE
resource "aws_security_group" "web" {
  ingress {
    from_port = 80
    to_port = 80
    cidr_blocks = ["10.0.0.0/8"] # ✅ Specific range
  }
  
  ingress {
    from_port = 443
    to_port = 443
    cidr_blocks = ["10.0.0.0/8"] # ✅ HTTPS only from internal
  }
}
```

### Step 2: Least Privilege IAM

```hcl
# ❌ VULNERABLE
resource "aws_iam_role_policy" "lambda" {
  policy = jsonencode({
    Effect = "Allow"
    Action = "*" # ❌ All actions
    Resource = "*" # ❌ All resources
  })
}

# ✅ SECURE
resource "aws_iam_role_policy" "lambda" {
  policy = jsonencode({
    Effect = "Allow"
    Action = [
      "s3:GetObject",
      "s3:PutObject"
    ] # ✅ Specific actions
    Resource = "arn:aws:s3:::my-bucket/*" # ✅ Specific resource
  })
}
```

### Step 3: Use Separate Accounts

```hcl
# ✅ SECURE: Separate accounts
provider "aws" {
  alias = "production"
  # Production account
}

provider "aws" {
  alias = "development"
  # Development account
}
```

## 📝 Code Examples

### ❌ Vulnerable

```hcl
# ❌ VULNERABLE: Open to world
resource "aws_security_group" "web" {
  ingress {
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_iam_role" "lambda" {
  assume_role_policy = jsonencode({
    Action = "*"
    Resource = "*"
  })
}
```

### ✅ Secure

```hcl
# ✅ SECURE: Restricted
resource "aws_security_group" "web" {
  ingress {
    cidr_blocks = ["10.0.0.0/8"]
  }
}

resource "aws_iam_role" "lambda" {
  assume_role_policy = jsonencode({
    Action = ["s3:GetObject"]
    Resource = "arn:aws:s3:::my-bucket/*"
  })
}
```

## 🧪 Testing Checklist

- [ ] No 0.0.0.0/0 in security groups
- [ ] Specific IP ranges used
- [ ] IAM policies use least privilege
- [ ] No wildcard permissions
- [ ] Resources properly scoped
- [ ] Separate accounts for environments

## 📚 References

- [OWASP: Cloud Security](https://owasp.org/www-project-cloud-security/)
- [AWS Security Best Practices](https://docs.aws.amazon.com/security/)

## 🔗 Related Vulnerabilities

- [18. Publicly Exposed Database](./18_publicly_exposed_database.md)
- [08. Shared Environment Infrastructure](./08_shared_environment_infrastructure.md)

---

**Classification**:
- **Confirmed** if wildcard permissions or 0.0.0.0/0 found
- **Likely** if permissions too broad
- **Not Applicable** if least privilege properly implemented
