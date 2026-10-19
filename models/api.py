"""
API models: Application and ApiKey.

An Application represents an external website/service that wants to
call Agha AI Studio's API. Each Application can have multiple ApiKeys.

Security:
- The full API key is NEVER stored. Only a SHA-256 hash and a short
  prefix (for display) are kept.
- The plaintext key is shown exactly once, at creation time.
"""
import hashlib
import secrets
from datetime import datetime, timezone

from extensions import db


KEY_PREFIX = "agha_sk_"
PREFIX_DISPLAY_LENGTH = 12  # characters of the key kept for display


def _now():
    return datetime.now(timezone.utc)


def generate_api_key() -> str:
    """Return a new plaintext API key. Format: agha_sk_<43 url-safe chars>."""
    return KEY_PREFIX + secrets.token_urlsafe(32)


def hash_api_key(plain: str) -> str:
    """Return the SHA-256 hex digest of a plaintext API key."""
    return hashlib.sha256(plain.encode("utf-8")).hexdigest()


class Application(db.Model):
    """An external website/service registered by a user."""

    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True,
    )
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(500), nullable=False, default="")
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=_now)

    # Relationships
    user = db.relationship("User", backref=db.backref("applications", lazy=True))
    api_keys = db.relationship(
        "ApiKey",
        backref="application",
        cascade="all, delete-orphan",
        lazy=True,
    )

    def __repr__(self) -> str:
        return f"<Application id={self.id} name={self.name!r} user_id={self.user_id}>"


class ApiKey(db.Model):
    """An API key belonging to an Application."""

    __tablename__ = "api_keys"

    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(
        db.Integer,
        db.ForeignKey("applications.id"),
        nullable=False,
        index=True,
    )
    # Denormalised for fast per-user filtering.
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    name = db.Column(db.String(120), nullable=False, default="Default key")
    key_prefix = db.Column(db.String(20), nullable=False, index=True)
    key_hash = db.Column(db.String(64), nullable=False, unique=True, index=True)

    # Comma-separated scopes, e.g. "generate"
    scopes = db.Column(db.String(255), nullable=False, default="generate")

    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=_now)
    last_used_at = db.Column(db.DateTime, nullable=True)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    @staticmethod
    def issue(application: "Application", name: str = "Default key", scopes: str = "generate"):
        """
        Create a new ApiKey. Returns (key_object, plaintext_key).

        The plaintext is returned ONLY here. Caller must show it once
        and never store it.
        """
        plain = generate_api_key()
        obj = ApiKey(
            application_id=application.id,
            user_id=application.user_id,
            name=name,
            key_prefix=plain[:PREFIX_DISPLAY_LENGTH],
            key_hash=hash_api_key(plain),
            scopes=scopes,
        )
        return obj, plain

    @staticmethod
    def find_active_by_plain(plain: str):
        """Return the ApiKey matching a plaintext key, or None."""
        if not plain:
            return None
        h = hash_api_key(plain)
        return ApiKey.query.filter_by(key_hash=h, is_active=True).first()

    def has_scope(self, scope: str) -> bool:
        return scope in [s.strip() for s in (self.scopes or "").split(",") if s.strip()]

    def __repr__(self) -> str:
        return f"<ApiKey id={self.id} prefix={self.key_prefix!r} active={self.is_active}>"
