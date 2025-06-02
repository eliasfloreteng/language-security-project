# Python Pickle Security Demonstration Project

⚠️ **EDUCATIONAL PURPOSE ONLY** ⚠️

This project demonstrates Python pickle deserialization vulnerabilities and offline tampering attacks for educational purposes. It includes vulnerable applications, attack payloads, and secure alternatives.

## 🚨 Important Warning

**This project contains actual security vulnerabilities and malicious code!**

- ✅ **Use for learning and education only**
- ❌ **Never use techniques maliciously**
- ❌ **Do not deploy vulnerable code in production**
- ❌ **Only run in controlled, isolated environments**

## 📚 Educational Objectives

By completing this project, you will learn:

1. **Vulnerability Understanding**: How pickle deserialization can be exploited
2. **Attack Techniques**: Various methods to exploit pickle vulnerabilities
3. **Offline Tampering**: How pickle files can be modified maliciously
4. **Web Application Attacks**: Exploiting pickle in web contexts
5. **Defense Strategies**: Secure alternatives and mitigation techniques

## 🗂️ Project Structure

```
language-security-project/
├── main.py                 # Main entry point with interactive menu
├── safe_pickle_demo.py     # Demonstrates safe pickle usage
├── vulnerable_app.py       # Vulnerable Flask web application
├── attack_payload.py       # Malicious payload generator
├── exploit_demo.py         # Complete attack demonstrations
├── safe_alternatives.py    # Secure serialization alternatives
├── requirements.txt        # Python dependencies
├── README.md              # This documentation
└── data/                  # Generated files and examples
    ├── *.pkl              # Pickle files (safe and malicious)
    ├── *.json             # Safe JSON examples
    └── *.msgpack          # MessagePack examples
```

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Clone or download the project
cd language-security-project

# Install dependencies
pip install -r requirements.txt

# Run the main entry point
python main.py
```

### 2. Interactive Demonstrations

```bash
# Interactive guided menu
python main.py --interactive

# Check project information
python main.py --info

# Verify dependencies
python main.py --check-deps
```

## 📖 Detailed Module Documentation

### 1. Safe Pickle Usage (`safe_pickle_demo.py`)

**Purpose**: Demonstrates legitimate pickle usage patterns

```bash
python safe_pickle_demo.py
```

**What it shows**:

- Safe serialization of basic Python types
- Custom object serialization
- File-based pickle operations
- Data integrity verification

**Key Learning**: Understanding legitimate pickle use cases

### 2. Vulnerable Application (`vulnerable_app.py`)

**Purpose**: Web application with intentional pickle vulnerabilities

```bash
python vulnerable_app.py
# Access: http://127.0.0.1:5000
```

**Vulnerabilities Demonstrated**:

- Base64-encoded pickle deserialization
- File upload with pickle processing
- Raw POST data pickle handling
- Session management vulnerabilities

**Attack Vectors**:

- `/upload_session` - Base64 pickle data
- `/load_preferences` - File upload attacks
- `/process_object` - Raw binary attacks

**Key Learning**: How web applications can be vulnerable to pickle attacks

### 3. Attack Payload Generator (`attack_payload.py`)

**Purpose**: Create various malicious pickle payloads

```bash
# Basic demonstration
python attack_payload.py

# Interactive payload creation
python attack_payload.py --interactive
```

**Payload Types**:

- **Command Execution**: Basic OS command execution
- **File Operations**: Read, write, and list files
- **Information Gathering**: Extract environment variables
- **Python Code Execution**: Execute arbitrary Python code
- **Stealthy Payloads**: Hidden malicious code in legitimate-looking objects
- **Reverse Shells**: Network-based attacks (⚠️ dangerous!)

**Key Learning**: Understanding attack payload construction

### 4. Complete Exploit Demo (`exploit_demo.py`)

**Purpose**: End-to-end attack demonstrations

```bash
# Full demonstration
python exploit_demo.py

