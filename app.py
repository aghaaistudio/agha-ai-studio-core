"""
Agha AI Studio — Flask application entry point.

This file is intentionally thin. Its only job is to:
    1. Create the Flask app.
    2. Load configuration.
    3. Initialise extensions (db, login_manager).
    4. Register blueprints (route groups).
    5. Run the development server when executed directly.
"""
from flask import Flask

from config import get_config
from extensions import db, login_manager
from routes.api import api_bp
from routes.main import main_bp


def create_app() -> Flask:
    """Application factory — build and configure the Flask app."""
    app = Flask(__name__)

    config = get_config()
    app.config["SECRET_KEY"] = config.SECRET_KEY
    app.config["ENV"] = config.ENV
    app.config["DEBUG"] = config.DEBUG
    app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = config.SQLALCHEMY_TRACK_MODIFICATIONS

    # Initialise shared extensions against this app.
    db.init_app(app)
    login_manager.init_app(app)

    # Tell Flask-Login how to load a user from the session cookie.
    from models.user import User

    @login_manager.user_loader
    def load_user(user_id: str):
        try:
            return db.session.get(User, int(user_id))
        except (TypeError, ValueError):
            return None

    # Register route groups (blueprints).
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=app.config["DEBUG"])
