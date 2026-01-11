# 45. Insecure Object Deserialization

## 🔴 Risk Level: **CRITICAL**

## 📋 Vulnerability Description

When generating Python or Java networking code (like multiplayer games), AI models often default to using `pickle` or `ObjectInputStream` for easy data transfer. These formats are inherently unsafe; an attacker can send a malicious serialized object that executes arbitrary code (RCE) on the server immediately upon unpacking.

**Impact:**
- Remote Code Execution
- Server compromise
- Data corruption
- Complete system access

## 🎯 Context: Why This Happens

AI-generated code:
- Uses pickle for "easy" serialization
- Doesn't understand security risks
- Uses native serialization
- Doesn't validate input

## 🔍 Detection Methods

### 1. Code Analysis

**Search for:**
```python
# ❌ VULNERABLE
pickle.loads(data)
pickle.load(file)

# Java
ObjectInputStream
readObject()
```

### 2. Testing

**Send malicious pickle:**
```python
import pickle
import os

class RCE:
    def __reduce__(self):
        return (os.system, ('rm -rf /',))

malicious = pickle.dumps(RCE())
# Send to server
```

## ✅ Verification Requirements

### Must Have:
1. **Safe Serialization**
   - Use JSON, Protobuf, MessagePack
   - Never use pickle for untrusted data
   - Validate before deserializing

2. **Input Validation**
   - Verify data format
   - Check signatures if needed
   - Whitelist allowed types

## 🚨 Exploit Path

### Scenario 1: RCE via Pickle
```
1. Attacker creates malicious pickle
2. Attacker sends to server
3. Server deserializes with pickle.loads()
4. Malicious code executes
5. Server compromised
```

## 🔧 Remediation Steps

### Step 1: Use JSON Instead

```python
# ❌ VULNERABLE
import pickle

data = pickle.loads(request.data) # ❌ Dangerous

# ✅ SECURE
import json

data = json.loads(request.data) # ✅ Safe
```

### Step 2: Use Protobuf

```python
# ✅ SECURE: Protobuf
import protobuf

# Define schema
message User {
  string name = 1;
  int32 age = 2;
}

# Serialize/deserialize
user = User()
user.ParseFromString(request.data) # ✅ Safe
```

### Step 3: Validate Before Deserializing

```python
import json
import jsonschema

schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "integer"}
    }
}

def safe_deserialize(data):
    try:
        obj = json.loads(data)
        jsonschema.validate(obj, schema) # ✅ Validate schema
        return obj
    except (json.JSONDecodeError, jsonschema.ValidationError):
        raise ValueError("Invalid data")
```

## 📝 Code Examples

### ❌ Vulnerable

```python
# ❌ VULNERABLE: Pickle
import pickle

@app.route('/api/data', methods=['POST'])
def receive_data():
    data = pickle.loads(request.data) # ❌ RCE risk
    return process(data)
```

### ✅ Secure

```python
# ✅ SECURE: JSON
import json
import jsonschema

schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "integer"}
    }
}

@app.route('/api/data', methods=['POST'])
def receive_data():
    try:
        obj = json.loads(request.data)
        jsonschema.validate(obj, schema)
        return process(obj)
    except (json.JSONDecodeError, jsonschema.ValidationError):
        return {"error": "Invalid data"}, 400
```

## 🧪 Testing Checklist

- [ ] No pickle for untrusted data
- [ ] JSON or safe format used
- [ ] Schema validation implemented
- [ ] Input validated before deserializing
- [ ] No ObjectInputStream in Java
- [ ] Safe serialization libraries used

## 📚 References

- [OWASP: Deserialization](https://owasp.org/www-community/vulnerabilities/Deserialization_of_untrusted_data)
- [CWE-502: Deserialization](https://cwe.mitre.org/data/definitions/502.html)

## 🔗 Related Vulnerabilities

- [10. Client-Side Input Validation Only](../input_validation/10_client_side_validation_only.md)
- [24. Prototype Pollution](../input_validation/24_prototype_pollution.md)

---

**Classification**:
- **Confirmed** if pickle/ObjectInputStream used for untrusted data
- **Likely** if deserialization not validated
- **Not Applicable** if safe formats with validation used
