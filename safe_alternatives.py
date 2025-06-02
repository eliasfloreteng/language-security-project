#!/usr/bin/env python3
"""
Safe Serialization Alternatives to Pickle
This script demonstrates safer methods for serializing and deserializing data
that don't have the security vulnerabilities associated with pickle.

WARNING: This is for educational purposes to show secure alternatives.
"""

import json
import hmac
import hashlib
import pickle
import base64
import time
from dataclasses import dataclass, asdict
from typing import Dict, List, Any
import sys

try:
    import msgpack

    MSGPACK_AVAILABLE = True
except ImportError:
    MSGPACK_AVAILABLE = False
    print("⚠️  MessagePack not installed. Install with: pip install msgpack")


@dataclass
class User:
    """Example data class for serialization demonstrations"""

    name: str
    age: int
    email: str
    preferences: Dict[str, Any]


class SafeSerializationDemo:
    """Demonstrates various safe serialization methods"""

    def __init__(self):
        self.secret_key = b"your-secret-key-here-change-in-production"

        # Sample data for demonstrations
        self.sample_user = User(
            name="Alice Smith",
            age=30,
            email="alice@example.com",
            preferences={"theme": "dark", "notifications": True, "language": "en"},
        )

        self.sample_data = {
            "users": [
                {"name": "Alice", "age": 30, "role": "admin"},
                {"name": "Bob", "age": 25, "role": "user"},
            ],
            "settings": {"debug": False, "version": "1.0.0"},
            "timestamp": time.time(),
        }

    def demonstrate_json_serialization(self):
        """Demonstrate JSON serialization - the safest option"""
        print("🔒 JSON SERIALIZATION (RECOMMENDED)")
        print("=" * 50)

        # Convert dataclass to dict for JSON serialization
        user_dict = asdict(self.sample_user)

        # Serialize to JSON
        json_data = json.dumps(user_dict, indent=2)
        print("📤 Serialized JSON:")
        print(json_data)

        # Deserialize from JSON
        deserialized = json.loads(json_data)
        print("\n📥 Deserialized data:")
        print(deserialized)

        # Recreate User object
        restored_user = User(**deserialized)
        print(f"\n✅ Restored user: {restored_user}")

        print("\n✅ Advantages:")
        print("  - Human readable")
        print("  - Cross-language support")
        print("  - No code execution risk")
        print("  - Wide ecosystem support")

        print("\n❌ Limitations:")
        print("  - Limited data types (no custom objects directly)")
        print("  - No circular references")
        print("  - Larger size than binary formats")

        return json_data, deserialized

    def demonstrate_msgpack_serialization(self):
        """Demonstrate MessagePack serialization"""
        if not MSGPACK_AVAILABLE:
            print("\n❌ MessagePack not available - skipping demo")
            return None, None

        print("\n🔒 MESSAGEPACK SERIALIZATION")
        print("=" * 50)

        # Convert dataclass to dict
        user_dict = asdict(self.sample_user)

        # Serialize to MessagePack
        msgpack_data = msgpack.packb(user_dict)
        print(f"📤 Serialized MessagePack ({len(msgpack_data)} bytes):")
        print(f"   {msgpack_data.hex()}")

        # Deserialize from MessagePack
        deserialized = msgpack.unpackb(msgpack_data, raw=False)
        print("\n📥 Deserialized data:")
        print(deserialized)

        # Recreate User object
        restored_user = User(**deserialized)
        print(f"\n✅ Restored user: {restored_user}")

        print("\n✅ Advantages:")
        print("  - More compact than JSON")
        print("  - Faster than JSON")
        print("  - Cross-language support")
        print("  - No code execution risk")

        print("\n❌ Limitations:")
        print("  - Binary format (not human readable)")
        print("  - Limited data types")
        print("  - Requires additional library")

        return msgpack_data, deserialized

    def demonstrate_hmac_signed_pickle(self):
        """Demonstrate HMAC-signed pickle for trusted sources"""
        print("\n🔐 HMAC-SIGNED PICKLE (FOR TRUSTED SOURCES ONLY)")
        print("=" * 60)

        # Create pickle data
        pickle_data = pickle.dumps(self.sample_data)

        # Create HMAC signature
        signature = hmac.new(self.secret_key, pickle_data, hashlib.sha256).hexdigest()

        print(f"📦 Pickle size: {len(pickle_data)} bytes")
        print(f"🔏 HMAC signature: {signature}")

        # Simulate sending/storing the data
        signed_package = {
            "data": base64.b64encode(pickle_data).decode("utf-8"),
            "signature": signature,
        }

        print("\n📤 Signed package created")

        # Verify and deserialize
        try:
            # Extract data and signature
            received_data = base64.b64decode(signed_package["data"])
            received_signature = signed_package["signature"]

            # Verify signature
            expected_signature = hmac.new(
                self.secret_key, received_data, hashlib.sha256
            ).hexdigest()

            if hmac.compare_digest(expected_signature, received_signature):
                print("✅ Signature verified - data integrity confirmed")
                deserialized = pickle.loads(received_data)
                print("📥 Deserialized data:")
                print(deserialized)
            else:
                print("❌ Signature verification failed - data may be tampered")
                return None

        except Exception as e:
            print(f"❌ Error during verification: {e}")
            return None

        print("\n✅ Use cases:")
        print("  - Internal system communication")
        print("  - Cached data with integrity checking")
        print("  - Configuration files")

        print("\n⚠️  Requirements:")
        print("  - Secure key management")
        print("  - Trusted data sources only")
        print("  - Regular key rotation")

        return signed_package, deserialized

    def demonstrate_custom_safe_serializer(self):
        """Demonstrate a custom safe serialization approach"""
        print("\n🛠️  CUSTOM SAFE SERIALIZER")
        print("=" * 50)

        class SafeSerializer:
            """A custom serializer that only handles safe data types"""

            ALLOWED_TYPES = (str, int, float, bool, list, dict, type(None))

            @classmethod
            def serialize(cls, obj):
                """Serialize object to JSON with type validation"""
                cls._validate_object(obj)
                return json.dumps(obj, indent=2)

            @classmethod
            def deserialize(cls, data):
                """Deserialize JSON data with validation"""
                obj = json.loads(data)
                cls._validate_object(obj)
                return obj

            @classmethod
            def _validate_object(cls, obj):
                """Recursively validate object contains only safe types"""
                if isinstance(obj, cls.ALLOWED_TYPES):
                    if isinstance(obj, dict):
                        for key, value in obj.items():
                            if not isinstance(key, str):
                                raise TypeError(
                                    f"Dictionary keys must be strings, got {type(key)}"
                                )
                            cls._validate_object(value)
                    elif isinstance(obj, list):
                        for item in obj:
                            cls._validate_object(item)
                else:
                    raise TypeError(f"Type {type(obj)} is not allowed")

        # Test the safe serializer
        try:
            serialized = SafeSerializer.serialize(self.sample_data)
            print("📤 Safe serialization successful:")
            print(serialized[:200] + "..." if len(serialized) > 200 else serialized)

            deserialized = SafeSerializer.deserialize(serialized)
            print("\n📥 Safe deserialization successful")
            print(f"   Data type: {type(deserialized)}")
            print(f"   Keys: {list(deserialized.keys())}")

        except Exception as e:
            print(f"❌ Safe serialization failed: {e}")
            return None, None

        # Demonstrate rejection of unsafe data
        print("\n🚫 Testing rejection of unsafe data:")
        try:
            # This should fail
            unsafe_data = {"function": lambda x: x, "safe": "data"}
            SafeSerializer.serialize(unsafe_data)
        except TypeError as e:
            print(f"✅ Correctly rejected unsafe data: {e}")

        return serialized, deserialized

    def compare_serialization_methods(self):
        """Compare different serialization methods"""
        print("\n📊 SERIALIZATION METHOD COMPARISON")
        print("=" * 60)

        methods = []

        # Test JSON
        start_time = time.time()
        json_data, _ = self.demonstrate_json_serialization()
        json_time = time.time() - start_time
        methods.append(("JSON", len(json_data.encode()), json_time, "Very Safe"))

        # Test MessagePack if available
        if MSGPACK_AVAILABLE:
            start_time = time.time()
            msgpack_data, _ = self.demonstrate_msgpack_serialization()
            msgpack_time = time.time() - start_time
            methods.append(
                ("MessagePack", len(msgpack_data), msgpack_time, "Very Safe")
            )

        # Test pickle (for comparison - NOT RECOMMENDED)
        start_time = time.time()
        pickle_data = pickle.dumps(self.sample_data)
        pickle_time = time.time() - start_time
        methods.append(("Pickle (UNSAFE)", len(pickle_data), pickle_time, "DANGEROUS"))

        print("\n📈 PERFORMANCE & SIZE COMPARISON:")
        print(f"{'Method':<20} {'Size (bytes)':<15} {'Time (ms)':<12} {'Safety':<12}")
        print("-" * 60)

        for name, size, exec_time, safety in methods:
            print(f"{name:<20} {size:<15} {exec_time * 1000:<12.2f} {safety:<12}")

    def demonstrate_secure_config_storage(self):
        """Demonstrate secure configuration file handling"""
        print("\n⚙️  SECURE CONFIGURATION STORAGE")
        print("=" * 50)

        config = {
            "database": {"host": "localhost", "port": 5432, "name": "myapp"},
            "features": {
                "debug_mode": False,
                "max_users": 1000,
                "allowed_origins": ["localhost", "example.com"],
            },
            "version": "1.0.0",
        }

        # Save config as JSON
        config_json = json.dumps(config, indent=2)

        print("📁 Configuration as JSON:")
        print(config_json)

        # Demonstrate configuration validation
        def validate_config(config_data):
            """Validate configuration structure"""
            required_sections = ["database", "features", "version"]

            for section in required_sections:
                if section not in config_data:
                    raise ValueError(f"Missing required section: {section}")

            # Validate database config
            db_config = config_data["database"]
            required_db_fields = ["host", "port", "name"]
            for field in required_db_fields:
                if field not in db_config:
                    raise ValueError(f"Missing database field: {field}")

            if not isinstance(db_config["port"], int):
                raise ValueError("Database port must be an integer")

            print("✅ Configuration validation passed")
            return True

        # Test validation
        loaded_config = json.loads(config_json)
        validate_config(loaded_config)

        print("\n💡 Best practices for config files:")
        print("  - Use JSON or YAML for configuration")
        print("  - Validate structure after loading")
        print("  - Store secrets separately (environment variables)")
        print("  - Use schema validation libraries")
        print("  - Version your configuration format")


