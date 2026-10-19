from flask import Blueprint, render_template

docs_bp = Blueprint("docs", __name__)

@docs_bp.get("/docs")
def api_docs():
    return render_template("docs.html")
