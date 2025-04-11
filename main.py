from flask import Flask, request, jsonify
from PyPDF2 import PdfReader
import requests
import io

app = Flask(__name__)

@app.route('/extract_text', methods=['POST'])
def extract_text():
    data = request.get_json()
    file_url = data.get('file_url')
    if not file_url:
        return jsonify({"error": "Missing file_url"}), 400

    try:
        response = requests.get(file_url)
        response.raise_for_status()
        reader = PdfReader(io.BytesIO(response.content))
        text = "\n".join(page.extract_text() or '' for page in reader.pages)
        return jsonify({"text": text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Bind to all interfaces and use dynamic Render port
import os
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
