"""
Safe Serialization Alternatives
===============================

This module demonstrates secure alternatives to pickle for data serialization,
including JSON, MessagePack, and secure pickle usage with HMAC signatures.

✅ This demonstrates SAFE serialization practices!
✅ Use these patterns in production code!
"""

import json
import hmac
import hashlib
import pickle
import base64
import os
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Dict, Any, List
import tempfile

# Optional dependencies - install with: pip install msgpack
try:
    import msgpack

    MSGPACK_AVAILABLE = True
except ImportError:
    MSGPACK_AVAILABLE = False
    print("Note: msgpack not available. Install with: pip install msgpack")


@dataclass
class User:
    """Example user class for serialization demonstrations."""

    user_id: int
    username: str
    email: str
    created_at: str
    permissions: List[str]
    preferences: Dict[str, Any]


@dataclass
class GameState:
    """Example game state for complex serialization."""

    player_name: str
    level: int
    score: int
    inventory: List[str]
    settings: Dict[str, Any]


class SecurePickleHandler:
    """
    Secure pickle handler that uses HMAC signatures to verify data integrity.

    This allows safe use of pickle with trusted data by preventing tampering.
    """

    def __init__(self, secret_key: bytes):
        """Initialize with a secret key for HMAC signatures."""
        self.secret_key = secret_key

    def secure_dumps(self, obj) -> bytes:
        """Serialize object and add HMAC signature."""
        # Serialize the object
        pickled_data = pickle.dumps(obj)

        # Create HMAC signature
        signature = hmac.new(self.secret_key, pickled_data, hashlib.sha256).digest()

        # Combine signature and data
        return signature + pickled_data

    def secure_loads(self, data: bytes):
        """Load object after verifying HMAC signature."""
        if len(data) < 32:  # SHA256 digest is 32 bytes
            raise ValueError("Data too short to contain signature")

        # Split signature and data
        signature = data[:32]
        pickled_data = data[32:]

        # Verify signature
        expected_signature = hmac.new(
            self.secret_key, pickled_data, hashlib.sha256
        ).digest()

        if not hmac.compare_digest(signature, expected_signature):
            raise ValueError(
                "HMAC signature verification failed - data may be tampered!"
            )

        # If signature is valid, unpickle the data
        return pickle.loads(pickled_data)


def demonstrate_json_serialization():
    """Demonstrate JSON serialization for simple data structures."""
    print("=" * 60)
    print("JSON SERIALIZATION DEMONSTRATION")
    print("=" * 60)
    print("✅ JSON is safe for untrusted data!")
    print("❌ JSON has limited data type support")
    print()

    # Create sample data
    user = User(
        user_id=1001,
        username="alice",
        email="alice@example.com",
        created_at=datetime.now().isoformat(),
        permissions=["read", "write"],
        preferences={
            "theme": "dark",
            "language": "en",
            "notifications": True,
            "max_items": 100,
        },
    )

    print(f"Original user: {user}")

    # Convert to dictionary for JSON serialization
    user_dict = asdict(user)

    # Serialize to JSON
    json_data = json.dumps(user_dict, indent=2)
    print(f"\nJSON serialized data:")
    print(json_data)

    # Deserialize from JSON
    loaded_user_dict = json.loads(json_data)
    loaded_user = User(**loaded_user_dict)

    print(f"\nLoaded user: {loaded_user}")
    print(f"Data integrity: {user == loaded_user}")

    # Demonstrate JSON safety
    print("\n" + "-" * 40)
    print("JSON SAFETY DEMONSTRATION")
    print("-" * 40)

    # Even malicious-looking JSON is safe
    malicious_json = """
    {
        "username": "attacker",
        "command": "rm -rf /",
        "exploit": "__import__('os').system('echo hacked')"
    }
    """

    print("Loading malicious-looking JSON:")
    print(malicious_json)

    try:
        safe_data = json.loads(malicious_json)
        print(f"Loaded safely: {safe_data}")
        print("✅ No code execution - just data!")
    except Exception as e:
        print(f"JSON parsing error: {e}")


