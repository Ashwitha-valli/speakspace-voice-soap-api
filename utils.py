import sqlite3
from datetime import datetime
from fpdf import FPDF
import os

DB_PATH = "storage/records.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS summaries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            note_id TEXT,
            timestamp TEXT,
            created_at TEXT,
            summary TEXT,
            pdf_path TEXT
        )
    """)
    conn.commit()
    conn.close()


def save_summary(note_id, timestamp, summary_text, pdf_path):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO summaries (note_id, timestamp, created_at, summary, pdf_path)
        VALUES (?, ?, ?, ?, ?)
    """, (
        note_id,
        timestamp,
        datetime.utcnow().isoformat(),
        summary_text,
        pdf_path
    ))
    conn.commit()
    conn.close()


def generate_pdf(summary_text, note_id):
    os.makedirs("pdfs", exist_ok=True)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    for line in summary_text.split("\n"):
        pdf.multi_cell(0, 8, line)

    filename = f"pdfs/summary_{note_id}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.pdf"
    pdf.output(filename)

    return filename
