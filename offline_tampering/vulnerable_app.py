import pickle


def run_vulnerable_app():
    print("Vulnerable application is attempting to load data...")
    with open("malicious.pickle", "rb") as f:
        _signature = f.readline()
        data = pickle.load(f)
    print(f"Successfully unpickled: {data}")


if __name__ == "__main__":
    run_vulnerable_app()
