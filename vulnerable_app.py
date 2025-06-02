import pickle


def run_vulnerable_app():
    print("Vulnerable application is attempting to load data...")
    try:
        with open("data.pickle", "rb") as f:
            data = pickle.load(f)
        print(f"Successfully unpickled: {data}")
    except Exception as e:
        print(f"An error occurred during unpickling: {e}")


if __name__ == "__main__":
    run_vulnerable_app()
