from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/extract_text', methods=['POST'])
def extract_text():
    # Force parsing of the body as JSON regardless of Content-Type
    data = request.get_json(force=True)

    if not data or 'file_url' not in data:
        return jsonify({"error": "Missing or invalid 'file_url'"}), 400

    file_url = data['file_url']

    # Placeholder for actual PDF extraction logic
    return jsonify({
        "message": "File URL received successfully",
        "file_url": file_url
    })
