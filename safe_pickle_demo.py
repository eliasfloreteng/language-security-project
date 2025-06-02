"""
Safe Pickle Demonstration
=========================

This module demonstrates the legitimate and safe usage of Python's pickle module.
Pickle is designed for serializing Python objects for storage or transmission.

WARNING: This is for educational purposes only. Never unpickle untrusted data!
"""

import pickle
import tempfile
import os
from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class User:
    """Example class to demonstrate object serialization."""

    name: str
    age: int
    email: str

    def __str__(self):
        return f"User(name='{self.name}', age={self.age}, email='{self.email}')"


@dataclass
class GameState:
    """Example game state for demonstrating complex object serialization."""

    player_name: str
    level: int
    score: int
    inventory: List[str]
    settings: Dict[str, Any]


def demonstrate_basic_types():
    """Demonstrate pickling of basic Python types."""
    print("=== Basic Types Pickle Demo ===")

    # Basic types
    data_types = {
        "string": "Hello, World!",
        "integer": 42,
        "float": 3.14159,
        "list": [1, 2, 3, 4, 5],
        "dict": {"key1": "value1", "key2": "value2"},
        "tuple": (1, 2, 3),
        "set": {1, 2, 3, 4, 5},
    }

    for type_name, data in data_types.items():
        # Serialize
        pickled = pickle.dumps(data)
        # Deserialize
        unpickled = pickle.loads(pickled)

        print(f"{type_name:10}: {data} -> {unpickled} (Match: {data == unpickled})")


def demonstrate_custom_objects():
    """Demonstrate pickling of custom objects."""
    print("\n=== Custom Objects Pickle Demo ===")

    # Create a user object
    user = User(name="Alice", age=30, email="alice@example.com")
    print(f"Original: {user}")

    # Serialize the user object
    pickled_user = pickle.dumps(user)
    print(f"Pickled size: {len(pickled_user)} bytes")

    # Deserialize the user object
    unpickled_user = pickle.loads(pickled_user)
    print(f"Unpickled: {unpickled_user}")
    print(f"Objects equal: {user == unpickled_user}")


def demonstrate_complex_objects():
    """Demonstrate pickling of complex nested objects."""
    print("\n=== Complex Objects Pickle Demo ===")

    # Create a complex game state
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

    print(f"Original game state:")
    print(f"  Player: {game_state.player_name}")
    print(f"  Level: {game_state.level}")
    print(f"  Score: {game_state.score}")
    print(f"  Inventory: {game_state.inventory}")
    print(f"  Settings: {game_state.settings}")

    # Serialize
    pickled_state = pickle.dumps(game_state)
    print(f"\nPickled size: {len(pickled_state)} bytes")

    # Deserialize
    unpickled_state = pickle.loads(pickled_state)
    print(f"\nObjects equal: {game_state == unpickled_state}")


def demonstrate_file_operations():
    """Demonstrate saving and loading pickle data to/from files."""
    print("\n=== File Operations Demo ===")

    # Create sample data
    data = {
        "users": [
            User("Alice", 30, "alice@example.com"),
            User("Bob", 25, "bob@example.com"),
            User("Charlie", 35, "charlie@example.com"),
        ],
        "metadata": {"created_at": "2024-01-01", "version": "1.0", "total_users": 3},
    }

    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)

    # Save to file
    filename = "data/safe_data.pkl"
    with open(filename, "wb") as f:
        pickle.dump(data, f)
    print(f"Data saved to {filename}")

    # Load from file
    with open(filename, "rb") as f:
        loaded_data = pickle.load(f)

    print(f"Data loaded successfully!")
    print(f"Number of users: {len(loaded_data['users'])}")
    print(f"Metadata: {loaded_data['metadata']}")

    # Verify data integrity
    original_users = [str(user) for user in data["users"]]
    loaded_users = [str(user) for user in loaded_data["users"]]
    print(f"Data integrity check: {original_users == loaded_users}")


def main():
    """Main demonstration function."""
    print("Python Pickle - Safe Usage Demonstration")
    print("=" * 50)
    print("This demonstrates the legitimate uses of Python's pickle module.")
    print("Remember: NEVER unpickle data from untrusted sources!\n")

    demonstrate_basic_types()
    demonstrate_custom_objects()
    demonstrate_complex_objects()
    demonstrate_file_operations()

    print("\n" + "=" * 50)
    print("Safe pickle demonstration completed.")
    print("All operations used trusted, locally-generated data.")


if __name__ == "__main__":
    main()
