"""
Shared Flask extension instances.

These objects are created here (not in app.py) so that models and
routes can import them without creating circular imports.

app.py initialises them against the Flask app via init_app().
"""
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail


# Database ORM
db = SQLAlchemy()

mail = Mail()

# Session/login manager
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Please log in to continue."
login_manager.login_message_category = "info"
