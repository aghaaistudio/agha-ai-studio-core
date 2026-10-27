from flask import Blueprint, jsonify, request
from flask_login import current_user
from extensions import db
from services.gemini import generate_text

api_bp = Blueprint("api", __name__)

@api_bp.post("/generate")
def generate():
    # 1. Check if user is logged in
    if not current_user.is_authenticated:
        return jsonify({"ok": False, "error": "Please log in to use the AI."}), 401
        
    # 2. Check if user has credits
    if current_user.credits <= 0:
        return jsonify({"ok": False, "error": "Insufficient credits. Please buy more."}), 403

    data = request.get_json(silent=True) or {}
    prompt = (data.get("prompt") or "").strip()
    model = data.get("model", "gemini-3.5-flash")

    if not prompt:
        return jsonify({"ok": False, "error": "Prompt is required."}), 400

    # 3. Generate Text
    result = generate_text(prompt, model)

    # 4. Deduct 1 credit on success
    if result.get("ok"):
        current_user.credits -= 1
        db.session.commit()

    return jsonify(result), 200 if result.get("ok") else 502
