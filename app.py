"""
Agha AI Studio — Flask application entry point.

This file is intentionally thin. Its only job is to:
    1. Create the Flask app.
    2. Load configuration.
    3. Register blueprints (route groups).
    4. Run the development server when executed directly.

Business logic lives in services/ and routes/.
Configuration lives in config.py.
"""
from flask import Flask

from config import get_config
from routes.api import api_bp
from routes.main import main_bp


def create_app() -> Flask:
    """Application factory — build and configure the Flask app."""
    app = Flask(__name__)

    config = get_config()
    app.config["SECRET_KEY"] = config.SECRET_KEY
    app.config["ENV"] = config.ENV
    app.config["DEBUG"] = config.DEBUG

    # Register route groups (blueprints)
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=app.config["DEBUG"])