def demonstrate_msgpack_serialization():
    """Demonstrate MessagePack serialization."""
    if not MSGPACK_AVAILABLE:
        print("MessagePack not available - skipping demonstration")
        return

    print("\n" + "=" * 60)
    print("MESSAGEPACK SERIALIZATION DEMONSTRATION")
    print("=" * 60)
    print("✅ MessagePack is safe for untrusted data!")
    print("✅ More efficient than JSON")
    print("❌ Still limited data type support")
    print()

    # Create complex game state
    game_state = GameState(
        player_name="Hero",
        level=15,
        score=12500,
        inventory=["sword", "shield", "potion", "key"],
        settings={
            "difficulty": "hard",
            "sound_enabled": True,
            "graphics_quality": "high",
            "key_bindings": {
                "move_up": "W",
                "move_down": "S",
                "move_left": "A",
                "move_right": "D",
            },
        },
    )

    print(f"Original game state: {game_state}")

    # Convert to dictionary
    game_dict = asdict(game_state)

    # Serialize with MessagePack
    msgpack_data = msgpack.packb(game_dict)
    print(f"\nMessagePack serialized size: {len(msgpack_data)} bytes")

    # Compare with JSON
    json_data = json.dumps(game_dict).encode()
    print(f"JSON serialized size: {len(json_data)} bytes")
    print(
        f"MessagePack is {((len(json_data) - len(msgpack_data)) / len(json_data) * 100):.1f}% smaller"
    )

    # Deserialize
    loaded_game_dict = msgpack.unpackb(msgpack_data)
    loaded_game_state = GameState(**loaded_game_dict)

    print(f"\nLoaded game state: {loaded_game_state}")
    print(f"Data integrity: {game_state == loaded_game_state}")


def demonstrate_secure_pickle():
    """Demonstrate secure pickle usage with HMAC signatures."""
    print("\n" + "=" * 60)
    print("SECURE PICKLE WITH HMAC DEMONSTRATION")
    print("=" * 60)
    print("✅ Secure for trusted environments with integrity verification")
    print("⚠️  Still requires secure key management")
    print()

    # Generate a secret key (in production, manage this securely!)
    secret_key = os.urandom(32)
    print(f"Secret key: {secret_key.hex()[:32]}... ({len(secret_key)} bytes)")

    # Create secure pickle handler
    secure_pickle = SecurePickleHandler(secret_key)

    # Create sample data (including complex objects)
    users = [
        User(
            1001,
            "alice",
            "alice@example.com",
            datetime.now().isoformat(),
            ["read", "write"],
            {"theme": "dark"},
        ),
        User(
            1002,
            "bob",
            "bob@example.com",
            datetime.now().isoformat(),
            ["read"],
            {"theme": "light"},
        ),
    ]

    print(f"Original data: {len(users)} users")

    # Secure serialization
    secure_data = secure_pickle.secure_dumps(users)
    print(f"Secure pickle size: {len(secure_data)} bytes (includes 32-byte signature)")

    # Demonstrate that we can load it safely
    try:
        loaded_users = secure_pickle.secure_loads(secure_data)
        print(f"Loaded data: {len(loaded_users)} users")
        print("✅ HMAC signature verified - data is authentic")
    except ValueError as e:
        print(f"❌ Security error: {e}")

    # Demonstrate tampering detection
    print("\n" + "-" * 40)
    print("TAMPERING DETECTION")
    print("-" * 40)

    # Tamper with the data
    tampered_data = bytearray(secure_data)
    tampered_data[-10] = 0xFF  # Change a byte near the end

    try:
        loaded_tampered = secure_pickle.secure_loads(bytes(tampered_data))
        print("❌ Tampering not detected!")
    except ValueError as e:
        print(f"✅ Tampering detected: {e}")

    # Demonstrate wrong key detection
    print("\n" + "-" * 40)
    print("WRONG KEY DETECTION")
    print("-" * 40)

    wrong_key_handler = SecurePickleHandler(os.urandom(32))

    try:
        loaded_wrong_key = wrong_key_handler.secure_loads(secure_data)
        print("❌ Wrong key not detected!")
    except ValueError as e:
        print(f"✅ Wrong key detected: {e}")


