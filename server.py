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


@app.route("/files/<filename>", methods=["DELETE"])
def delete_file(filename):
    for file_hash, metadata in file_store.items():
        if metadata["name"] == filename:
            os.remove(metadata["path"])
            del file_store[file_hash]
            return jsonify({"message": f"{filename} deleted successfully"}), 200

    return jsonify({"error": "File not found"}), 404


@app.route("/files/<filename>", methods=["PUT"])
def update_file(filename):
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    uploaded_file = request.files["file"]
    file_content = uploaded_file.read()
    file_hash = compute_hash(file_content)

    for hash_key, metadata in file_store.items():
        if metadata["name"] == filename:
            os.remove(metadata["path"])
            del file_store[hash_key]
            break

    file_path = os.path.join(storage_dir, filename)
    with open(file_path, "wb") as f:
        f.write(file_content)

    file_store[file_hash] = {"name": filename, "path": file_path}
    return jsonify({"message": f"{filename} updated successfully"}), 200


@app.route("/files/wordcount", methods=["GET"])
def word_count():
    total_words = 0
    for metadata in file_store.values():
        with open(metadata["path"], "r") as f:
            total_words += len(f.read().split())

    return jsonify({"word_count": total_words})


@app.route("/files/frequent", methods=["GET"])
def frequent_words():
    from collections import Counter

    limit = int(request.args.get("limit", 10))
    order = request.args.get("order", "desc").lower() == "desc"

    word_counter = Counter()
    for metadata in file_store.values():
        with open(metadata["path"], "r") as f:
            word_counter.update(f.read().split())

    most_common = word_counter.most_common(limit) if order else word_counter.most_common()[:-limit - 1:-1]
    return jsonify(dict(most_common))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000,debug=True)
