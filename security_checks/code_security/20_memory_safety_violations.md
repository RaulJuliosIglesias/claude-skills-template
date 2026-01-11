# 20. Memory Safety Violations (Buffer Overflow)

## 🔴 Risk Level: **CRITICAL**

## 📋 Vulnerability Description

When vibe coding in C/C++ (e.g., parsing binary files like GGUF), AI often generates code using `malloc` and `memcpy` without strict bounds checking. It frequently misses integer overflows (e.g., `size + 1` wrapping to 0), allowing attackers to crash the app or overwrite memory to execute code.

**Impact:**
- Remote Code Execution
- Application crash
- Memory corruption
- System compromise

## 🎯 Context: Why This Happens

AI-generated C/C++ code:
- Uses unsafe functions
- Doesn't check bounds
- Misses integer overflows
- Doesn't use safe alternatives

## 🔍 Detection Methods

### 1. Code Analysis

**Search for:**
```c
// ❌ VULNERABLE patterns
strcpy(dest, src)
sprintf(buffer, ...)
malloc(size + 1) // Integer overflow risk
memcpy(dest, src, size) // No bounds check
```

### 2. Static Analysis

**Tools:**
- Valgrind
- AddressSanitizer
- Static analyzers

## ✅ Verification Requirements

### Must Have:
1. **Safe Functions**
   - strncpy instead of strcpy
   - snprintf instead of sprintf
   - Bounds checking
   - Integer overflow protection

2. **Modern C++**
   - Smart pointers
   - std::vector
   - RAII patterns

## 🚨 Exploit Path

### Scenario 1: Buffer Overflow
```
1. Attacker sends oversized input
2. Code uses strcpy without bounds
3. Buffer overflows
4. Memory corrupted
5. Code execution possible
```

## 🔧 Remediation Steps

### Step 1: Use Safe Functions

```c
// ❌ VULNERABLE
char buffer[100];
strcpy(buffer, user_input); // No bounds check

// ✅ SECURE
char buffer[100];
strncpy(buffer, user_input, sizeof(buffer) - 1);
buffer[sizeof(buffer) - 1] = '\0'; // Ensure null terminator
```

### Step 2: Use Modern C++

```cpp
// ✅ SECURE: Use std::vector
#include <vector>
#include <string>

std::vector<char> buffer(100);
std::string input = get_user_input();
if (input.length() < buffer.size()) {
  std::copy(input.begin(), input.end(), buffer.begin());
}
```

### Step 3: Bounds Checking

```c
void safe_copy(char *dest, size_t dest_size, const char *src) {
  if (dest_size == 0) return;
  
  size_t src_len = strlen(src);
  size_t copy_len = (src_len < dest_size - 1) ? src_len : dest_size - 1;
  
  memcpy(dest, src, copy_len);
  dest[copy_len] = '\0';
}
```

## 📝 Code Examples

### ❌ Vulnerable

```c
// ❌ VULNERABLE: No bounds check
void process_input(char *input) {
  char buffer[100];
  strcpy(buffer, input); // ❌ Buffer overflow
}
```

### ✅ Secure

```c
// ✅ SECURE: Bounds checked
void process_input(char *input) {
  char buffer[100];
  strncpy(buffer, input, sizeof(buffer) - 1);
  buffer[sizeof(buffer) - 1] = '\0';
}
```

## 🧪 Testing Checklist

- [ ] No unsafe string functions
- [ ] Bounds checking implemented
- [ ] Integer overflow protection
- [ ] Static analysis passed
- [ ] Memory sanitizers used
- [ ] Modern C++ patterns

## 📚 References

- [OWASP: Buffer Overflow](https://owasp.org/www-community/vulnerabilities/Buffer_Overflow)
- [CWE-120: Buffer Overflow](https://cwe.mitre.org/data/definitions/120.html)

## 🔗 Related Vulnerabilities

- [19. Unbounded Payload Processing](../input_validation/19_unbounded_payload_processing.md)
- [10. Client-Side Input Validation Only](../input_validation/10_client_side_validation_only.md)

---

**Classification**:
- **Confirmed** if unsafe functions used without bounds
- **Likely** if bounds checking incomplete
- **Not Applicable** if safe functions and modern patterns used