def demonstrate_custom_serialization():
    """Demonstrate custom serialization for specific use cases."""
    print("\n" + "=" * 60)
    print("CUSTOM SERIALIZATION DEMONSTRATION")
    print("=" * 60)
    print("✅ Maximum control and security")
    print("✅ Optimized for specific use cases")
    print()

    class CustomUserSerializer:
        """Custom serializer for User objects."""

        @staticmethod
        def serialize(user: User) -> bytes:
            """Serialize user to a custom binary format."""
            # Create a simple binary format
            data = {
                "version": 1,
                "user_id": user.user_id,
                "username": user.username,
                "email": user.email,
                "created_at": user.created_at,
                "permissions": user.permissions,
                "preferences": user.preferences,
            }
            # Use JSON as the underlying format but could be custom binary
            return json.dumps(data).encode("utf-8")

        @staticmethod
        def deserialize(data: bytes) -> User:
            """Deserialize user from custom binary format."""
            try:
                parsed = json.loads(data.decode("utf-8"))

                # Validate version
                if parsed.get("version") != 1:
                    raise ValueError("Unsupported serialization version")

                # Validate required fields
                required_fields = [
                    "user_id",
                    "username",
                    "email",
                    "created_at",
                    "permissions",
                    "preferences",
                ]
                for field in required_fields:
                    if field not in parsed:
                        raise ValueError(f"Missing required field: {field}")

                # Validate data types
                if not isinstance(parsed["user_id"], int):
                    raise ValueError("user_id must be an integer")
                if not isinstance(parsed["permissions"], list):
                    raise ValueError("permissions must be a list")
                if not isinstance(parsed["preferences"], dict):
                    raise ValueError("preferences must be a dict")

                # Create and return user object
                return User(
                    user_id=parsed["user_id"],
                    username=parsed["username"],
                    email=parsed["email"],
                    created_at=parsed["created_at"],
                    permissions=parsed["permissions"],
                    preferences=parsed["preferences"],
                )

            except (json.JSONDecodeError, KeyError, TypeError) as e:
                raise ValueError(f"Invalid serialization format: {e}")

    # Test custom serialization
    original_user = User(
        user_id=2001,
        username="charlie",
        email="charlie@example.com",
        created_at=datetime.now().isoformat(),
        permissions=["admin"],
        preferences={"theme": "auto", "debug": True},
    )

    print(f"Original user: {original_user}")

    # Serialize
    serialized = CustomUserSerializer.serialize(original_user)
    print(f"Serialized size: {len(serialized)} bytes")

    # Deserialize
    deserialized_user = CustomUserSerializer.deserialize(serialized)
    print(f"Deserialized user: {deserialized_user}")
    print(f"Data integrity: {original_user == deserialized_user}")

    # Demonstrate validation
    print("\n" + "-" * 40)
    print("VALIDATION DEMONSTRATION")
    print("-" * 40)

    # Try to deserialize invalid data
    invalid_data = b'{"version": 2, "invalid": "data"}'
    try:
        CustomUserSerializer.deserialize(invalid_data)
    except ValueError as e:
        print(f"✅ Validation caught invalid data: {e}")


def demonstrate_performance_comparison():
    """Compare performance of different serialization methods."""
    print("\n" + "=" * 60)
    print("PERFORMANCE COMPARISON")
    print("=" * 60)

    import time

    # Create test data
    test_data = {
        "users": [
            {
                "user_id": i,
                "username": f"user_{i}",
                "email": f"user_{i}@example.com",
                "permissions": ["read", "write"] if i % 2 == 0 else ["read"],
                "preferences": {
                    "theme": "dark" if i % 3 == 0 else "light",
                    "language": "en",
                    "notifications": True,
                    "items_per_page": 25 + (i % 50),
                },
            }
            for i in range(1000)
        ]
    }

    print(f"Test data: {len(test_data['users'])} users")

    # Test JSON
    start_time = time.time()
    json_data = json.dumps(test_data)
    json_serialize_time = time.time() - start_time

    start_time = time.time()
    json_loaded = json.loads(json_data)
    json_deserialize_time = time.time() - start_time

    print(f"\nJSON:")
    print(f"  Serialize: {json_serialize_time:.4f}s")
    print(f"  Deserialize: {json_deserialize_time:.4f}s")
    print(f"  Size: {len(json_data.encode())} bytes")

    # Test MessagePack (if available)
    if MSGPACK_AVAILABLE:
        start_time = time.time()
        msgpack_data = msgpack.packb(test_data)
        msgpack_serialize_time = time.time() - start_time

        start_time = time.time()
        msgpack_loaded = msgpack.unpackb(msgpack_data)
        msgpack_deserialize_time = time.time() - start_time

        print(f"\nMessagePack:")
        print(f"  Serialize: {msgpack_serialize_time:.4f}s")
        print(f"  Deserialize: {msgpack_deserialize_time:.4f}s")
        print(f"  Size: {len(msgpack_data)} bytes")
        print(
            f"  Size reduction: {((len(json_data.encode()) - len(msgpack_data)) / len(json_data.encode()) * 100):.1f}%"
        )

    # Test Pickle (for comparison - NOT recommended for untrusted data)
    start_time = time.time()
    pickle_data = pickle.dumps(test_data)
    pickle_serialize_time = time.time() - start_time

    start_time = time.time()
    pickle_loaded = pickle.loads(pickle_data)
    pickle_deserialize_time = time.time() - start_time

    print(f"\nPickle (⚠️ NOT SAFE for untrusted data):")
    print(f"  Serialize: {pickle_serialize_time:.4f}s")
    print(f"  Deserialize: {pickle_deserialize_time:.4f}s")
    print(f"  Size: {len(pickle_data)} bytes")

    # Test Secure Pickle
    secret_key = os.urandom(32)
    secure_pickle = SecurePickleHandler(secret_key)

    start_time = time.time()
    secure_pickle_data = secure_pickle.secure_dumps(test_data)
    secure_pickle_serialize_time = time.time() - start_time

    start_time = time.time()
    secure_pickle_loaded = secure_pickle.secure_loads(secure_pickle_data)
    secure_pickle_deserialize_time = time.time() - start_time

    print(f"\nSecure Pickle (with HMAC):")
    print(f"  Serialize: {secure_pickle_serialize_time:.4f}s")
    print(f"  Deserialize: {secure_pickle_deserialize_time:.4f}s")
    print(f"  Size: {len(secure_pickle_data)} bytes (includes signature)")


