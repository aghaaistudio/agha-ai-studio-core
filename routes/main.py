"""
Frontend page routes for Agha AI Studio.

These routes render HTML pages for the browser. API routes
that return JSON live in routes/api.py.
"""
from flask import Blueprint, render_template


main_bp = Blueprint("main", __name__)


@main_bp.get("/")
def home():
    """Render the dashboard homepage."""
    return render_template("index.html")
