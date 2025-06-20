import pickle
import hmac
import hashlib


def run_secure_app():
    print("Secure application is attempting to load data...")
    with open("malicious_hmac_valid.pickle", "rb") as f:
        print("Reading malicious_hmac_valid.pickle...")
        # Read the signature and pickled data
        signature = f.readline().strip()
        pickled_data = f.read()

        # Verify the HMAC signature
        expected_signature = hmac.new(
            b"secret_key", pickled_data, hashlib.sha256
        ).digest()
        if signature != expected_signature:
            raise ValueError("Invalid signature! Data may have been tampered with.")

        # Load the pickled data
        data = pickle.loads(pickled_data)
        print(f"Successfully unpickled: {data}")

    with open("malicious_hmac_invalid.pickle", "rb") as f:
        print("Reading malicious_hmac_invalid.pickle...")
        # Read the signature and pickled data
        signature = f.readline().strip()
        pickled_data = f.read()

        # Verify the HMAC signature
        expected_signature = hmac.new(
            b"secret_key", pickled_data, hashlib.sha256
        ).digest()
        if signature != expected_signature:
            raise ValueError("Invalid signature! Data may have been tampered with.")

        # Load the pickled data
        data = pickle.loads(pickled_data)
        print(f"Successfully unpickled: {data}")


if __name__ == "__main__":
    run_secure_app()
