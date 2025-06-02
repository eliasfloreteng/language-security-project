#!/usr/bin/env python3
"""
Python Pickle Module Security Vulnerability Demonstration
Main entry point for the security demonstration project.

This project explores the security risks associated with Python's pickle library
and demonstrates how manipulated pickled files can lead to arbitrary code execution.

WARNING: This code is for educational purposes only.
Only use on systems you own or have explicit permission to test.
"""

import sys
import os
from pathlib import Path


def print_banner():
    """Print project banner"""
    print("🥒" * 20)
    print("🥒 PYTHON PICKLE SECURITY DEMONSTRATION 🥒")
    print("🥒" * 20)
    print()
    print("⚠️  WARNING: Educational purposes only!")
    print("   Only use on systems you own or have permission to test.")
    print()


def show_menu():
    """Display main menu options"""
    print("📋 AVAILABLE DEMONSTRATIONS:")
    print("=" * 50)
    print("1. 🌐 Start Vulnerable Web Application")
    print("2. ⚔️  Generate Attack Payloads")
    print("3. 🔒 Demonstrate Safe Alternatives")
    print("4. 💻 Command Execution Exploits")
    print("5. 📁 File Operation Exploits")
    print("6. 🐚 Reverse Shell Exploits")
    print("7. 📚 Show Project Information")
    print("8. 🚪 Exit")
    print("=" * 50)


def start_vulnerable_app():
    """Start the vulnerable Flask application"""
    print("🌐 Starting Vulnerable Web Application...")
    print("=" * 40)
    try:
        import vulnerable_app

        # This will start the Flask app
        vulnerable_app.app.run(host="127.0.0.1", port=5000, debug=True)
    except ImportError as e:
        print(f"❌ Error importing vulnerable_app: {e}")
    except Exception as e:
        print(f"❌ Error starting application: {e}")


def generate_attack_payloads():
    """Generate various attack payloads"""
    print("⚔️  Generating Attack Payloads...")
    print("=" * 40)
    try:
        import attack_payloads

        attack_payloads.demonstrate_payloads()
    except ImportError as e:
        print(f"❌ Error importing attack_payloads: {e}")
    except Exception as e:
        print(f"❌ Error generating payloads: {e}")


def demonstrate_safe_alternatives():
    """Demonstrate safe serialization alternatives"""
    print("🔒 Demonstrating Safe Alternatives...")
    print("=" * 40)
    try:
        import safe_alternatives

        safe_alternatives.main()
    except ImportError as e:
        print(f"❌ Error importing safe_alternatives: {e}")
    except Exception as e:
        print(f"❌ Error demonstrating alternatives: {e}")


def run_command_exploits():
    """Run command execution exploits"""
    print("💻 Command Execution Exploits...")
    print("=" * 40)
    try:
        sys.path.append(str(Path("exploits")))
        import command_execution

        command_execution.demonstrate_payloads()
    except ImportError as e:
        print(f"❌ Error importing command_execution: {e}")
    except Exception as e:
        print(f"❌ Error running command exploits: {e}")


def run_file_exploits():
    """Run file operation exploits"""
    print("📁 File Operation Exploits...")
    print("=" * 40)
    try:
        sys.path.append(str(Path("exploits")))
        import file_operations

        file_operations.demonstrate_file_operations()
    except ImportError as e:
        print(f"❌ Error importing file_operations: {e}")
    except Exception as e:
        print(f"❌ Error running file exploits: {e}")


def run_shell_exploits():
    """Run reverse shell exploits"""
    print("🐚 Reverse Shell Exploits...")
    print("=" * 40)
    try:
        sys.path.append(str(Path("exploits")))
        import reverse_shell

        reverse_shell.demonstrate_reverse_shells()
    except ImportError as e:
        print(f"❌ Error importing reverse_shell: {e}")
    except Exception as e:
        print(f"❌ Error running shell exploits: {e}")


