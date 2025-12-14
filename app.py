from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from openai import OpenAI

from utils import init_db, save_summary, generate_pdf

# --------------------------------------------------
# Setup
# --------------------------------------------------

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
API_SECRET_KEY = os.getenv("API_SECRET_KEY")

client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

app = Flask(__name__)

os.makedirs("storage", exist_ok=True)
os.makedirs("pdfs", exist_ok=True)

init_db()


# --------------------------------------------------
# Helpers
# --------------------------------------------------

def authorize(req):
    return req.headers.get("x-api-key") == API_SECRET_KEY


# --------------------------------------------------
# Routes
# --------------------------------------------------

@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "SpeakSpace workflow API running"}), 200


@app.route("/api/generate-summary", methods=["POST"])
def generate_summary():
    if not authorize(request):
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json() or {}

    prompt_text = data.get("prompt")
    note_id = data.get("note_id", "unknown")
    timestamp = data.get("timestamp", "")

    if not prompt_text:
        return jsonify({"error": "Prompt missing"}), 400

    # --------------------------------------------------
    # AI Summary Generation
    # --------------------------------------------------

    try:
        if not client:
            raise Exception("OpenAI client unavailable")

        response = client.responses.create(
            model="gpt-4o-mini",
            input=[
                {
                    "role": "system",
                    "content": (
                        "You are a medical documentation assistant. "
                        "Convert the input into a SOAP-style medical summary "
                        "(Subjective, Objective, Assessment, Plan). "
                        "Do NOT provide medical advice."
                    )
                },
                {
                    "role": "user",
                    "content": prompt_text
                }
            ]
        )

        summary_text = response.output_text

    except Exception:
        summary_text = (
            "SOAP SUMMARY (Fallback)\n\n"
            f"Subjective: {prompt_text}\n"
            "Objective: Voice journal data\n"
            "Assessment: Automated summary generated\n"
            "Plan: Review by clinician"
        )

    # --------------------------------------------------
    # Persist Results
    # --------------------------------------------------

    pdf_path = generate_pdf(summary_text, note_id)
    save_summary(note_id, timestamp, summary_text, pdf_path)

    # --------------------------------------------------
    # SpeakSpace-Compatible Response
    # --------------------------------------------------
return jsonify({
    "status": "success",
    "pdf_url": f"http://127.0.0.1:5000/{pdf_path}"
}), 200



# --------------------------------------------------
# Run
# --------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
