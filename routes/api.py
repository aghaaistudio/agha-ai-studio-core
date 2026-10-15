"""
Public JSON API endpoints for the Agha AI Studio web UI.

These routes are used by the dashboard's frontend (index.html).
They are NOT the external API gateway — that is a separate module
built in a later step and uses API keys instead of sessions.
"""
from flask import Blueprint, jsonify, request

from services.gemini import generate_text


api_bp = Blueprint("api", __name__)


@api_bp.get("/health")
def health():
    """Liveness probe: confirms the app is up."""
    return jsonify({
        "status": "ok",
        "service": "Agha AI Studio",
    })


@api_bp.post("/generate")
def generate():
    """
    Generate text from a prompt using the currently selected provider.

    For now only Gemini is wired up. The response shape is stable:
    success -> {"ok": true, "model": "...", "text": "..."}
    failure -> {"ok": false, "error": "..."}
    """
    data = request.get_json(silent=True) or {}
    prompt = (data.get("prompt") or "").strip()

    if not prompt:
        return jsonify({"ok": False, "error": "Prompt is required."}), 400

    result = generate_text(prompt)

    if result.get("ok"):
        return jsonify(result), 200

    # Map provider error to HTTP status
    status = 502
    provider_status = result.get("provider_status")
    if provider_status == 400:
        status = 400
    elif provider_status == 429:
        status = 429

    return jsonify(result), status
