from datetime import datetime, timezone
from extensions import db

class Transaction(db.Model):
    __tablename__ = "transactions"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    amount_pkr = db.Column(db.Float, nullable=False) # Amount in PKR
    credits_added = db.Column(db.Integer, nullable=False)
    payment_method = db.Column(db.String(50), nullable=False) # e.g., EasyPaisa, Card
    status = db.Column(db.String(20), nullable=False, default="Pending") # Pending, Completed, Failed
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Transaction id={self.id} amount={self.amount_pkr} status={self.status}>"
