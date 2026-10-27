import os

import psycopg
from flask import Flask, jsonify, request
from psycopg.rows import dict_row

app = Flask(__name__)


def connection_string():
    return (
        f"host={os.getenv('DB_HOST', 'db')} "
        f"port={os.getenv('DB_PORT', '5432')} "
        f"dbname={os.getenv('POSTGRES_DB', 'portfolio_demo')} "
        f"user={os.getenv('POSTGRES_USER', 'demo')} "
        f"password={os.getenv('POSTGRES_PASSWORD', 'local_demo_only')}"
    )


def init_db():
    with psycopg.connect(connection_string()) as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS notes ("
            "id SERIAL PRIMARY KEY, text VARCHAR(500) NOT NULL, "
            "created_at TIMESTAMPTZ NOT NULL DEFAULT NOW())"
        )


@app.get("/health")
def health():
    try:
        with psycopg.connect(connection_string(), connect_timeout=2) as conn:
            conn.execute("SELECT 1")
        return jsonify(status="ok", database="connected"), 200
    except psycopg.Error:
        return jsonify(status="degraded", database="unavailable"), 503


@app.get("/notes")
def list_notes():
    with psycopg.connect(connection_string(), row_factory=dict_row) as conn:
        rows = conn.execute(
            "SELECT id, text, created_at FROM notes ORDER BY id DESC"
        ).fetchall()
    return jsonify(notes=[{**row, "created_at": row["created_at"].isoformat()} for row in rows])


@app.post("/notes")
def create_note():
    payload = request.get_json(silent=True) or {}
    text = payload.get("text")
    if not isinstance(text, str) or not text.strip() or len(text) > 500:
        return jsonify(error="Provide a non-empty text value of at most 500 characters."), 400

    with psycopg.connect(connection_string(), row_factory=dict_row) as conn:
        row = conn.execute(
            "INSERT INTO notes (text) VALUES (%s) RETURNING id, text, created_at",
            (text.strip(),),
        ).fetchone()
    return jsonify(note={**row, "created_at": row["created_at"].isoformat()}), 201


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=8000)
