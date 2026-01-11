# 18. Publicly Exposed Database Port

## 🔴 Risk Level: **CRITICAL**

## 📋 Vulnerability Description

To make it easier for local AI tools or external dashboards to connect to the database, vibe coders often configure the database service to listen on `0.0.0.0` and open port 5432 (Postgres) or 3306 (MySQL) to the entire internet. This exposes the database to immediate brute-force attacks and zero-day exploits.

**Impact:**
- Direct database access
- Brute force attacks
- Data breach
- Complete database compromise

## 🎯 Context: Why This Happens

AI-generated configs:
- Default to 0.0.0.0 for "easy access"
- Don't restrict network access
- Expose ports for "convenience"
- Don't use VPCs or private networks

## 🔍 Detection Methods

### 1. Configuration Review

**Check database config:**
```bash
# PostgreSQL
grep -r "listen_addresses.*0.0.0.0" .
grep -r "host.*all.*all.*0.0.0.0" .

# MySQL
grep -r "bind-address.*0.0.0.0" .
```

### 2. Network Testing

```bash
# Test if port is open
nmap -p 5432 your-server-ip
# If open → VULNERABLE
```

## ✅ Verification Requirements

### Must Have:
1. **Database Not Public**
   - Ports closed to internet
   - Only accessible via VPN/SSH
   - VPC/private network used

2. **Access Control**
   - IP whitelisting
   - VPN required
   - SSH tunnel for remote access

## 🚨 Exploit Path

### Scenario 1: Brute Force Attack
```
1. Attacker scans for open database ports
2. Finds PostgreSQL on port 5432
3. Attacker brute forces credentials
4. Gains database access
5. Extracts all data
6. Database compromised
```

## 🔧 Remediation Steps

### Step 1: Restrict Database Access

**PostgreSQL:**
```conf
# postgresql.conf
listen_addresses = 'localhost'  # Not 0.0.0.0

# pg_hba.conf
# Only allow local connections
host    all    all    127.0.0.1/32    md5
# Reject all other connections
host    all    all    0.0.0.0/0       reject
```

**MySQL:**
```conf
# my.cnf
bind-address = 127.0.0.1  # Not 0.0.0.0
```

### Step 2: Use VPC/Private Network

**AWS RDS:**
- Create in private subnet
- No public accessibility
- Access via VPN or bastion host

**Docker:**
```yaml
# docker-compose.yml
services:
  postgres:
    ports:
      # ❌ VULNERABLE: Exposes to host
      # - "5432:5432"
      
      # ✅ SECURE: Internal network only
    networks:
      - internal
```

### Step 3: SSH Tunnel for Remote Access

```bash
# Create SSH tunnel
ssh -L 5432:localhost:5432 user@server

# Connect through tunnel
psql -h localhost -p 5432 -U user -d database
```

## 📝 Code Examples

### ❌ Vulnerable

```conf
# ❌ VULNERABLE: PostgreSQL
listen_addresses = '0.0.0.0'  # Listens on all interfaces
port = 5432

# pg_hba.conf
host    all    all    0.0.0.0/0    md5  # Allows all IPs
```

### ✅ Secure

```conf
# ✅ SECURE: PostgreSQL
listen_addresses = 'localhost'  # Only local
port = 5432

# pg_hba.conf
host    all    all    127.0.0.1/32    md5  # Only localhost
host    all    all    0.0.0.0/0       reject  # Reject all others
```

## 🧪 Testing Checklist

- [ ] Database port not accessible from internet
- [ ] listen_addresses = localhost only
- [ ] Firewall blocks database ports
- [ ] VPC/private network configured
- [ ] SSH tunnel required for remote access
- [ ] No public IP on database instance

## 📚 References

- [OWASP: Security Misconfiguration](https://owasp.org/www-project-top-ten/)
- [PostgreSQL Security](https://www.postgresql.org/docs/current/auth-pg-hba-conf.html)

## 🔗 Related Vulnerabilities

- [08. Shared Environment Infrastructure](./08_shared_environment_infrastructure.md)
- [44. Insecure Infrastructure as Code](./44_insecure_iac.md)

---

**Classification**:
- **Confirmed** if database port open to 0.0.0.0
- **Likely** if port accessible from internet
- **Not Applicable** if database in private network/VPC