def save_examples_to_files():
    """Save example serialized data to files for inspection."""
    print("\n" + "=" * 60)
    print("SAVING EXAMPLES TO FILES")
    print("=" * 60)

    os.makedirs("data", exist_ok=True)

    # Sample data
    sample_user = User(
        user_id=3001,
        username="example_user",
        email="example@test.com",
        created_at=datetime.now().isoformat(),
        permissions=["read", "write"],
        preferences={"theme": "dark", "language": "en"},
    )

    # Save as JSON
    with open("data/safe_user.json", "w") as f:
        json.dump(asdict(sample_user), f, indent=2)
    print("✅ Saved JSON example: data/safe_user.json")

    # Save as MessagePack (if available)
    if MSGPACK_AVAILABLE:
        with open("data/safe_user.msgpack", "wb") as f:
            msgpack.pack(asdict(sample_user), f)
        print("✅ Saved MessagePack example: data/safe_user.msgpack")

    # Save as secure pickle
    secret_key = b"example_key_do_not_use_in_production_environments"
    secure_pickle = SecurePickleHandler(secret_key)

    with open("data/safe_user.secure_pickle", "wb") as f:
        f.write(secure_pickle.secure_dumps(sample_user))
    print("✅ Saved secure pickle example: data/safe_user.secure_pickle")

    # Save the key for reference (NEVER do this in production!)
    with open("data/example_key.txt", "w") as f:
        f.write(f"Example key (HEX): {secret_key.hex()}\n")
        f.write("WARNING: This is for educational purposes only!\n")
        f.write("NEVER store keys in plaintext in production!\n")
    print("⚠️  Saved example key: data/example_key.txt (for educational purposes only)")


def main():
    """Main demonstration function."""
    print("Python Safe Serialization Alternatives")
    print("=" * 60)
    print("This demonstrates secure alternatives to unsafe pickle usage.")
    print("✅ These patterns are SAFE for production use!")
    print("=" * 60)

    demonstrate_json_serialization()
    demonstrate_msgpack_serialization()
    demonstrate_secure_pickle()
    demonstrate_custom_serialization()
    demonstrate_performance_comparison()
    save_examples_to_files()

    print("\n" + "=" * 60)
    print("🎓 SAFE SERIALIZATION SUMMARY")
    print("=" * 60)
    print("Recommendations by use case:")
    print()
    print("🌐 Web APIs & Untrusted Data:")
    print("   → Use JSON (human-readable, widely supported)")
    print("   → Use MessagePack (binary, more efficient)")
    print()
    print("🏢 Internal Systems & Trusted Data:")
    print("   → Use JSON/MessagePack for simple data")
    print("   → Use secure pickle with HMAC for complex objects")
    print("   → Use custom serialization for maximum control")
    print()
    print("🚫 Never Use Regular Pickle For:")
    print("   → Data from external sources")
    print("   → Data transmitted over networks")
    print("   → Data stored in accessible locations")
    print("   → Any untrusted data!")
    print("=" * 60)


if __name__ == "__main__":
    main()
