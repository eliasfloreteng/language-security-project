"""
Vulnerable Application - Unsafe Pickle Deserialization
======================================================

This module demonstrates a vulnerable application that unsafely deserializes
pickle data from untrusted sources. This is a common security vulnerability.

⚠️  DANGER: This code contains intentional security vulnerabilities!
⚠️  EDUCATIONAL USE ONLY - Never use patterns like this in production!
"""

import pickle
import base64
import os
import tempfile
from datetime import datetime
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Simple in-memory storage for demonstration
app_data = {"sessions": {}, "user_preferences": {}, "uploaded_objects": []}


class UserSession:
    """Simple user session class."""

    def __init__(self, username, login_time=None):
        self.username = username
        self.login_time = login_time or datetime.now()
        self.permissions = ["read"]

    def __str__(self):
        return f"Session for {self.username} at {self.login_time}"


class UserPreferences:
    """User preferences class."""

    def __init__(self, theme="light", language="en", notifications=True):
        self.theme = theme
        self.language = language
        self.notifications = notifications


# HTML template for the web interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Vulnerable Pickle App - Educational Demo</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .warning { background: #ffebee; border: 2px solid #f44336; padding: 15px; margin: 20px 0; border-radius: 4px; }
        .endpoint { background: #f8f9fa; border: 1px solid #dee2e6; padding: 15px; margin: 10px 0; border-radius: 4px; }
        .method { display: inline-block; padding: 4px 8px; background: #007bff; color: white; border-radius: 3px; font-size: 12px; margin-right: 10px; }
        .vulnerable { color: #dc3545; font-weight: bold; }
        textarea { width: 100%; min-height: 100px; font-family: monospace; }
        button { background: #007bff; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; }
        button:hover { background: #0056b3; }
        .result { background: #e8f5e9; border: 1px solid #4caf50; padding: 10px; margin: 10px 0; border-radius: 4px; }
        .error { background: #ffebee; border: 1px solid #f44336; padding: 10px; margin: 10px 0; border-radius: 4px; }
        pre { background: #f8f9fa; padding: 10px; border-radius: 4px; overflow-x: auto; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚨 Vulnerable Pickle Application</h1>
        
        <div class="warning">
            <h3>⚠️ EDUCATIONAL WARNING</h3>
            <p>This application contains <strong>intentional security vulnerabilities</strong> for educational purposes only!</p>
            <p>Never use these patterns in production code!</p>
        </div>
        
        <h2>Available Endpoints</h2>
        
        <div class="endpoint">
            <h3><span class="method">POST</span>/upload_session <span class="vulnerable">[VULNERABLE]</span></h3>
            <p>Upload a base64-encoded pickled user session object.</p>
            <form action="/upload_session" method="post">
                <textarea name="data" placeholder="Enter base64-encoded pickle data here..."></textarea><br><br>
                <button type="submit">Upload Session</button>
            </form>
        </div>
        
        <div class="endpoint">
            <h3><span class="method">POST</span>/load_preferences <span class="vulnerable">[VULNERABLE]</span></h3>
            <p>Load user preferences from a pickle file.</p>
            <form action="/load_preferences" method="post" enctype="multipart/form-data">
                <input type="file" name="file" accept=".pkl"><br><br>
                <button type="submit">Load Preferences</button>
            </form>
        </div>
        
        <div class="endpoint">
            <h3><span class="method">POST</span>/process_object <span class="vulnerable">[VULNERABLE]</span></h3>
            <p>Process any pickled Python object sent as raw POST data.</p>
            <textarea id="rawData" placeholder="Paste raw pickle data here..."></textarea><br><br>
            <button onclick="sendRawData()">Send Raw Data</button>
        </div>
        
        <div class="endpoint">
            <h3><span class="method">GET</span>/status</h3>
            <p>View current application status (safe endpoint).</p>
            <a href="/status"><button>View Status</button></a>
        </div>
        
        <h2>Sample Valid Data</h2>
        <p>For testing purposes, here's a base64-encoded safe user session:</p>
        <pre id="sampleData">{{ sample_data }}</pre>
        <button onclick="copySample()">Copy Sample Data</button>
        
        <script>
            function copySample() {
                const sample = document.getElementById('sampleData').textContent;
                navigator.clipboard.writeText(sample).then(() => {
                    alert('Sample data copied to clipboard!');
                });
            }
            
            function sendRawData() {
                const data = document.getElementById('rawData').value;
                if (!data.trim()) {
                    alert('Please enter some data');
                    return;
                }
                
                fetch('/process_object', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/octet-stream',
                    },
                    body: data
                })
                .then(response => response.json())
                .then(result => {
                    alert('Response: ' + JSON.stringify(result, null, 2));
                })
                .catch(error => {
                    alert('Error: ' + error);
                });
            }
        </script>
    </div>
</body>
</html>
"""


@app.route("/")
def index():
    """Main page with vulnerability demonstration interface."""
    # Create sample safe data for testing
    sample_session = UserSession("test_user")
    sample_data = base64.b64encode(pickle.dumps(sample_session)).decode()

    return render_template_string(HTML_TEMPLATE, sample_data=sample_data)


@app.route("/upload_session", methods=["POST"])
def upload_session():
    """
    VULNERABLE: Accepts base64-encoded pickle data and deserializes it.

    This endpoint demonstrates the classic pickle deserialization vulnerability.
    An attacker can send malicious pickle data to execute arbitrary code.
    """
    try:
        data = request.form.get("data", "").strip()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        print(f"[VULNERABLE] Received base64 data: {data[:50]}...")

        # VULNERABILITY: Blindly decode and unpickle user data
        decoded_data = base64.b64decode(data)
        print(f"[VULNERABLE] Decoded pickle data, attempting to unpickle...")

        # This is where the attack happens!
        user_session = pickle.loads(decoded_data)

        # Store the session
        session_id = len(app_data["sessions"])
        app_data["sessions"][session_id] = user_session

        return jsonify(
            {
                "success": True,
                "message": f"Session uploaded successfully",
                "session_id": session_id,
                "session_info": str(user_session),
            }
        )

    except Exception as e:
        print(f"[ERROR] Exception during unpickling: {e}")
        return jsonify({"error": f"Failed to process session: {str(e)}"}), 500


@app.route("/load_preferences", methods=["POST"])
def load_preferences():
    """
    VULNERABLE: Loads pickle files from uploaded files.

    This demonstrates file-based pickle attacks where malicious
    pickle files can be uploaded and executed.
    """
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "No file selected"}), 400

        print(f"[VULNERABLE] Received file: {file.filename}")

        # VULNERABILITY: Directly unpickle uploaded file content
        file_data = file.read()
        print(
            f"[VULNERABLE] File size: {len(file_data)} bytes, attempting to unpickle..."
        )

        # This is where file-based attacks happen!
        preferences = pickle.loads(file_data)

        # Store preferences
        pref_id = len(app_data["user_preferences"])
        app_data["user_preferences"][pref_id] = preferences

        return jsonify(
            {
                "success": True,
                "message": "Preferences loaded successfully",
                "preference_id": pref_id,
                "preferences": str(preferences),
            }
        )

    except Exception as e:
        print(f"[ERROR] Exception during file unpickling: {e}")
        return jsonify({"error": f"Failed to load preferences: {str(e)}"}), 500


@app.route("/process_object", methods=["POST"])
def process_object():
    """
    VULNERABLE: Processes raw pickle data from POST body.

    This demonstrates direct pickle deserialization of raw data,
    which is another common attack vector.
    """
    try:
        raw_data = request.get_data()
        if not raw_data:
            return jsonify({"error": "No data provided"}), 400

        print(f"[VULNERABLE] Received raw data: {len(raw_data)} bytes")
        print(f"[VULNERABLE] Data preview: {raw_data[:50]}...")

        # VULNERABILITY: Direct unpickling of raw POST data
        print(f"[VULNERABLE] Attempting to unpickle raw data...")

        # This is where raw data attacks happen!
        obj = pickle.loads(raw_data)

        # Store object
        obj_id = len(app_data["uploaded_objects"])
        app_data["uploaded_objects"].append(obj)

        return jsonify(
            {
                "success": True,
                "message": "Object processed successfully",
                "object_id": obj_id,
                "object_info": str(obj),
            }
        )

    except Exception as e:
        print(f"[ERROR] Exception during raw data unpickling: {e}")
        return jsonify({"error": f"Failed to process object: {str(e)}"}), 500


@app.route("/status")
def status():
    """Safe endpoint that shows current application status."""
    return jsonify(
        {
            "status": "running",
            "sessions": len(app_data["sessions"]),
            "preferences": len(app_data["user_preferences"]),
            "objects": len(app_data["uploaded_objects"]),
            "warning": "This application contains intentional vulnerabilities for educational purposes",
        }
    )


def create_sample_files():
    """Create sample files for demonstration."""
    os.makedirs("data", exist_ok=True)

    # Create a safe preferences file
    safe_prefs = UserPreferences(theme="dark", language="en", notifications=False)
    with open("data/safe_preferences.pkl", "wb") as f:
        pickle.dump(safe_prefs, f)

    print("Created sample files in data/ directory")


def main():
    """Main function to run the vulnerable application."""
    print("=" * 60)
    print("🚨 VULNERABLE PICKLE APPLICATION - EDUCATIONAL DEMO")
    print("=" * 60)
    print("⚠️  WARNING: This application contains intentional vulnerabilities!")
    print("⚠️  DO NOT USE IN PRODUCTION!")
    print("⚠️  FOR EDUCATIONAL PURPOSES ONLY!")
    print("=" * 60)
    print()
    print("This Flask application demonstrates common pickle vulnerabilities:")
    print("1. Base64-encoded pickle deserialization")
    print("2. File upload with pickle loading")
    print("3. Raw POST data pickle processing")
    print()
    print("Starting server on http://127.0.0.1:5000")
    print("Use Ctrl+C to stop the server")
    print("=" * 60)

    create_sample_files()
    app.run(host="127.0.0.1", port=5000, debug=True)


if __name__ == "__main__":
    main()
