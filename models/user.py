"""
User model for Agha AI Studio.
"""
from datetime import datetime, timedelta
import secrets
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from extensions import db

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(120), nullable=False, default="")
    role = db.Column(db.String(20), nullable=False, default="user")
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    credits = db.Column(db.Integer, nullable=False, default=10)
    
    reset_token = db.Column(db.String(100), nullable=True)
    reset_token_expiry = db.Column(db.DateTime, nullable=True)

    def set_password(self, raw_password: str) -> None:
        self.password_hash = generate_password_hash(raw_password)

    def check_password(self, raw_password: str) -> bool:
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, raw_password)

    def generate_reset_token(self):
        self.reset_token = secrets.token_urlsafe(32)
        # Timezone issue fix: use utcnow() for naive datetime comparison
        self.reset_token_expiry = datetime.utcnow() + timedelta(hours=1)
        return self.reset_token

    def verify_reset_token(self, token):
        if self.reset_token == token and self.reset_token_expiry:
            if self.reset_token_expiry > datetime.utcnow():
                return True
        return False

    @property
    def is_admin(self) -> bool:
        return self.role == "admin"

    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email!r} role={self.role!r} credits={self.credits}>"
