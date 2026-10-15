"""
User model for Agha AI Studio.

Passwords are NEVER stored in plain text — only a salted hash.
Verification happens via check_password(), never by string equality.
"""
from datetime import datetime, timezone

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from extensions import db


class User(UserMixin, db.Model):
    """A registered user of the platform."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(
        db.String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    password_hash = db.Column(db.String(255), nullable=False)

    name = db.Column(db.String(120), nullable=False, default="")

    # "user" (default) or "admin"
    role = db.Column(db.String(20), nullable=False, default="user")

    is_active = db.Column(db.Boolean, nullable=False, default=True)

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    # ------------------------------------------------------------------
    # Password helpers
    # ------------------------------------------------------------------
    def set_password(self, raw_password: str) -> None:
        """Hash and store a password. Never store the raw value."""
        self.password_hash = generate_password_hash(raw_password)

    def check_password(self, raw_password: str) -> bool:
        """Return True if raw_password matches the stored hash."""
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, raw_password)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    @property
    def is_admin(self) -> bool:
        return self.role == "admin"

    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email!r} role={self.role!r}>"
