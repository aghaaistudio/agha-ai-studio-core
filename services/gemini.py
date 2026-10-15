"""
Google Gemini provider integration.

This module is the ONLY place that talks to Gemini's API.
Both the web UI and the API gateway call generate_text()
through this single interface.
"""
import requests

from config import get_config


def generate_text(prompt: str) -> dict:
    """
    Send a prompt to Google Gemini and return a structured result.

    Always returns a dict. Never raises.
    Success: {"ok": True, "text": "...", "model": "..."}
    Failure: {"ok": False, "error": "...", "provider_status": <int, optional>}
    """
    config = get_config()

    if not prompt or not prompt.strip():
        return {"ok": False, "error": "Prompt is required."}

    if not config.GEMINI_API_KEY:
        return {"ok": False, "error": "Gemini API key is not configured."}

    model = config.GEMINI_MODEL
    url = (
        "https://generativelanguage.googleapis.com/v1beta/"
        f"models/{model}:generateContent"
    )
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": config.GEMINI_API_KEY,
    }
    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        response = requests.post(
            url,
            json=payload,
            headers=headers,
            timeout=config.REQUEST_TIMEOUT,
        )
    except requests.RequestException as exc:
        return {
            "ok": False,
            "error": f"Network error contacting Gemini: {exc.__class__.__name__}",
        }

    if response.status_code != 200:
        return {
            "ok": False,
            "error": "Gemini request failed. Check model access, API key and quota.",
            "provider_status": response.status_code,
        }

    try:
        data = response.json()
        text = data["candidates"][0]["content"]["parts"][0]["text"]
    except (ValueError, KeyError, IndexError, TypeError):
        return {"ok": False, "error": "Unexpected response shape from Gemini."}

    return {"ok": True, "model": model, "text": text}
