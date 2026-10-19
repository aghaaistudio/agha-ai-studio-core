from flask import Flask
from config import get_config
from extensions import db, login_manager
from routes.api import api_bp
from routes.auth import auth_bp
from routes.main import main_bp
from routes.developer import developer_bp
from routes.gateway import gateway_bp
from routes.docs import docs_bp
from routes.billing import billing_bp

def create_app() -> Flask:
    app = Flask(__name__)
    config = get_config()
    app.config["SECRET_KEY"] = config.SECRET_KEY
    app.config["ENV"] = config.ENV
    app.config["DEBUG"] = config.DEBUG
    app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = config.SQLALCHEMY_TRACK_MODIFICATIONS

    db.init_app(app)
    login_manager.init_app(app)

    from models.user import User
    @login_manager.user_loader
    def load_user(user_id: str):
        try:
            return db.session.get(User, int(user_id))
        except (TypeError, ValueError):
            return None

    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(auth_bp)
    app.register_blueprint(developer_bp)
    app.register_blueprint(gateway_bp, url_prefix="/api")
    app.register_blueprint(docs_bp)
    app.register_blueprint(billing_bp)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=app.config["DEBUG"])
