import pickle
import hmac
import hashlib

def run_secure_app():
    print("Secure application is attempting to load data...")
    try:
        with open("secure.pickle", "rb") as f:
            # Read the signature and pickled data
            signature = f.readline().strip()
            pickled_data = f.read()

            # Verify the HMAC signature
            expected_signature = hmac.new(b'secret_key', pickled_data, hashlib.sha256).digest()
            if signature != expected_signature:
                raise ValueError("Invalid signature! Data may have been tampered with.")

            # Load the pickled data
            data = pickle.loads(pickled_data)
            print(f"Successfully unpickled: {data}")
    except Exception as e:
        print(f"An error occurred during unpickling: {e}")
        
if __name__ == "__main__":
    run_secure_app()