from flask import Flask, request, jsonify
import requests
import pdfplumber
from io import BytesIO

app = Flask(__name__)

@app.route("/extract_text", methods=["POST"])
def extract_text():
    data = request.get_json()
    file_url = data.get("file_url")
    if not file_url:
        return jsonify({"error": "Missing file_url"}), 400

    response = requests.get(file_url)
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch PDF"}), 400

    with pdfplumber.open(BytesIO(response.content)) as pdf:
        text = "\n".join(page.extract_text() or "" for page in pdf.pages)

    return jsonify({"extracted_text": text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
