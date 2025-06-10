# Python Pickle Module Security Vulnerability Demonstration

This project explores the security risks of Python's `pickle` module, which is used for serializing and deserializing objects but is explicitly insecure for untrusted data, as maliciously crafted pickle data can lead to arbitrary code execution during unpickling. The goal is to demonstrate how manipulated pickled files can achieve arbitrary code execution and to propose mitigation strategies or safer alternatives for deserializing Python objects. This work is part of the Language-Based Security course at KTH (DD2525).

## Demonstrations

This project includes two main demonstrations of pickle deserialization vulnerabilities:

### 1. Offline Tampering

This scenario demonstrates how an attacker can modify a pickled file stored on disk to achieve arbitrary code execution when a vulnerable application later loads the tampered file.

- `offline_tampering/vulnerable_app.py`: This script simulates a simple application that loads a pickled object from a file (`data.pickle`). It represents a common scenario where an application might deserialize data without proper validation.
- `offline_tampering/generate_malicious_pickle.py`: This script crafts a malicious pickled payload. The payload leverages the `__reduce__` method to execute a system command (e.g., `echo Malicious code executed!`) when unpickled. The `__reduce__` method is a special method in Python that allows objects to define how they should be pickled. When an object implementing `__reduce__` is pickled, this method is called, and its return value (a string or a tuple) dictates how the object is represented in the pickle stream. If a tuple is returned, its first element is a callable object, and the second is a tuple of arguments for that callable. During unpickling, this callable is invoked with the provided arguments. Attackers can abuse this mechanism by making `__reduce__` return a dangerous callable (like `os.system` or `eval`) and a malicious command as its argument, leading to arbitrary code execution.
- `offline_tampering/secure_app.py`: This script demonstrates a safer approach to handling pickled data by using HMAC (Hash-based Message Authentication Code) to verify the integrity of the pickled data before unpickling.

To run this demonstration:

