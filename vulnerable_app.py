#!/usr/bin/env python3
"""
Vulnerable Flask Application - Pickle Deserialization Demo
This application demonstrates a critical security vulnerability where
user-supplied pickled data is deserialized without validation.

WARNING: This code is intentionally vulnerable and for educational purposes only.
Never run this in a production environment or expose it to the internet.
"""

import pickle
import base64
import os
from flask import Flask, request, render_template_string, jsonify

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Vulnerable Pickle Demo</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .container { max-width: 800px; margin: 0 auto; }
        .warning { background: #ffebee; padding: 20px; border-left: 4px solid #f44336; margin-bottom: 20px; }
        .form-group { margin-bottom: 15px; }
        textarea { width: 100%; height: 200px; font-family: monospace; }
        button { background: #2196F3; color: white; padding: 10px 20px; border: none; cursor: pointer; }
        .result { background: #f5f5f5; padding: 15px; margin-top: 20px; border-radius: 4px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🥒 Vulnerable Pickle Deserialization Demo</h1>
        
        <div class="warning">
            <strong>⚠️ WARNING:</strong> This application is intentionally vulnerable for educational purposes.
            It demonstrates how pickle deserialization can lead to arbitrary code execution.
        </div>

        <h2>Upload Pickled Data</h2>
        <form action="/process_pickle" method="post" enctype="multipart/form-data">
            <div class="form-group">
                <label for="pickle_file">Upload Pickle File:</label><br>
                <input type="file" id="pickle_file" name="pickle_file" accept=".pkl,.pickle">
            </div>
            <button type="submit">Process Pickle File</button>
        </form>

        <h2>Submit Base64 Encoded Pickle</h2>
        <form action="/process_b64_pickle" method="post">
            <div class="form-group">
                <label for="pickle_data">Base64 Encoded Pickle Data:</label><br>
                <textarea name="pickle_data" placeholder="Paste base64 encoded pickle data here..."></textarea>
            </div>
            <button type="submit">Process Pickle Data</button>
        </form>

        <h2>Test with Safe Data</h2>
        <form action="/create_safe_pickle" method="post">
            <div class="form-group">
                <label for="test_data">Test Data (will be pickled safely):</label><br>
                <input type="text" name="test_data" value="Hello, World!" style="width: 100%; padding: 8px;">
            </div>
            <button type="submit">Create & Process Safe Pickle</button>
        </form>
    </div>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)


@app.route("/process_pickle", methods=["POST"])
def process_pickle():
    """
    Vulnerable endpoint that processes uploaded pickle files.
    This demonstrates file-based pickle attacks.
    """
    try:
        if "pickle_file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["pickle_file"]
        if file.filename == "":
            return jsonify({"error": "No file selected"}), 400

        # Read the pickle file content
        pickle_data = file.read()

        # VULNERABLE: Directly unpickling user-supplied data
        print(f"[VULNERABLE] Processing pickle file: {file.filename}")
        print(f"[VULNERABLE] Pickle data size: {len(pickle_data)} bytes")

        # This is where the attack happens!
        deserialized_data = pickle.loads(pickle_data)

        return jsonify(
            {
                "success": True,
                "message": "Pickle processed successfully",
                "data_type": str(type(deserialized_data)),
                "data_repr": repr(deserialized_data)[:200],  # Limit output for safety
            }
        )

    except Exception as e:
        return jsonify(
            {"error": f"Error processing pickle: {str(e)}", "type": type(e).__name__}
        ), 500


@app.route("/process_b64_pickle", methods=["POST"])
def process_b64_pickle():
    """
    Vulnerable endpoint that processes base64-encoded pickle data.
    This simulates network-based pickle attacks.
    """
    try:
        pickle_b64 = request.form.get("pickle_data", "").strip()
        if not pickle_b64:
            return jsonify({"error": "No pickle data provided"}), 400

        # Decode base64 data
        try:
            pickle_data = base64.b64decode(pickle_b64)
        except Exception as e:
            return jsonify({"error": f"Invalid base64 data: {str(e)}"}), 400

        # VULNERABLE: Directly unpickling user-supplied data
        print(f"[VULNERABLE] Processing base64 pickle data")
        print(f"[VULNERABLE] Decoded size: {len(pickle_data)} bytes")

        # This is where the attack happens!
        deserialized_data = pickle.loads(pickle_data)

        return jsonify(
            {
                "success": True,
                "message": "Base64 pickle processed successfully",
                "data_type": str(type(deserialized_data)),
                "data_repr": repr(deserialized_data)[:200],  # Limit output for safety
            }
        )

    except Exception as e:
        return jsonify(
            {"error": f"Error processing pickle: {str(e)}", "type": type(e).__name__}
        ), 500


@app.route("/create_safe_pickle", methods=["POST"])
def create_safe_pickle():
    """
    Demonstrates safe pickle usage with trusted data.
    This shows how pickle works under normal circumstances.
    """
    try:
        test_data = request.form.get("test_data", "Default test data")

        # Create a safe pickle
        pickled_data = pickle.dumps(test_data)

        # Process it back (this is safe since we created it)
        unpickled_data = pickle.loads(pickled_data)

        return jsonify(
            {
                "success": True,
                "message": "Safe pickle created and processed",
                "original_data": test_data,
                "unpickled_data": unpickled_data,
                "pickle_size": len(pickled_data),
                "base64_pickle": base64.b64encode(pickled_data).decode("utf-8"),
            }
        )

    except Exception as e:
        return jsonify(
            {"error": f"Error with safe pickle: {str(e)}", "type": type(e).__name__}
        ), 500


@app.route("/info")
def info():
    """
    Provides information about the system for demonstration purposes.
    """
    return jsonify(
        {
            "message": "System Information",
            "python_version": os.sys.version,
            "working_directory": os.getcwd(),
            "user": os.environ.get("USER", "unknown"),
            "platform": os.sys.platform,
        }
    )


if __name__ == "__main__":
    print("=" * 60)
    print("🥒 VULNERABLE PICKLE DEMONSTRATION SERVER")
    print("=" * 60)
    print("⚠️  WARNING: This server is intentionally vulnerable!")
    print("   - Only use for educational purposes")
    print("   - Do not expose to the internet")
    print("   - Run in isolated environment only")
    print("=" * 60)
    print("📍 Server will start at: http://127.0.0.1:5000")
    print("🔗 Upload interface: http://127.0.0.1:5000/")
    print("📊 System info: http://127.0.0.1:5000/info")
    print("=" * 60)

    # Only bind to localhost for safety
    app.run(host="127.0.0.1", port=5000, debug=True)
