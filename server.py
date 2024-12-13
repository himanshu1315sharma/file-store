from flask import Flask, request, jsonify, abort
import os
import hashlib

app = Flask(__name__)

# In-memory metadata storage
file_store = {}
storage_dir = "/app/files"
os.makedirs(storage_dir, exist_ok=True)


# Helper to compute file hash
def compute_hash(content):
    return hashlib.sha256(content).hexdigest()


@app.route("/files", methods=["POST"])
def add_files():
    if "files" not in request.files:
        return jsonify({"error": "No files provided"}), 400

    uploaded_files = request.files.getlist("files")
    response = {}

    for uploaded_file in uploaded_files:
        file_content = uploaded_file.read()
        file_hash = compute_hash(file_content)

        if file_hash in file_store:
            response[uploaded_file.filename] = "File already exists"
        else:
            file_path = os.path.join(storage_dir, uploaded_file.filename)
            with open(file_path, "wb") as f:
                f.write(file_content)

            file_store[file_hash] = {
                "name": uploaded_file.filename,
                "path": file_path,
            }
            response[uploaded_file.filename] = "File uploaded successfully"

    return jsonify(response), 200


@app.route("/files", methods=["GET"])
def list_files():
    return jsonify([data["name"] for data in file_store.values()])



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000,debug=True)
