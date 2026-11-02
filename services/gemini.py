"""
Google Gemini provider integration.
"""
import requests
from config import get_config

def generate_text(prompt: str, model: str = "gemini-3.5-flash") -> dict:
    config = get_config()

    if not prompt or not prompt.strip():
        return {"ok": False, "error": "Prompt is required."}

    if not config.GEMINI_API_KEY:
        return {"ok": False, "error": "Gemini API key is not configured."}

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={config.GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=config.REQUEST_TIMEOUT)
    except requests.RequestException as exc:
        return {"ok": False, "error": f"Network error contacting Gemini: {exc.__class__.__name__}"}

    if response.status_code != 200:
        # Yahan hum Google ka asal error message bhej rahe hain
        try:
            error_data = response.json()
            exact_error = error_data.get("error", {}).get("message", response.text)
        except:
            exact_error = response.text
            
        return {
            "ok": False,
            "error": f"Google API Error ({response.status_code}): {exact_error}"
        }

    try:
        data = response.json()
        text = data["candidates"][0]["content"]["parts"][0]["text"]
    except (ValueError, KeyError, IndexError, TypeError):
        return {"ok": False, "error": "Unexpected response shape from Gemini."}

    return {"ok": True, "model": model, "text": text}
