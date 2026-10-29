from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from extensions import db
from models.user import User
from functools import wraps

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash("Access denied. Admins only.", "error")
            return redirect(url_for("main.home"))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route("/")
@login_required
@admin_required
def dashboard():
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template("admin/dashboard.html", users=users)

@admin_bp.route("/toggle/<int:user_id>", methods=["POST"])
@login_required
@admin_required
def toggle_user(user_id):
    user = User.query.get(user_id)
    if user and user.id != current_user.id:
        user.is_active = not user.is_active
        db.session.commit()
        status = "unblocked" if user.is_active else "blocked"
        flash(f"User {user.email} has been {status}.", "success")
    return redirect(url_for("admin.dashboard"))

@admin_bp.route("/add-credits/<int:user_id>", methods=["POST"])
@login_required
@admin_required
def add_credits(user_id):
    user = User.query.get(user_id)
    if user:
        amount = int(request.form.get("amount", 0))
        user.credits += amount
        db.session.commit()
        flash(f"Added {amount} credits to {user.email}.", "success")
    return redirect(url_for("admin.dashboard"))