1.  **Generate malicious pickle files:**
    Run `generate_malicious_pickle.py` to create three files:

    - `malicious.pickle`: Contains a malicious payload without any signature.
    - `malicious_hmac_valid.pickle`: Contains the malicious payload with a valid HMAC signature (signed with the correct secret key).
    - `malicious_hmac_invalid.pickle`: Contains the malicious payload with an invalid HMAC signature (signed with an incorrect key, simulating an attacker's attempt to tamper).

    ```bash
    cd offline_tampering
    python generate_malicious_pickle.py
    ```

2.  **Execute the vulnerable application with malicious data:**
    Run `vulnerable_app.py`. It will load and unpickle the `malicious.pickle` file, leading to arbitrary code execution. Observe the creation of `you_have_been_hacked.txt`.

    ```bash
    cd offline_tampering
    python vulnerable_app.py
    ```

3.  **Demonstrate the secure application:**
    Run `secure_app.py`. This script will attempt to load both `malicious_hmac_valid.pickle` and `malicious_hmac_invalid.pickle`.

    - It will successfully unpickle `malicious_hmac_valid.pickle` because the HMAC signature is correct.
    - It will detect tampering and raise a `ValueError` when attempting to load `malicious_hmac_invalid.pickle` due to the invalid HMAC signature, preventing the malicious code from executing.

    ```bash
    cd offline_tampering
    python secure_app.py
    ```

### 2. Web App Demonstration

This scenario illustrates how deserialization vulnerabilities can lead to Remote Code Execution (RCE) in web applications if a web endpoint deserializes untrusted data directly from user input. This also highlights a potential risk in supply-chain attacks, where a legitimate GitHub repository or a third-party library might inadvertently contain or use a maliciously crafted pickle file, compromising systems that import or process it.

- `web_app/diary_app.py`: This is a Flask web application that simulates a simple diary. It allows users to "save" and "load" diary entries, which are serialized using `pickle`. The vulnerability lies in the "load" functionality, which directly unpickles user-provided data without proper validation.
- `web_app/generate_malicious_diary.py`: This script generates a malicious pickled diary entry that, when unpickled by `diary_app.py`, will execute arbitrary code on the server.

To run this demonstration:

1.  Generate the malicious payload:

```bash
cd web_app
python generate_malicious_diary.py
```

2.  Start the Flask web application:

```bash
cd web_app
python diary_app.py
```

3. Access the web application in your browser at `http://localhost:5000/`. Use the "Load Diary" functionality to load the malicious diary entry. The server will execute the code embedded in the pickled data, demonstrating the RCE vulnerability.

## Results

For the **Offline Tampering** demonstration:

- When `offline_tampering/vulnerable_app.py` attempts to unpickle the malicious data from `malicious.pickle` (generated by `offline_tampering/generate_malicious_pickle.py`), the system command embedded within the payload will be executed. This demonstrates the arbitrary code execution vulnerability inherent in unpickling untrusted data. You will observe the creation of a file named `you_have_been_hacked.txt` in the project root, confirming the successful execution of the injected command.
- When `offline_tampering/secure_app.py` is run, it first attempts to load `malicious_hmac_valid.pickle`. Since this file has a valid HMAC signature, the data will be successfully unpickled, and no error will occur.
- Next, `secure_app.py` attempts to load `malicious_hmac_invalid.pickle`. Because this file has an invalid HMAC signature, the application will detect the tampering and raise a `ValueError`, preventing the malicious payload from being unpickled and executed. This highlights how HMAC can effectively mitigate offline tampering attacks by ensuring data integrity and authenticity.

For the **Web App Demonstration**, when a malicious pickled diary entry generated by `web_app/generate_malicious_diary.py` is sent to and unpickled by `web_app/diary_app.py`, the arbitrary code embedded within the payload will be executed on the server. This demonstrates Remote Code Execution (RCE) in a web application context.

Both demonstrations underscore the critical importance of validating and securing deserialization processes, especially when dealing with data from untrusted sources.

## Mitigation Strategies

To safely handle serialization and deserialization in Python, it is crucial to avoid `pickle` when dealing with untrusted data. Safer alternatives and practices include:

- **Using Data-Only Serialization Formats**: For untrusted data, prefer formats like JSON (JavaScript Object Notation), YAML, or MessagePack. These formats are designed for data interchange and do not inherently support arbitrary code execution during deserialization.
  - **JSON**: Lightweight, human-readable, and language-agnostic. Python's built-in `json` module is suitable for this.
  - **MessagePack**: A binary serialization format that is more compact and faster than JSON, suitable for performance-critical applications.
  - **Note on PyYAML and jsonpickle**: While JSON and YAML are generally safer, it's important to note that certain libraries like `PyYAML` (when using `yaml.load` without specifying a safe loader) and `jsonpickle` can also be vulnerable to similar deserialization attacks if not used carefully, as they might allow deserialization of arbitrary Python objects or execution of code. Always ensure you are using safe loading functions (e.g., `yaml.safe_load` for PyYAML) and understand the security implications of any serialization library.
- **Message Authentication Codes (MAC)**: If you must use `pickle` for trusted data (e.g., internal communication where data integrity is paramount), generate a cryptographic signature (e.g., using `hmac`) for the pickled data. The receiver can then validate this signature before unpickling to ensure the data has not been tampered with. This protects against offline tampering but does not mitigate vulnerabilities if the original source of the pickled data is compromised.
- **Restricting Globals**: For advanced use cases where `pickle` is unavoidable, you can customize `Unpickler.find_class` to restrict which classes and functions can be imported during unpickling. This acts as a whitelist, preventing the deserialization of dangerous objects. However, this is complex and prone to error, as it requires a deep understanding of all possible "gadgets" that could be exploited.

## References

- [Python `pickle` module documentation](https://docs.python.org/3/library/pickle.html)
- [Exploiting Python pickles - David Hamann](https://davidhamann.de/2020/04/05/exploiting-python-pickle/)
- [Unsafe Deserialization in Python | SecureFlag Security Knowledge Base](https://knowledge-base.secureflag.com/vulnerabilities/unsafe_deserialization/unsafe_deserialization_python.html)
- [The ultimate guide to Python pickle | Snyk](https://snyk.io/blog/guide-to-python-pickle/)
- [Python Pickle Risks and Safer Serialization Alternatives | ArjanCodes](https://arjancodes.com/blog/python-pickle-module-security-risks-and-safer-alternatives/)
- [OWASP Deserialization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Deserialization_Cheat_Sheet.html)
