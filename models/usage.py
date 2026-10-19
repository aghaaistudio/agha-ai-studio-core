"""
UsageRecord model for tracking API consumption.

Every successful (and failed) request through the API Gateway
will create a record here. This is the foundation for billing.
"""
from datetime import datetime, timezone
from extensions import db

def _now():
    return datetime.now(timezone.utc)

class UsageRecord(db.Model):
    __tablename__ = "usage_records"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    api_key_id = db.Column(db.Integer, db.ForeignKey("api_keys.id"), nullable=False, index=True)
    
    endpoint = db.Column(db.String(100), nullable=False) # e.g. "/api/v1/generate"
    provider = db.Column(db.String(50), nullable=False, default="gemini")
    model_name = db.Column(db.String(50), nullable=False, default="")
    
    success = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=_now)

    def __repr__(self):
        return f"<UsageRecord id={self.id} user_id={self.user_id} success={self.success}>"
