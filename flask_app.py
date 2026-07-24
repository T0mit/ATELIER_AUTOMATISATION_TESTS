from flask import Flask, render_template, jsonify, request
import storage
from tester.runner import execute_run

app = Flask(__name__)

# Initialise la base de données au démarrage
storage.init_db()

@app.route("/")
def index():
    return '<p>API Tester is running. Go to <a href="/dashboard">/dashboard</a></p>'

@app.route("/run", methods=["GET", "POST"])
def trigger_run():
    """Déclenche une session de test et enregistre le résultat dans SQLite."""
    run_result = execute_run()
    storage.save_run(run_result)
    return jsonify({"message": "Run completed successfully", "data": run_result})

@app.route("/dashboard")
def dashboard():
    """Affiche le tableau de bord avec le dernier run et l'historique."""
    runs = storage.list_runs(limit=15)
    latest = runs[0] if runs else None
    return render_template("dashboard.html", latest=latest, runs=runs)

# --- BONUS ENDPOINTS ---

@app.route("/health")
def health():
    """Bonus : Endpoint /health indiquant l'état de santé du service."""
    latest = storage.get_latest_run()
    if not latest:
        return jsonify({"status": "UNKNOWN", "message": "No test run recorded yet"}), 200
    
    is_healthy = latest["summary"]["error_rate"] == 0
    return jsonify({
        "status": "HEALTHY" if is_healthy else "DEGRADED",
        "last_run": latest["timestamp"],
        "error_rate": latest["summary"]["error_rate"],
        "latency_ms_avg": latest["summary"]["latency_ms_avg"]
    }), (200 if is_healthy else 503)

@app.route("/api/runs/latest/json")
def export_latest_json():
    """Bonus : Export JSON du dernier run."""
    latest = storage.get_latest_run()
    if not latest:
        return jsonify({"error": "No runs found"}), 404
    return jsonify(latest)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