def main():
    """Run all demonstrations"""
    print("🔐 SAFE SERIALIZATION ALTERNATIVES DEMONSTRATION")
    print("=" * 70)
    print("This script demonstrates secure alternatives to pickle serialization")
    print("=" * 70)

    demo = SafeSerializationDemo()

    try:
        # Run all demonstrations
        demo.demonstrate_json_serialization()
        demo.demonstrate_msgpack_serialization()
        demo.demonstrate_hmac_signed_pickle()
        demo.demonstrate_custom_safe_serializer()
        demo.demonstrate_secure_config_storage()
        demo.compare_serialization_methods()

        print("\n🎯 KEY RECOMMENDATIONS:")
        print("=" * 40)
        print("1. Use JSON for most use cases")
        print("2. Use MessagePack for performance-critical applications")
        print("3. NEVER use pickle with untrusted data")
        print("4. If using pickle, implement HMAC signing")
        print("5. Validate all deserialized data")
        print("6. Consider using schema validation libraries")

        print("\n📚 Additional Libraries to Consider:")
        print("  - pydantic: Data validation using Python type hints")
        print("  - marshmallow: Object serialization/deserialization")
        print("  - protobuf: Google's Protocol Buffers")
        print("  - avro: Apache Avro serialization")

    except Exception as e:
        print(f"❌ Error during demonstration: {e}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
