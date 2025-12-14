SpeakSpace Voice-to-SOAP Workflow API
Overview

This project implements a backend workflow API that converts voice-based notes into structured SOAP medical summaries and generates PDF documentation stored server-side for later retrieval or downstream integration.
It is designed specifically for SpeakSpace Custom Actions, enabling automated execution of clinical documentation workflows from voice inputs.

The system focuses on intent execution rather than passive transcription, transforming raw spoken input into a structured, persistent artifact suitable for review, sharing, or integration into healthcare workflows.

Key Features

Converts voice-transcribed text into SOAP-style medical summaries

Uses AI to organize content into:

Subjective

Objective

Assessment

Plan

Generates PDF reports automatically

Stores summaries and metadata in a database

Secured using API-key–based authorization

Designed for SpeakSpace Custom Action compatibility using the official workflow specification

Modular architecture enabling future scalability and integration

Workflow
Voice Input (SpeakSpace)
        ↓
Configured Prompt
        ↓
SOAP Summary Generation (AI / Fallback)
        ↓
PDF Generation
        ↓
Database Storage
        ↓
Execution Confirmation to SpeakSpace

Tech Stack

Backend: Flask (Python)

AI: OpenAI API (GPT-4o-mini)

Database: SQLite

Document Generation: FPDF

Environment Management: python-dotenv

Project Structure
sampleUnstop/
│
├── app.py            # Flask API and workflow orchestration
├── utils.py          # Database and PDF utilities
├── storage/
│   └── records.db    # SQLite database
├── pdfs/             # Generated SOAP summary PDFs
├── .env.example      # Environment variable template
└── README.md

API Endpoint
Generate SOAP Summary

POST /api/generate-summary

Headers
Content-Type: application/json
x-api-key: <API_SECRET_KEY>

Request Body
{
  "prompt": "Patient reports stress and sleep issues for one week.",
  "note_id": "note_001",
  "timestamp": "2025-01-13T10:30:00"
}

Response
{
  "status": "success"
}


The API intentionally returns a minimal response, as SpeakSpace actions do not require large payloads or UI rendering.

SpeakSpace Integration

This API is intended to be configured as a SpeakSpace Custom Action.

Action Configuration (SpeakSpace Dashboard)

Method: POST

API URL:

https://<your-public-url>/api/generate-summary

Headers
Content-Type: application/json
x-api-key: <API_SECRET_KEY>

Prompt Template
Convert the following voice note into a SOAP-style medical summary:

{{note.content}}

Why utils.py Exists

The project intentionally separates concerns:

app.py

Handles API routing

Authorization

Workflow orchestration

utils.py

Database operations

PDF generation logic

This separation allows storage engines, file systems, or export formats to be replaced without modifying the core workflow logic, improving maintainability and scalability.

Error Handling & Fallback Strategy

If the AI service is unavailable or rate-limited, a fallback SOAP summary is generated

This ensures the workflow completes reliably even during external service failures

Errors are handled server-side and logged for debugging and observability

Current Limitations

Storage is local (SQLite and server filesystem)

PDFs are stored server-side and not directly attached back into SpeakSpace

SpeakSpace integration has been validated via API-level testing and dashboard configuration; full end-to-end testing requires Workflow Module access

These constraints are intentional to prioritize workflow correctness, clarity, and reliability within the hackathon scope.



Future Enhancements

Cloud database and object storage (PostgreSQL + S3)

User-level and multi-tenant support

Workflow execution status tracking (pending / completed / failed)

Automatic attachment of generated PDFs back into SpeakSpace notes

Webhooks for EHR systems or clinician notification workflows

How to Run Locally
pip install -r requirements.txt
python app.py


The API will be available at:

http://127.0.0.1:5000

Summary

This project demonstrates a real-world voice-first workflow pattern: converting spoken intent into structured medical documentation through automation.
It is designed to be integration-ready, extendable, and aligned with SpeakSpace’s vision of actionable voice-driven systems, while maintaining a clear and honest MVP scope suitable for real deployment.