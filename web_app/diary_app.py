from flask import Flask, request, send_file, render_template_string
import pickle
import io

app = Flask(__name__)


class Diary:
    def __init__(self, content=""):
        self.content = content


# Global diary object
diary_object = Diary("Welcome to your diary!")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Simple Diary App</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        textarea { width: 80%; height: 200px; margin-bottom: 10px; }
        input[type="submit"], button { padding: 10px 15px; margin-right: 10px; cursor: pointer; }
    </style>
</head>
<body>
    <h1>Your Diary</h1>
    <form method="POST" action="/">
        <textarea name="diary_entry">{{ diary_content }}</textarea><br>
        <input type="submit" value="Save Diary">
    </form>

    <h2>Manage Diary Files</h2>
    <form method="GET" action="/download">
        <button type="submit">Download Diary (pickle)</button>
    </form>

    <form method="POST" action="/upload" enctype="multipart/form-data">
        <input type="file" name="diary_file">
        <input type="submit" value="Upload Diary (pickle)">
    </form>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def index():
    global diary_object
    if request.method == "POST":
        diary_object.content = request.form["diary_entry"]
    return render_template_string(HTML_TEMPLATE, diary_content=diary_object.content)


@app.route("/download")
def download_diary():
    global diary_object
    # Pickle the diary object
    pickled_data = pickle.dumps(diary_object)
    # Create a BytesIO object to serve the file from memory
    return send_file(
        io.BytesIO(pickled_data),
        mimetype="application/octet-stream",
        as_attachment=True,
        download_name="diary.pickle",
    )


@app.route("/upload", methods=["POST"])
def upload_diary():
    global diary_object
    if "diary_file" not in request.files:
        return "No file part", 400
    file = request.files["diary_file"]
    if file.filename == "":
        return "No selected file", 400
    if file:
        try:
            # Load the pickled data
            loaded_object = pickle.loads(file.read())
            # Assign the loaded object to diary_object
            diary_object = loaded_object
            return "Diary uploaded successfully! <a href='/'>Go back</a>"
        except Exception as e:
            return f"Error loading pickle file: {e}", 400
    return "Something went wrong", 500


if __name__ == "__main__":
    app.run(debug=True)