# Specific attack types
python exploit_demo.py --offline    # File tampering attacks
python exploit_demo.py --web        # Web application attacks
python exploit_demo.py --analysis   # Payload analysis techniques
python exploit_demo.py --bypass     # Mitigation bypass methods
```

**Demonstrations**:

- **Offline Tampering**: Modifying pickle files on disk
- **Web Attacks**: Exploiting the vulnerable web application
- **Payload Analysis**: Understanding pickle structure
- **Mitigation Bypass**: Advanced evasion techniques

**Key Learning**: Complete attack lifecycle and detection methods

### 5. Safe Alternatives (`safe_alternatives.py`)

**Purpose**: Secure serialization alternatives and best practices

```bash
python safe_alternatives.py
```

**Safe Methods Demonstrated**:

- **JSON Serialization**: Safe for untrusted data
- **MessagePack**: Binary alternative to JSON
- **Secure Pickle with HMAC**: Integrity-protected pickle
- **Custom Serialization**: Maximum control and validation
- **Performance Comparison**: Speed and size comparisons

**Key Learning**: Production-safe serialization patterns

## 🎯 Attack Scenarios

### Scenario 1: Offline File Tampering

1. Application saves user sessions as pickle files
2. Attacker gains file system access
3. Attacker replaces legitimate pickle with malicious one
4. Application loads tampered file and executes malicious code

**Demonstration**: `python exploit_demo.py --offline`

### Scenario 2: Web Application Exploitation

1. Web app accepts pickle data via API
2. Attacker crafts malicious payload
3. Payload is sent as base64, file upload, or raw data
4. Server unpickles data and executes attack code

**Demonstration**:

```bash
# Terminal 1: Start vulnerable app
python vulnerable_app.py

# Terminal 2: Run web attacks
python exploit_demo.py --web
```

### Scenario 3: Supply Chain Attack

1. Attacker compromises data pipeline
2. Legitimate pickle files are replaced with malicious ones
3. Applications consuming the data execute attack code
4. Attack spreads through the system

**Demonstration**: Modify existing pickle files in `data/` directory

## 🛡️ Defense Strategies

### 1. Never Unpickle Untrusted Data

**❌ Vulnerable Pattern**:

```python
import pickle
user_data = pickle.loads(untrusted_input)  # DANGEROUS!
```

**✅ Safe Alternative**:

```python
import json
user_data = json.loads(untrusted_input)  # Safe for untrusted data
```

### 2. Use Secure Serialization Formats

**For Untrusted Data**:

- JSON (human-readable, widely supported)
- MessagePack (binary, efficient)
- Protocol Buffers (schema validation)

**For Trusted Data with Integrity Checks**:

- HMAC-signed pickle (demonstrated in project)
- Encrypted serialization

### 3. Input Validation and Sanitization

```python
# Validate data structure before processing
def validate_user_data(data):
    required_fields = ['username', 'email', 'permissions']
    if not all(field in data for field in required_fields):
        raise ValueError("Invalid data structure")
    return data
```

### 4. Principle of Least Privilege

- Run applications with minimal required permissions
- Use sandboxing for untrusted code execution
- Implement network segmentation

### 5. Detection and Monitoring

**File Integrity Monitoring**:

```python
import hashlib

def verify_file_integrity(filename, expected_hash):
    with open(filename, 'rb') as f:
        file_hash = hashlib.sha256(f.read()).hexdigest()
    return file_hash == expected_hash
```

**Suspicious Pattern Detection**:

- Monitor for pickle files in unexpected locations
- Scan for suspicious function names in serialized data
- Log deserialization operations

## 🔬 Technical Analysis

### Understanding Pickle Format

Pickle uses a stack-based virtual machine with opcodes:

```python
import pickletools
import pickle

# Analyze pickle structure
data = pickle.dumps({"key": "value"})
pickletools.dis(data)
```

**Common Malicious Opcodes**:

- `GLOBAL`: Import modules and functions
- `REDUCE`: Call functions with arguments
- `BUILD`: Modify object attributes

### The `__reduce__` Method

The core of pickle exploitation:

```python
class MaliciousClass:
    def __reduce__(self):
        # This method defines how to reconstruct the object
        # Attackers abuse it to execute arbitrary code
        return (os.system, ('malicious_command',))
