from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/extract_text", methods=["POST"])
def extract_text():
    try:
        # Parse JSON body
        data = request.get_json(force=True)  # forces parsing even if no Content-Type header

        # Validate input
        file_url = data.get("file_url")
        if not file_url:
            return jsonify({"error": "Missing 'file_url' in request body"}), 400

        # Download PDF
        response = requests.get(file_url)
        if response.status_code != 200:
            return jsonify({"error": "Failed to download file"}), 400

        pdf_content = response.content

        # Here you would extract text from PDF
        # Placeholder result
        extracted_text = "Simulated extracted text from PDF"

        return jsonify({"text": extracted_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
