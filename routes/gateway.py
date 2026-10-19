from flask import Blueprint, jsonify, request
from extensions import db
from models.api import ApiKey
from models.user import User
from models.usage import UsageRecord
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

    # CHECK USER CREDITS
    user = User.query.get(key_obj.user_id)
    if not user or user.credits <= 0:
        return jsonify({"ok": False, "error": "Insufficient credits. Please top up your account."}), 403

    data = request.get_json(silent=True) or {}
    prompt = (data.get("prompt") or "").strip()
    
    if not prompt:
        return jsonify({"ok": False, "error": "Prompt is required"}), 400

    result = generate_text(prompt)
    
    # Deduct 1 credit upon success
    if result.get("ok"):
        user.credits -= 1
        key_obj.last_used_at = datetime.now(timezone.utc)
        record = UsageRecord(
            user_id=key_obj.user_id,
            api_key_id=key_obj.id,
            endpoint="/api/v1/generate",
            provider="gemini",
            model_name=result.get("model", ""),
            success=True
        )
        db.session.add(record)
        db.session.commit()
        return jsonify(result), 200
    
    return jsonify(result), 500