def show_project_info():
    """Display project information"""
    print("📚 PROJECT INFORMATION")
    print("=" * 50)

    print("\n🎯 OBJECTIVE:")
    print("This project demonstrates the security risks associated with Python's")
    print("pickle module when handling untrusted data. It shows how malicious")
    print("pickle payloads can lead to arbitrary code execution.")

    print("\n📁 PROJECT STRUCTURE:")
    structure = """
language-security-project/
├── README.md                    # Comprehensive documentation
├── main.py                      # This main entry point
├── vulnerable_app.py           # Flask app with pickle vulnerability
├── attack_payloads.py          # Various malicious payload examples
├── safe_alternatives.py        # Safer serialization methods
└── exploits/                   # Specific exploit examples
    ├── command_execution.py    # Command execution attacks
    ├── file_operations.py      # File manipulation attacks
    └── reverse_shell.py        # Network-based attacks
"""
    print(structure)

    print("🔍 KEY FINDINGS:")
    print("- Pickle can execute arbitrary code during deserialization")
    print("- Any Python code can be executed with application privileges")
    print("- Attacks are cross-platform and difficult to detect")
    print("- JSON and MessagePack are safer alternatives")

    print("\n💡 RECOMMENDATIONS:")
    print("1. Never unpickle data from untrusted sources")
    print("2. Use JSON or MessagePack for data exchange")
    print("3. If pickle is required, implement HMAC signatures")
    print("4. Run applications with minimal privileges")
    print("5. Monitor for unexpected process executions")

    print("\n📖 EDUCATIONAL VALUE:")
    print("This demonstration helps developers understand:")
    print("- The risks of insecure deserialization")
    print("- How to identify vulnerable code patterns")
    print("- Proper secure coding practices")
    print("- The importance of input validation")


def show_quick_start():
    """Show quick start guide"""
    print("\n🚀 QUICK START GUIDE:")
    print("=" * 30)
    print("1. Generate payloads: Choose option 2")
    print("2. Start vulnerable app: Choose option 1")
    print("3. Visit: http://127.0.0.1:5000")
    print("4. Upload .pkl files or paste base64 payloads")
    print("5. Observe code execution in terminal")
    print("\n⚠️  Remember: Educational use only!")


def handle_choice(choice):
    """Handle user menu choice"""
    if choice == "1":
        start_vulnerable_app()
    elif choice == "2":
        generate_attack_payloads()
    elif choice == "3":
        demonstrate_safe_alternatives()
    elif choice == "4":
        run_command_exploits()
    elif choice == "5":
        run_file_exploits()
    elif choice == "6":
        run_shell_exploits()
    elif choice == "7":
        show_project_info()
    elif choice == "8":
        print("👋 Thank you for using the Pickle Security Demonstration!")
        print("Remember: Always code securely! 🔒")
        return False
    else:
        print("❌ Invalid choice. Please select 1-8.")

    return True


def check_dependencies():
    """Check if required dependencies are available"""
    missing_deps = []

    try:
        import flask
    except ImportError:
        missing_deps.append("flask")

    try:
        import msgpack
    except ImportError:
        missing_deps.append("msgpack")

    if missing_deps:
        print("⚠️  MISSING DEPENDENCIES:")
        print(f"   {', '.join(missing_deps)}")
        print("\n📦 Install with:")
        print("   pip install flask msgpack")
        print("   # Or: pip install -e .")
        print()
        return False

    return True


def main():
    """Main function"""
    print_banner()

    # Check dependencies
    if not check_dependencies():
        print("❌ Please install dependencies before continuing.")
        return 1

    show_project_info()
    show_quick_start()

    # Main interaction loop
    while True:
        print("\n")
        show_menu()

        try:
            choice = input("\n🔍 Enter your choice (1-8): ").strip()
            print()

            if not handle_choice(choice):
                break

            if choice != "8":
                input("\n⏎ Press Enter to continue...")

        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except EOFError:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ An error occurred: {e}")
            input("\n⏎ Press Enter to continue...")

    return 0


if __name__ == "__main__":
    sys.exit(main())
