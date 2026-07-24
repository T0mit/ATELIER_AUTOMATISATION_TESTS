import sqlite3
import json
from datetime import datetime

DB_NAME = "test_history.db"

def init_db():
    """Initialise la table des runs si elle n'existe pas."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            api_name TEXT NOT NULL,
            passed INTEGER NOT NULL,
            failed INTEGER NOT NULL,
            error_rate REAL NOT NULL,
            latency_ms_avg REAL NOT NULL,
            latency_ms_p95 REAL NOT NULL,
            details_json TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def save_run(run_data):
    """Enregistre les résultats d'un run."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    summary = run_data["summary"]
    cursor.execute('''
        INSERT INTO runs (timestamp, api_name, passed, failed, error_rate, latency_ms_avg, latency_ms_p95, details_json)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        run_data["timestamp"],
        run_data["api"],
        summary["passed"],
        summary["failed"],
        summary["error_rate"],
        summary["latency_ms_avg"],
        summary["latency_ms_p95"],
        json.dumps(run_data["tests"])
    ))
    
    conn.commit()
    conn.close()

def list_runs(limit=20):
    """Récupère l'historique des runs récents."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM runs ORDER BY id DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    
    runs = []
    for row in rows:
        runs.append({
            "id": row["id"],
            "timestamp": row["timestamp"],
            "api": row["api_name"],
            "summary": {
                "passed": row["passed"],
                "failed": row["failed"],
                "error_rate": row["error_rate"],
                "latency_ms_avg": row["latency_ms_avg"],
                "latency_ms_p95": row["latency_ms_p95"]
            },
            "tests": json.loads(row["details_json"])
        })
    return runs

def get_latest_run():
    """Retourne le tout dernier run enregistré."""
    runs = list_runs(limit=1)
    return runs[0] if runs else None
