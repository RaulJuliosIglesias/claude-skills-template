# 33. AI-Induced Race Conditions

## 🟠 Risk Level: **HIGH**

## 📋 Vulnerability Description

Asynchronous payment processing logic lacks proper concurrency controls in generated code. When multiple requests are sent simultaneously, the system processes them in parallel before the first transaction updates the balance, resulting in users being charged multiple times for a single action.

**Impact:**
- Double charging
- Balance manipulation
- Financial loss
- Data inconsistency

## 🎯 Context: Why This Happens

AI-generated async code:
- Doesn't use transactions
- No locking mechanisms
- Processes in parallel
- Doesn't handle concurrency

## 🔍 Detection Methods

### 1. Code Analysis

**Search for:**
- Database transactions
- Locking mechanisms
- Idempotency keys
- Race condition handling

### 2. Testing

**Concurrent requests:**
```bash
# Send same request multiple times simultaneously
for i in {1..10}; do
  curl -X POST https://api.example.com/payment &
done
# If charged 10 times → VULNERABLE
```

## ✅ Verification Requirements

### Must Have:
1. **Database Transactions**
   - ACID compliance
   - Transaction isolation
   - Rollback on error

2. **Idempotency**
   - Idempotency keys
   - Duplicate detection
   - Idempotent operations

## 🚨 Exploit Path

### Scenario 1: Double Charging
```
1. User clicks "Pay" button twice quickly
2. Two requests sent simultaneously
3. Both check balance (same value)
4. Both process payment
5. User charged twice
6. Financial loss
```

## 🔧 Remediation Steps

### Step 1: Use Database Transactions

```javascript
const { sequelize } = require('./models');

app.post('/api/payment', requireAuth, async (req, res) => {
  const transaction = await sequelize.transaction();
  
  try {
    // Lock row for update
    const user = await User.findByPk(req.user.id, {
      lock: transaction.LOCK.UPDATE,
      transaction
    });
    
    // Check balance
    if (user.balance < req.body.amount) {
      await transaction.rollback();
      return res.status(400).json({ error: 'Insufficient balance' });
    }
    
    // Update balance
    await user.update({
      balance: user.balance - req.body.amount
    }, { transaction });
    
    // Create payment record
    await Payment.create({
      userId: user.id,
      amount: req.body.amount
    }, { transaction });
    
    await transaction.commit();
    res.json({ success: true });
  } catch (err) {
    await transaction.rollback();
    res.status(500).json({ error: 'Payment failed' });
  }
});
```

### Step 2: Implement Idempotency

```javascript
app.post('/api/payment', requireAuth, async (req, res) => {
  const idempotencyKey = req.headers['idempotency-key'];
  
  if (!idempotencyKey) {
    return res.status(400).json({ error: 'Idempotency key required' });
  }
  
  // Check if already processed
  const existing = await Payment.findOne({
    where: { idempotencyKey }
  });
  
  if (existing) {
    // Already processed, return same result
    return res.json({ 
      success: true,
      paymentId: existing.id,
      message: 'Duplicate request ignored'
    });
  }
  
  // Process payment
  const transaction = await sequelize.transaction();
  try {
    // ... payment logic ...
    
    await Payment.create({
      idempotencyKey,
      userId: req.user.id,
      amount: req.body.amount
    }, { transaction });
    
    await transaction.commit();
    res.json({ success: true });
  } catch (err) {
    await transaction.rollback();
    throw err;
  }
});
```

## 📝 Code Examples

### ❌ Vulnerable

```javascript
// ❌ VULNERABLE: No transaction
app.post('/api/payment', async (req, res) => {
  const user = await User.findByPk(req.user.id);
  
  if (user.balance < req.body.amount) {
    return res.status(400).json({ error: 'Insufficient balance' });
  }
  
  // ❌ Race condition: Two requests can both pass check
  await user.update({ balance: user.balance - req.body.amount });
  await Payment.create({ amount: req.body.amount });
  
  res.json({ success: true });
});
```

### ✅ Secure

```javascript
// ✅ SECURE: Transaction + idempotency
app.post('/api/payment', requireAuth, async (req, res) => {
  const idempotencyKey = req.headers['idempotency-key'];
  
  // Check duplicate
  const existing = await Payment.findOne({ where: { idempotencyKey } });
  if (existing) {
    return res.json({ success: true, paymentId: existing.id });
  }
  
  const transaction = await sequelize.transaction();
  try {
    // Lock row
    const user = await User.findByPk(req.user.id, {
      lock: transaction.LOCK.UPDATE,
      transaction
    });
    
    if (user.balance < req.body.amount) {
      await transaction.rollback();
      return res.status(400).json({ error: 'Insufficient balance' });
    }
    
    await user.update({
      balance: user.balance - req.body.amount
    }, { transaction });
    
    await Payment.create({
      idempotencyKey,
      userId: user.id,
      amount: req.body.amount
    }, { transaction });
    
    await transaction.commit();
    res.json({ success: true });
  } catch (err) {
    await transaction.rollback();
    throw err;
  }
});
```

## 🧪 Testing Checklist

- [ ] Transactions used for critical operations
- [ ] Row locking implemented
- [ ] Idempotency keys required
- [ ] Duplicate requests handled
- [ ] Concurrent requests tested
- [ ] Race conditions prevented

## 📚 References

- [OWASP: Race Conditions](https://owasp.org/www-community/vulnerabilities/Race_Condition)
- [Database Transactions](https://en.wikipedia.org/wiki/Database_transaction)

## 🔗 Related Vulnerabilities

- [07. Missing Row Level Security](../database_security/07_missing_row_level_security.md)
- [19. Unbounded Payload Processing](../input_validation/19_unbounded_payload_processing.md)

---

**Classification**:
- **Confirmed** if critical operations lack transactions
- **Likely** if idempotency not implemented
- **Not Applicable** if transactions and idempotency used
