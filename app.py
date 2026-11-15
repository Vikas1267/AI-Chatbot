"""
app.py — Flask API server for ARIA chatbot.
"""

from datetime import datetime, timezone

from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

from chatbot_engine import get_response, get_conversation_log, get_all_intents, _INTENTS_DATA

app = Flask(__name__)
CORS(app)


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "intents_loaded": len(_INTENTS_DATA),
    })


@app.route("/api/intents", methods=["GET"])
def intents():
    return jsonify(get_all_intents())


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True, silent=True) or {}
    message = (data.get("message") or "").strip()
    session_id = (data.get("session_id") or "default").strip()

    if not message:
        return jsonify({"error": "message is required"}), 400

    result = get_response(message, session_id)
    result["timestamp"] = datetime.now(timezone.utc).isoformat()
    return jsonify(result)


@app.route("/api/history/<session_id>", methods=["GET"])
def history(session_id: str):
    log = get_conversation_log(session_id)
    return jsonify(log)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=False, port=5000)
