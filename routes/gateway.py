from flask import Blueprint, jsonify, request
from extensions import db
from models.api import ApiKey
from services.gemini import generate_text
from datetime import datetime, timezone

gateway_bp = Blueprint("gateway", __name__)

@gateway_bp.post("/v1/generate")
def api_generate():
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return jsonify({"ok": False, "error": "Missing or invalid Authorization header"}), 401
    
    plain_key = auth_header.replace("Bearer ", "").strip()
    key_obj = ApiKey.find_active_by_plain(plain_key)
    
    if not key_obj:
        return jsonify({"ok": False, "error": "Invalid or revoked API key"}), 401
        
    if not key_obj.has_scope("generate"):
        return jsonify({"ok": False, "error": "API key lacks 'generate' scope"}), 403

    data = request.get_json(silent=True) or {}
    prompt = (data.get("prompt") or "").strip()
    
    if not prompt:
        return jsonify({"ok": False, "error": "Prompt is required"}), 400

    result = generate_text(prompt)
    
    key_obj.last_used_at = datetime.now(timezone.utc)
    db.session.commit()
    
    if result.get("ok"):
        return jsonify(result), 200
    return jsonify(result), 500
