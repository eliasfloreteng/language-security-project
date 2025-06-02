import pickle
import os
import sys

# Ensure the current directory is in the Python path for module imports
sys.path.insert(0, os.path.dirname(__file__))

from vulnerable_app import run_vulnerable_app
from exploit import generate_malicious_pickle


def create_benign_pickle():
    print("\n--- Step 1: Creating a benign pickled file ---")
    benign_data = {"message": "Hello, secure world!"}
    with open("data.pickle", "wb") as f:
        pickle.dump(benign_data, f)
    print("Benign data saved to data.pickle")


def simulate_attacker_tampering():
    print("\n--- Step 2: Simulating attacker tampering ---")
    print("An attacker replaces data.pickle with a malicious payload.")
    generate_malicious_pickle()


def run_vulnerable_application():
    print("\n--- Step 3: Running the vulnerable application ---")
    print("The vulnerable application will now attempt to load data.pickle.")
    run_vulnerable_app()


if __name__ == "__main__":
    # Clean up any existing data.pickle before starting
    if os.path.exists("data.pickle"):
        os.remove("data.pickle")

    create_benign_pickle()

    # Verify benign load (optional, but good for demonstration)
    print("\n--- Verifying benign load ---")
    run_vulnerable_app()

    simulate_attacker_tampering()
    run_vulnerable_application()

    print("\n--- Attack demonstration complete ---")
    print(
        "Check the output above for 'Malicious code executed!' to confirm the attack."
    )

    # Clean up generated pickle file
    if os.path.exists("data.pickle"):
        os.remove("data.pickle")
