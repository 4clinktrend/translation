from flask import Flask, request, jsonify
import requests
import json
import tempfile
import os
from PyPDF2 import PdfReader

app = Flask(__name__)

@app.route("/extract_text", methods=["POST"])
def extract_text():
    try:
        # Ensure JSON is parsed correctly even if n8n sends it as raw string
        try:
            data = request.get_json(force=True)
        except:
            data = json.loads(request.get_data())

        file_url = data.get("file_url")
        if not file_url:
            return jsonify({"error": "Missing 'file_url'"}), 400

        # Download the PDF file
        response = requests.get(file_url)
        if response.status_code != 200:
            return jsonify({"error": "Failed to download PDF"}), 400

        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(response.content)
            tmp_path = tmp.name

        # Extract text
        reader = PdfReader(tmp_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""

        os.remove(tmp_path)
        return jsonify({"text": text.strip()})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run()
