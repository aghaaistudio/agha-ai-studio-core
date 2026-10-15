import os
import requests
from flask import Flask, jsonify, render_template, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "agha-ai-secure-key")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
@app.get("/")
def home():
    return render_template("index.html")

@app.get("/api/health")
def health():
    return jsonify({
        "status": "ok",
        "service": "Agha AI Studio"
    })
@app.post("/api/generate")
def generate():
    data = request.get_json() or {}
    prompt = data.get("prompt", "")
    api_key = os.getenv("GEMINI_API_KEY", "")
    
    if not api_key:
        return jsonify({"ok": False, "error": "Gemini API key is missing in settings/env."}), 400

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMNI_MODEL if 'GEMNI_MODEL' in globals() else GEMINI_MODEL}:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        if response.status_code != 200:
            return jsonify({
                "ok": False,
                "error": "Gemini request failed. Check model access, API key and quota.",
                "provider_status": response.status_code
            }), 502

        result = response.json()
        text = result["candidates"][0]["content"]["parts"][0]["text"]
        return jsonify({
            "ok": True,
            "model": GEMINI_MODEL,
            "text": text
        })
    except (requests.RequestException, KeyError, IndexError, TypeError, ValueError):
        return jsonify({
            "ok": False,
            "error": "Gemini could not complete the test request."
        }), 502
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