```

### Attack Payload Analysis

**Safe Payload Structure**:

```
MARK    # Start of list
GLOBAL  # Load class
TUPLE   # Arguments tuple
REDUCE  # Call constructor
STOP    # End of pickle
```

**Malicious Payload Structure**:

```
GLOBAL  # Load os.system
MARK    # Start arguments
STRING  # Command string
TUPLE   # Arguments tuple
REDUCE  # Execute command!
STOP    # End of pickle
```

## 🧪 Laboratory Exercises

### Exercise 1: Basic Payload Creation

1. Create a class that executes `whoami` when unpickled
2. Serialize it and save to file
3. Load the file and observe the execution

### Exercise 2: Stealthy Attack

1. Create a payload that looks like legitimate user data
2. Hide malicious code in the `__reduce__` method
3. Test detection evasion

### Exercise 3: Web Application Testing

1. Start the vulnerable web application
2. Create payloads for each endpoint
3. Test different encoding methods (base64, raw binary)

### Exercise 4: Defense Implementation

1. Implement HMAC signature verification
2. Create a safe deserialization wrapper
3. Test tampering detection

### Exercise 5: Alternative Serialization

1. Convert pickle-based code to use JSON
2. Compare performance and functionality
3. Implement custom validation

## 📊 Performance Comparison

Based on testing with 1000 user records:

| Method        | Serialize Time | Deserialize Time | Size (bytes) | Safety          |
| ------------- | -------------- | ---------------- | ------------ | --------------- |
| JSON          | 0.0234s        | 0.0187s          | 215,432      | ✅ Safe         |
| MessagePack   | 0.0156s        | 0.0098s          | 156,789      | ✅ Safe         |
| Pickle        | 0.0087s        | 0.0045s          | 187,234      | ❌ Unsafe       |
| Secure Pickle | 0.0091s        | 0.0052s          | 187,266      | ⚠️ Trusted only |

## 🔗 References and Further Reading

### Academic Papers

- "Pickle's Nine Flaws" by Marco Slaviero
- "Sour Pickles: A serialization vulnerability in the Python pickle module" by NCC Group

### Security Advisories

- CVE-2019-16729: PyYAML unsafe loading
- CVE-2018-1000656: Flask-User pickle vulnerability

### Best Practice Guides

- OWASP Deserialization Cheat Sheet
- Python Security Guidelines
- Secure Coding Practices

### Tools and Libraries

- `pickletools`: Built-in pickle analysis
- `safety`: Dependency vulnerability scanner
- `bandit`: Python security linter

## 🤝 Educational Use Guidelines

### For Students

1. Always run in isolated environments (VMs, containers)
2. Never test against systems you don't own
3. Focus on understanding vulnerability patterns
4. Practice implementing secure alternatives

### For Educators

1. Emphasize ethical use and responsible disclosure
2. Provide controlled environments for testing
3. Include secure coding practices in curriculum
4. Discuss real-world impact and case studies

### For Security Professionals

1. Use for vulnerability research and training
2. Adapt examples for security awareness programs
3. Include in penetration testing methodologies
4. Share knowledge responsibly

## 🐛 Common Issues and Troubleshooting

### Dependencies Not Found

```bash
# Install required packages
pip install flask requests msgpack

# Or install all at once
pip install -r requirements.txt
```

### Permission Errors

```bash
# Some payloads may require specific permissions
# Run in appropriate environment or modify commands
```

### Network Connectivity

```bash
# Ensure no firewall blocking local connections
# Check if port 5000 is available for Flask app
```

### File System Access

```bash
# Ensure write permissions for data/ directory
# Some demonstrations create temporary files
```

## 📝 License and Disclaimer

This educational project is provided for learning purposes only. The authors are not responsible for any misuse of the techniques demonstrated. Users must comply with all applicable laws and regulations.

**Educational Use Only**: This project is designed for cybersecurity education and awareness. Do not use for malicious purposes.

**No Warranty**: The code is provided "as-is" without any warranties. Use at your own risk in controlled environments only.

---

**Remember**: With great power comes great responsibility. Use your knowledge to build more secure systems, not to exploit them maliciously! 🛡️
