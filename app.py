import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from utils import init_db, generate_pdf, save_summary

load_dotenv()

API_SECRET_KEY = os.getenv("API_SECRET_KEY")

app = Flask(__name__)

# Ensure folders exist
os.makedirs("storage", exist_ok=True)
os.makedirs("pdfs", exist_ok=True)

# Initialize DB
init_db()


@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "SpeakSpace workflow API running"})


@app.route("/api/generate-summary", methods=["POST"])
def generate_summary():
    # --- API Key validation ---
    api_key = request.headers.get("x-api-key")
    if api_key != API_SECRET_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()

    prompt = data.get("prompt")
    note_id = data.get("note_id")
    timestamp = data.get("timestamp")

    if not prompt or not note_id:
        return jsonify({"error": "Invalid request"}), 400

    # --- Generate SOAP summary ---
    soap_text = generate_soap_summary(prompt)

    # --- Generate PDF ---
    pdf_path = generate_pdf(note_id, soap_text)

    # --- Save to DB ---
    save_record(note_id, prompt, soap_text, pdf_path, timestamp)

    # --- SpeakSpace expects minimal response ---
    return jsonify({"status": "success"})
    

if __name__ == "__main__":
    app.run(debug=True)
