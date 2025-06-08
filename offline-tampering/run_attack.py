import pickle
import os
import sys
import hmac
import hashlib

# Ensure the current directory is in the Python path for module imports
sys.path.insert(0, os.path.dirname(__file__))

from vulnerable_app import run_vulnerable_app
from exploit import generate_malicious_pickle
from secure_app import run_secure_app


def create_benign_pickle():
    print("\n--- Step 1a: Creating a benign pickled file ---")
    benign_data = {"message": "Hello, secure world!"}
    with open("benign.pickle", "wb") as f:
        pickle.dump(benign_data, f)
    print("Benign data saved to benign.pickle")

def create_secure_pickle():
    print("\n--- Step 1b: Creating a secure pickled file ---")
    benign_data = {"message": "Hello, secure world!"}
    with open("secure.pickle", "wb") as f:
        pickled_data = pickle.dumps(benign_data)
        # Create a HMAC signature for the pickled data
        signature = hmac.new(b'secret_key', pickled_data, hashlib.sha256).digest()
        # Write the pickled data and signature to the file
        f.write(signature + b'\n' + pickled_data)
    print("Secure pickled file created with HMAC signature.")


def simulate_attacker_tampering():
    print("\n--- Step 2: Simulating attacker tampering ---")
    print("An attacker replaces benign.pickle, secure.pickle with a malicious payload.")
    generate_malicious_pickle()


def run_vulnerable_application():
    print("\n--- Step 3a: Running the vulnerable application ---")
    print("The vulnerable application will now attempt to load benign.pickle.")
    run_vulnerable_app()
    
def run_secure_application():
    print("\n--- Step 3b: Running the secure application ---")
    print("The secure application will now attempt to load secure.pickle.")
    run_secure_app()

if __name__ == "__main__":
    # Clean up any existing pickle files before starting
    if os.path.exists("benign.pickle"):
        os.remove("benign.pickle")
    if os.path.exists("secure.pickle"):
        os.remove("secure.pickle")

    create_benign_pickle()
    create_secure_pickle()

    # Verify benign load (optional, but good for demonstration)
    print("\n--- Verifying benign load ---")
    run_vulnerable_app()
    
    # Verify secure load (optional, but good for demonstration)
    print("\n--- Verifying secure load ---")
    run_secure_app()

    simulate_attacker_tampering()
    run_vulnerable_application()
    run_secure_application()

    print("\n--- Attack demonstration complete ---")
    print(
        "Check the output above for 'Malicious code executed!' to confirm the attack."
    )

    # Clean up generated pickle file
    if os.path.exists("benign.pickle"):
        os.remove("benign.pickle")
    if os.path.exists("secure.pickle"):
        os.remove("secure.pickle")
