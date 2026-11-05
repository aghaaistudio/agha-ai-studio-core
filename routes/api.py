from flask import Blueprint, jsonify, request
from flask_login import current_user
from extensions import db
from services.gemini import generate_text
from models.usage import UsageRecord

api_bp = Blueprint("api", __name__)

@api_bp.post("/generate")
def generate():
    if not current_user.is_authenticated:
        return jsonify({"ok": False, "error": "Please log in to use the AI."}), 401
        
    if not current_user.is_unlimited and current_user.credits <= 0:
        return jsonify({"ok": False, "error": "Insufficient credits. Please buy more."}), 403

    data = request.get_json(silent=True) or {}
    prompt = (data.get("prompt") or "").strip()
    model = data.get("model", "gemini-3.5-flash-lite")

    if not prompt:
        return jsonify({"ok": False, "error": "Prompt is required."}), 400

    result = generate_text(prompt, model)

    if result.get("ok"):
        if not current_user.is_unlimited:
                current_user.credits -= 1
        
        # Save Usage Record for Web UI (api_key_id=None)
        record = UsageRecord(
            user_id=current_user.id,
            api_key_id=None,
            endpoint="/api/generate",
            provider="gemini",
            model_name=result.get("model", ""),
            success=True
        )
        db.session.add(record)
        db.session.commit()
        result["new_credits"] = current_user.credits

    return jsonify(result), 200 if result.get("ok") else 502
