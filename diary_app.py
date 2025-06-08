from flask import Flask, request, send_file, render_template_string
import pickle
import io

app = Flask(__name__)

# Simple in-memory diary storage
diary_content = ""

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
    global diary_content
    if request.method == "POST":
        diary_content = request.form["diary_entry"]
    return render_template_string(HTML_TEMPLATE, diary_content=diary_content)


@app.route("/download")
def download_diary():
    global diary_content
    # Pickle the diary content
    pickled_data = pickle.dumps(diary_content)
    # Create a BytesIO object to serve the file from memory
    return send_file(
        io.BytesIO(pickled_data),
        mimetype="application/octet-stream",
        as_attachment=True,
        download_name="diary.pickle",
    )


@app.route("/upload", methods=["POST"])
def upload_diary():
    global diary_content
    if "diary_file" not in request.files:
        return "No file part", 400
    file = request.files["diary_file"]
    if file.filename == "":
        return "No selected file", 400
    if file:
        try:
            # Load the pickled data
            loaded_data = pickle.loads(file.read())
            # Assuming the loaded data is a string for the diary content
            if isinstance(loaded_data, str):
                diary_content = loaded_data
                return "Diary uploaded successfully! <a href='/'>Go back</a>"
            else:
                return "Invalid pickle file content. Expected a string.", 400
        except Exception as e:
            return f"Error loading pickle file: {e}", 400
    return "Something went wrong", 500


if __name__ == "__main__":
    app.run(debug=True)
